import Sidebar from '../components/layout/Sidebar';

export default function MainLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-y-auto scrollbar-hide bg-gradient-to-b from-transparent via-[var(--bg-secondary)]/40 to-[var(--bg-primary)]/80">
        {children}
      </main>
    </div>
  );
}
