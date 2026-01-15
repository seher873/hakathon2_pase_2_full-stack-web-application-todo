'use client';

import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useTasks } from '../../hooks/useTasks';
import { TaskForm } from '../../components/TaskForm';
import { TaskList } from '../../components/TaskList';
import { Task } from '../../types';
import ProtectedRoute from '../../components/ProtectedRoute';

const TodoPage = () => {
  const { user } = useAuth();
  const {
    tasks,
    isLoading: tasksLoading,
    error,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskComplete,
    setFilter,
    setSearchQuery,
    filter,
    searchQuery,
  } = useTasks();
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showForm, setShowForm] = useState(false);

  const handleCreateTask = async (taskData: any) => {
    await createTask(taskData);
    setShowForm(false);
    setEditingTask(null);
  };

  const handleUpdateTask = async (taskData: any) => {
    if (!editingTask) return;

    await updateTask(editingTask.id, taskData);
    setShowForm(false);
    setEditingTask(null);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleSubmitForm = async (taskData: any) => {
    if (editingTask) {
      await handleUpdateTask(taskData);
    } else {
      await handleCreateTask(taskData);
    }
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  return (
    <ProtectedRoute>
      <main className="max-w-7xl mx-auto py-6 px-4 sm:py-8 sm:px-6 lg:px-8">
        <div className="px-2 sm:px-0">
          {/* Page Header */}
          <div className="mb-6 sm:mb-8">
            <div className="flex flex-col sm:flex-row md:flex-row sm:items-center md:items-center sm:justify-between md:justify-between gap-4 sm:gap-0">
              <div className="flex-1 min-w-0">
                <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl md:leading-9 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                  My Tasks
                </h2>
                <p className="mt-1 text-sm text-gray-600 sm:mt-2">
                  Manage and track your daily tasks efficiently
                </p>
              </div>
              <div className="flex justify-center sm:justify-end">
                <button
                  onClick={() => {
                    setEditingTask(null);
                    setShowForm(true);
                  }}
                  className="inline-flex items-center px-4 py-2 text-sm font-semibold text-white bg-gradient-to-r from-indigo-600 to-purple-600 border border-transparent rounded-lg shadow-sm sm:px-6 sm:py-3 sm:text-base hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200"
                >
                  <svg className="-ml-1 mr-2 h-4 w-4 sm:h-5 sm:w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Add Task
                </button>
              </div>
            </div>
          </div>

          {/* Task Form Section */}
          {showForm && (
            <div className="mb-6 sm:mb-8">
              <TaskForm
                onSubmit={handleSubmitForm}
                initialTitle={editingTask?.title || ''}
                initialDescription={editingTask?.description || ''}
                onCancel={handleCancelForm}
                submitButtonText={editingTask ? 'Update Task' : 'Add Task'}
              />
            </div>
          )}

          {/* Task List Section */}
          <div className="transition-all duration-300 ease-in-out">
            <TaskList
              tasks={tasks}
              isLoading={tasksLoading}
              error={error}
              onDelete={deleteTask}
              onToggleComplete={toggleTaskComplete}
              onEdit={handleEditTask}
              filter={filter}
              searchQuery={searchQuery}
              onFilterChange={setFilter}
              onSearchChange={setSearchQuery}
            />
          </div>
        </div>
      </main>
    </ProtectedRoute>
  );
};

export default TodoPage;