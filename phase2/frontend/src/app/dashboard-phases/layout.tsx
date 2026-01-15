import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI-Powered Todo Dashboard',
  description: 'Track your progress through each phase of the AI-Powered Todo App development',
};

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-indigo-50 to-violet-50">
      {children}
    </div>
  );
}