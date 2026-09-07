import React, { useState, useEffect } from 'react';
import { Crown, Star, Users, ShieldCheck, X, UserRound, Quote } from 'lucide-react';
import { committee, testimonials, boardMembers, generalMembers, founderMessage } from '../data/mock';

const Committee = () => {
  const [openModal, setOpenModal] = useState(null); // 'board' | 'members' | null

  // Lock body scroll & allow Esc to close while a modal is open
  useEffect(() => {
    if (openModal) {
      document.body.style.overflow = 'hidden';
      const onKey = (e) => {
        if (e.key === 'Escape') setOpenModal(null);
      };
      window.addEventListener('keydown', onKey);
      return () => {
        document.body.style.overflow = '';
        window.removeEventListener('keydown', onKey);
      };
    }
  }, [openModal]);

  const initials = (name) =>
    name.split(' ').filter((s) => s !== 'Mr.' && s !== 'Mrs.')[0].charAt(0);

  return (
    <section id="committee" className="relative py-28 bg-[#faf6ef]">
      <div className="mx-auto max-w-7xl px-6">
        <div className="max-w-2xl mb-14">
          <div className="text-[11px] uppercase tracking-[0.4em] color-gold font-bold mb-4">
            The People
          </div>
          <h2 className="font-display text-4xl md:text-6xl font-bold text-[#2a1810] leading-tight">
            Executive <span className="italic text-crimson-gradient">Committee</span>
          </h2>
          <p className="font-serif-2 text-lg text-[#2a1810]/65 mt-4">
            From founding pillars to present stewards — the hearts behind our association.
          </p>
        </div>

        {(() => {
          const founder = committee[0];
          const rest = committee.slice(1);
          const Card = (m, featured) => (
            <div
              key={m.name}
              onClick={featured ? () => setOpenModal('founder') : undefined}
              role={featured ? 'button' : undefined}
              tabIndex={featured ? 0 : undefined}
              onKeyDown={
                featured
                  ? (e) => {
                      if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        setOpenModal('founder');
                      }
                    }
                  : undefined
              }
              className={`group relative rounded-3xl p-8 border transition-all hover:-translate-y-1 ${
                featured
                  ? 'bg-gradient-to-br from-[#2a1810] to-[#1a0f0a] text-[#fef6e4] border-[#c8862a]/40 shadow-xl cursor-pointer hover:shadow-2xl hover:border-[#c8862a]/70'
                  : 'bg-[#fef6e4] text-[#2a1810] border-[#c8862a]/25 hover:shadow-lg'
              }`}
              data-testid={`committee-card-${m.name.replace(/[^a-zA-Z]/g, '-').toLowerCase()}`}
            >
              {featured && (
                <div className="absolute top-5 right-5 w-8 h-8 rounded-full bg-[#c8862a] text-[#1a0f0a] flex items-center justify-center">
                  <Crown size={14} />
                </div>
              )}

              <div
                className={`w-16 h-16 rounded-2xl flex items-center justify-center font-display text-2xl font-bold mb-5 ${
                  featured
                    ? 'bg-[#c8862a] text-[#1a0f0a]'
                    : 'bg-gradient-to-br from-[#8b1a1a] to-[#b8593a] text-[#fef6e4]'
                }`}
              >
                {m.initials || m.name.split(' ').filter((s) => s !== 'Mr.' && s !== 'Mrs.')[0].charAt(0)}
              </div>

              <div
                className={`text-[10px] uppercase tracking-[0.3em] font-bold mb-2 ${
                  featured ? 'text-[#f5c76a]' : 'color-gold'
                }`}
              >
                {m.role}
              </div>
              <div className="font-display text-2xl font-bold leading-tight">{m.name}</div>
              <div
                className={`text-xs mt-2 ${
                  featured ? 'text-[#fef6e4]/60' : 'text-[#2a1810]/50'
                }`}
              >
                {m.tenure}
              </div>

              {featured && (
                <div className="mt-5 inline-flex items-center gap-2 text-xs font-bold uppercase tracking-[0.2em] text-[#f5c76a] group-hover:gap-3 transition-all">
                  Read the message
                  <span aria-hidden="true">&rarr;</span>
                </div>
              )}
            </div>
          );

          return (
            <div className="space-y-6">
              {/* Founder — top row alone */}
              <div className="grid md:grid-cols-3">
                <div>{Card(founder, true)}</div>
              </div>

              {/* Current stewards */}
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {rest.map((m) => Card(m, false))}
              </div>
            </div>
          );
        })()}

        {/* Directory buttons */}
        <div className="mt-14 flex flex-col sm:flex-row items-center justify-center gap-4">
          <button
            type="button"
            onClick={() => setOpenModal('board')}
            data-testid="open-board-members-btn"
            className="group inline-flex items-center gap-3 rounded-full px-8 py-4 font-display text-lg font-bold text-[#fef6e4] bg-gradient-to-br from-[#8b1a1a] to-[#b8593a] border border-[#c8862a]/40 shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all"
          >
            <ShieldCheck size={20} className="text-[#f5c76a]" />
            Board Members
          </button>
          <button
            type="button"
            onClick={() => setOpenModal('members')}
            data-testid="open-members-btn"
            className="group inline-flex items-center gap-3 rounded-full px-8 py-4 font-display text-lg font-bold text-[#2a1810] bg-[#fef6e4] border border-[#c8862a]/50 shadow-lg hover:shadow-xl hover:-translate-y-0.5 hover:bg-[#faf0dc] transition-all"
          >
            <Users size={20} className="color-gold" />
            Members
          </button>
        </div>

        {/* Testimonials */}
        <div className="mt-24">
          <div className="text-[11px] uppercase tracking-[0.4em] color-gold font-bold mb-4">
            Voices
          </div>
          <h3 className="font-display text-3xl md:text-5xl font-bold text-[#2a1810] mb-10">
            What our <span className="italic text-crimson-gradient">members</span> say
          </h3>

          <div className="grid md:grid-cols-3 gap-6">
            {testimonials.map((t) => (
              <div
                key={t.id}
                className="relative rounded-3xl p-8 bg-[#fef6e4] border border-[#c8862a]/25 hover:border-[#8b1a1a]/40 hover:-translate-y-1 transition-all shadow-sm hover:shadow-xl"
              >
                <div className="flex items-center gap-1 mb-4 color-gold">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} size={14} fill="currentColor" />
                  ))}
                </div>
                <p className="font-serif-2 text-lg text-[#2a1810]/80 leading-relaxed mb-6">
                  “{t.text}”
                </p>
                <div className="pt-6 border-t border-[#c8862a]/20">
                  <div className="font-display text-lg font-bold text-[#2a1810]">{t.name}</div>
                  <div className="text-xs color-gold uppercase tracking-[0.2em] font-semibold mt-0.5">
                    {t.role}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ===== Founder / Ex-President Message Modal ===== */}
      {openModal === 'founder' && (
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6"
          data-testid="founder-modal"
        >
          <div
            className="absolute inset-0 bg-[#1a0f0a]/70 backdrop-blur-sm"
            onClick={() => setOpenModal(null)}
          />
          <div className="relative w-full max-w-3xl max-h-[88vh] overflow-y-auto rounded-3xl bg-[#faf6ef] border border-[#c8862a]/40 shadow-2xl animate-[fadeUp_0.3s_ease]">
            {/* Header */}
            <div className="sticky top-0 z-10 flex items-center justify-between px-8 py-6 bg-gradient-to-br from-[#2a1810] to-[#1a0f0a] rounded-t-3xl">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-2xl bg-[#c8862a] text-[#1a0f0a] flex items-center justify-center font-display text-xl font-bold">
                  FP
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-[0.3em] text-[#f5c76a] font-bold">
                    A Few Words By Our Founding &amp; Ex-President
                  </div>
                  <h3 className="font-display text-2xl font-bold text-[#fef6e4] leading-tight">
                    {committee[0].name}
                  </h3>
                  <div className="text-xs text-[#fef6e4]/60 mt-0.5">{committee[0].tenure}</div>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setOpenModal(null)}
                data-testid="close-founder-modal"
                className="shrink-0 w-9 h-9 rounded-full bg-[#fef6e4]/10 hover:bg-[#fef6e4]/20 text-[#fef6e4] flex items-center justify-center transition-colors"
                aria-label="Close"
              >
                <X size={18} />
              </button>
            </div>

            <div className="p-8 sm:p-10">
              <Quote size={34} className="color-gold mb-5" />
              <div className="space-y-4">
                {founderMessage.map((para, i) => (
                  <p
                    key={i}
                    className="font-serif-2 text-[17px] leading-relaxed text-[#2a1810]/80"
                  >
                    {para}
                  </p>
                ))}
              </div>
              <div className="mt-8 pt-6 border-t border-[#c8862a]/20">
                <div className="font-display text-xl font-bold text-[#2a1810]">
                  {committee[0].name}
                </div>
                <div className="text-xs color-gold uppercase tracking-[0.2em] font-semibold mt-1">
                  Founding &amp; Ex-President
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ===== Board Members Modal ===== */}
      {openModal === 'board' && (
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6"
          data-testid="board-members-modal"
        >
          <div
            className="absolute inset-0 bg-[#1a0f0a]/70 backdrop-blur-sm"
            onClick={() => setOpenModal(null)}
          />
          <div className="relative w-full max-w-2xl max-h-[85vh] overflow-y-auto rounded-3xl bg-[#faf6ef] border border-[#c8862a]/40 shadow-2xl animate-[fadeUp_0.3s_ease]">
            {/* Header */}
            <div className="sticky top-0 z-10 flex items-center justify-between px-8 py-6 bg-gradient-to-br from-[#2a1810] to-[#1a0f0a] rounded-t-3xl">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 rounded-2xl bg-[#c8862a] text-[#1a0f0a] flex items-center justify-center">
                  <ShieldCheck size={20} />
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-[0.3em] text-[#f5c76a] font-bold">
                    The Board
                  </div>
                  <h3 className="font-display text-2xl font-bold text-[#fef6e4] leading-tight">
                    Board Members
                  </h3>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setOpenModal(null)}
                data-testid="close-board-modal"
                className="w-9 h-9 rounded-full bg-[#fef6e4]/10 hover:bg-[#fef6e4]/20 text-[#fef6e4] flex items-center justify-center transition-colors"
                aria-label="Close"
              >
                <X size={18} />
              </button>
            </div>

            <div className="p-8 space-y-10">
              {/* Management Members */}
              <div>
                <div className="flex items-center gap-3 mb-5">
                  <Crown size={16} className="color-gold" />
                  <h4 className="text-[11px] uppercase tracking-[0.35em] color-gold font-bold">
                    Management Members
                  </h4>
                  <div className="flex-1 h-px bg-[#c8862a]/25" />
                </div>
                <div className="grid sm:grid-cols-2 gap-4">
                  {boardMembers.management.map((m) => (
                    <div
                      key={m.name}
                      className="flex items-center gap-4 rounded-2xl bg-[#fef6e4] border border-[#c8862a]/25 p-4 hover:shadow-md hover:-translate-y-0.5 transition-all"
                    >
                      <div className="w-12 h-12 shrink-0 rounded-xl bg-gradient-to-br from-[#8b1a1a] to-[#b8593a] text-[#fef6e4] flex items-center justify-center font-display text-xl font-bold">
                        {initials(m.name)}
                      </div>
                      <div>
                        <div className="text-[10px] uppercase tracking-[0.25em] color-gold font-bold mb-0.5">
                          {m.role}
                        </div>
                        <div className="font-display text-lg font-bold text-[#2a1810] leading-tight">
                          {m.name}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Advisory Board Members */}
              <div>
                <div className="flex items-center gap-3 mb-5">
                  <Star size={16} className="color-gold" fill="currentColor" />
                  <h4 className="text-[11px] uppercase tracking-[0.35em] color-gold font-bold">
                    Advisory Board Members
                  </h4>
                  <div className="flex-1 h-px bg-[#c8862a]/25" />
                </div>
                <div className="grid sm:grid-cols-2 gap-4">
                  {boardMembers.advisory.map((m) => (
                    <div
                      key={m.name}
                      className="flex items-center gap-4 rounded-2xl bg-[#fef6e4] border border-[#c8862a]/25 p-4 hover:shadow-md hover:-translate-y-0.5 transition-all"
                    >
                      <div className="w-12 h-12 shrink-0 rounded-xl bg-gradient-to-br from-[#2a1810] to-[#1a0f0a] text-[#f5c76a] flex items-center justify-center font-display text-xl font-bold">
                        {initials(m.name)}
                      </div>
                      <div className="font-display text-lg font-bold text-[#2a1810] leading-tight">
                        {m.name}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ===== Members Modal ===== */}
      {openModal === 'members' && (
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6"
          data-testid="members-modal"
        >
          <div
            className="absolute inset-0 bg-[#1a0f0a]/70 backdrop-blur-sm"
            onClick={() => setOpenModal(null)}
          />
          <div className="relative w-full max-w-2xl max-h-[85vh] overflow-y-auto rounded-3xl bg-[#faf6ef] border border-[#c8862a]/40 shadow-2xl animate-[fadeUp_0.3s_ease]">
            {/* Header */}
            <div className="sticky top-0 z-10 flex items-center justify-between px-8 py-6 bg-gradient-to-br from-[#2a1810] to-[#1a0f0a] rounded-t-3xl">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 rounded-2xl bg-[#c8862a] text-[#1a0f0a] flex items-center justify-center">
                  <Users size={20} />
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-[0.3em] text-[#f5c76a] font-bold">
                    Our Community
                  </div>
                  <h3 className="font-display text-2xl font-bold text-[#fef6e4] leading-tight">
                    Members
                  </h3>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setOpenModal(null)}
                data-testid="close-members-modal"
                className="w-9 h-9 rounded-full bg-[#fef6e4]/10 hover:bg-[#fef6e4]/20 text-[#fef6e4] flex items-center justify-center transition-colors"
                aria-label="Close"
              >
                <X size={18} />
              </button>
            </div>

            <div className="p-8">
              {generalMembers.length > 0 ? (
                <div className="grid sm:grid-cols-2 gap-4">
                  {generalMembers.map((m) => (
                    <div
                      key={m.name}
                      className="flex items-center gap-4 rounded-2xl bg-[#fef6e4] border border-[#c8862a]/25 p-4 hover:shadow-md hover:-translate-y-0.5 transition-all"
                    >
                      <div className="w-12 h-12 shrink-0 rounded-xl bg-gradient-to-br from-[#8b1a1a] to-[#b8593a] text-[#fef6e4] flex items-center justify-center font-display text-xl font-bold">
                        {initials(m.name)}
                      </div>
                      <div className="font-display text-lg font-bold text-[#2a1810] leading-tight">
                        {m.name}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center text-center py-14">
                  <div className="w-16 h-16 rounded-2xl bg-[#fef6e4] border border-[#c8862a]/30 flex items-center justify-center mb-5">
                    <UserRound size={26} className="color-gold" />
                  </div>
                  <div className="font-display text-2xl font-bold text-[#2a1810] mb-2">
                    Members list coming soon
                  </div>
                  <p className="font-serif-2 text-[#2a1810]/60 max-w-sm">
                    Our members directory is being finalized and will appear here shortly.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default Committee;
