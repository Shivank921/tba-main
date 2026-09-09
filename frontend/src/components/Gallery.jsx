import React, { useState, useEffect } from 'react';
import { X, ImageIcon, ArrowLeft } from 'lucide-react';
import { galleryAlbums as fallbackAlbums } from '../data/mock';

const BACKEND = process.env.REACT_APP_BACKEND_URL;
const resolveSrc = (u) => (u && u.startsWith('/api/') ? `${BACKEND}${u}` : u);

const Gallery = () => {
  const [albums, setAlbums] = useState(fallbackAlbums);
  const [openId, setOpenId] = useState(null);
  const [lightbox, setLightbox] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetch(`${BACKEND}/api/gallery`)
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then((data) => {
        if (cancelled || !Array.isArray(data) || data.length === 0) return;
        // Normalize API albums to the shape this component renders
        setAlbums(
          data.map((a) => ({
            id: a.id,
            title: a.title,
            blurb: a.blurb,
            cover: resolveSrc(a.cover),
            photos: (a.photos || []).map((p) => resolveSrc(p.url)),
          }))
        );
      })
      .catch(() => {
        /* keep static fallback */
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const album = albums.find((a) => a.id === openId);

  return (
    <section id="gallery" className="relative py-28 bg-[#fef6e4] overflow-hidden">
      <div className="mx-auto max-w-7xl px-6">
        <div className="max-w-2xl mb-12">
          <div className="text-[11px] uppercase tracking-[0.4em] color-gold font-bold mb-4">
            Moments
          </div>
          <h2 className="font-display text-4xl md:text-6xl font-bold text-[#2a1810] leading-tight">
            Frames of <span className="italic text-crimson-gradient">Devotion</span>
          </h2>
          <p className="font-serif-2 text-lg text-[#2a1810]/65 mt-4">
            Glimpses from our celebrations — the dhaak, the alpana, the joy.
          </p>
        </div>

        {/* Album preview cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {albums.map((a) => (
            <button
              key={a.id}
              onClick={() => setOpenId(a.id)}
              data-testid={`gallery-album-${a.id}`}
              className="group relative text-left rounded-3xl overflow-hidden shadow-md hover:shadow-2xl hover:-translate-y-1 transition-all h-[340px]"
            >
              <img
                src={a.cover}
                alt={a.title}
                className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#1a0f0a]/90 via-[#1a0f0a]/25 to-transparent" />
              <div className="absolute inset-x-0 bottom-0 p-6 text-[#fef6e4]">
                <div className="flex items-center gap-2 text-[10px] uppercase tracking-[0.3em] color-gold font-bold mb-1">
                  <ImageIcon size={12} /> {a.photos.length} Photos
                </div>
                <div className="font-display text-2xl font-bold">{a.title}</div>
                <div className="text-sm text-[#fef6e4]/75 mt-1">{a.blurb}</div>
                <div className="text-[11px] font-semibold text-[#f5c76a] mt-3 translate-y-2 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all">
                  Open Album →
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Album modal */}
      {album && (
        <div
          className="fixed inset-0 z-[60] bg-[#1a0f0a]/80 backdrop-blur-sm flex items-start md:items-center justify-center p-4 md:p-8 overflow-y-auto"
          onClick={() => setOpenId(null)}
        >
          <div
            className="relative bg-[#fef6e4] rounded-3xl w-full max-w-5xl my-auto p-6 md:p-10"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <div>
                <div className="text-[10px] uppercase tracking-[0.3em] color-gold font-bold mb-1">
                  Album
                </div>
                <h3 className="font-display text-3xl font-bold text-[#2a1810]">{album.title}</h3>
              </div>
              <button
                onClick={() => setOpenId(null)}
                data-testid="gallery-modal-close"
                className="w-10 h-10 rounded-full bg-[#8b1a1a] text-[#fef6e4] flex items-center justify-center hover:bg-[#6f1414] transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            {album.photos.length === 0 ? (
              <div className="text-center py-20 text-[#2a1810]/50 font-serif-2 text-lg italic">
                Photos coming soon — check back shortly.
              </div>
            ) : (
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {album.photos.map((src, i) => (
                  <button
                    key={i}
                    onClick={() => setLightbox(src)}
                    className="group relative rounded-2xl overflow-hidden aspect-square shadow-sm hover:shadow-xl transition-all"
                  >
                    <img
                      src={src}
                      alt={`${album.title} ${i + 1}`}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    />
                    <div className="absolute inset-0 bg-[#1a0f0a]/0 group-hover:bg-[#1a0f0a]/20 transition-colors" />
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Fullscreen lightbox */}
      {lightbox && (
        <div
          className="fixed inset-0 z-[70] bg-[#1a0f0a]/95 flex items-center justify-center p-4"
          onClick={() => setLightbox(null)}
        >
          <button
            onClick={() => setLightbox(null)}
            className="absolute top-6 left-6 inline-flex items-center gap-2 text-[#fef6e4] text-sm font-semibold"
          >
            <ArrowLeft size={16} /> Back
          </button>
          <img
            src={lightbox}
            alt="View"
            className="max-h-[88vh] max-w-full rounded-2xl object-contain"
            onClick={(e) => e.stopPropagation()}
          />
        </div>
      )}
    </section>
  );
};

export default Gallery;
