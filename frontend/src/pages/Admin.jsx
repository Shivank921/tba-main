import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import axios from 'axios';
import {
  LogOut,
  Mail,
  Phone,
  Search,
  Loader2,
  CheckCircle2,
  Circle,
  Users,
  Inbox,
  Newspaper,
  ClipboardCheck,
  ArrowLeft,
  Copy,
  Images,
} from 'lucide-react';
import { toast } from 'sonner';
import { useAuth } from '../context/AuthContext';
import GalleryManager from '../components/admin/GalleryManager';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const formatDate = (iso) => {
  try {
    const d = new Date(iso);
    return d.toLocaleString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return iso;
  }
};

const Admin = () => {
  const { user, loading, logout, authHeader } = useAuth();
  const navigate = useNavigate();

  const [tab, setTab] = useState('inquiries');
  const [inquiries, setInquiries] = useState([]);
  const [subscribers, setSubscribers] = useState([]);
  const [stats, setStats] = useState(null);
  const [busy, setBusy] = useState(true);
  const [q, setQ] = useState('');
  const [filter, setFilter] = useState('all'); // all | pending | handled
  const [updating, setUpdating] = useState({});

  const loadAll = async () => {
    setBusy(true);
    try {
      const [c, s, st] = await Promise.all([
        axios.get(`${API}/contact`, { headers: authHeader() }),
        axios.get(`${API}/newsletter`, { headers: authHeader() }),
        axios.get(`${API}/admin/stats`, { headers: authHeader() }),
      ]);
      setInquiries(c.data);
      setSubscribers(s.data);
      setStats(st.data);
    } catch (err) {
      if (err?.response?.status === 401) {
        toast.error('Session expired, please sign in again.');
        logout();
      } else {
        toast.error('Could not load dashboard data.');
      }
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    if (user) loadAll();
     
  }, [user]);

  const filteredInquiries = useMemo(() => {
    let items = inquiries;
    if (filter === 'pending') items = items.filter((i) => !i.handled);
    if (filter === 'handled') items = items.filter((i) => i.handled);
    if (q.trim()) {
      const s = q.toLowerCase();
      items = items.filter(
        (i) =>
          i.name.toLowerCase().includes(s) ||
          (i.email || '').toLowerCase().includes(s) ||
          (i.phone || '').toLowerCase().includes(s) ||
          i.message.toLowerCase().includes(s)
      );
    }
    return items;
  }, [inquiries, q, filter]);

  const filteredSubscribers = useMemo(() => {
    if (!q.trim()) return subscribers;
    const s = q.toLowerCase();
    return subscribers.filter((x) => x.email.toLowerCase().includes(s));
  }, [subscribers, q]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#faf6ef]">
        <Loader2 className="animate-spin color-crimson" />
      </div>
    );
  }
  if (!user) return <Navigate to="/admin/login" replace />;

  const toggleHandled = async (item) => {
    setUpdating((u) => ({ ...u, [item.id]: true }));
    try {
      const { data } = await axios.patch(
        `${API}/contact/${item.id}`,
        { handled: !item.handled },
        { headers: authHeader() }
      );
      setInquiries((prev) => prev.map((x) => (x.id === item.id ? data : x)));
      // refresh stats
      const st = await axios.get(`${API}/admin/stats`, { headers: authHeader() });
      setStats(st.data);
      toast.success(data.handled ? 'Marked as handled' : 'Reopened');
    } catch {
      toast.error('Could not update inquiry.');
    } finally {
      setUpdating((u) => ({ ...u, [item.id]: false }));
    }
  };

  const copyEmail = (email) => {
    navigator.clipboard.writeText(email);
    toast.success(`Copied ${email}`);
  };

  const statCards = [
    {
      label: 'Total Inquiries',
      value: stats?.total_inquiries ?? '—',
      icon: Inbox,
      tone: 'from-[#8b1a1a] to-[#6b1414]',
    },
    {
      label: 'Pending',
      value: stats?.pending_inquiries ?? '—',
      icon: Circle,
      tone: 'from-[#e08a1e] to-[#c8862a]',
    },
    {
      label: 'Handled',
      value: stats?.handled_inquiries ?? '—',
      icon: ClipboardCheck,
      tone: 'from-[#4a7c2e] to-[#2f5a1a]',
    },
    {
      label: 'Subscribers',
      value: stats?.total_subscribers ?? '—',
      icon: Newspaper,
      tone: 'from-[#b8593a] to-[#8b3a24]',
    },
  ];

  return (
    <div className="min-h-screen bg-[#faf6ef]">
      {/* Top bar */}
      <header className="sticky top-0 z-30 bg-[#1a0f0a] text-[#fef6e4] border-b border-[#c8862a]/20">
        <div className="mx-auto max-w-7xl px-6 py-4 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate('/')}
              className="w-9 h-9 rounded-full bg-[#fef6e4]/10 hover:bg-[#fef6e4]/20 flex items-center justify-center transition-colors"
              title="Back to site"
            >
              <ArrowLeft size={16} />
            </button>
            <div>
              <div className="text-[10px] uppercase tracking-[0.35em] color-gold font-bold">
                Committee Portal
              </div>
              <div className="font-display text-lg font-bold leading-tight">
                Admin Dashboard
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#fef6e4]/10 text-xs">
              <span className="w-2 h-2 rounded-full bg-[#4ade80] animate-pulse" />
              Signed in as <span className="font-semibold text-[#f5c76a]">{user.username}</span>
            </div>
            <button
              onClick={() => {
                logout();
                navigate('/admin/login', { replace: true });
                toast.success('Signed out');
              }}
              className="inline-flex items-center gap-2 rounded-full bg-[#8b1a1a] hover:bg-[#6b1414] px-4 py-2 text-sm font-semibold transition-colors"
            >
              <LogOut size={14} /> Sign out
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-10">
        {/* Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {statCards.map((s) => (
            <div
              key={s.label}
              className="relative rounded-2xl bg-white border border-[#c8862a]/20 p-5 overflow-hidden hover:-translate-y-0.5 transition-transform shadow-sm hover:shadow-md"
            >
              <div className={`absolute inset-x-0 top-0 h-1 bg-gradient-to-r ${s.tone}`} />
              <div className="flex items-start justify-between">
                <div>
                  <div className="text-[10px] uppercase tracking-[0.25em] color-gold font-bold">
                    {s.label}
                  </div>
                  <div className="font-display text-4xl font-bold text-[#2a1810] mt-1 tabular-nums">
                    {s.value}
                  </div>
                </div>
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${s.tone} text-[#fef6e4] flex items-center justify-center`}>
                  <s.icon size={18} />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Tabs + search */}
        <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
          <div className="flex items-center gap-2 rounded-full bg-white border border-[#c8862a]/25 p-1">
            <button
              onClick={() => setTab('inquiries')}
              className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition-all ${
                tab === 'inquiries'
                  ? 'bg-[#8b1a1a] text-[#fef6e4] shadow'
                  : 'text-[#2a1810] hover:bg-[#faf6ef]'
              }`}
            >
              <Inbox size={14} /> Inquiries
              {stats?.pending_inquiries > 0 && (
                <span className={`ml-1 px-2 py-0.5 rounded-full text-[10px] font-bold ${tab === 'inquiries' ? 'bg-[#c8862a] text-[#1a0f0a]' : 'bg-[#8b1a1a] text-[#fef6e4]'}`}>
                  {stats.pending_inquiries}
                </span>
              )}
            </button>
            <button
              onClick={() => setTab('subscribers')}
              className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition-all ${
                tab === 'subscribers'
                  ? 'bg-[#8b1a1a] text-[#fef6e4] shadow'
                  : 'text-[#2a1810] hover:bg-[#faf6ef]'
              }`}
            >
              <Users size={14} /> Subscribers
            </button>
            <button
              onClick={() => setTab('gallery')}
              data-testid="admin-tab-gallery"
              className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition-all ${
                tab === 'gallery'
                  ? 'bg-[#8b1a1a] text-[#fef6e4] shadow'
                  : 'text-[#2a1810] hover:bg-[#faf6ef]'
              }`}
            >
              <Images size={14} /> Gallery
            </button>
          </div>

          <div className="flex items-center gap-2">
            {tab === 'inquiries' && (
              <div className="flex items-center gap-1 rounded-full bg-white border border-[#c8862a]/25 p-1 text-xs">
                {['all', 'pending', 'handled'].map((f) => (
                  <button
                    key={f}
                    onClick={() => setFilter(f)}
                    className={`px-3 py-1.5 rounded-full font-semibold capitalize transition-colors ${
                      filter === f
                        ? 'bg-[#c8862a] text-[#1a0f0a]'
                        : 'text-[#2a1810]/60 hover:text-[#2a1810]'
                    }`}
                  >
                    {f}
                  </button>
                ))}
              </div>
            )}
            {tab !== 'gallery' && (
              <div className="relative">
                <Search
                  size={14}
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-[#2a1810]/40"
                />
                <input
                  value={q}
                  onChange={(e) => setQ(e.target.value)}
                  placeholder="Search . . ."
                  className="rounded-full pl-9 pr-4 py-2 text-sm bg-white border border-[#c8862a]/25 focus:outline-none focus:border-[#8b1a1a] w-56"
                />
              </div>
            )}
          </div>
        </div>

        {/* Content */}
        {tab === 'gallery' ? (
          <GalleryManager
            authHeader={authHeader}
            onUnauthorized={() => {
              toast.error('Session expired, please sign in again.');
              logout();
            }}
          />
        ) : busy ? (
          <div className="flex items-center justify-center py-24 text-[#2a1810]/60">
            <Loader2 className="animate-spin mr-2" size={18} /> Loading . . .
          </div>
        ) : tab === 'inquiries' ? (
          <div className="space-y-3">
            {filteredInquiries.length === 0 && (
              <div className="text-center py-16 text-[#2a1810]/50 font-serif-2 italic text-lg">
                No inquiries match your filter.
              </div>
            )}
            {filteredInquiries.map((item) => (
              <article
                key={item.id}
                className={`relative rounded-2xl border p-5 md:p-6 shadow-sm transition-all ${
                  item.handled
                    ? 'bg-[#f5ebd7]/60 border-[#4a7c2e]/30'
                    : 'bg-white border-[#c8862a]/25 hover:shadow-md'
                }`}
              >
                <div className="grid md:grid-cols-[1fr_auto] gap-4">
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-3 mb-2">
                      <span
                        className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] uppercase tracking-[0.2em] font-bold ${
                          item.handled
                            ? 'bg-[#4a7c2e]/15 text-[#4a7c2e]'
                            : 'bg-[#e08a1e]/15 text-[#8a5a1c]'
                        }`}
                      >
                        {item.handled ? (
                          <>
                            <CheckCircle2 size={10} /> Handled
                          </>
                        ) : (
                          <>
                            <Circle size={10} /> Pending
                          </>
                        )}
                      </span>
                      <span className="text-xs text-[#2a1810]/50">
                        {formatDate(item.created_at)}
                      </span>
                    </div>
                    <div className="font-display text-xl font-bold text-[#2a1810] mb-1">
                      {item.name}
                    </div>
                    <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-[#2a1810]/70 mb-3">
                      {item.phone && (
                        <span className="inline-flex items-center gap-1.5">
                          <Phone size={13} /> {item.phone}
                        </span>
                      )}
                      {item.email && (
                        <button
                          onClick={() => copyEmail(item.email)}
                          className="inline-flex items-center gap-1.5 hover:color-crimson transition-colors"
                          title="Copy email"
                        >
                          <Mail size={13} /> {item.email}
                          <Copy size={11} className="opacity-50" />
                        </button>
                      )}
                    </div>
                    <p className="font-serif-2 text-[#2a1810]/85 leading-relaxed break-words whitespace-pre-wrap">
                      {item.message}
                    </p>
                  </div>

                  <div className="flex md:flex-col items-start md:items-end gap-2 md:min-w-[180px]">
                    <button
                      onClick={() => toggleHandled(item)}
                      disabled={updating[item.id]}
                      className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition-all shadow-sm ${
                        item.handled
                          ? 'bg-[#faf6ef] border border-[#4a7c2e]/40 text-[#4a7c2e] hover:bg-[#f5ebd7]'
                          : 'bg-[#4a7c2e] text-[#fef6e4] hover:bg-[#3a6220]'
                      }`}
                    >
                      {updating[item.id] ? (
                        <>
                          <Loader2 size={14} className="animate-spin" />
                        </>
                      ) : item.handled ? (
                        <>
                          <Circle size={14} /> Reopen
                        </>
                      ) : (
                        <>
                          <CheckCircle2 size={14} /> Mark handled
                        </>
                      )}
                    </button>
                    {item.email && (
                      <a
                        href={`mailto:${item.email}?subject=Re:%20Your%20inquiry%20-%20Bengali%20Association%20Coimbatore`}
                        className="inline-flex items-center gap-2 rounded-full border border-[#8b1a1a]/30 px-4 py-2 text-sm font-semibold text-[#8b1a1a] hover:bg-[#8b1a1a] hover:text-[#fef6e4] transition-colors"
                      >
                        <Mail size={14} /> Reply
                      </a>
                    )}
                  </div>
                </div>
              </article>
            ))}
          </div>
        ) : (
          <div className="rounded-2xl bg-white border border-[#c8862a]/25 overflow-hidden shadow-sm">
            <div className="grid grid-cols-[1fr_auto] items-center px-6 py-3 bg-[#faf6ef] border-b border-[#c8862a]/20">
              <div className="text-[10px] uppercase tracking-[0.25em] font-bold color-gold">
                Email
              </div>
              <div className="text-[10px] uppercase tracking-[0.25em] font-bold color-gold">
                Subscribed
              </div>
            </div>
            {filteredSubscribers.length === 0 && (
              <div className="text-center py-16 text-[#2a1810]/50 font-serif-2 italic">
                No subscribers found.
              </div>
            )}
            {filteredSubscribers.map((s) => (
              <div
                key={s.id}
                className="grid grid-cols-[1fr_auto] items-center px-6 py-3 border-b border-[#c8862a]/10 last:border-none hover:bg-[#faf6ef]/60 transition-colors"
              >
                <button
                  onClick={() => copyEmail(s.email)}
                  className="text-left inline-flex items-center gap-2 text-sm text-[#2a1810] hover:color-crimson transition-colors"
                >
                  <Mail size={14} className="color-gold" />
                  {s.email}
                  <Copy size={11} className="opacity-40" />
                </button>
                <div className="text-xs text-[#2a1810]/50 tabular-nums">
                  {formatDate(s.subscribed_at)}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Admin;
