'use client';

import React, { useState, useEffect } from 'react';
import ChatPanel from '../../components/chat/ChatPanel';
import { useAuth } from '../../hooks/useAuth'; // Assuming there's an auth hook

const DashboardPage = () => {
  const { user, loading } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [showChat, setShowChat] = useState(true);

  if (loading) {
    return <div className="dashboard">Loading...</div>;
  }

  if (!user) {
    return <div className="dashboard">Please log in to access the dashboard</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Todo Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user.name || user.email}!</span>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-content">
          <section className="tasks-section">
            <div className="section-header">
              <h2>Your Tasks</h2>
              <button className="toggle-chat-btn" onClick={() => setShowChat(!showChat)}>
                {showChat ? 'Hide Chat' : 'Show Chat'}
              </button>
            </div>

            {/* Tasks list would go here */}
            <div className="tasks-list">
              <p>You have no tasks yet. Try using the AI chat to create some!</p>
            </div>
          </section>
        </div>

        {showChat && (
          <aside className="chat-sidebar">
            <div className="chat-container">
              <ChatPanel user={user} />
            </div>
          </aside>
        )}
      </main>
    </div>
  );
};

export default DashboardPage;