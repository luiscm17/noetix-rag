import { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  User, 
  Settings as SettingsIcon, 
  Shield, 
  Cpu, 
  Palette, 
  Bell, 
  Key, 
  Monitor,
  LogOut,
  Zap,
  Sun,
  Moon
} from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { useThemeStore } from '../store/themeStore';

const sections = [
  { id: 'general', icon: <SettingsIcon size={18} aria-hidden="true" />, label: 'General' },
  { id: 'account', icon: <User size={18} aria-hidden="true" />, label: 'Account' },
  { id: 'appearance', icon: <Palette size={18} aria-hidden="true" />, label: 'Appearance' },
  { id: 'ai', icon: <Cpu size={18} aria-hidden="true" />, label: 'AI Configuration' },
  { id: 'security', icon: <Shield size={18} aria-hidden="true" />, label: 'Security' },
  { id: 'notifications', icon: <Bell size={18} aria-hidden="true" />, label: 'Notifications' },
];

export default function Settings() {
  const { logout } = useAuthStore();
  const { theme, setTheme } = useThemeStore();
  const [activeTab, setActiveTab] = useState('general');

  return (
    <div className="p-10 max-w-6xl mx-auto h-full overflow-y-auto scrollbar-hide">
      <header className="mb-12">
        <h1 className="text-3xl font-display font-semibold text-[var(--text-primary)] tracking-tight">Settings</h1>
        <p className="text-[var(--text-muted)] mt-2">Manage your preferences and system configuration.</p>
      </header>

      <div className="flex flex-col lg:flex-row gap-12">
        <aside className="lg:w-64 shrink-0 space-y-2">
           {sections.map((section) => (
             <button
               key={section.id}
               onClick={() => setActiveTab(section.id)}
               className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                 activeTab === section.id 
                   ? 'bg-[var(--accent-dim)] text-[var(--accent-hover)] border border-[var(--accent-dim)]' 
                   : 'text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-elevated)] border border-transparent'
               }`}
             >
               {section.icon}
               {section.label}
             </button>
           ))}
           <div className="pt-8 mt-8 border-t border-nexus-border">
             <button 
               onClick={logout}
               className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-red-500 hover:bg-red-500/5 transition-all"
             >
                <LogOut size={18} aria-hidden="true" /> Logout Session
             </button>
           </div>
        </aside>

        <main className="flex-1 max-w-2xl">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-8"
          >
             {activeTab === 'general' && (
               <div className="space-y-8">
                  <section className="space-y-4">
                     <h3 className="text-xl font-display font-semibold text-[var(--text-primary)] tracking-tight">System Environment</h3>
                     <div className="p-6 bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-3xl space-y-6 shadow-sm">
                        <div className="flex items-center justify-between">
                           <div className="flex items-center gap-3">
                              <div className="w-10 h-10 rounded-xl bg-[var(--bg-secondary)] flex items-center justify-center text-[var(--text-muted)]">
                                 <Monitor size={20} aria-hidden="true" />
                              </div>
                              <div>
                                 <p className="text-sm font-medium text-[var(--text-primary)]">Interface Mode</p>
                                 <p className="text-xs text-[var(--text-muted)]">Current: Noetix {theme === 'dark' ? 'Dark' : 'Light'}</p>
                              </div>
                           </div>
                           <button className="px-4 py-2 bg-[var(--accent)] hover:bg-[var(--accent-hover)] rounded-lg text-xs font-medium text-white transition-all">Change</button>
                        </div>
                        
                        <div className="flex items-center justify-between">
                           <div className="flex items-center gap-3">
                              <div className="w-10 h-10 rounded-xl bg-[var(--bg-secondary)] flex items-center justify-center text-[var(--text-muted)]">
                                 <Zap size={20} aria-hidden="true" />
                              </div>
                              <div>
                                 <p className="text-sm font-medium text-[var(--text-primary)]">Turbo Mode</p>
                                 <p className="text-xs text-[var(--text-muted)]">Accelerated semantic indexing</p>
                              </div>
                           </div>
<button 
                           type="button"
                           role="switch"
                           aria-checked="true"
                           className="w-12 h-6 bg-[var(--accent)] rounded-full relative cursor-pointer shadow-[0_0_10px_rgba(127,166,196,0.35)] focus-visible:ring-2 focus-visible:ring-[var(--accent)] focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--bg-primary)]"
                           aria-label="Toggle Turbo Mode"
                         >
                           <span className="absolute right-0.5 top-0.5 w-5 h-5 bg-white rounded-full" />
                         </button>
                        </div>
                     </div>
                  </section>

                  <section className="space-y-4">
                     <h3 className="text-xl font-display font-semibold text-[var(--text-primary)] tracking-tight">AI Provider</h3>
                     <div className="p-6 bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-3xl space-y-6 shadow-sm">
                        <div className="p-4 bg-[var(--bg-secondary)] border border-[var(--border-subtle)] rounded-2xl flex items-center justify-between">
                           <div className="flex items-center gap-4">
                              <div className="w-10 h-10 rounded-full bg-[var(--bg-tertiary)] p-2">
                                 <img src="https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg" alt="OpenAI" className="w-full h-full invert opacity-60" width={40} height={40} />
                              </div>
                              <div>
                                 <p className="text-sm font-medium text-[var(--text-primary)]">OpenAI API</p>
                                 <p className="text-xs text-[var(--text-muted)]">Connected: gpt-4o-mini</p>
                              </div>
                           </div>
                           <div className="flex items-center gap-2">
                              <Key size={14} className="text-[var(--text-primary)]" aria-hidden="true" />
                              <span className="text-[10px] font-mono text-[var(--text-muted)]/80">**** **** **** 4291</span>
                           </div>
                        </div>
                        <button className="w-full py-4 bg-[var(--bg-secondary)] hover:bg-[var(--bg-tertiary)] border border-dashed border-[var(--border-subtle)] rounded-2xl text-xs font-medium text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-all">
                           + Add New Model Provider
                        </button>
                     </div>
                  </section>
               </div>
             )}

             {activeTab === 'appearance' && (
               <div className="space-y-8">
                  <section className="space-y-4">
                     <h3 className="text-xl font-display font-semibold text-[var(--text-primary)] tracking-tight">Interface Theme</h3>
                     <p className="text-[var(--text-muted)] text-sm">Choose how Noetix looks on your screen.</p>
                     
                     <div className="grid grid-cols-2 gap-4">
                        <button 
                          onClick={() => setTheme('light')}
                          className={`p-6 rounded-3xl border transition-all text-left group ${
                            theme === 'light' 
                              ? 'bg-[var(--bg-elevated)] border-[var(--accent)] ring-4 ring-[var(--accent-dim)]' 
                              : 'bg-[var(--bg-elevated)]/80 border-transparent hover:border-[var(--accent-dim)]'
                          }`}
                        >
                           <div className={`w-12 h-12 rounded-2xl flex items-center justify-center mb-6 transition-colors ${
                             theme === 'light' ? 'bg-[var(--accent)] text-white' : 'bg-[var(--bg-elevated)] text-[var(--text-muted)]'
                          }`}>
                              <Sun size={24} aria-hidden="true" />
                           </div>
                           <p className={`font-semibold transition-colors ${theme === 'light' ? 'text-[var(--text-primary)]' : 'text-[var(--text-secondary)]'}`}>Light Mode</p>
                           <p className="text-xs text-[var(--text-muted)] mt-1">Clean and high contrast</p>
                        </button>

                        <button 
                          onClick={() => setTheme('dark')}
                          className={`p-6 rounded-3xl border transition-all text-left group ${
                            theme === 'dark' 
                              ? 'bg-[var(--bg-tertiary)] border-[var(--accent)] ring-4 ring-[var(--accent-dim)]' 
                              : 'bg-[var(--bg-tertiary)]/80 border-[var(--border-subtle)] hover:border-[var(--border-default)]'
                          }`}
                        >
                           <div className={`w-12 h-12 rounded-2xl flex items-center justify-center mb-6 transition-colors ${
                             theme === 'dark' ? 'bg-[var(--accent)] text-[var(--bg-primary)]' : 'bg-[var(--bg-secondary)] text-[var(--text-muted)]'
                           }`}>
                              <Moon size={24} aria-hidden="true" />
                           </div>
                           <p className={`font-semibold transition-colors ${theme === 'dark' ? 'text-[var(--text-primary)]' : 'text-[var(--text-secondary)]'}`}>Noetix Dark</p>
                           <p className="text-xs text-[var(--text-muted)] mt-1">Immersive and ergonomic</p>
                        </button>
                     </div>
                  </section>
               </div>
             )}

             {activeTab !== 'general' && activeTab !== 'appearance' && (
               <div className="h-64 flex flex-col items-center justify-center border-2 border-dashed border-[var(--border-subtle)] rounded-3xl opacity-60">
                  <Zap size={32} className="text-[var(--border-default)] mb-4" />
                  <p className="text-sm font-medium text-[var(--text-muted)]/70 tracking-widest uppercase">Placeholder for {activeTab}</p>
               </div>
             )}
          </motion.div>
        </main>
      </div>
    </div>
  );
}

