import React, { useState, useEffect } from 'react';
import { Check, Copy, Download, FileText, HeartHandshake, ScanLine, ShieldCheck, Smartphone, X } from 'lucide-react';
import { toast } from 'sonner';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const UPI_ID = 'thebengali2002@kotak';
const UPI_NUMBER = '9894280001';
const MEMBERSHIP_FORM_URL = '/membership-form.pdf';

const writeToClipboard = async (text) => {
  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(text);
      return;
    } catch {
      // Continue to the browser-compatible fallback below.
    }
  }

  const textArea = document.createElement('textarea');
  textArea.value = text;
  textArea.setAttribute('readonly', '');
  textArea.style.position = 'fixed';
  textArea.style.opacity = '0';
  document.body.appendChild(textArea);
  textArea.select();
  const copied = document.execCommand('copy');
  document.body.removeChild(textArea);
  if (!copied) throw new Error('Clipboard unavailable');
};

export default function Donate() {
  const [copied, setCopied] = useState(false);
  const [showMemberForm, setShowMemberForm] = useState(false);

  useEffect(() => {
    if (showMemberForm) {
      document.body.style.overflow = 'hidden';
      const onKey = (e) => {
        if (e.key === 'Escape') setShowMemberForm(false);
      };
      window.addEventListener('keydown', onKey);
      return () => {
        document.body.style.overflow = '';
        window.removeEventListener('keydown', onKey);
      };
    }
  }, [showMemberForm]);

  const copyUpiId = async () => {
    try {
      await writeToClipboard(UPI_ID);
      setCopied(true);
      toast.success('UPI ID copied to clipboard');
      window.setTimeout(() => setCopied(false), 2200);
    } catch {
      toast.error('Could not copy the UPI ID. Please copy it manually.');
    }
  };

  return (
    <div className="min-h-screen bg-[#faf6ef] text-[#2a1810]">
      <Navbar />

      <main className="relative overflow-hidden paisley-bg" data-testid="donation-page">
        <div className="absolute inset-x-0 top-0 h-[540px] bg-gradient-to-b from-[#1a0f0a] via-[#4a1715] to-[#6b2923] sm:h-[500px] lg:h-[460px]" />
        <div className="absolute top-0 left-0 right-0 h-8 alpana-border opacity-50" />

        <section className="relative mx-auto grid min-h-[calc(100vh-2rem)] max-w-7xl items-center gap-12 px-6 pb-20 pt-32 lg:grid-cols-[0.9fr_1.1fr] lg:gap-20 lg:pt-36">
          <div className="animate-fadeUp text-[#fef6e4] lg:self-start lg:pt-20">
            <div
              className="mb-5 inline-flex items-center gap-2 text-xs font-bold uppercase tracking-[0.28em] text-[#f5c76a]"
              data-testid="donation-kicker"
            >
              <HeartHandshake size={17} aria-hidden="true" /> Community Giving
            </div>
            <h1
              className="max-w-2xl font-display text-4xl font-bold leading-[1.08] sm:text-5xl lg:text-6xl"
              data-testid="donation-heading"
            >
              A small act... <br />A stronger community!
            </h1>
            <p
              className="mt-6 max-w-xl font-serif-2 text-xl leading-relaxed text-[#fef6e4]/78 sm:text-2xl"
              data-testid="donation-description"
            >
              Your contribution helps us celebrate Bengali culture, serve our community,
              and bring generations together in Coimbatore.
            </p>

            <button
              type="button"
              onClick={() => setShowMemberForm(true)}
              data-testid="become-member-btn"
              className="group mt-8 inline-flex items-center gap-3 rounded-full bg-[#c8862a] px-8 py-4 font-display text-lg font-bold text-[#1a0f0a] shadow-[0_14px_40px_rgba(200,134,42,0.4)] transition-all duration-200 hover:-translate-y-0.5 hover:bg-[#e0a544] hover:shadow-[0_18px_50px_rgba(200,134,42,0.55)] focus:outline-none focus:ring-2 focus:ring-[#f5c76a] focus:ring-offset-2 focus:ring-offset-[#4a1715]"
            >
              <HeartHandshake size={22} aria-hidden="true" />
              Become A Member
              <span className="transition-transform duration-200 group-hover:translate-x-1" aria-hidden="true">&rarr;</span>
            </button>

            <div className="mt-10 grid max-w-xl gap-5 text-[#fef6e4] sm:grid-cols-2 lg:mt-28 lg:text-[#2a1810]">
              <div className="border-l-2 border-[#c8862a] bg-[#1a0f0a]/85 p-4 lg:bg-transparent lg:py-0 lg:pr-0" data-testid="donation-step-open-app">
                <Smartphone className="mb-3 text-[#f5c76a] lg:text-[#8b1a1a]" size={22} aria-hidden="true" />
                <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#f5c76a] lg:text-[#8b1a1a]">Step 01</p>
                <p className="mt-1 font-display text-lg font-bold">Open any UPI app</p>
              </div>
              <div className="border-l-2 border-[#c8862a] bg-[#1a0f0a]/85 p-4 lg:bg-transparent lg:py-0 lg:pr-0" data-testid="donation-step-scan">
                <ScanLine className="mb-3 text-[#f5c76a] lg:text-[#8b1a1a]" size={22} aria-hidden="true" />
                <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#f5c76a] lg:text-[#8b1a1a]">Step 02</p>
                <p className="mt-1 font-display text-lg font-bold">Scan, verify and pay</p>
              </div>
            </div>
          </div>

          <div className="animate-fadeUp delay-200 lg:py-8">
            <div className="relative mx-auto w-full max-w-[580px] border border-[#c8862a]/30 bg-white/95 p-5 shadow-[0_24px_80px_rgba(42,24,16,0.22)] backdrop-blur-md sm:p-8">
              <div className="absolute -left-2 -top-2 h-16 w-16 border-l-2 border-t-2 border-[#c8862a]" />
              <div className="absolute -bottom-2 -right-2 h-16 w-16 border-b-2 border-r-2 border-[#c8862a]" />

              <div className="text-center">
                <p className="text-xs font-bold uppercase tracking-[0.26em] text-[#8b1a1a]">Scan to contribute</p>
                <h2
                  className="mt-2 font-display text-2xl font-bold sm:text-3xl"
                  data-testid="donation-payee-name"
                >
                  The Bengali Association Coimbatore
                </h2>
              </div>

              <div className="mx-auto my-7 aspect-square w-full max-w-[360px] bg-white p-4 shadow-[inset_0_0_0_1px_rgba(200,134,42,0.28)] sm:p-5">
                <img
                  src="/images/donation-qr.jpeg"
                  alt="Bengali Association Coimbatore donation QR code"
                  className="h-full w-full object-contain"
                  data-testid="donation-qr-code"
                />
              </div>

              <p className="mb-6 text-center text-sm text-[#2a1810]/65" data-testid="donation-scan-guidance">
                Scan using Google Pay, PhonePe, Paytm, BHIM, or any UPI-enabled app.
              </p>

              <div className="border-y border-[#c8862a]/25 py-5">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div className="min-w-0">
                    <p className="text-[10px] font-bold uppercase tracking-[0.24em] text-[#8b1a1a]">UPI ID</p>
                    <p className="mt-1 break-all text-lg font-semibold" data-testid="donation-upi-id">
                      {UPI_ID}
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={copyUpiId}
                    className="inline-flex shrink-0 items-center justify-center gap-2 rounded-full bg-[#8b1a1a] px-5 py-2.5 text-sm font-semibold text-[#fef6e4] shadow-md transition-[background-color,transform,box-shadow] duration-200 hover:-translate-y-0.5 hover:bg-[#6b1414] hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-[#c8862a] focus:ring-offset-2"
                    aria-label="Copy UPI ID"
                    data-testid="copy-upi-id-button"
                  >
                    {copied ? <Check size={16} aria-hidden="true" /> : <Copy size={16} aria-hidden="true" />}
                    {copied ? 'Copied' : 'Copy UPI ID'}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between gap-4 py-5">
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-[0.24em] text-[#8b1a1a]">UPI Number</p>
                  <p className="mt-1 text-lg font-semibold tabular-nums" data-testid="donation-upi-number">
                    {UPI_NUMBER}
                  </p>
                </div>
                <ShieldCheck className="shrink-0 text-[#4a7c2e]" size={28} aria-hidden="true" />
              </div>

              <p
                className="bg-[#f5ebd7]/65 px-4 py-3 text-center text-xs leading-relaxed text-[#2a1810]/70"
                data-testid="donation-verification-note"
              >
                Please verify the payee name before confirming payment in your UPI app.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* ===== Membership Form Modal ===== */}
      {showMemberForm && (
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center p-3 sm:p-6"
          data-testid="membership-modal"
        >
          <div
            className="absolute inset-0 bg-[#1a0f0a]/75 backdrop-blur-sm"
            onClick={() => setShowMemberForm(false)}
          />
          <div className="relative flex h-[90vh] w-full max-w-4xl flex-col overflow-hidden rounded-3xl border border-[#c8862a]/40 bg-[#faf6ef] shadow-2xl animate-fadeUp">
            {/* Header */}
            <div className="flex shrink-0 items-center justify-between gap-4 bg-gradient-to-br from-[#2a1810] to-[#1a0f0a] px-6 py-5 sm:px-8">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#c8862a] text-[#1a0f0a]">
                  <FileText size={20} />
                </div>
                <div>
                  <div className="text-[10px] font-bold uppercase tracking-[0.3em] text-[#f5c76a]">
                    Join Us
                  </div>
                  <h3 className="font-display text-xl font-bold leading-tight text-[#fef6e4] sm:text-2xl">
                    Membership Registration Form
                  </h3>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <a
                  href={MEMBERSHIP_FORM_URL}
                  download="TBA-Membership-Registration-Form.pdf"
                  data-testid="download-membership-pdf"
                  className="inline-flex items-center gap-2 rounded-full bg-[#c8862a] px-4 py-2 text-sm font-bold text-[#1a0f0a] transition-colors hover:bg-[#e0a544]"
                >
                  <Download size={16} />
                  <span className="hidden sm:inline">Download</span>
                </a>
                <button
                  type="button"
                  onClick={() => setShowMemberForm(false)}
                  data-testid="close-membership-modal"
                  className="flex h-9 w-9 items-center justify-center rounded-full bg-[#fef6e4]/10 text-[#fef6e4] transition-colors hover:bg-[#fef6e4]/20"
                  aria-label="Close"
                >
                  <X size={18} />
                </button>
              </div>
            </div>

            {/* PDF viewer */}
            <div className="min-h-0 flex-1 bg-[#e9e2d4]">
              <object
                data={`${MEMBERSHIP_FORM_URL}#toolbar=1&view=FitH`}
                type="application/pdf"
                className="h-full w-full"
                aria-label="Membership Registration Form PDF"
              >
                <div className="flex h-full flex-col items-center justify-center gap-4 p-8 text-center">
                  <FileText size={40} className="color-gold" />
                  <p className="font-serif-2 text-lg text-[#2a1810]/70">
                    Your browser can&apos;t display the PDF inline.
                  </p>
                  <a
                    href={MEMBERSHIP_FORM_URL}
                    download="TBA-Membership-Registration-Form.pdf"
                    className="inline-flex items-center gap-2 rounded-full bg-[#8b1a1a] px-6 py-3 font-bold text-[#fef6e4] transition-colors hover:bg-[#6b1414]"
                  >
                    <Download size={18} />
                    Download the form
                  </a>
                </div>
              </object>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
}