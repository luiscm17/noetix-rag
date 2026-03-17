import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { BookOpen, Shield, Zap, ArrowRight, User as UserIcon, Lock, Mail, Sparkles } from 'lucide-react';
import { getAuthService } from '../services/factory';
import { useAuthStore } from '../store/authStore';

export default function Register() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const authService = getAuthService();
      const response = await authService.register(email, username, password);
      if (response.access_token) {
        setAuth({ access_token: response.access_token, token_type: response.token_type, user: response.user });
      }
      navigate('/dashboard');
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } } };
      setError(e.response?.data?.detail || 'Failed to create account');
    } finally {
      setLoading(false);
    }
  };

  const handleDevBypass = () => {
    const mockResponse = {
      access_token: 'mock_token_' + Date.now(),
      token_type: 'bearer',
      user: {
        user_id: 1,
        email: 'dev@noetix.ai',
        username: 'DevUser',
        full_name: 'Development User',
        role: 'user',
        is_active: true,
        is_superuser: false
      }
    };
    setAuth(mockResponse);
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-[var(--bg-primary)] px-4 py-12 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-[500px] bg-gradient-to-b from-brand/10 to-transparent" />
      <div className="absolute bottom-0 right-0 w-[600px] h-[600px] bg-gradient-to-tl from-brand/5 via-transparent to-transparent rounded-full blur-3xl" />
      
      <motion.div 
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        className="w-full max-w-md z-10"
      >
        <div className="text-center mb-12">
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.1, duration: 0.5 }}
            className="inline-flex items-center justify-center mb-8"
          >
            <div className="w-16 h-16 rounded-2xl bg-brand/10 border border-brand/40 flex items-center justify-center">
              <BookOpen className="text-brand" size={32} strokeWidth={1.5} aria-hidden="true" />
            </div>
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
            className="text-5xl font-display font-semibold text-[var(--text-primary)] mb-3 tracking-tight"
          >
            Noetix
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-stone-500 text-sm font-medium tracking-wide"
          >
            Begin your journey with intelligent documents.
          </motion.p>
        </div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25, duration: 0.5 }}
          className="glass-panel p-8 rounded-3xl relative overflow-hidden"
        >
          <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-brand/40 to-transparent" />
          
          {error && (
            <motion.div 
              initial={{ opacity: 0, height: 0, y: -10 }}
              animate={{ opacity: 1, height: 'auto', y: 0 }}
              className="mb-6 text-brand text-sm p-4 bg-brand/10 border border-brand/30 rounded-xl flex items-start gap-3"
            >
              <Shield size={18} className="shrink-0 mt-0.5" aria-hidden="true" /> 
              <span>{error}</span>
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-2">
              <label className="text-xs font-semibold text-stone-500 uppercase ml-1 tracking-wider">Email</label>
              <div className="relative group">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-stone-600 group-focus-within:text-brand transition-colors duration-300" size={18} />
                <input
                  type="email"
                  placeholder="name@company.com"
                  required
                  autoComplete="email"
                  name="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-stone-900/50 border border-stone-800 rounded-xl py-3.5 pl-11 pr-4 text-sm focus:outline-none focus:border-brand/30 focus:ring-2 focus:ring-brand/10 text-stone-200 transition-colors placeholder:text-stone-600"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-stone-500 uppercase ml-1 tracking-wider">Username</label>
              <div className="relative group">
                <UserIcon className="absolute left-4 top-1/2 -translate-y-1/2 text-stone-600 group-focus-within:text-brand transition-colors duration-300" size={18} />
                <input
                  type="text"
                  placeholder="Choose a username"
                  required
                  minLength={3}
                  maxLength={50}
                  autoComplete="username"
                  name="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-stone-900/50 border border-stone-800 rounded-xl py-3.5 pl-11 pr-4 text-sm focus:outline-none focus:border-brand/30 focus:ring-2 focus:ring-brand/10 text-stone-200 transition-colors placeholder:text-stone-600"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-stone-500 uppercase ml-1 tracking-wider">Password</label>
              <div className="relative group">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-stone-600 group-focus-within:text-brand transition-colors duration-300" size={18} />
                <input
                  type="password"
                  placeholder="Create a password"
                  required
                  minLength={8}
                  autoComplete="new-password"
                  name="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-stone-900/50 border border-stone-800 rounded-xl py-3.5 pl-11 pr-4 text-sm focus:outline-none focus:border-brand/30 focus:ring-2 focus:ring-brand/10 text-stone-200 transition-colors placeholder:text-stone-600"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-2 relative w-full bg-brand text-[#020617] font-semibold py-3.5 rounded-xl hover:bg-brand-hover/95 transition-all disabled:opacity-60 flex items-center justify-center gap-2 shadow-md shadow-brand/15 hover:shadow-lg hover:shadow-brand/20 overflow-hidden group"
            >
              <span className="relative z-10 flex items-center gap-2">
                {loading ? (
                  <Zap className="animate-spin" size={18} aria-hidden="true" />
                ) : (
                  <>
                    <span>Create Account</span>
                    <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </span>
            </button>
          </form>

          <div className="mt-8 flex items-center justify-center gap-4 text-stone-600 text-[10px] uppercase font-bold tracking-[0.25em]">
            <div className="h-px flex-1 bg-stone-800" />
            <span className="flex items-center gap-2">
              <Sparkles size={10} aria-hidden="true" />
              Development
            </span>
            <div className="h-px flex-1 bg-stone-800" />
          </div>

          <button
            onClick={handleDevBypass}
            className="mt-4 w-full border border-dashed border-stone-800 text-stone-500 py-3 rounded-xl hover:border-brand/30 hover:text-brand/80 hover:bg-[var(--bg-elevated)] transition-all text-xs font-medium flex items-center justify-center gap-2 group"
          >
            <Zap size={14} className="group-hover:text-brand" aria-hidden="true" />
            Bypass for Frontend Development
          </button>
        </motion.div>

        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-8 text-center text-stone-500 text-sm"
        >
          Already have an account?{' '}
          <Link to="/login" className="text-brand hover:text-brand/80 font-medium ml-1 transition-colors">
            Sign in
          </Link>
        </motion.p>
      </motion.div>
    </div>
  );
}
