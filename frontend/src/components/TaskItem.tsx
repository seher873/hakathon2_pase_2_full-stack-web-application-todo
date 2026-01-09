/**
 * Individual task item component.
 *
 * Displays a single task with controls for completing,
 * editing, and deleting the task.
 */

import React, { useState } from 'react';
import { TaskItemProps } from '../types';

export const TaskItem: React.FC<TaskItemProps> = ({
  task,
  onDelete,
  onToggleComplete,
  onEdit,
  isLoading = false,
}) => {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      setIsDeleting(true);
      try {
        await onDelete();
      } finally {
        setIsDeleting(false);
      }
    }
  };

  const handleToggleComplete = async () => {
    try {
      await onToggleComplete(!task.completed);
    } catch (error) {
      // Error is handled by parent component
    }
  };

  return (
    <li className={`bg-white rounded-xl shadow-sm border transition-all duration-200 hover:shadow-md ${
      task.completed
        ? 'border-gray-200 bg-gray-50'
        : 'border-gray-200 hover:border-indigo-200'
    }`}>
      <div className="p-5 flex items-start justify-between">
        <div className="flex items-start space-x-4 flex-1 min-w-0">
          <button
            onClick={handleToggleComplete}
            disabled={isLoading}
            className={`mt-1 flex-shrink-0 h-5 w-5 rounded-full border flex items-center justify-center transition-all duration-200 ${
              task.completed
                ? 'bg-green-500 border-green-500 text-white'
                : 'border-gray-300 hover:border-indigo-500'
            }`}
          >
            {task.completed && (
              <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>

          <div className="flex-1 min-w-0">
            <div className="flex items-center">
              <h3
                className={`text-base font-semibold truncate ${
                  task.completed ? 'line-through text-gray-500' : 'text-gray-900'
                }`}
              >
                {task.title}
              </h3>
              {task.completed && (
                <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Completed
                </span>
              )}
            </div>

            {task.description && (
              <p className={`mt-1 text-sm truncate ${
                task.completed ? 'text-gray-400' : 'text-gray-600'
              }`}>
                {task.description}
              </p>
            )}

            <div className="mt-2 flex items-center text-xs text-gray-500">
              <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2 flex-shrink-0 ml-4">
          <button
            onClick={onEdit}
            disabled={isLoading}
            className="p-2 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
            title="Edit task"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>

          <button
            onClick={handleDelete}
            disabled={isLoading || isDeleting}
            className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50"
            title="Delete task"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </li>
  );
};