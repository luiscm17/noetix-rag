import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MessageSquare, X, ArrowLeft, Loader2, Send, 
  ChevronRight, AlertCircle, ZoomIn, 
  ZoomOut, Bot, Sparkles, Search, Languages,
  ChevronLeft, FileText, Share2, MoreHorizontal,
  LayoutGrid, BookOpen
} from 'lucide-react';
import { getDocumentService } from '../services/factory';
import type { Document } from '../types/document';
import { useChatStore } from '../store/chatStore';

export default function Reader() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [isChatOpen, setIsChatOpen] = useState(true);
  const [doc, setDoc] = useState<Document | null>(null);
  const [loadingDoc, setLoadingDoc] = useState(true);
  const [zoom, setZoom] = useState(1);
  const [isScanning, setIsScanning] = useState(false);
  
  const { messages, loading: chatLoading, sendMessage, clearSession } = useChatStore();
  const [inputMsg, setInputMsg] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    clearSession();
    const fetchDoc = async () => {
      try {
        if (id) {
          const documentService = getDocumentService();
          const res = await documentService.getById(id);
          setDoc(res.document);
        }
      } catch (err) {
        console.error("Failed to load document", err);
      } finally {
        setLoadingDoc(false);
      }
    };
    fetchDoc();
  }, [id, clearSession]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!inputMsg.trim() || chatLoading) return;
    sendMessage(inputMsg.trim());
    setInputMsg('');
  };

  const handleDeepScan = () => {
    setIsScanning(true);
    setTimeout(() => {
      setIsScanning(false);
      sendMessage("I've analyzed the primary sections of this research. The methodology focuses on neural networks for rate prediction. What specific metric should I clarify?");
    }, 2000);
  };

  return (
    <div className="h-full flex flex-col bg-[var(--bg-primary)] text-[var(--text-primary)] overflow-hidden relative">
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-gradient-to-br from-brand/10 to-transparent rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-gradient-to-tl from-brand/5 to-transparent rounded-full blur-[150px] pointer-events-none" />

      <header className="h-16 border-b border-[var(--border-subtle)] flex items-center justify-between px-4 sm:px-6 bg-[var(--bg-elevated)]/90 backdrop-blur-2xl z-40">
        <div className="flex items-center gap-4 min-w-0">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2.5 px-3 py-2 hover:bg-[var(--bg-secondary)]/70 rounded-xl transition-all text-[var(--text-secondary)] hover:text-[var(--text-primary)] group border border-transparent hover:border-[var(--border-default)]"
          >
            <ArrowLeft size={18} className="group-hover:-translate-x-0.5 transition-transform" aria-hidden="true" />
            <span className="text-xs font-medium uppercase tracking-widest hidden sm:block">Library</span>
          </button>
          
          <div className="h-4 w-[1px] bg-[var(--border-subtle)] hidden sm:block" />
          
          {doc && (
            <div className="flex items-center gap-3 min-w-0">
              <div className="w-8 h-8 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-subtle)] flex items-center justify-center shrink-0">
                <FileText size={16} className="text-brand" aria-hidden="true" />
              </div>
              <div className="min-w-0 flex flex-col">
                <h2 className="text-sm font-medium truncate max-w-[200px] sm:max-w-md text-stone-200 tracking-tight">
                  {doc.title}
                </h2>
                <span className="text-[10px] text-stone-500 font-mono uppercase tracking-widest hidden sm:block">Research Document • v1.0</span>
              </div>
            </div>
          )}
        </div>
        
        <div className="flex items-center gap-2 sm:gap-3">
          <div className="hidden md:flex items-center bg-[var(--bg-secondary)]/70 border border-[var(--border-subtle)] rounded-lg h-9 px-1">
            <button className="p-1.5 hover:bg-[var(--bg-tertiary)] rounded-md text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors" aria-label="Share document">
              <Share2 size={16} />
            </button>
            <div className="w-[1px] h-4 bg-[var(--border-subtle)] mx-1" />
            <button className="p-1.5 hover:bg-[var(--bg-tertiary)] rounded-md text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors" aria-label="More options">
              <MoreHorizontal size={16} />
            </button>
          </div>

          <button
            onClick={() => setIsChatOpen(!isChatOpen)}
            className={`flex items-center gap-2 px-4 h-9 rounded-lg font-medium text-xs uppercase tracking-widest transition-all ${
              isChatOpen 
                ? 'bg-brand text-[#020617] shadow-md shadow-brand/20 hover:bg-brand-hover/95' 
                : 'bg-[var(--bg-secondary)] hover:bg-[var(--bg-tertiary)] text-[var(--text-secondary)] border border-[var(--border-subtle)]'
            }`}
          >
            <MessageSquare size={14} aria-hidden="true" />
            <span className="hidden sm:inline">AI Assistant</span>
          </button>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden relative">
        <main className="flex-1 overflow-y-auto bg-[var(--bg-primary)] p-4 sm:p-6 lg:p-8 relative scrollbar-hide">
          <div className="max-w-4xl mx-auto flex flex-col items-center">
            {loadingDoc ? (
              <div className="flex flex-col items-center justify-center py-40 gap-6">
                <div className="relative">
                  <Loader2 className="animate-spin text-brand" size={48} strokeWidth={1.5} />
                  <Sparkles className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-brand/40" size={16} aria-hidden="true" />
                </div>
                <div className="text-center">
                  <h3 className="text-stone-100 font-medium tracking-widest uppercase text-[10px] mb-2">Neural Ingestion Pipeline</h3>
                  <p className="text-stone-500 text-xs animate-pulse">Scanning semantic architecture...</p>
                </div>
              </div>
            ) : doc ? (
              <motion.div 
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                className="w-full relative group"
              >
                <div className="absolute top-4 left-1/2 -translate-x-1/2 flex items-center bg-[var(--bg-elevated)]/95 backdrop-blur-xl border border-[var(--border-subtle)] rounded-2xl p-1.5 shadow-2xl transition-all opacity-0 group-hover:opacity-100 focus-within:opacity-100 hover:scale-[1.02] z-30 translate-y-2 group-hover:translate-y-0">
                  <div className="flex items-center gap-1.5 px-3 border-r border-[var(--border-subtle)]">
                     <button onClick={() => setZoom(prev => Math.max(0.5, prev - 0.1))} className="p-1.5 hover:bg-[var(--bg-secondary)] rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors" aria-label="Zoom out">
                       <ZoomOut size={16} />
                     </button>
                     <span className="text-[10px] font-mono text-[var(--text-secondary)] w-10 text-center tracking-tighter">{Math.round(zoom * 100)}%</span>
                     <button onClick={() => setZoom(prev => Math.min(2, prev + 0.1))} className="p-1.5 hover:bg-[var(--bg-secondary)] rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors" aria-label="Zoom in">
                       <ZoomIn size={16} />
                     </button>
                  </div>
                  
                  <div className="flex items-center gap-1.5 px-3 border-r border-[var(--border-subtle)]">
                     <button className="p-1.5 hover:bg-[var(--bg-secondary)] rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors" aria-label="Previous page">
                        <ChevronLeft size={16} />
                     </button>
                     <span className="text-[10px] font-mono text-[var(--text-secondary)] tracking-[0.2em]">1/12</span>
                     <button className="p-1.5 hover:bg-[var(--bg-secondary)] rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors" aria-label="Next page">
                        <ChevronRight size={16} />
                     </button>
                  </div>

                  <div className="flex items-center gap-2 pl-2 pr-1">
                     <button 
                       onClick={handleDeepScan}
                       disabled={isScanning}
                       className="flex items-center gap-2 px-3 py-1.5 bg-brand/10 hover:bg-brand/20 text-brand rounded-xl transition-all border border-brand/25 overflow-hidden relative"
                     >
                       {isScanning ? (
                         <Loader2 size={14} className="animate-spin" />
                       ) : (
                         <Sparkles size={14} aria-hidden="true" />
                       )}
                       <span className="text-[10px] font-semibold uppercase tracking-tighter">Deep Scan</span>
                       {isScanning && (
                          <motion.div 
                            initial={{ x: '-100%' }}
                            animate={{ x: '100%' }}
                            transition={{ repeat: Infinity, duration: 1.5 }}
                            className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent"
                          />
                       )}
                     </button>
                     
                     <button className="p-1.5 hover:bg-[var(--bg-secondary)] rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors">
                        <LayoutGrid size={16} />
                     </button>
                  </div>
                </div>

                <div 
                  className="bg-[var(--bg-elevated)] backdrop-blur-3xl shadow-[0_40px_100px_rgba(15,23,42,0.45)] rounded-2xl overflow-hidden border border-[var(--border-subtle)] mx-auto transition-all"
                  style={{ width: `${zoom * 100}%`, maxWidth: '1000px' }}
                >
                  <div className="h-8 bg-[var(--bg-secondary)] border-b border-[var(--border-subtle)] flex items-center justify-between px-6">
                    <div className="flex items-center gap-2">
                       <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                       <span className="text-[9px] font-mono text-[var(--text-muted)] uppercase tracking-widest">Document Ingested</span>
                    </div>
                    <span className="text-[9px] font-mono text-[var(--text-muted)] uppercase tracking-[0.2em]">{doc.title} — PAGE 1</span>
                  </div>

                  <div className="w-full aspect-[1/1.414] bg-[var(--bg-primary)] relative group">
                    {doc?.file_path ? (
                      <iframe
                        src={`${doc.file_path}#toolbar=0&navpanes=0&view=FitH`}
                        className="w-full h-full border-none"
                        title={doc.title}
                      />
                    ) : (
                      <div className="flex flex-col items-center justify-center h-full text-stone-500 gap-4">
                        <AlertCircle size={48} className="opacity-20" aria-hidden="true" />
                        <p className="font-medium">Deep analysis engine ready. Document source missing.</p>
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="mt-12 mb-32 flex flex-col items-center gap-6">
                   <div className="flex gap-4">
                      <button className="px-6 py-2.5 bg-[var(--bg-secondary)] hover:bg-[var(--bg-tertiary)] border border-[var(--border-subtle)] rounded-xl text-xs font-medium text-[var(--text-primary)] transition-all shadow-md">
                        Identify Key Insights
                      </button>
                      <button className="px-6 py-2.5 bg-[var(--bg-secondary)] hover:bg-[var(--bg-tertiary)] border border-[var(--border-subtle)] rounded-xl text-xs font-medium text-[var(--text-primary)] transition-all shadow-md">
                        Synthesize Methodology
                      </button>
                   </div>
                   <p className="text-[10px] text-stone-700 uppercase tracking-[0.4em] font-mono">End of Surface Layer</p>
                </div>
              </motion.div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center py-40">
                <AlertCircle size={48} className="text-red-900/50 mb-4" />
                <h3 className="text-xl font-display font-semibold text-stone-300 tracking-tight">Access Denied</h3>
                <p className="text-stone-600 mt-2 text-sm">The document integrity check failed for this ID.</p>
              </div>
            )}
          </div>
        </main>

        <AnimatePresence>
          {isChatOpen && (
            <motion.aside 
              initial={{ x: 450, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 450, opacity: 0 }}
              transition={{ type: 'spring', damping: 30, stiffness: 200 }}
              className="fixed inset-y-0 right-0 sm:relative w-full sm:w-[420px] lg:w-[480px] bg-[var(--bg-elevated)] backdrop-blur-3xl border-l border-[var(--border-subtle)] flex flex-col shadow-[-32px_0_60px_rgba(15,23,42,0.25)] z-50 overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-brand/10 via-transparent to-transparent pointer-events-none" />

              <div className="h-16 border-b border-[var(--border-subtle)] flex items-center justify-between px-6 relative z-10">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-xl bg-brand/10 flex items-center justify-center border border-brand/25 relative group overflow-hidden">
                    <Bot size={18} className="text-brand" aria-hidden="true" />
                    <motion.div 
                      className="absolute inset-0 bg-white/20"
                      initial={{ scale: 0, opacity: 0 }}
                      whileHover={{ scale: 2, opacity: 1 }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                  <div className="flex flex-col">
                    <span className="font-semibold text-[10px] uppercase tracking-[0.2em] text-[var(--text-primary)]">Noetix Intelligence</span>
                    <span className="text-[9px] text-brand uppercase font-medium tracking-widest">Active reasoning: multi-agent</span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                   <button className="p-2 hover:bg-[var(--bg-secondary)] rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors" aria-label="Language settings">
                     <Languages size={18} />
                   </button>
                   <button
                     onClick={() => setIsChatOpen(false)}
                     className="p-2 hover:bg-[var(--bg-secondary)] rounded-lg text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors"
                     aria-label="Close chat"
                   >
                     <X size={18} />
                   </button>
                </div>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-8 scrollbar-hide relative z-10">
                {messages.length === 0 && (
                  <div className="h-full flex flex-col items-center justify-center text-center px-8 relative">
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-brand/5 rounded-full blur-[80px]" />
                    <div className="w-24 h-24 rounded-[32px] bg-[var(--bg-secondary)] flex items-center justify-center mb-8 border border-[var(--border-subtle)] relative overflow-hidden group">
                      <BookOpen size={40} className="text-stone-300 group-hover:text-brand transition-colors duration-700" aria-hidden="true" />
                      <div className="absolute inset-0 bg-gradient-to-tr from-brand/15 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                    <h3 className="text-[var(--text-primary)] font-display font-semibold text-2xl mb-4 tracking-tight">Research Co-pilot</h3>
                    <p className="text-[var(--text-secondary)] text-sm leading-relaxed font-medium">
                      Deep-scan enabled. I can extract semantic links, verify citations, and synthesize methodology across this entire document.
                    </p>
                    <div className="mt-10 grid grid-cols-1 gap-3 w-full">
                      {['Summarize Abstract', 'Analyze Methodology', 'Key Findings'].map(suggestion => (
                        <button 
                          key={suggestion}
                          onClick={() => sendMessage(suggestion)}
                          className="px-4 py-3 bg-[var(--bg-elevated)] hover:bg-[var(--bg-secondary)]/70 border border-[var(--border-subtle)] rounded-2xl text-[10px] font-semibold uppercase tracking-widest text-[var(--text-muted)] hover:text-brand transition-all"
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
                
                {messages.map((msg) => (
                  <motion.div
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    key={msg.id}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[85%] relative ${
                        msg.role === 'user'
                          ? 'bg-[var(--bg-elevated)] border border-[var(--border-default)] text-[var(--text-primary)] rounded-2xl rounded-tr-sm px-5 py-4 text-sm'
                          : 'bg-[var(--bg-secondary)]/60 border border-[var(--border-subtle)] text-[var(--text-primary)] rounded-3xl rounded-tl-sm px-6 py-5 text-sm shadow-md'
                      }`}
                    >
                      {msg.role === 'assistant' && (
                        <div className="flex items-center gap-2 mb-3">
                           <Bot size={12} className="text-brand" />
                           <span className="text-[9px] font-semibold uppercase tracking-widest text-stone-500">Response Analysis</span>
                        </div>
                      )}
                      
                      <div className="leading-relaxed font-medium text-[13px]">
                        {msg.content}
                      </div>

                      {msg.role === 'assistant' && (
                        <div className="mt-4 flex items-center gap-4 pt-4 border-t border-[var(--border-subtle)]">
                           <button className="flex items-center gap-1.5 text-[9px] font-semibold text-brand/80 hover:text-[var(--text-primary)] uppercase tracking-widest transition-all">
                             <Search size={10} aria-hidden="true" /> Link to Source
                           </button>
                           <div className="w-1 h-1 rounded-full bg-[var(--border-subtle)]" />
                           <button className="flex items-center gap-1.5 text-[9px] font-semibold text-[var(--text-muted)] hover:text-[var(--text-primary)] uppercase tracking-widest transition-all">
                             Verify Cite
                           </button>
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))}
                
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-[var(--bg-secondary)]/70 border border-[var(--border-subtle)] rounded-3xl px-6 py-4 flex items-center gap-4">
                      <div className="flex gap-1.5">
                        <span className="w-1.5 h-1.5 bg-brand rounded-full animate-bounce" />
                        <span className="w-1.5 h-1.5 bg-brand rounded-full animate-bounce [animation-delay:0.2s]" />
                        <span className="w-1.5 h-1.5 bg-brand rounded-full animate-bounce [animation-delay:0.4s]" />
                      </div>
                      <div className="flex flex-col">
                        <span className="text-[10px] uppercase font-medium tracking-[0.2em] text-stone-500">Contextualizing</span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              <div className="p-8 border-t border-[var(--border-subtle)] bg-[var(--bg-elevated)] relative z-10">
                <form onSubmit={handleSend} className="relative">
                  <input
                    type="text"
                    placeholder="Enter deep-reasoning prompt..."
                    className="w-full bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-3xl py-5 pl-6 pr-16 text-sm focus:outline-none focus:border-[var(--accent-dim)] focus:ring-2 focus:ring-[var(--accent-dim)] transition-all placeholder:text-[var(--text-muted)] font-medium"
                    value={inputMsg}
                    onChange={(e) => setInputMsg(e.target.value)}
                  />
                  <button
                    type="submit"
                    disabled={!inputMsg.trim() || chatLoading}
                    className="absolute right-2 top-2 w-[52px] h-[52px] bg-brand text-[#020617] rounded-[22px] flex items-center justify-center hover:scale-105 active:scale-95 transition-all disabled:opacity-30 disabled:hover:scale-100 shadow-md shadow-brand/20"
                  >
                    <Send size={20} aria-hidden="true" />
                  </button>
                </form>
                <div className="mt-6 flex items-center justify-center gap-6">
                   <div className="flex items-center gap-2">
                     <div className="w-1.5 h-1.5 rounded-full bg-brand" />
                     <span className="text-[9px] font-mono uppercase tracking-[0.2em] text-stone-600">Pro 3.5</span>
                   </div>
                   <div className="flex items-center gap-2">
                     <div className="w-1.5 h-1.5 rounded-full bg-stone-800" />
                     <span className="text-[9px] font-mono uppercase tracking-[0.2em] text-stone-600">RAG-Verified</span>
                   </div>
                </div>
              </div>
            </motion.aside>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
