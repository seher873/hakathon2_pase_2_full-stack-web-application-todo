/**
 * Task form component for creating and editing tasks.
 *
 * Provides a form interface for users to create new tasks
 * or update existing ones with validation and error handling.
 */

import React, { useState } from 'react';
import type { TaskFormProps, CreateTaskRequest, UpdateTaskRequest } from '../types';

interface TaskFormComponentProps extends Omit<TaskFormProps, 'onSubmit'> {
  onSubmit: (data: CreateTaskRequest | UpdateTaskRequest) => Promise<void>;
  onCancel?: () => void;
  submitButtonText?: string;
}

export const TaskForm: React.FC<TaskFormComponentProps> = ({
  onSubmit,
  isLoading = false,
  error,
  initialTitle = '',
  initialDescription = '',
  onCancel,
  submitButtonText = 'Add Task',
}) => {
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!title.trim()) {
      newErrors.title = 'Title is required';
    } else if (title.trim().length > 255) {
      newErrors.title = 'Title must be 255 characters or less';
    }

    if (description && description.length > 1000) {
      newErrors.description = 'Description must be 1000 characters or less';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      // Determine if this is an update or create based on whether we have initial values
      const isUpdate = !!initialTitle || !!initialDescription;

      const taskData = isUpdate ? {
        title: title.trim() || undefined,
        description: description.trim() || undefined,
      } : {
        title: title.trim(),
        description: description.trim() || undefined,
      };

      await onSubmit(taskData);

      // Reset form after successful submission (only for create)
      if (!isUpdate) {
        setTitle('');
        setDescription('');
        setErrors({});
      }
    } catch (err) {
      // Error is handled by parent component
    }
  };

  const handleReset = () => {
    setTitle(initialTitle);
    setDescription(initialDescription);
    setErrors({});
    if (onCancel) {
      onCancel();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <div className="px-6 py-6">
          <div className="grid grid-cols-1 gap-6">
            <div>
              <label
                htmlFor="title"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Task Title *
              </label>
              <input
                type="text"
                id="title"
                value={title}
                onChange={(e) => {
                  setTitle(e.target.value);
                  if (errors.title) {
                    setErrors((prev) => {
                      const newErrors = { ...prev };
                      delete newErrors.title;
                      return newErrors;
                    });
                  }
                }}
                className={`w-full px-4 py-3 text-base border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 ${
                  errors.title ? 'border-red-300 bg-red-50' : 'border-gray-300 hover:border-gray-400'
                }`}
                placeholder="What needs to be done?"
                disabled={isLoading}
              />
              {errors.title && (
                <p className="mt-2 text-sm text-red-600 flex items-center">
                  <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  {errors.title}
                </p>
              )}
            </div>

            <div>
              <label
                htmlFor="description"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Description
              </label>
              <textarea
                id="description"
                rows={4}
                value={description}
                onChange={(e) => {
                  setDescription(e.target.value);
                  if (errors.description) {
                    setErrors((prev) => {
                      const newErrors = { ...prev };
                      delete newErrors.description;
                      return newErrors;
                    });
                  }
                }}
                className={`w-full px-4 py-3 text-base border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 ${
                  errors.description ? 'border-red-300 bg-red-50' : 'border-gray-300 hover:border-gray-400'
                }`}
                placeholder="Add details about this task..."
                disabled={isLoading}
              />
              {errors.description && (
                <p className="mt-2 text-sm text-red-600 flex items-center">
                  <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  {errors.description}
                </p>
              )}
            </div>
          </div>

          {error && (
            <div className="mt-4 rounded-lg bg-red-50 border border-red-200 p-4">
              <div className="flex items-center">
                <div className="flex-shrink-0">
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
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">{error}</h3>
                </div>
              </div>
            </div>
          )}
        </div>
        <div className="bg-gray-50 px-6 py-4 flex justify-end space-x-3">
          {(onCancel || initialTitle) && (
            <button
              type="button"
              onClick={handleReset}
              disabled={isLoading}
              className="px-5 py-2.5 text-base font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-all duration-200"
            >
              Cancel
            </button>
          )}
          <button
            type="submit"
            disabled={isLoading}
            className="px-5 py-2.5 text-base font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-all duration-200 shadow-sm hover:shadow-md flex items-center"
          >
            {isLoading && (
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            )}
            {isLoading ? 'Saving...' : submitButtonText}
          </button>
        </div>
      </div>
    </form>
  );
};