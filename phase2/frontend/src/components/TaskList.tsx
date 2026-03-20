/**
 * Task list component for displaying user tasks.
 *
 * Renders a list of tasks with filtering and sorting options and
 * integrates with the task management context.
 */

import React from 'react';
import { TaskListProps, Task, TaskFilter, TaskSortBy, TaskSortOrder } from '../types';
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
  sortBy = 'created_at',
  sortOrder = 'desc',
  onSortChange,
}) => {
  // Filter tasks based on the selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'completed') return task.completed;
    if (filter === 'pending') return !task.completed;
    return true; // 'all' filter
  });

  // Count tasks by status
  const completedCount = tasks?.filter(t => t.completed)?.length || 0;
  const pendingCount = (tasks?.length || 0) - completedCount;

  // Sort options
  const sortOptions: { value: TaskSortBy; label: string }[] = [
    { value: 'created_at', label: 'Date Created' },
    { value: 'title', label: 'Title' },
    { value: 'priority', label: 'Priority' },
    { value: 'due_date', label: 'Due Date' },
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      {/* Search, Filter and Sort Controls */}
      <div className="bg-gray-50 px-4 py-3 flex flex-col gap-3">
        {/* First row: Task count and filter buttons */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 md:gap-0">
          <div className="flex flex-col md:flex-row flex-wrap items-start md:items-center gap-2 md:gap-3 w-full md:w-auto">
            <div className="text-sm text-gray-600 bg-white px-2 py-1 rounded-md shadow-sm border border-gray-200 mb-2 md:mb-0 min-w-[80px] text-center md:text-left">
              {tasks?.length || 0} {(tasks?.length || 0) === 1 ? 'task' : 'tasks'}
            </div>

            <div className="flex flex-wrap gap-2 justify-center md:justify-start">
              <button
                onClick={() => onFilterChange && onFilterChange('all')}
                className={`px-3 py-1.5 text-xs md:text-sm font-medium rounded-md transition-all duration-200 ${
                  filter === 'all'
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
                }`}
              >
                All ({tasks?.length || 0})
              </button>
              <button
                onClick={() => onFilterChange && onFilterChange('pending')}
                className={`px-3 py-1.5 text-xs md:text-sm font-medium rounded-md transition-all duration-200 ${
                  filter === 'pending'
                    ? 'bg-amber-500 text-white shadow-sm'
                    : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
                }`}
              >
                Pending ({pendingCount})
              </button>
              <button
                onClick={() => onFilterChange && onFilterChange('completed')}
                className={`px-3 py-1.5 text-xs md:text-sm font-medium rounded-md transition-all duration-200 ${
                  filter === 'completed'
                    ? 'bg-green-500 text-white shadow-sm'
                    : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
                }`}
              >
                Completed ({completedCount})
              </button>
            </div>
          </div>

          {/* Search Input */}
          {onSearchChange && (
            <div className="w-full md:w-64 mt-2 md:mt-0">
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
                  className="block w-full pl-10 pr-3 py-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200"
                  placeholder="Search tasks..."
                />
              </div>
            </div>
          )}
        </div>

        {/* Second row: Sort controls */}
        {onSortChange && (
          <div className="flex flex-wrap items-center gap-3 pt-2 border-t border-gray-200">
            <span className="text-sm text-gray-600 font-medium">Sort by:</span>
            <select
              value={sortBy}
              onChange={(e) => onSortChange(e.target.value as TaskSortBy, sortOrder)}
              className="flex h-9 rounded-md border border-gray-300 bg-white px-3 py-1 text-sm ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {sortOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <button
              onClick={() => onSortChange(sortBy, sortOrder === 'asc' ? 'desc' : 'asc')}
              className="flex items-center gap-1 px-3 py-1.5 text-xs md:text-sm font-medium rounded-md bg-white text-gray-700 hover:bg-gray-50 border border-gray-300 transition-all duration-200"
              title={`Currently ${sortOrder === 'asc' ? 'ascending' : 'descending'}`}
            >
              {sortOrder === 'asc' ? (
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                </svg>
              ) : (
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              )}
              {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
            </button>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-3 mx-4 mt-3 rounded-md bg-gradient-to-r from-red-50 to-red-100">
          <div className="flex flex-col md:flex-row items-center">
            <div className="flex-shrink-0 mb-2 md:mb-0">
              <svg
                className="h-5 w-5 text-red-500"
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
            <div className="ml-0 md:ml-3">
              <p className="text-sm font-medium text-red-800">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && !tasks.length && (
        <div className="px-4 py-12">
          <div className="flex flex-col items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600 mb-3"></div>
            <p className="text-gray-500 text-base">Loading your tasks...</p>
            <p className="text-gray-400 text-sm mt-1">Please wait a moment</p>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && (!filteredTasks || filteredTasks.length === 0) && (
        <div className="px-4 py-12 text-center">
          <div className="mx-auto w-16 h-16 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mb-4">
            <svg
              className="w-8 h-8 text-gray-400"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </div>
          <h3 className="mt-2 text-lg font-semibold text-gray-900">No tasks yet</h3>
          <p className="mt-2 text-gray-600 text-sm max-w-md mx-auto">
            {filter === 'completed'
              ? "You haven't completed any tasks yet. Start by creating a new task!"
              : filter === 'pending'
              ? "You have no pending tasks. Great job staying on top of things!"
              : "Get started by creating your first task."}
          </p>
          {!filter || filter === 'all' && (
            <p className="mt-2 text-xs text-gray-500">
              Your tasks will appear here once you create them.
            </p>
          )}
        </div>
      )}

      {/* Task List */}
      {filteredTasks && filteredTasks.length > 0 && (
        <ul className="divide-y divide-gray-100">
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
