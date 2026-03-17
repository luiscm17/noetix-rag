import { 
  LayoutDashboard, 
  FileText, 
  MessageSquare, 
  Database, 
  Settings,
  Menu,
  ChevronLeft,
  LogOut,
  BookOpen
} from 'lucide-react';
import { NavLink, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useState } from 'react';
import { useAuthStore } from '../../store/authStore';

const navItems = [
  { icon: <LayoutDashboard size={20} aria-hidden="true" />, label: 'Dashboard', path: '/dashboard' },
  { icon: <FileText size={20} aria-hidden="true" />, label: 'Documents', path: '/dashboard' },
  { icon: <MessageSquare size={20} aria-hidden="true" />, label: 'Chat', path: '/chat' },
  { icon: <Database size={20} aria-hidden="true" />, label: 'Knowledge Base', path: '/knowledge' },
];

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(true);
  const navigate = useNavigate();
  const logout = useAuthStore((state) => state.logout);
  const user = useAuthStore((state) => state.user);

  return (
    <aside 
      className={`
        h-screen flex flex-col 
        bg-[var(--bg-primary)] border-r border-[var(--border-subtle)] 
        transition-all duration-300 relative z-50 
        ${isCollapsed ? 'w-20' : 'w-64'}
      `}
    >
      <div className="absolute inset-0 bg-gradient-to-b from-brand/5 to-transparent pointer-events-none" />
      
      <div className="h-16 flex items-center px-6 mb-8 mt-2 relative z-10">
        <div className="w-9 h-9 rounded-xl bg-brand/10 border border-brand/20 flex items-center justify-center shrink-0">
          <BookOpen className="text-brand" size={20} strokeWidth={1.5} aria-hidden="true" />
        </div>
        {!isCollapsed && (
          <motion.span 
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            className="ml-3 font-display font-semibold text-lg tracking-tight text-[var(--text-primary)] whitespace-nowrap"
          >
            Noetix
          </motion.span>
        )}
      </div>

      <nav className="flex-1 px-3.5 space-y-1.5 relative z-10">
        {navItems.map((item) => (
          <NavLink
            key={item.label}
            to={item.path}
            className={({ isActive }) => `
              flex items-center h-12 rounded-xl transition-all relative group
              ${isActive 
                ? 'bg-brand/10 text-brand border border-brand/20 shadow-sm' 
                : 'text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-secondary)]/40'
              }
              ${isCollapsed ? 'justify-center px-0' : 'px-4'}
            `}
          >
            <div className="shrink-0">{item.icon}</div>
            {!isCollapsed && (
              <motion.span 
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="ml-3 font-medium text-sm"
              >
                {item.label}
              </motion.span>
            )}
            
            {isCollapsed && (
              <div className="absolute left-full ml-4 px-2 py-1 bg-[var(--bg-secondary)] border border-[var(--border-subtle)] rounded text-xs text-[var(--text-primary)] opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity whitespace-nowrap z-[60]">
                {item.label}
              </div>
            )}
          </NavLink>
        ))}
      </nav>

      <div className="px-3.5 pb-6 space-y-1.5 relative z-10">
        <NavLink
            to="/settings"
            className={({ isActive }) => `
              flex items-center h-12 rounded-xl transition-all relative group
              ${isActive 
                ? 'bg-brand/10 text-brand border border-brand/20 shadow-sm' 
                : 'text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-secondary)]/40'
              }
              ${isCollapsed ? 'justify-center px-0' : 'px-4'}
            `}
          >
          <Settings size={20} aria-hidden="true" />
          {!isCollapsed && (
             <motion.span 
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="ml-3 font-medium text-sm"
             >
               Settings
             </motion.span>
         )}
        </NavLink>

        <button 
            onClick={() => {
              logout();
              navigate('/login');
            }}
            className={`
              w-full flex items-center h-12 rounded-xl transition-colors relative group
              text-red-500/70 hover:text-red-500 hover:bg-red-500/5 border border-transparent hover:border-red-500/10
              ${isCollapsed ? 'justify-center px-0' : 'px-4'}
            `}
            aria-label="Logout"
          >
           <LogOut size={20} aria-hidden="true" />
           {!isCollapsed && (
             <motion.span 
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="ml-3 font-medium text-sm"
             >
               Logout
             </motion.span>
         )}
        </button>

        <div className="pt-4 border-t border-[var(--border-subtle)] mt-4">
           <button 
             onClick={() => setIsCollapsed(!isCollapsed)}
             className={`
               w-full h-10 rounded-xl 
               bg-[var(--bg-secondary)]/50 hover:bg-[var(--bg-tertiary)]
               flex items-center transition-colors border border-[var(--border-subtle)] 
               text-[var(--text-muted)] hover:text-[var(--text-primary)]
               ${isCollapsed ? 'justify-center' : 'px-4 gap-3'}
             `}
             aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
           >
             {isCollapsed ? <Menu size={18} aria-hidden="true" /> : (
               <>
                 <ChevronLeft size={16} aria-hidden="true" />
                 <span className="text-[10px] font-semibold uppercase tracking-widest">Collapse</span>
               </>
             )}
           </button>
        </div>

        <div className={`mt-6 flex items-center transition-all ${isCollapsed ? 'justify-center' : 'px-2'}`}>
           <div className="w-10 h-10 rounded-full bg-[var(--bg-tertiary)] border border-[var(--border-default)] flex items-center justify-center overflow-hidden">
               <img 
                 src={`https://ui-avatars.com/api/?name=${user?.username || 'User'}&background=1c1917&color=fafaf9`} 
                 alt="User avatar" 
                 width={40} 
                 height={40} 
               />
           </div>
           {!isCollapsed && (
             <motion.div 
               initial={{ opacity: 0 }}
               animate={{ opacity: 1 }}
               className="ml-3 min-w-0"
             >
                <p className="text-xs font-medium text-[var(--text-primary)] truncate">{user?.username || 'User'}</p>
                <p className="text-[10px] text-[var(--text-muted)] font-mono uppercase tracking-widest">Premium</p>
             </motion.div>
           )}
        </div>
      </div>
    </aside>
  );
}
