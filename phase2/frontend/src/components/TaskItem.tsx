/**
 * Individual task item component.
 *
 * Displays a single task with controls for completing,
 * editing, and deleting the task. Shows priority, tags, and due date.
 */

import React, { useState } from 'react';
import { TaskItemProps, TaskPriority } from '../types';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';

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

  // Priority badge colors
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  // Check if due date is overdue
  const isOverdue = (dueDate?: string) => {
    if (!dueDate) return false;
    return new Date(dueDate) < new Date() && !task.completed;
  };

  // Format due date for display
  const formatDueDate = (dueDate?: string) => {
    if (!dueDate) return '';
    const date = new Date(dueDate);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <li className={`bg-white rounded-lg shadow-sm border transition-all duration-200 hover:shadow-md ${
      task.completed
        ? 'border-gray-200 bg-gray-50'
        : 'border-gray-200 hover:border-indigo-200'
    }`}>
      <div className="p-3 sm:p-4 flex flex-col md:flex-row items-start justify-between gap-3 md:gap-0">
        <div className="flex flex-col md:flex-row items-start md:items-start w-full gap-2 md:gap-3">
          <Checkbox
            checked={task.completed}
            onCheckedChange={() => handleToggleComplete()}
            disabled={isLoading}
            className="mt-0.5"
          />

          <div className="flex-1 min-w-0 w-full">
            <div className="flex flex-col md:flex-row md:items-center gap-1 md:gap-2 mb-1">
              <h3
                className={`text-sm md:text-base font-semibold ${
                  task.completed ? 'line-through text-gray-500' : 'text-gray-900'
                }`}
              >
                {task.title}
              </h3>
              <div className="flex flex-wrap items-center gap-1">
                {task.completed && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 whitespace-nowrap">
                    Completed
                  </span>
                )}
                {task.priority && (
                  <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border whitespace-nowrap ${getPriorityColor(task.priority)}`}>
                    {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)} Priority
                  </span>
                )}
                {task.due_date && (
                  <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium whitespace-nowrap ${
                    isOverdue(task.due_date)
                      ? 'bg-red-100 text-red-800 border border-red-200'
                      : 'bg-blue-50 text-blue-700 border border-blue-200'
                  }`}>
                    <svg className="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {formatDueDate(task.due_date)}
                    {isOverdue(task.due_date) && ' (Overdue)'}
                  </span>
                )}
              </div>
            </div>

            {task.description && (
              <p className={`mt-1 text-xs md:text-sm ${
                task.completed ? 'text-gray-400' : 'text-gray-600'
              } break-words max-w-full`}>
                {task.description}
              </p>
            )}

            {task.tags && task.tags.trim() && (
              <div className="flex flex-wrap gap-1 mt-2">
                {task.tags.split(',').filter(tag => tag.trim()).map((tag, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-50 text-indigo-700 border border-indigo-200"
                  >
                    #{tag.trim()}
                  </span>
                ))}
              </div>
            )}

            <div className="mt-2 flex items-center text-xs text-gray-500">
              <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-1 md:space-x-2 flex-shrink-0 mt-2 md:mt-0">
          {task.url && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => window.open(task.url, '_blank')}
              disabled={isLoading}
              className="h-8 w-8 p-0"
              title="Open link"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </Button>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={onEdit}
            disabled={isLoading}
            className="h-8 w-8 p-0"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={handleDelete}
            disabled={isLoading || isDeleting}
            className="h-8 w-8 p-0"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </Button>
        </div>
      </div>
    </li>
  );
};
