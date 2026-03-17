import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Send, 
  Sparkles, 
  Search, 
  MessageSquare, 
  Plus, 
  Clock, 
  User,
  Bot as BotIcon,
  MoreHorizontal,

} from 'lucide-react';
import { useChatStore } from '../store/chatStore';

export default function Chat() {
  const { messages, loading, sendMessage } = useChatStore();
  const [input, setInput] = useState('');
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    sendMessage(input);
    setInput('');
  };

  return (
    <div className="h-full flex flex-col bg-[var(--bg-primary)] relative overflow-hidden">
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-gradient-to-bl from-brand/10 to-transparent blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-gradient-to-tr from-brand/5 to-transparent blur-[120px] rounded-full pointer-events-none" />

      <header className="h-16 border-b border-[var(--border-subtle)] flex items-center justify-between px-8 bg-[var(--bg-elevated)]/80 backdrop-blur-xl z-10 shrink-0">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-brand/10 border border-brand/30 flex items-center justify-center">
            <MessageSquare size={20} className="text-brand" aria-hidden="true" />
          </div>
          <div>
            <h1 className="text-lg font-display font-semibold text-[var(--text-primary)] tracking-tight">Noetix Chat</h1>
            <p className="text-[10px] text-[var(--text-muted)] font-medium uppercase tracking-widest">Multi-Agent Intelligence Session</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
<button className="flex items-center gap-2 px-4 py-2 bg-[var(--bg-elevated)] hover:bg-[var(--bg-secondary)]/70 border border-[var(--border-subtle)] rounded-xl text-xs font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-all" aria-label="View history">
              <Clock size={14} aria-hidden="true" /> History
           </button>
           <button className="flex items-center gap-2 px-4 py-2 bg-brand text-[#020617] rounded-xl text-xs font-semibold hover:bg-brand-hover shadow-md shadow-brand/20 transition-all">
             <Plus size={14} /> New Session
           </button>
        </div>
      </header>

      <div className="flex-1 overflow-hidden flex flex-col max-w-4xl mx-auto w-full relative z-10">
        <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center px-12">
               <motion.div 
                 initial={{ opacity: 0, scale: 0.9 }}
                 animate={{ opacity: 1, scale: 1 }}
                 className="w-20 h-20 rounded-[32px] bg-[var(--bg-secondary)] border border-[var(--border-subtle)] flex items-center justify-center mb-8"
               >
                 <Sparkles size={32} className="text-brand" aria-hidden="true" />
               </motion.div>
               <h2 className="text-3xl font-display font-semibold text-[var(--text-primary)] mb-4 tracking-tight">How can I help you today?</h2>
               <p className="text-[var(--text-secondary)] max-w-md text-sm leading-relaxed mb-10">
                 Ask anything about your documents, synthesize data across your library, or start a reasoning process.
               </p>
               
               <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
                 {[
                   "Summarize my latest research",
                   "Compare drilling rate models",
                   "Explain Neural Network findings",
                   "Draft a technical summary"
                 ].map((suggestion, idx) => (
                   <motion.button 
                     key={suggestion}
                     initial={{ opacity: 0, y: 10 }}
                     animate={{ opacity: 1, y: 0 }}
                     transition={{ delay: 0.1 + idx * 0.05 }}
                     onClick={() => sendMessage(suggestion)}
                     className="p-4 bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-2xl text-left transition-all group hover:bg-[var(--bg-secondary)]/70"
                   >
                     <p className="text-xs font-semibold text-[var(--text-muted)] group-hover:text-brand mb-1 transition-colors uppercase tracking-widest">Suggestion</p>
                     <p className="text-sm text-[var(--text-primary)] group-hover:text-brand transition-colors">{suggestion}</p>
                   </motion.button>
                 ))}
               </div>
            </div>
          ) : (
            <div className="space-y-8 pb-10">
              {messages.map((msg, idx) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex gap-4 max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border ${
                      msg.role === 'user' 
                        ? 'bg-[var(--bg-secondary)] border-[var(--border-default)]' 
                        : 'bg-brand/10 border-brand/25'
                    }`}>
                      {msg.role === 'user' ? <User size={16} className="text-[var(--text-muted)]" aria-hidden="true" /> : <BotIcon size={16} className="text-brand" aria-hidden="true" />}
                    </div>
                    
                    <div className={`p-5 rounded-2xl border ${
                      msg.role === 'user'
                        ? 'bg-[var(--bg-elevated)] border-[var(--border-default)] text-[var(--text-primary)]'
                        : 'bg-[var(--bg-secondary)]/60 border-[var(--border-subtle)] text-[var(--text-primary)]'
                    }`}>
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                      {msg.role === 'assistant' && (
                        <div className="mt-4 pt-4 border-t border-[var(--border-subtle)] flex items-center justify-between">
                           <div className="flex gap-4">
<button className="text-[10px] font-semibold text-[var(--text-muted)] hover:text-brand uppercase tracking-widest transition-colors flex items-center gap-1" aria-label="View sources">
                                <Search size={10} aria-hidden="true" /> View Sources
                              </button>
                              <button className="text-[10px] font-semibold text-[var(--text-muted)] hover:text-[var(--text-primary)] uppercase tracking-widest transition-colors flex items-center gap-1" aria-label="Compare versions">
                                Compare v1.0
                             </button>
                           </div>
<button className="text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors" aria-label="More options">
                               <MoreHorizontal size={14} />
                            </button>
                        </div>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
              <div ref={scrollRef} />
              
              {loading && (
                <div className="flex justify-start">
                   <div className="flex gap-4 max-w-[85%]">
                      <div className="w-8 h-8 rounded-lg bg-brand/10 border border-brand/25 flex items-center justify-center shrink-0 animate-pulse">
                         <Sparkles size={16} className="text-brand" />
                      </div>
                      <div className="bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-2xl px-6 py-4 flex items-center gap-4">
                        <div className="flex gap-1.5">
                          <span className="w-1.5 h-1.5 bg-brand rounded-full animate-bounce" />
                          <span className="w-1.5 h-1.5 bg-brand rounded-full animate-bounce [animation-delay:0.2s]" />
                          <span className="w-1.5 h-1.5 bg-brand rounded-full animate-bounce [animation-delay:0.4s]" />
                        </div>
                      </div>
                   </div>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="p-6 bg-transparent shrink-0">
          <form 
            onSubmit={handleSend}
            className="relative max-w-4xl mx-auto group"
          >
            <input 
              type="text" 
              placeholder="Ask anything about your documents…"
              autoComplete="off"
              name="chat-message"
              className="w-full h-16 bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-2xl pl-6 pr-16 text-sm focus:outline-none focus:border-[var(--accent-dim)] focus:ring-2 focus:ring-[var(--accent-dim)] transition-colors placeholder:text-[var(--text-muted)]"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button 
              type="submit"
              disabled={!input.trim() || loading}
              className="absolute right-2 top-2 w-12 h-12 bg-brand text-[#020617] rounded-[14px] flex items-center justify-center hover:scale-105 active:scale-95 transition-all disabled:opacity-30 disabled:hover:scale-100 shadow-md shadow-brand/20"
            >
              <Send size={20} aria-hidden="true" />
            </button>
          </form>
          <div className="mt-4 flex items-center justify-center gap-8">
             <div className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-brand" />
                <span className="text-[9px] font-mono text-[var(--text-muted)] uppercase tracking-widest">Active: Pro 3.5</span>
             </div>
             <div className="flex items-center gap-2 text-stone-600">
                <span className="text-[9px] font-mono uppercase tracking-widest">RAG Engine: ONLINE</span>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}
