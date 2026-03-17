import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useDocStore } from '../store/docStore';
import { 
  UploadCloud, 
  Clock, 
  AlertCircle, 
  Search, 
  Plus, 
  MoreHorizontal,
  Download,
  FileText,
  ChevronDown,
  LayoutGrid,
  List,

} from 'lucide-react';

export default function Dashboard() {
  const { documents, loading, error, fetchDocuments, uploadDocument } = useDocStore();
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('table');

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      try {
        setIsUploading(true);
        await uploadDocument(file);
      } catch (err) {
        console.error("Upload failed", err);
      } finally {
        setIsUploading(false);
        if (fileInputRef.current) fileInputRef.current.value = '';
      }
    }
  };

  const getStatusStyle = (status: string) => {
    switch (status.toLowerCase()) {
      case 'processed':
      case 'ready':
        return 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20';
      case 'indexing':
        return 'bg-nexus-accent/10 text-nexus-accent border-nexus-accent/20';
      case 'processing':
        return 'bg-blue-500/10 text-blue-500 border-blue-500/20';
      case 'analyzed':
        return 'bg-teal-500/10 text-teal-500 border-teal-500/20';
      case 'error':
        return 'bg-red-500/10 text-red-500 border-red-500/20';
      default:
        return 'bg-nexus-panel/50 text-nexus-text-muted border-nexus-border';
    }
  };

  return (
    <div className="p-6 sm:p-10 max-w-[1400px] mx-auto">
      <header className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-10">
        <div>
          <h1 className="text-4xl font-display font-semibold text-[var(--text-primary)] tracking-tight flex items-center gap-4">
            My Documents 
            <span className="text-[var(--text-muted)] font-body font-medium text-lg">— {documents.length} files</span>
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="relative group">
            <button className="flex items-center gap-2 px-4 h-11 bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-xl text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-secondary)]/70 shadow-sm transition-all">
              All Documents <ChevronDown size={14} aria-hidden="true" />
            </button>
          </div>

          <div className="relative flex-1 sm:min-w-[300px]">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-[var(--text-muted)]" size={18} aria-hidden="true" />
            <input 
              type="text" 
              placeholder="Search documents…"
              autoComplete="off"
              name="search"
              className="w-full h-11 bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-xl pl-12 pr-4 text-sm focus:outline-none focus:border-[var(--accent-dim)] focus:ring-2 focus:ring-[var(--accent-dim)] transition-colors placeholder:text-[var(--text-muted)]"
            />
          </div>

          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isUploading}
            className="flex items-center gap-2 px-6 h-11 bg-[var(--accent)] text-white rounded-xl font-semibold text-sm hover:bg-[var(--accent-hover)] shadow-md shadow-[var(--accent-dim)] transition-all disabled:opacity-50"
          >
            {isUploading ? (
              <Clock className="animate-spin" size={16} />
            ) : (
              <Plus size={18} />
            )}
            New Document
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
            accept=".pdf"
          />

          <div className="flex bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-xl p-1 shadow-sm">
            <button 
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-lg transition-all ${viewMode === 'grid' ? 'bg-[var(--bg-secondary)]/70 text-[var(--text-primary)] shadow-sm' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'}`}
            >
              <LayoutGrid size={18} />
            </button>
            <button 
              onClick={() => setViewMode('table')}
              className={`p-2 rounded-lg transition-all ${viewMode === 'table' ? 'bg-[var(--bg-secondary)]/70 text-[var(--text-primary)] shadow-sm' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'}`}
            >
              <List size={18} />
            </button>
          </div>
        </div>
      </header>

      {error && (
        <div className="mb-8 p-4 bg-[var(--accent-dim)] border border-[var(--accent-dim)] rounded-2xl flex items-center gap-3 text-[var(--accent-hover)] text-sm" role="alert">
          <AlertCircle size={20} aria-hidden="true" />
          <span>{error}</span>
        </div>
      )}

      {documents.length === 0 && !loading && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          onClick={() => fileInputRef.current?.click()}
          className="border-2 border-dashed border-[var(--border-subtle)] rounded-[32px] bg-[var(--bg-elevated)] py-24 flex flex-col items-center justify-center cursor-pointer group hover:bg-[var(--bg-secondary)]/70 hover:border-[var(--border-default)] transition-all shadow-sm"
        >
          <div className="w-20 h-20 rounded-3xl bg-[var(--bg-secondary)] flex items-center justify-center mb-6 group-hover:scale-110 transition-transform border border-[var(--border-subtle)] shadow-sm">
             <UploadCloud size={32} className="text-[var(--text-muted)] group-hover:text-[var(--accent)] transition-colors" aria-hidden="true" />
          </div>
          <p className="text-lg font-medium text-[var(--text-secondary)]">Drag & drop PDF files or <span className="text-[var(--accent)] underline cursor-pointer">browse</span></p>
          <p className="text-[var(--text-muted)] text-sm mt-2 font-mono text-xs">Maximum file size 50MB</p>
        </motion.div>
      )}

      {loading && documents.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-32 gap-6">
           <div className="w-12 h-12 rounded-full border-2 border-[var(--accent-dim)] border-t-[var(--accent)] animate-spin" />
           <p className="text-[var(--text-muted)] font-medium uppercase tracking-widest text-[10px]">Loading Collection</p>
        </div>
      ) : documents.length > 0 && (
        <div className="overflow-x-auto">
           <table className="w-full border-separate border-spacing-y-3">
             <thead>
               <tr className="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-[0.2em]">
                 <th className="px-6 py-4 text-left font-medium">Name</th>
                 <th className="px-6 py-4 text-left font-medium">Pages</th>
                 <th className="px-6 py-4 text-left font-medium">Uploaded</th>
                 <th className="px-6 py-4 text-left font-medium">Status</th>
                 <th className="px-6 py-4 text-right font-medium">Actions</th>
               </tr>
             </thead>
             <tbody>
               {documents.map((doc, idx) => (
                 <motion.tr
                   key={doc.document_id}
                   initial={{ opacity: 0, y: 10 }}
                   animate={{ opacity: 1, y: 0 }}
                   transition={{ delay: idx * 0.03 }}
                   className="group cursor-pointer"
                   onClick={() => navigate(`/reader/${doc.document_id}`)}
                 >
                   <td className="px-6 py-4 bg-[var(--bg-elevated)] border-y border-l border-[var(--border-subtle)] rounded-l-2xl group-hover:bg-[var(--bg-secondary)]/60 transition-colors">
                     <div className="flex items-center gap-4">
                       <div className="w-10 h-10 rounded-xl bg-[var(--accent-dim)] flex items-center justify-center border border-[var(--accent-dim)] text-[var(--accent)]">
                         <FileText size={20} aria-hidden="true" />
                       </div>
                       <span className="font-medium text-[var(--text-primary)] group-hover:text-[var(--accent)] transition-colors truncate max-w-[300px]">
                         {doc.title}
                       </span>
                     </div>
                   </td>
                   <td className="px-6 py-4 bg-[var(--bg-elevated)] border-y border-[var(--border-subtle)] group-hover:bg-[var(--bg-secondary)]/60 transition-colors">
                     <span className="text-sm font-mono text-[var(--text-muted)]">{doc.page_count}</span>
                   </td>
                   <td className="px-6 py-4 bg-[var(--bg-elevated)] border-y border-[var(--border-subtle)] group-hover:bg-[var(--bg-secondary)]/60 transition-colors">
                     <span className="text-sm text-[var(--text-muted)]">Just now</span>
                   </td>
                   <td className="px-6 py-4 bg-[var(--bg-elevated)] border-y border-[var(--border-subtle)] group-hover:bg-[var(--bg-secondary)]/60 transition-colors">
                     <span className={`px-3 py-1 rounded-lg text-[10px] font-semibold uppercase tracking-widest flex items-center gap-2 w-fit border ${getStatusStyle(doc.status)}`}>
                       <span className={`w-1.5 h-1.5 rounded-full ${doc.status === 'processed' ? 'bg-emerald-500' : 'bg-current'}`} />
                       {doc.status}
                     </span>
                   </td>
                   <td className="px-6 py-4 bg-[var(--bg-elevated)] border-y border-r border-[var(--border-subtle)] rounded-r-2xl group-hover:bg-[var(--bg-secondary)]/60 transition-colors text-right">
                     <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
<button className="p-2 hover:bg-[var(--accent-dim)] rounded-lg text-[var(--text-muted)] hover:text-[var(--accent-hover)] transition-colors" aria-label="Download document">
                          <Download size={16} />
                        </button>
<button className="p-2 hover:bg-[var(--accent-dim)] rounded-lg text-[var(--text-muted)] hover:text-[var(--accent-hover)] transition-colors" aria-label="More options">
                          <MoreHorizontal size={16} />
                        </button>
                     </div>
                   </td>
                 </motion.tr>
               ))}
             </tbody>
           </table>
        </div>
      )}
    </div>
  );
}

