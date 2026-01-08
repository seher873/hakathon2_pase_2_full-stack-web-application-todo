'use client';

import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useTasks } from '../../hooks/useTasks';
import { TaskForm } from '../../components/TaskForm';
import { TaskList } from '../../components/TaskList';
import { Task } from '../../types';
import ProtectedRoute from '../../components/ProtectedRoute';

const DashboardPage = () => {
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
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="md:flex md:items-center md:justify-between mb-6">
            <div className="flex-1 min-w-0">
              <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                My Tasks
              </h2>
            </div>
            <div className="mt-4 flex md:mt-0 md:ml-4">
              <button
                onClick={() => {
                  setEditingTask(null);
                  setShowForm(true);
                }}
                className="ml-3 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Add Task
              </button>
            </div>
          </div>

          {showForm && (
            <TaskForm
              onSubmit={handleSubmitForm}
              initialTitle={editingTask?.title || ''}
              initialDescription={editingTask?.description || ''}
              onCancel={handleCancelForm}
              submitButtonText={editingTask ? 'Update Task' : 'Add Task'}
            />
          )}

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
      </main>
    </ProtectedRoute>
  );
};

export default DashboardPage;