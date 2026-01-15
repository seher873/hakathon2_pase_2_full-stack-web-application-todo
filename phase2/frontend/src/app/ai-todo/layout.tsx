import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI-Powered Todo App',
  description: 'Manage tasks with natural language processing',
};

export default function AITodoLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-600 via-purple-700 to-purple-800">
      {children}
    </div>
  );
}