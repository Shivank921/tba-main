import React, { useState } from 'react';
import axios from 'axios';
import { MapPin, Mail, Phone, Send, Check, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { contact } from '../data/mock';

const API = `${process.env.REACT_APP_BACKEND_URL || ''}/api`;

const Contact = () => {
  const [form, setForm] = useState({ name: '', email: '', phone: '', message: '' });
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (!form.name || !form.phone || !form.message) {
      toast.error('Please fill in your name, phone, and message.');
      return;
    }
    try {
      setLoading(true);
      await axios.post(`${API}/contact`, {
        name: form.name.trim(),
        email: form.email.trim() || null,
        phone: form.phone.trim(),
        message: form.message.trim(),
      });
      setSent(true);
      toast.success('Pranaam! Your message has reached us. We shall respond soon.');
      setForm({ name: '', email: '', phone: '', message: '' });
      setTimeout(() => setSent(false), 3500);
    } catch (err) {
      const detail = err?.response?.data?.detail;
      toast.error(
        typeof detail === 'string'
          ? detail
          : 'Sorry — we could not send your message. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="contact" className="relative py-28 bg-gradient-to-b from-[#f5ebd7] to-[#faf6ef]">
      <div className="mx-auto max-w-7xl px-6">
        <div className="grid lg:grid-cols-[1fr_1.2fr] gap-14">
          {/* Left — info */}
          <div>
            <div className="text-[11px] uppercase tracking-[0.4em] color-gold font-bold mb-4">
              Get In Touch
            </div>
            <h2 className="font-display text-4xl md:text-6xl font-bold text-[#2a1810] leading-tight">
              Come, celebrate <br />
              <span className="italic text-crimson-gradient">with us.</span>
            </h2>
            <p className="font-serif-2 text-lg text-[#2a1810]/65 mt-4 max-w-md">
              Whether you are a Probashi Bengali or a lover of the culture — we would be delighted to hear from you.
            </p>

            <div className="mt-10 space-y-5">
              <div className="flex items-start gap-4 group">
                <div className="w-12 h-12 rounded-2xl bg-[#8b1a1a] text-[#fef6e4] flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform">
                  <MapPin size={18} />
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-[0.3em] color-gold font-bold mb-1">Venue</div>
                  <div className="font-display text-lg font-semibold text-[#2a1810]">{contact.venue}</div>
                  <div className="text-sm text-[#2a1810]/70">{contact.address}</div>
                </div>
              </div>

              <div className="flex items-start gap-4 group">
                <div className="w-12 h-12 rounded-2xl bg-[#c8862a] text-[#1a0f0a] flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform">
                  <Mail size={18} />
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-[0.3em] color-gold font-bold mb-1">Email</div>
                  <div className="font-display text-lg font-semibold text-[#2a1810]">{contact.email}</div>
                </div>
              </div>

              <div className="flex items-start gap-4 group">
                <div className="w-12 h-12 rounded-2xl bg-[#b8593a] text-[#fef6e4] flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform">
                  <Phone size={18} />
                </div>
                <div>
                  <div className="text-[10px] uppercase tracking-[0.3em] color-gold font-bold mb-1">Call</div>
                  {contact.phones.map((p) => (
                    <div key={p.number} className="mb-1">
                      <span className="font-display text-lg font-semibold text-[#2a1810]">{p.name}</span>
                      <span className="text-[#2a1810]/70"> : </span>
                      <a href={`tel:${p.number}`} className="font-display text-lg font-semibold text-[#8b1a1a] hover:underline">{p.number}</a>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="mt-10 pt-6 border-t border-[#c8862a]/25">
              <div className="text-[10px] uppercase tracking-[0.3em] color-gold font-bold mb-3">Follow</div>
              <div className="flex items-center gap-3">
                {contact.socials.map((s) => (
                  <a
                    key={s.name}
                    href={s.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    data-testid={`social-${s.name.toLowerCase()}-link`}
                    className="px-4 py-2 rounded-full border border-[#8b1a1a]/30 text-sm font-medium text-[#2a1810] hover:bg-[#8b1a1a] hover:text-[#fef6e4] transition-colors"
                  >
                    {s.name}
                  </a>
                ))}
              </div>
            </div>
          </div>

          {/* Right — form */}
          <div id="membership" className="relative">
            <div className="absolute -top-6 -right-6 w-40 h-40 rounded-full bg-[#c8862a]/20 blur-3xl" />
            <form
              onSubmit={submit}
              className="relative rounded-3xl bg-gradient-to-br from-[#fef6e4] to-[#faf6ef] border-2 border-[#c8862a]/30 p-8 md:p-10 shadow-2xl"
            >
              <div className="text-[11px] uppercase tracking-[0.4em] color-gold font-bold mb-2">
                Membership · Inquiry
              </div>
              <h3 className="font-display text-3xl md:text-4xl font-bold text-[#2a1810] mb-8">
                Send us a message
              </h3>

              <div className="grid md:grid-cols-2 gap-5">
                <div>
                  <label className="text-xs uppercase tracking-[0.2em] font-bold text-[#2a1810]/60 mb-2 block">
                    Full Name
                  </label>
                  <input
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    className="w-full rounded-xl border-2 border-[#c8862a]/30 bg-white/80 px-4 py-3 font-serif-2 text-[#2a1810] focus:outline-none focus:border-[#8b1a1a] transition-colors"
                    placeholder="Sri / Srimati . . ."
                  />
                </div>
                <div>
                  <label className="text-xs uppercase tracking-[0.2em] font-bold text-[#2a1810]/60 mb-2 block">
                    Email (optional)
                  </label>
                  <input
                    type="email"
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    className="w-full rounded-xl border-2 border-[#c8862a]/30 bg-white/80 px-4 py-3 font-serif-2 text-[#2a1810] focus:outline-none focus:border-[#8b1a1a] transition-colors"
                    placeholder="you@email.com"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="text-xs uppercase tracking-[0.2em] font-bold text-[#2a1810]/60 mb-2 block">
                    Phone
                  </label>
                  <input
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    className="w-full rounded-xl border-2 border-[#c8862a]/30 bg-white/80 px-4 py-3 font-serif-2 text-[#2a1810] focus:outline-none focus:border-[#8b1a1a] transition-colors"
                    placeholder="+91 . . ."
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="text-xs uppercase tracking-[0.2em] font-bold text-[#2a1810]/60 mb-2 block">
                    Your Message
                  </label>
                  <textarea
                    rows="4"
                    value={form.message}
                    onChange={(e) => setForm({ ...form, message: e.target.value })}
                    className="w-full rounded-xl border-2 border-[#c8862a]/30 bg-white/80 px-4 py-3 font-serif-2 text-[#2a1810] focus:outline-none focus:border-[#8b1a1a] transition-colors resize-none"
                    placeholder="Tell us how we can help . . ."
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={sent || loading}
                className="mt-6 w-full inline-flex items-center justify-center gap-3 rounded-xl bg-[#8b1a1a] hover:bg-[#6b1414] disabled:bg-[#4a7c2e] text-[#fef6e4] py-4 font-semibold shadow-md hover:shadow-xl transition-all disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <Loader2 size={18} className="animate-spin" /> Sending . . .
                  </>
                ) : sent ? (
                  <>
                    <Check size={18} /> Message sent — Pranaam!
                  </>
                ) : (
                  <>
                    Send Message <Send size={16} />
                  </>
                )}
              </button>

              <p className="text-xs text-center text-[#2a1810]/50 mt-4">
                By submitting, you agree to be contacted regarding your inquiry.
              </p>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
