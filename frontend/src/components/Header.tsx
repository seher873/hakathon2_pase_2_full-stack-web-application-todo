/**
 * Header component with navigation and user controls.
 *
 * Displays:
 * - App logo/title
 * - Navigation links (when authenticated)
 * - User email and logout button (when authenticated)
 * - Login/signup links (when not authenticated)
 */

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../hooks/useAuth';

const Header = () => {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold text-indigo-600">Todo App</span>
            </Link>
            {isAuthenticated && (
              <nav className="ml-6 flex space-x-8">
                <Link
                  href="/dashboard"
                  className="text-gray-900 hover:text-indigo-600 px-1 pt-1 text-sm font-medium"
                >
                  Dashboard
                </Link>
              </nav>
            )}
          </div>
          <div className="flex items-center">
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700 hidden md:block">
                  Welcome, {user?.email}
                </span>
                <button
                  onClick={logout}
                  className="ml-4 bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex space-x-4">
                <Link
                  href="/login"
                  className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Log in
                </Link>
                <Link
                  href="/signup"
                  className="bg-indigo-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-indigo-700"
                >
                  Sign up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;