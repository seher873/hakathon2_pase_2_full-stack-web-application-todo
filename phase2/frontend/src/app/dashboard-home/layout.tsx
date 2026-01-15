import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Dashboard Home | AI-Powered Todo App',
  description: 'Home page for dashboard options',
};

export default function DashboardHomeLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
      {children}
    </div>
  );
}