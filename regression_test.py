#!/usr/bin/env python3
"""
Regression Test for Vercel Deployment Prep
Tests that the UPLOAD_DIR try/except change doesn't break local operation
"""

import requests
import json
import os
from pathlib import Path
from PIL import Image
import io

# Base URL from frontend/.env
BASE_URL = "https://prep-changes-1.preview.emergentagent.com/api"
UPLOAD_DIR = Path("/app/backend/uploads")

def print_test_header(test_name):
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"{'='*80}")

def print_result(passed, message):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {message}")

def test_1_health_check():
    """Test 1: GET /api/ returns 200 {"message":"Hello World"}"""
    print_test_header("1. Health Check - GET /api/")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        checks = [
            (response.status_code == 200, f"Status code is 200"),
            (response.json().get('message') == 'Hello World', "Message is 'Hello World'")
        ]
        
        all_passed = True
        for check, desc in checks:
            print_result(check, desc)
            if not check:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_2_gallery_public():
    """Test 2: GET /api/gallery returns 4 albums with 5 photos each"""
    print_test_header("2. Gallery Public - GET /api/gallery")
    
    try:
        response = requests.get(f"{BASE_URL}/gallery", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            albums = response.json()
            print(f"Number of albums: {len(albums)}")
            
            checks = [
                (len(albums) == 4, f"Expected 4 albums, got {len(albums)}"),
                (albums[0]['id'] == 'puja', f"First album is 'puja'"),
                (albums[1]['id'] == 'programs', f"Second album is 'programs'"),
                (albums[2]['id'] == 'activities', f"Third album is 'activities'"),
                (albums[3]['id'] == 'news-media', f"Fourth album is 'news-media'"),
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            # Check each album has 5 photos
            for album in albums:
                photo_count = len(album.get('photos', []))
                check = photo_count == 5
                print_result(check, f"Album '{album['id']}' has 5 photos: {photo_count}")
                if not check:
                    all_passed = False
            
            return all_passed, albums
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False, None
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None

def test_3_admin_login():
    """Test 3: POST /api/admin/login with admin/admin123 returns a token"""
    print_test_header("3. Admin Login - POST /api/admin/login")
    
    payload = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/login", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            checks = [
                ('access_token' in data, "Response has 'access_token' field"),
                ('token_type' in data and data['token_type'] == 'bearer', "token_type is 'bearer'"),
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            return all_passed, data.get('access_token', '')
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False, ''
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, ''

def test_4_upload_photo(token):
    """Test 4: Upload one small image to programs album, verify file in /app/backend/uploads"""
    print_test_header("4. Upload Photo - POST /api/gallery/albums/programs/photos")
    
    try:
        # Create a small test image (20x20 PNG)
        img = Image.new('RGB', (20, 20), color='green')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        headers = {"Authorization": f"Bearer {token}"}
        files = {'file': ('regression_test.png', img_bytes, 'image/png')}
        response = requests.post(f"{BASE_URL}/gallery/albums/programs/photos", files=files, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            photo = response.json()
            checks = [
                ('id' in photo, "Photo has 'id' field"),
                ('url' in photo, "Photo has 'url' field"),
                ('file' in photo, "Photo has 'file' field"),
                (photo['url'].startswith('/api/uploads/'), f"URL starts with '/api/uploads/': {photo['url']}")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            # CRITICAL: Verify file is in /app/backend/uploads (NOT /tmp/uploads)
            if photo.get('file'):
                local_file_path = UPLOAD_DIR / photo['file']
                tmp_file_path = Path('/tmp/uploads') / photo['file']
                
                file_in_backend = local_file_path.is_file()
                file_in_tmp = tmp_file_path.is_file()
                
                print_result(file_in_backend, f"File exists in /app/backend/uploads: {local_file_path}")
                print_result(not file_in_tmp, f"File NOT in /tmp/uploads (correct): {tmp_file_path}")
                
                if not file_in_backend:
                    print_result(False, "❌ CRITICAL: File not found in /app/backend/uploads!")
                    all_passed = False
                
                if file_in_tmp:
                    print_result(False, "❌ CRITICAL: File found in /tmp/uploads (should be in /app/backend/uploads)!")
                    all_passed = False
            
            return all_passed, photo
        else:
            print_result(False, f"Expected 201, got {response.status_code}")
            return False, None
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False, None

def test_5_serve_uploaded_file(photo_url):
    """Test 5: GET /api/uploads/{filename} serves the uploaded file"""
    print_test_header("5. Serve Uploaded File - GET /api/uploads/{filename}")
    
    try:
        filename = photo_url.split('/')[-1]
        response = requests.get(f"{BASE_URL}/uploads/{filename}", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
        checks = [
            (response.status_code == 200, f"Status code is 200"),
            (len(response.content) > 0, f"File has content ({len(response.content)} bytes)")
        ]
        
        all_passed = True
        for check, desc in checks:
            print_result(check, desc)
            if not check:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_6_delete_photo(token, photo_id, photo_file):
    """Test 6: DELETE photo and verify file is removed from /app/backend/uploads"""
    print_test_header("6. Delete Photo - DELETE /api/gallery/albums/programs/photos/{id}")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{BASE_URL}/gallery/albums/programs/photos/{photo_id}", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            checks = [
                ('ok' in data and data['ok'] == True, "Response has 'ok': true"),
                ('deleted' in data and data['deleted'] == photo_id, f"Deleted photo ID matches")
            ]
            
            all_passed = True
            for check, desc in checks:
                print_result(check, desc)
                if not check:
                    all_passed = False
            
            # CRITICAL: Verify file is removed from /app/backend/uploads
            if photo_file:
                local_file_path = UPLOAD_DIR / photo_file
                file_exists = local_file_path.is_file()
                
                print_result(not file_exists, f"File removed from /app/backend/uploads: {local_file_path}")
                
                if file_exists:
                    print_result(False, "❌ CRITICAL: File still exists in /app/backend/uploads after delete!")
                    all_passed = False
            
            return all_passed
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def test_7_verify_programs_album():
    """Test 7: Confirm programs album is back to exactly 5 seeded photos"""
    print_test_header("7. Verify Programs Album - Back to 5 seeded photos")
    
    try:
        response = requests.get(f"{BASE_URL}/gallery", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            albums = response.json()
            programs_album = next((a for a in albums if a['id'] == 'programs'), None)
            
            if programs_album:
                photo_count = len(programs_album.get('photos', []))
                print(f"Programs album photo count: {photo_count}")
                
                checks = [
                    (photo_count == 5, f"Programs album has exactly 5 photos: {photo_count}"),
                ]
                
                all_passed = True
                for check, desc in checks:
                    print_result(check, desc)
                    if not check:
                        all_passed = False
                
                # Verify all photos are seeded photos (not uploaded ones)
                for i, photo in enumerate(programs_album['photos'], 1):
                    is_seeded = not photo['url'].startswith('/api/uploads/')
                    print_result(is_seeded, f"Photo {i} is seeded photo: {photo['url']}")
                    if not is_seeded:
                        all_passed = False
                
                return all_passed
            else:
                print_result(False, "Programs album not found")
                return False
        else:
            print_result(False, f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Exception: {str(e)}")
        return False

def main():
    print("\n" + "="*80)
    print("REGRESSION TEST - Vercel Deployment Prep")
    print(f"Base URL: {BASE_URL}")
    print(f"Upload Directory: {UPLOAD_DIR}")
    print("="*80)
    
    results = {}
    
    # Test 1: Health check
    results['health_check'] = test_1_health_check()
    
    # Test 2: Gallery public
    gallery_passed, albums = test_2_gallery_public()
    results['gallery_public'] = gallery_passed
    
    # Test 3: Admin login
    login_passed, token = test_3_admin_login()
    results['admin_login'] = login_passed
    
    if not token:
        print("\n❌ CRITICAL: Cannot proceed without admin token")
        print_summary(results)
        return
    
    # Test 4: Upload photo
    upload_passed, photo = test_4_upload_photo(token)
    results['upload_photo'] = upload_passed
    
    if not photo:
        print("\n❌ CRITICAL: Cannot proceed without uploaded photo")
        print_summary(results)
        return
    
    photo_id = photo['id']
    photo_url = photo['url']
    photo_file = photo.get('file')
    
    # Test 5: Serve uploaded file
    results['serve_file'] = test_5_serve_uploaded_file(photo_url)
    
    # Test 6: Delete photo
    results['delete_photo'] = test_6_delete_photo(token, photo_id, photo_file)
    
    # Test 7: Verify programs album restored
    results['verify_programs_album'] = test_7_verify_programs_album()
    
    # Print summary
    print_summary(results)

def print_summary(results):
    print("\n" + "="*80)
    print("REGRESSION TEST SUMMARY")
    print("="*80)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "-"*80)
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
    print("-"*80)
    
    if failed == 0:
        print("\n🎉 ALL REGRESSION TESTS PASSED!")
        print("✅ UPLOAD_DIR try/except change did NOT break local operation")
        print("✅ Files are correctly written to /app/backend/uploads (NOT /tmp/uploads)")
    else:
        print(f"\n❌ {failed} TEST(S) FAILED - REGRESSION DETECTED")

if __name__ == "__main__":
    main()
