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
    <li className="col-span-1 bg-white rounded-lg shadow divide-y divide-gray-200">
      <div className="w-full flex items-center justify-between p-6 space-x-6">
        <div className="flex-1 truncate">
          <div className="flex items-center space-x-3">
            <h3
              className={`text-sm font-medium truncate ${
                task.completed ? 'line-through text-gray-500' : 'text-gray-900'
              }`}
            >
              {task.title}
            </h3>
            {task.completed && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Completed
              </span>
            )}
          </div>
          {task.description && (
            <p className="mt-1 text-sm text-gray-500 truncate">{task.description}</p>
          )}
          <div className="mt-2 flex items-center text-xs text-gray-500">
            <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
          </div>
        </div>
        <div className="flex flex-col items-center space-y-2">
          <button
            onClick={handleToggleComplete}
            disabled={isLoading}
            className={`relative inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
              task.completed
                ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
            } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50`}
          >
            {task.completed ? 'Mark Pending' : 'Mark Complete'}
          </button>
        </div>
      </div>
      <div>
        <div className="-mt-px flex divide-x divide-gray-200">
          <div className="w-0 flex-1 flex">
            <button
              onClick={onEdit}
              disabled={isLoading}
              className="relative -mr-px w-0 flex-1 inline-flex items-center justify-center py-4 text-sm text-gray-700 font-medium border border-transparent rounded-bl-lg hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              <svg
                className="w-5 h-5 text-gray-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
              <span className="ml-3">Edit</span>
            </button>
          </div>
          <div className="-ml-px w-0 flex-1 flex">
            <button
              onClick={handleDelete}
              disabled={isLoading || isDeleting}
              className="relative w-0 flex-1 inline-flex items-center justify-center py-4 text-sm text-gray-700 font-medium border border-transparent rounded-br-lg hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              <svg
                className="w-5 h-5 text-gray-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="ml-3">{isDeleting ? 'Deleting...' : 'Delete'}</span>
            </button>
          </div>
        </div>
      </div>
    </li>
  );
};