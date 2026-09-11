import React, { useState } from 'react';
import axios from 'axios';
import { ArrowUp, Heart, Loader2, Check } from 'lucide-react';
import { toast } from 'sonner';
import { navLinks } from '../data/mock';
import { Link, useLocation } from 'react-router-dom';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const Footer = () => {
  const [subLoading, setSubLoading] = useState(false);
  const [subDone, setSubDone] = useState(false);
  const location = useLocation();
  const pageHref = (href) => (location.pathname === '/' ? href : `/${href}`);

  const handleSubscribe = async (e) => {
    e.preventDefault();
    const email = e.target.email.value.trim();
    if (!email) return;
    try {
      setSubLoading(true);
      await axios.post(`${API}/newsletter`, { email });
      setSubDone(true);
      toast.success('Subscribed — welcome to the family!');
      e.target.reset();
      setTimeout(() => setSubDone(false), 3500);
    } catch (err) {
      const detail = err?.response?.data?.detail;
      toast.error(
        typeof detail === 'string' ? detail : 'Could not subscribe. Please try again.'
      );
    } finally {
      setSubLoading(false);
    }
  };

  return (
    <footer className="relative bg-[#1a0f0a] text-[#fef6e4] pt-20 pb-8 overflow-hidden" data-testid="site-footer">
      <div className="absolute top-0 left-0 right-0 h-8 alpana-border opacity-40" />
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-1/4 w-96 h-96 rounded-full bg-[#8b1a1a] blur-[120px]" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 rounded-full bg-[#c8862a] blur-[120px]" />
      </div>

      <div className="relative mx-auto max-w-7xl px-6">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-10 pb-14 border-b border-[#c8862a]/20">
          <div className="lg:col-span-2">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#8b1a1a] to-[#c8862a] flex items-center justify-center font-display text-xl font-bold">
                ব
              </div>
              <div>
                <div className="font-display text-xl font-bold">Bengali Association</div>
                <div className="text-[10px] uppercase tracking-[0.3em] color-gold font-semibold">
                  Coimbatore · Since 2002
                </div>
              </div>
            </div>
            <p className="font-serif-2 text-lg text-[#fef6e4]/70 leading-relaxed max-w-md">
              An umbrella of Probashi Bengalis in Coimbatore — preserving the traditions and culture of Bengal, one celebration at a time.
            </p>
            <div className="mt-6 inline-flex items-center gap-2 text-[10px] uppercase tracking-[0.3em] color-gold font-bold">
              <span className="w-8 h-px bg-[#c8862a]" /> Regd. No. 189/2002
            </div>
          </div>

          <div>
            <div className="text-[10px] uppercase tracking-[0.3em] color-gold font-bold mb-5">
              Navigate
            </div>
            <ul className="space-y-3">
              {navLinks.map((l) => (
                <li key={l.href}>
                  <a
                    href={pageHref(l.href)}
                    className="text-sm text-[#fef6e4]/70 hover:text-[#f5c76a] transition-colors"
                    data-testid={`footer-nav-${l.label.toLowerCase()}-link`}
                  >
                    {l.label}
                  </a>
                </li>
              ))}
              <li>
                <Link
                  to="/donate"
                  className="inline-flex items-center gap-2 text-sm font-semibold text-[#f5c76a] transition-colors hover:text-white"
                  data-testid="footer-donate-link"
                >
                  <Heart size={13} aria-hidden="true" /> Donate
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <div className="text-[10px] uppercase tracking-[0.3em] color-gold font-bold mb-5">
              Newsletter
            </div>
            <p className="text-sm text-[#fef6e4]/70 mb-4">
              Receive festival updates, event invitations and cultural stories.
            </p>
            <form
              onSubmit={handleSubscribe}
              className="flex items-center gap-2"
              data-testid="footer-newsletter-form"
            >
              <input
                name="email"
                type="email"
                required
                placeholder="your@email.com"
                className="flex-1 rounded-full bg-[#fef6e4]/10 border border-[#c8862a]/30 px-4 py-2.5 text-sm text-[#fef6e4] placeholder-[#fef6e4]/40 focus:outline-none focus:border-[#c8862a]"
                data-testid="footer-newsletter-email-input"
              />
              <button
                type="submit"
                disabled={subLoading || subDone}
                className="rounded-full bg-[#c8862a] hover:bg-[#b8762a] disabled:opacity-70 text-[#1a0f0a] px-5 py-2.5 text-sm font-semibold transition-colors inline-flex items-center gap-1.5"
                data-testid="footer-newsletter-submit-button"
              >
                {subLoading ? (
                  <><Loader2 size={14} className="animate-spin" /> ...</>
                ) : subDone ? (
                  <><Check size={14} /> Done</>
                ) : (
                  'Join'
                )}
              </button>
            </form>
          </div>
        </div>

        <div className="pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-xs text-[#fef6e4]/50">
            © {new Date().getFullYear()} The Bengali Association — Coimbatore. Made with <Heart size={12} className="inline color-crimson" fill="currentColor" /> by Shivank Chakraborty for the community.
          </div>
          <button
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            className="inline-flex items-center gap-2 text-xs uppercase tracking-[0.25em] color-gold font-bold hover:text-[#f5c76a] transition-colors"
            data-testid="footer-back-to-top-button"
          >
            Back to Top <ArrowUp size={14} />
          </button>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
