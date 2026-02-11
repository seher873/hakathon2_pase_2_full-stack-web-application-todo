'use client';

import { useState } from 'react';
import { TaskForm } from '@/components/TaskForm';
import { TaskList } from '@/components/TaskList';
import { useTasks } from '@/hooks/useTasks';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Plus } from 'lucide-react';

export default function DashboardPage() {
  const { 
    tasks, 
    isLoading, 
    error, 
    createTask, 
    updateTask, 
    deleteTask, 
    toggleTaskComplete,
    filter,
    searchQuery,
    setFilter,
    setSearchQuery
  } = useTasks();
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  const handleAddTask = async (taskData) => {
    try {
      await createTask(taskData);
      setShowAddForm(false);
    } catch (err) {
      // Error is handled by the hook
      console.error('Error adding task:', err);
    }
  };

  const handleUpdateTask = async (taskData) => {
    try {
      await updateTask(editingTask.id, taskData);
      setEditingTask(null);
    } catch (err) {
      // Error is handled by the hook
      console.error('Error updating task:', err);
    }
  };

  const handleEditClick = (task) => {
    setEditingTask(task);
    setShowAddForm(false);
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <Card className="rounded-xl shadow-lg">
          <CardHeader className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-t-xl">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <CardTitle className="text-2xl">Todo Dashboard</CardTitle>
              <Button 
                onClick={() => {
                  setShowAddForm(!showAddForm);
                  setEditingTask(null);
                }}
                className="bg-white text-indigo-600 hover:bg-indigo-50 flex items-center gap-2"
              >
                <Plus className="h-4 w-4" />
                {showAddForm ? 'Cancel' : 'Add Task'}
              </Button>
            </div>
          </CardHeader>
          <CardContent className="p-6">
            {showAddForm && (
              <TaskForm
                onSubmit={handleAddTask}
                isLoading={false}
                error={error}
              />
            )}

            {editingTask && (
              <TaskForm
                onSubmit={handleUpdateTask}
                isLoading={false}
                error={error}
                initialTitle={editingTask.title}
                initialDescription={editingTask.description || ''}
                onCancel={handleCancelEdit}
                submitButtonText="Update Task"
              />
            )}

            <TaskList
              tasks={tasks}
              isLoading={isLoading}
              error={error}
              onDelete={deleteTask}
              onToggleComplete={toggleTaskComplete}
              onEdit={handleEditClick}
              filter={filter}
              onFilterChange={setFilter}
              searchQuery={searchQuery}
              onSearchChange={setSearchQuery}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}