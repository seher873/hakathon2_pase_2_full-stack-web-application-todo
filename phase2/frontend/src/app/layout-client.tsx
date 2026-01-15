'use client';

import React from 'react';
import Header from '../components/Header';
import { TaskProvider } from '../hooks/useTasks';

interface LayoutClientProps {
  children: React.ReactNode;
}

const LayoutClient: React.FC<LayoutClientProps> = ({ children }) => {
  return (
    <TaskProvider>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main>
          {children}
        </main>
      </div>
    </TaskProvider>
  );
};

export default LayoutClient;