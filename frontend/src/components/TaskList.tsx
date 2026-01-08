/**
 * Task list component for displaying user tasks.
 * 
 * Renders a list of tasks with filtering options and
 * integrates with the task management context.
 */

import React from 'react';
import { TaskListProps, Task, TaskFilter } from '../types';
import { TaskItem } from './TaskItem';

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  isLoading,
  error,
  onDelete,
  onToggleComplete,
  onEdit,
  filter = 'all',
  onFilterChange,
  searchQuery = '',
  onSearchChange,
}) => {
  // Filter tasks based on the selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'completed') return task.completed;
    if (filter === 'pending') return !task.completed;
    return true; // 'all' filter
  });

  // Count tasks by status
  const completedCount = tasks.filter(t => t.completed).length;
  const pendingCount = tasks.length - completedCount;

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-md">
      {/* Search and Filter Controls */}
      <div className="bg-gray-50 px-4 py-3 flex flex-col sm:flex-row items-start sm:items-center justify-between sm:px-6 border-b space-y-3 sm:space-y-0">
        <div className="flex items-center">
          <span className="mr-4 text-sm text-gray-700">
            {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
          </span>
          <div className="flex space-x-2">
            <button
              onClick={() => onFilterChange('all')}
              className={`px-3 py-1 text-xs font-medium rounded-full ${
                filter === 'all'
                  ? 'bg-indigo-100 text-indigo-800'
                  : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
              }`}
            >
              All ({tasks.length})
            </button>
            <button
              onClick={() => onFilterChange('pending')}
              className={`px-3 py-1 text-xs font-medium rounded-full ${
                filter === 'pending'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
              }`}
            >
              Pending ({pendingCount})
            </button>
            <button
              onClick={() => onFilterChange('completed')}
              className={`px-3 py-1 text-xs font-medium rounded-full ${
                filter === 'completed'
                  ? 'bg-green-100 text-green-800'
                  : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
              }`}
            >
              Completed ({completedCount})
            </button>
          </div>
        </div>

        {/* Search Input */}
        {onSearchChange && (
          <div className="w-full sm:w-auto">
            <div className="relative rounded-md shadow-sm">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                </svg>
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => onSearchChange(e.target.value)}
                className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 pr-12 py-2 sm:text-sm border border-gray-300 rounded-md"
                placeholder="Search tasks..."
              />
            </div>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mx-4 mt-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-red-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && !tasks.length && (
        <div className="px-4 py-12 sm:px-6">
          <div className="flex justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          </div>
          <p className="mt-4 text-center text-sm text-gray-500">Loading tasks...</p>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && filteredTasks.length === 0 && (
        <div className="px-4 py-12 sm:px-6 text-center">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
          <p className="mt-1 text-sm text-gray-500">
            {filter === 'completed'
              ? "You haven't completed any tasks yet."
              : filter === 'pending'
              ? "You have no pending tasks. Great job!"
              : "Get started by creating a new task."}
          </p>
        </div>
      )}

      {/* Task List */}
      {filteredTasks.length > 0 && (
        <ul className="divide-y divide-gray-200">
          {filteredTasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onDelete={() => onDelete(task.id)}
              onToggleComplete={(completed) => onToggleComplete(task.id, completed)}
              onEdit={() => onEdit(task)}
              isLoading={isLoading}
            />
          ))}
        </ul>
      )}
    </div>
  );
};