import React, { useCallback, useEffect, useRef, useState } from 'react';
import axios from 'axios';
import {
  Images,
  ImagePlus,
  Loader2,
  ChevronLeft,
  ChevronRight,
  Star,
  Trash2,
} from 'lucide-react';
import { toast } from 'sonner';

const API = `${process.env.REACT_APP_BACKEND_URL || ''}/api`;
const resolveSrc = (u) => (u && u.startsWith('/api/') ? `${process.env.REACT_APP_BACKEND_URL || ''}${u}` : u);
// Vercel rejects function bodies over 4.5 MB, so photos must stay below that.
const MAX_BYTES = 4 * 1024 * 1024;

const GalleryManager = ({ authHeader, onUnauthorized }) => {
  const [albums, setAlbums] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [busy, setBusy] = useState(true);
  const [uploading, setUploading] = useState(null); // "2/5" style progress text
  const [working, setWorking] = useState({}); // per-photo action spinners
  const fileInputRef = useRef(null);

  const load = useCallback(async () => {
    setBusy(true);
    try {
      const { data } = await axios.get(`${API}/gallery`);
      setAlbums(data);
      setActiveId((cur) => (cur && data.some((a) => a.id === cur) ? cur : data[0]?.id ?? null));
    } catch (err) {
      if (err?.response?.status === 401) onUnauthorized?.();
      else toast.error('Could not load gallery.');
    } finally {
      setBusy(false);
    }
  }, [onUnauthorized]);

  useEffect(() => {
    load();
  }, [load]);

  const album = albums.find((a) => a.id === activeId);
  const setWorkingOn = (pid, v) => setWorking((w) => ({ ...w, [pid]: v }));

  const uploadFiles = async (files) => {
    const list = Array.from(files || []).filter(Boolean);
    if (!list.length || !album) return;
    for (const f of list) {
      if (f.size > MAX_BYTES) {
        toast.error(`"${f.name}" is larger than 4 MB and was skipped.`);
        continue;
      }
    }
    let done = 0;
    for (const f of list) {
      if (f.size > MAX_BYTES) continue;
      done += 1;
      setUploading(`${done}/${list.length}`);
      try {
        const form = new FormData();
        form.append('file', f);
        await axios.post(`${API}/gallery/albums/${album.id}/photos`, form, {
          headers: { ...authHeader(), 'Content-Type': 'multipart/form-data' },
        });
      } catch (err) {
        if (err?.response?.status === 401) {
          onUnauthorized?.();
          break;
        }
        toast.error(err?.response?.data?.detail || `Failed to upload "${f.name}"`);
      }
    }
    setUploading(null);
    toast.success('Photos added to the album');
    await load();
  };

  const move = async (index, dir) => {
    if (!album) return;
    const photos = [...album.photos];
    const j = index + dir;
    if (j < 0 || j >= photos.length) return;
    [photos[index], photos[j]] = [photos[j], photos[index]];
    setAlbums((prev) =>
      prev.map((a) => (a.id === album.id ? { ...a, photos } : a))
    );
    try {
      await axios.put(
        `${API}/gallery/albums/${album.id}/order`,
        { photo_ids: photos.map((p) => p.id) },
        { headers: authHeader() }
      );
    } catch (err) {
      if (err?.response?.status === 401) onUnauthorized?.();
      else toast.error('Could not save the new order.');
      load();
    }
  };

  const setCover = async (photo) => {
    setWorkingOn(photo.id, 'cover');
    try {
      await axios.patch(
        `${API}/gallery/albums/${album.id}/cover`,
        { photo_id: photo.id },
        { headers: authHeader() }
      );
      setAlbums((prev) =>
        prev.map((a) =>
          a.id === album.id ? { ...a, cover: photo.url, cover_photo_id: photo.id } : a
        )
      );
      toast.success('Album cover updated');
    } catch (err) {
      if (err?.response?.status === 401) onUnauthorized?.();
      else toast.error('Could not set the cover.');
    } finally {
      setWorkingOn(photo.id, false);
    }
  };

  const remove = async (photo) => {
    if (!window.confirm('Remove this photo from the album?')) return;
    setWorkingOn(photo.id, 'delete');
    try {
      await axios.delete(`${API}/gallery/albums/${album.id}/photos/${photo.id}`, {
        headers: authHeader(),
      });
      toast.success('Photo removed');
      await load();
    } catch (err) {
      if (err?.response?.status === 401) onUnauthorized?.();
      else toast.error('Could not remove the photo.');
    } finally {
      setWorkingOn(photo.id, false);
    }
  };

  if (busy) {
    return (
      <div className="flex items-center justify-center py-24 text-[#2a1810]/60">
        <Loader2 className="animate-spin mr-2" size={18} /> Loading gallery . . .
      </div>
    );
  }

  return (
    <div data-testid="gallery-manager">
      {/* Album selector */}
      <div className="flex flex-wrap items-center gap-2 mb-6">
        {albums.map((a) => (
          <button
            key={a.id}
            onClick={() => setActiveId(a.id)}
            data-testid={`gallery-tab-${a.id}`}
            className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold border transition-all ${
              activeId === a.id
                ? 'bg-[#8b1a1a] text-[#fef6e4] border-[#8b1a1a] shadow'
                : 'bg-white text-[#2a1810] border-[#c8862a]/25 hover:bg-[#faf6ef]'
            }`}
          >
            <Images size={14} />
            {a.title}
            <span
              className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                activeId === a.id ? 'bg-[#c8862a] text-[#1a0f0a]' : 'bg-[#faf6ef] text-[#8b1a1a]'
              }`}
            >
              {a.photos.length}
            </span>
          </button>
        ))}
      </div>

      {album && (
        <div className="rounded-2xl bg-white border border-[#c8862a]/25 shadow-sm overflow-hidden">
          {/* Panel header */}
          <div className="flex flex-wrap items-center justify-between gap-3 px-6 py-4 bg-[#faf6ef] border-b border-[#c8862a]/20">
            <div>
              <div className="text-[10px] uppercase tracking-[0.25em] font-bold color-gold">
                Album · {album.photos.length} photo{album.photos.length === 1 ? '' : 's'}
              </div>
              <div className="font-display text-xl font-bold text-[#2a1810]">{album.title}</div>
            </div>
            <div className="flex items-center gap-3">
              {uploading && (
                <span className="inline-flex items-center gap-2 text-xs font-semibold text-[#8b1a1a]">
                  <Loader2 size={13} className="animate-spin" /> Uploading {uploading}
                </span>
              )}
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                multiple
                className="hidden"
                onChange={(e) => {
                  uploadFiles(e.target.files);
                  e.target.value = '';
                }}
              />
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={!!uploading}
                data-testid="add-photos-btn"
                className="inline-flex items-center gap-2 rounded-full bg-[#8b1a1a] hover:bg-[#6b1414] px-4 py-2 text-sm font-semibold text-[#fef6e4] shadow transition-colors disabled:opacity-60"
              >
                <ImagePlus size={14} /> Add Photos
              </button>
            </div>
          </div>

          {/* Photo grid */}
          {album.photos.length === 0 ? (
            <div className="text-center py-16 text-[#2a1810]/50 font-serif-2 italic text-lg">
              No photos yet — add the first one.
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-6">
              {album.photos.map((p, i) => {
                const isCover = album.cover_photo_id === p.id || (!album.cover_photo_id && album.cover === p.url);
                return (
                  <div
                    key={p.id}
                    data-testid={`gallery-photo-${i}`}
                    className={`relative rounded-2xl overflow-hidden border shadow-sm group ${
                      isCover ? 'border-[#c8862a] ring-2 ring-[#c8862a]/60' : 'border-[#c8862a]/20'
                    }`}
                  >
                    <div className="aspect-square bg-[#faf6ef]">
                      <img
                        src={resolveSrc(p.url)}
                        alt={`${album.title} ${i + 1}`}
                        className="w-full h-full object-cover"
                        loading="lazy"
                      />
                    </div>

                    {/* badges */}
                    <div className="absolute top-2 left-2 px-2 py-0.5 rounded-full bg-[#1a0f0a]/80 text-[#fef6e4] text-[10px] font-bold">
                      #{i + 1}
                    </div>
                    {isCover && (
                      <div className="absolute top-2 right-2 inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-[#c8862a] text-[#1a0f0a] text-[10px] font-bold">
                        <Star size={10} fill="currentColor" /> Cover
                      </div>
                    )}

                    {/* controls */}
                    <div className="absolute inset-x-0 bottom-0 flex items-center justify-center gap-1.5 p-2 bg-gradient-to-t from-[#1a0f0a]/85 to-transparent">
                      <button
                        onClick={() => move(i, -1)}
                        disabled={i === 0 || working[p.id]}
                        title="Move left"
                        className="w-7 h-7 rounded-full bg-[#fef6e4]/90 text-[#2a1810] flex items-center justify-center hover:bg-[#fef6e4] disabled:opacity-30 transition-colors"
                      >
                        <ChevronLeft size={14} />
                      </button>
                      <button
                        onClick={() => move(i, 1)}
                        disabled={i === album.photos.length - 1 || working[p.id]}
                        title="Move right"
                        className="w-7 h-7 rounded-full bg-[#fef6e4]/90 text-[#2a1810] flex items-center justify-center hover:bg-[#fef6e4] disabled:opacity-30 transition-colors"
                      >
                        <ChevronRight size={14} />
                      </button>
                      <button
                        onClick={() => setCover(p)}
                        disabled={isCover || working[p.id]}
                        title="Set as album cover"
                        className={`w-7 h-7 rounded-full flex items-center justify-center transition-colors disabled:opacity-30 ${
                          isCover
                            ? 'bg-[#c8862a] text-[#1a0f0a]'
                            : 'bg-[#fef6e4]/90 text-[#8b5a1c] hover:bg-[#f5c76a]'
                        }`}
                      >
                        {working[p.id] === 'cover' ? (
                          <Loader2 size={13} className="animate-spin" />
                        ) : (
                          <Star size={14} />
                        )}
                      </button>
                      <button
                        onClick={() => remove(p)}
                        disabled={working[p.id]}
                        title="Remove photo"
                        data-testid={`delete-photo-${i}`}
                        className="w-7 h-7 rounded-full bg-[#8b1a1a]/90 text-[#fef6e4] flex items-center justify-center hover:bg-[#8b1a1a] disabled:opacity-40 transition-colors"
                      >
                        {working[p.id] === 'delete' ? (
                          <Loader2 size={13} className="animate-spin" />
                        ) : (
                          <Trash2 size={13} />
                        )}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default GalleryManager;
