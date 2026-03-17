import { motion } from 'framer-motion';
import { 
  Database, 
  Layers, 
  CheckCircle2, 
  AlertCircle,
  Activity,
  HardDrive,
  RefreshCw,
  MoreHorizontal,
  ChevronRight,
  Cpu,

} from 'lucide-react';

const stats = [
  { label: 'Total Vectors', value: '1.2M', icon: <Layers size={18} />, color: 'text-brand' },
  { label: 'Indexed Pages', value: '4,821', icon: <Database size={18} />, color: 'text-sky-500' },
  { label: 'Avg Latency', value: '124ms', icon: <Activity size={18} />, color: 'text-emerald-500' },
  { label: 'Storage Used', value: '2.4GB', icon: <HardDrive size={18} />, color: 'text-sky-400' },
];

const jobs = [
  { name: 'Financial_Q3_Analysis', status: 'completed', type: 'Vector Indexing', time: '2 mins ago' },
  { name: 'Technical_Review_v2', status: 'processing', type: 'Semantic Chunking', time: 'Active' },
  { name: 'Market_Trends_2024', status: 'error', type: 'Ingestion', time: '1 hour ago' },
  { name: 'Drilling_Rate_Model', status: 'completed', type: 'Re-indexing', time: '3 hours ago' },
];

export default function KnowledgeBase() {
  return (
    <div className="p-10 max-w-7xl mx-auto h-full overflow-y-auto scrollbar-hide">
      <header className="mb-12 flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-4xl font-display font-semibold text-[var(--text-primary)] tracking-tight flex items-center gap-4">
            Knowledge Base
            <span className="text-xs px-2 py-1 bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 rounded-lg uppercase tracking-widest font-semibold">Online</span>
          </h1>
          <p className="text-[var(--text-secondary)] mt-2 text-lg">Manage and monitor your decentralized RAG engine.</p>
        </div>
        
        <button className="flex items-center gap-2 px-6 py-3 bg-[var(--bg-elevated)] hover:bg-[var(--bg-secondary)]/70 border border-[var(--border-subtle)] rounded-xl text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-all">
          <RefreshCw size={18} /> Re-sync All
        </button>
      </header>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {stats.map((stat, idx) => (
            <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="p-6 bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-3xl shadow-sm"
          >
            <div className={`w-10 h-10 rounded-xl bg-[var(--bg-secondary)] flex items-center justify-center mb-4 ${stat.color}`}>
              {stat.icon}
            </div>
            <p className="text-3xl font-display font-semibold text-[var(--text-primary)] mb-1">{stat.value}</p>
            <p className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-widest">{stat.label}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-display font-semibold text-[var(--text-primary)] tracking-tight">Recent Indexing Jobs</h3>
            <button className="text-xs font-semibold text-brand hover:underline uppercase tracking-widest">View History</button>
          </div>
          
          <div className="space-y-3">
             {jobs.map((job) => (
               <div key={job.name} className="p-4 bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-2xl flex items-center justify-between group hover:bg-[var(--bg-secondary)]/70 transition-all">
                  <div className="flex items-center gap-4">
                     <div className={`p-2 rounded-lg ${
                       job.status === 'completed' ? 'bg-emerald-500/10 text-emerald-500' :
                       job.status === 'error' ? 'bg-red-500/10 text-red-500' :
                       'bg-brand/10 text-brand animate-pulse'
                     }`}>
                        {job.status === 'completed' ? <CheckCircle2 size={18} /> : 
                         job.status === 'error' ? <AlertCircle size={18} /> : 
                         <RefreshCw size={18} className="animate-spin" />}
                     </div>
                     <div>
                        <p className="text-sm font-medium text-[var(--text-primary)]">{job.name}</p>
                        <p className="text-[10px] text-[var(--text-muted)] font-mono uppercase tracking-widest">{job.type} • {job.time}</p>
                     </div>
                  </div>
                  <button className="p-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <MoreHorizontal size={18} className="text-[var(--text-muted)] hover:text-[var(--text-primary)]" />
                  </button>
               </div>
             ))}
          </div>
        </div>

        <div className="space-y-6">
           <h3 className="text-xl font-display font-semibold text-[var(--text-primary)] tracking-tight">System Health</h3>
           <div className="p-6 bg-[var(--bg-elevated)] border border-[var(--border-subtle)] rounded-3xl space-y-6">
              <div className="space-y-3">
                 <div className="flex justify-between items-center">
                    <span className="text-xs font-medium text-[var(--text-secondary)] uppercase tracking-widest">Vector Store (Pinecone)</span>
                    <span className="text-[10px] font-mono text-emerald-500">OPTIMAL</span>
                 </div>
                 <div className="h-1.5 w-full bg-[var(--bg-secondary)] rounded-full overflow-hidden">
                    <div className="h-full w-[88%] bg-emerald-500 rounded-full" />
                 </div>
              </div>

              <div className="space-y-3">
                 <div className="flex justify-between items-center">
                    <span className="text-xs font-medium text-[var(--text-secondary)] uppercase tracking-widest">Embedding API</span>
                    <span className="text-[10px] font-mono text-brand">99.2% Uptime</span>
                 </div>
                 <div className="h-1.5 w-full bg-[var(--bg-secondary)] rounded-full overflow-hidden">
                    <div className="h-full w-[94%] bg-brand rounded-full shadow-[0_0_10px_rgba(127,166,196,0.4)]" />
                 </div>
              </div>

              <div className="space-y-3">
                 <div className="flex justify-between items-center">
                    <span className="text-xs font-medium text-[var(--text-secondary)] uppercase tracking-widest">Local Cache</span>
                    <span className="text-[10px] font-mono text-sky-500">HEAVY LOAD</span>
                 </div>
                 <div className="h-1.5 w-full bg-[var(--bg-secondary)] rounded-full overflow-hidden">
                    <div className="h-full w-[72%] bg-sky-500 rounded-full" />
                 </div>
              </div>

              <div className="pt-4 border-t border-[var(--border-subtle)]">
                 <button className="w-full flex items-center justify-between p-4 bg-[var(--bg-secondary)] hover:bg-[var(--bg-tertiary)] border border-[var(--border-subtle)] rounded-xl transition-all group">
                    <div className="flex items-center gap-3">
                       <Cpu size={18} className="text-[var(--text-muted)] group-hover:text-brand" />
                       <span className="text-sm font-medium text-[var(--text-primary)]">GPU Resource Monitor</span>
                    </div>
                    <ChevronRight size={16} className="text-[var(--text-muted)] group-hover:text-[var(--text-primary)]" />
                 </button>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
}
