from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, UploadFile, File, Response
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import jwt
from passlib.context import CryptContext


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT / Password config
JWT_SECRET = os.environ.get('JWT_SECRET', 'change-me')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
JWT_EXPIRES_HOURS = int(os.environ.get('JWT_EXPIRES_HOURS', '24'))
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login", auto_error=False)

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# ============================================================
# Auth Utilities (JWT + bcrypt)
# ============================================================
def _hash_password(pw: str) -> str:
    return pwd_context.hash(pw)


def _verify_password(pw: str, hashed: str) -> bool:
    return pwd_context.verify(pw, hashed)


def _create_token(sub: str) -> str:
    payload = {
        "sub": sub,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRES_HOURS),
        "iat": datetime.now(timezone.utc),
        "role": "admin",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


async def require_admin(token: Optional[str] = Depends(oauth2_scheme)) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired, please login again")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks


# ============================================================
# Contact Inquiries
# ============================================================
class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    phone: str = Field(..., min_length=5, max_length=40)
    message: str = Field(..., min_length=5, max_length=4000)


class Contact(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: Optional[EmailStr] = None
    phone: str
    message: str
    handled: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


@api_router.post("/contact", response_model=Contact, status_code=201)
async def create_contact(payload: ContactCreate):
    obj = Contact(**payload.model_dump())
    doc = obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.contacts.insert_one(doc)
    logger.info("New contact inquiry from %s <%s>", obj.name, obj.phone)
    return obj


@api_router.get("/contact", response_model=List[Contact])
async def list_contacts(limit: int = 200, admin: dict = Depends(require_admin)):
    _ = admin
    items = await db.contacts.find({}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    for it in items:
        if isinstance(it.get('created_at'), str):
            it['created_at'] = datetime.fromisoformat(it['created_at'])
        it.setdefault('handled', False)
    return items


class ContactPatch(BaseModel):
    handled: bool


@api_router.patch("/contact/{contact_id}", response_model=Contact)
async def update_contact(contact_id: str, payload: ContactPatch, admin: dict = Depends(require_admin)):
    _ = admin
    result = await db.contacts.update_one(
        {"id": contact_id}, {"$set": {"handled": payload.handled}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    doc = await db.contacts.find_one({"id": contact_id}, {"_id": 0})
    if isinstance(doc.get('created_at'), str):
        doc['created_at'] = datetime.fromisoformat(doc['created_at'])
    return doc


# ============================================================
# Newsletter Subscribers
# ============================================================
class SubscribeCreate(BaseModel):
    email: EmailStr


class Subscriber(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    subscribed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


@api_router.post("/newsletter", response_model=Subscriber, status_code=201)
async def subscribe(payload: SubscribeCreate):
    email_lc = payload.email.lower()
    existing = await db.subscribers.find_one({"email": email_lc}, {"_id": 0})
    if existing:
        # Already subscribed — treat idempotently
        if isinstance(existing.get('subscribed_at'), str):
            existing['subscribed_at'] = datetime.fromisoformat(existing['subscribed_at'])
        return existing
    obj = Subscriber(email=email_lc)
    doc = obj.model_dump()
    doc['subscribed_at'] = doc['subscribed_at'].isoformat()
    await db.subscribers.insert_one(doc)
    logger.info("New newsletter subscriber: %s", email_lc)
    return obj


@api_router.get("/newsletter", response_model=List[Subscriber])
async def list_subscribers(limit: int = 500, admin: dict = Depends(require_admin)):
    _ = admin
    items = await db.subscribers.find({}, {"_id": 0}).sort("subscribed_at", -1).to_list(limit)
    for it in items:
        if isinstance(it.get('subscribed_at'), str):
            it['subscribed_at'] = datetime.fromisoformat(it['subscribed_at'])
    return items


# ============================================================
# Admin Auth Endpoints
# ============================================================
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    expires_hours: int


@api_router.post("/admin/login", response_model=LoginResponse)
async def admin_login(payload: LoginRequest):
    user = await db.admin_users.find_one({"username": payload.username.lower()}, {"_id": 0})
    if not user or not _verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = _create_token(user["username"])
    return LoginResponse(
        access_token=token,
        username=user["username"],
        expires_hours=JWT_EXPIRES_HOURS,
    )


@api_router.get("/admin/me")
async def admin_me(admin: dict = Depends(require_admin)):
    return {"username": admin.get("sub"), "role": admin.get("role")}


@api_router.get("/admin/stats")
async def admin_stats(admin: dict = Depends(require_admin)):
    _ = admin
    total_contacts = await db.contacts.count_documents({})
    pending = await db.contacts.count_documents({"handled": {"$ne": True}})
    total_subs = await db.subscribers.count_documents({})
    return {
        "total_inquiries": total_contacts,
        "pending_inquiries": pending,
        "handled_inquiries": total_contacts - pending,
        "total_subscribers": total_subs,
    }


# ============================================================
# Gallery Management (Frames of Devotion)
# ============================================================
# Uploaded photos are stored in MongoDB (GridFS) rather than on disk.
# Serverless filesystems are ephemeral and per-instance: a file written while
# serving one request disappears on the next cold start, and a request served by
# another instance cannot see it at all — which left the gallery full of broken
# images while the MongoDB photo records survived.
GALLERY_BUCKET = 'gallery_files'
_gallery_files = None


def _gallery_fs() -> AsyncIOMotorGridFSBucket:
    """GridFS bucket holding the gallery photo bytes.

    Built lazily on first use: motor resolves the event loop when a bucket is
    constructed, so creating it at import time raises
    "There is no current event loop" on serverless runtimes that import the app
    outside a running loop.
    """
    global _gallery_files
    if _gallery_files is None:
        _gallery_files = AsyncIOMotorGridFSBucket(db, bucket_name=GALLERY_BUCKET)
    return _gallery_files

# Legacy on-disk upload location. Only read as a fallback for photos uploaded
# before storage moved into MongoDB; nothing is written here any more.
UPLOAD_DIR = ROOT_DIR / 'uploads'

ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/avif'}
# Vercel caps both the request and the response body of a Function at 4.5 MB,
# and uploads arrive as multipart bodies, so keep photos comfortably below it.
MAX_UPLOAD_BYTES = 4 * 1024 * 1024  # 4 MB per photo

GALLERY_SEED = [
    {
        'id': 'puja',
        'title': 'Puja',
        'blurb': 'Durga Puja, Saraswati Puja & sacred rituals.',
        'cover': '/durga-puja-dhunuchi.webp',
        'photos': [
            '/gallery/puja/puja-1.jpeg',
            '/gallery/puja/puja-2.jpeg',
            '/gallery/puja/puja-3.jpeg',
            '/gallery/puja/puja-4.jpeg',
            '/gallery/puja/puja-5.jpeg',
        ],
    },
    {
        'id': 'programs',
        'title': 'Programs',
        'blurb': 'Cultural nights, music, dance & performances.',
        'cover': '/cultural-sangeet.jpeg',
        'photos': [
            '/gallery/programs/prog-1.webp',
            '/gallery/programs/prog-2.webp',
            '/gallery/programs/prog-3.jpg',
            '/gallery/programs/prog-4.webp',
            '/gallery/programs/prog-5.jpeg',
        ],
    },
    {
        'id': 'activities',
        'title': 'Activities',
        'blurb': 'Community service, sports & get-togethers.',
        'cover': '/events-football.webp',
        'photos': [
            '/gallery/activities/act-1.jpeg',
            '/gallery/activities/act-2.jpg',
            '/gallery/activities/act-3.jpg',
            '/gallery/activities/act-4.jpg',
            '/gallery/activities/act-5.jpg',
        ],
    },
    {
        'id': 'news-media',
        'title': 'News & Media',
        'blurb': 'Press coverage, features & recognitions.',
        'cover': '/community-group.webp',
        'photos': [
            '/gallery/news/news-1.jpg',
            '/gallery/news/news-2.webp',
            '/gallery/news/news-3.jpg',
            '/gallery/news/news-4.webp',
            '/gallery/news/news-5.jpg',
        ],
    },
]
GALLERY_ALBUM_ORDER = [a['id'] for a in GALLERY_SEED]


def _photo(url: str, stored_file: Optional[str] = None) -> dict:
    return {
        'id': str(uuid.uuid4()),
        'url': url,
        'file': stored_file,  # server-side filename for uploaded photos
        'created_at': datetime.now(timezone.utc).isoformat(),
    }


async def _store_upload(name: str, data: bytes, content_type: str) -> None:
    """Persist photo bytes in MongoDB so they outlive the serverless instance."""
    await _gallery_fs().upload_from_stream(
        name, data, metadata={'content_type': content_type}
    )


async def _open_upload(name: str):
    """GridFS stream for a stored photo, or None if the bytes are missing."""
    try:
        return await _gallery_fs().open_download_stream_by_name(name)
    except Exception:  # gridfs.errors.NoFile
        return None


async def _available_uploads(names: set) -> set:
    """Subset of `names` whose bytes still exist (GridFS, or legacy disk)."""
    if not names:
        return set()
    found = set()
    cursor = db[f'{GALLERY_BUCKET}.files'].find(
        {'filename': {'$in': list(names)}}, {'filename': 1}
    )
    async for doc in cursor:
        found.add(doc['filename'])
    for stale in names - found:
        if (UPLOAD_DIR / stale).is_file():
            found.add(stale)
    return found


async def _delete_upload(name: str) -> None:
    """Remove a stored photo's bytes (GridFS plus any legacy disk copy)."""
    doc = await db[f'{GALLERY_BUCKET}.files'].find_one({'filename': name}, {'_id': 1})
    if doc:
        await _gallery_fs().delete(doc['_id'])
    legacy = UPLOAD_DIR / name
    if legacy.is_file():
        legacy.unlink()


async def _get_album(album_id: str) -> dict:
    doc = await db.gallery_albums.find_one({'id': album_id}, {'_id': 0})
    if not doc:
        raise HTTPException(status_code=404, detail='Album not found')
    return doc


@api_router.get('/gallery')
async def list_gallery():
    """Public — all albums with photos in display order."""
    albums = await db.gallery_albums.find({}, {'_id': 0}).to_list(100)
    order = {a: i for i, a in enumerate(GALLERY_ALBUM_ORDER)}
    albums.sort(key=lambda a: order.get(a['id'], 99))

    # Hide uploaded photos whose bytes are gone (e.g. lost to the old ephemeral
    # filesystem) so the public gallery never renders broken images.
    stored = {p['file'] for a in albums for p in a.get('photos', []) if p.get('file')}
    available = await _available_uploads(stored)
    for a in albums:
        photos = a.get('photos', [])
        kept = [p for p in photos if not p.get('file') or p['file'] in available]
        if len(kept) == len(photos):
            continue
        logger.warning(
            "Album '%s': hiding %d photo(s) with missing upload bytes",
            a['id'], len(photos) - len(kept),
        )
        a['photos'] = kept
        if a.get('cover', '').startswith('/api/uploads/') and a['cover'] not in {p['url'] for p in kept}:
            default = next((s['cover'] for s in GALLERY_SEED if s['id'] == a['id']), '')
            a['cover'] = default or (kept[0]['url'] if kept else '')
            a['cover_photo_id'] = None
    return albums


@api_router.get('/uploads/{filename}')
async def serve_upload(filename: str):
    """Serve admin-uploaded gallery photos from MongoDB (GridFS)."""
    safe = os.path.basename(filename)
    stream = await _open_upload(safe)
    if stream is not None:
        data = await stream.read()
        content_type = (stream.metadata or {}).get('content_type') or 'application/octet-stream'
        return Response(
            content=data,
            media_type=content_type,
            # Filenames are unique per upload, so the bytes never change.
            headers={'Cache-Control': 'public, max-age=31536000, immutable'},
        )

    # Legacy photos uploaded before storage moved into MongoDB
    path = UPLOAD_DIR / safe
    if path.is_file():
        return FileResponse(path)
    raise HTTPException(status_code=404, detail='File not found')


@api_router.post('/gallery/albums/{album_id}/photos', status_code=201)
async def upload_gallery_photo(album_id: str, file: UploadFile = File(...), admin: dict = Depends(require_admin)):
    _ = admin
    album = await _get_album(album_id)
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail='Only image files are allowed')

    data = await file.read()
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=400,
            detail='Photo exceeds the 4 MB limit — please resize it and try again',
        )

    ext = os.path.splitext(file.filename or '')[1].lower() or '.jpg'
    stored = f'{album_id}-{uuid.uuid4().hex}{ext}'
    await _store_upload(stored, data, file.content_type)

    photo = _photo(f'/api/uploads/{stored}', stored_file=stored)
    await db.gallery_albums.update_one({'id': album_id}, {'$push': {'photos': photo}})
    logger.info('Gallery photo added to %s: %s', album_id, stored)
    return photo


@api_router.delete('/gallery/albums/{album_id}/photos/{photo_id}')
async def delete_gallery_photo(album_id: str, photo_id: str, admin: dict = Depends(require_admin)):
    _ = admin
    album = await _get_album(album_id)
    target = next((p for p in album['photos'] if p['id'] == photo_id), None)
    if not target:
        raise HTTPException(status_code=404, detail='Photo not found')

    updates = {'$pull': {'photos': {'id': photo_id}}}
    await db.gallery_albums.update_one({'id': album_id}, updates)

    # If the removed photo was the cover, fall back to the next photo or the album default
    if album.get('cover_photo_id') == photo_id or album.get('cover') == target['url']:
        remaining = [p for p in album['photos'] if p['id'] != photo_id]
        new_cover = remaining[0]['url'] if remaining else ''
        await db.gallery_albums.update_one(
            {'id': album_id}, {'$set': {'cover': new_cover, 'cover_photo_id': remaining[0]['id'] if remaining else None}}
        )

    # Delete the stored bytes (legacy static photos have file=None)
    if target.get('file'):
        await _delete_upload(target['file'])
    return {'ok': True, 'deleted': photo_id}


class OrderPayload(BaseModel):
    photo_ids: List[str]


@api_router.put('/gallery/albums/{album_id}/order')
async def reorder_gallery(album_id: str, payload: OrderPayload, admin: dict = Depends(require_admin)):
    _ = admin
    album = await _get_album(album_id)
    by_id = {p['id']: p for p in album['photos']}
    new_order = [by_id[pid] for pid in payload.photo_ids if pid in by_id]
    # keep any photos missing from payload at the end (safety)
    new_order += [p for p in album['photos'] if p['id'] not in set(payload.photo_ids)]
    await db.gallery_albums.update_one({'id': album_id}, {'$set': {'photos': new_order}})
    return {'ok': True, 'count': len(new_order)}


class CoverPayload(BaseModel):
    photo_id: str


@api_router.patch('/gallery/albums/{album_id}/cover')
async def set_gallery_cover(album_id: str, payload: CoverPayload, admin: dict = Depends(require_admin)):
    _ = admin
    album = await _get_album(album_id)
    target = next((p for p in album['photos'] if p['id'] == payload.photo_id), None)
    if not target:
        raise HTTPException(status_code=404, detail='Photo not found')
    await db.gallery_albums.update_one(
        {'id': album_id}, {'$set': {'cover': target['url'], 'cover_photo_id': payload.photo_id}}
    )
    return {'ok': True, 'cover': target['url']}


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def seed_admin():
    existing = await db.admin_users.find_one({"username": ADMIN_USERNAME.lower()})
    if not existing:
        await db.admin_users.insert_one({
            "id": str(uuid.uuid4()),
            "username": ADMIN_USERNAME.lower(),
            "password_hash": _hash_password(ADMIN_PASSWORD),
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        logger.info("Seeded default admin user '%s'", ADMIN_USERNAME.lower())


@app.on_event("startup")
async def seed_gallery():
    """Seed the 4 gallery albums once (keeps existing data on later boots)."""
    count = await db.gallery_albums.count_documents({})
    if count > 0:
        return
    for a in GALLERY_SEED:
        photos = [_photo(url) for url in a['photos']]
        await db.gallery_albums.insert_one({
            'id': a['id'],
            'title': a['title'],
            'blurb': a['blurb'],
            'cover': a['cover'],
            'cover_photo_id': None,
            'photos': photos,
            'created_at': datetime.now(timezone.utc).isoformat(),
        })
    logger.info("Seeded %d gallery albums", len(GALLERY_SEED))


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()