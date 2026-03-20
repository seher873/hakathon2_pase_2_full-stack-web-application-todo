/**
 * Task form component for creating and editing tasks.
 *
 * Provides a form interface for users to create new tasks
 * or update existing ones with validation and error handling.
 * Includes priority, tags, and due date fields.
 */

import React, { useState } from 'react';
import type { TaskFormProps, CreateTaskRequest, UpdateTaskRequest, TaskPriority } from '../types';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

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
  const [url, setUrl] = useState('');
  const [priority, setPriority] = useState<TaskPriority>('medium');
  const [tags, setTags] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!title.trim()) {
      newErrors.title = 'Title is required';
    } else if (title.trim().length > 200) {
      newErrors.title = 'Title must be 200 characters or less';
    }

    if (description && description.length > 1000) {
      newErrors.description = 'Description must be 1000 characters or less';
    }

    if (url && !isValidUrl(url)) {
      newErrors.url = 'Please enter a valid URL';
    }

    if (dueDate) {
      const selectedDate = new Date(dueDate);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      if (selectedDate < today) {
        newErrors.dueDate = 'Due date cannot be in the past';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const isValidUrl = (string: string): boolean => {
    try {
      new URL(string);
      return true;
    } catch (_) {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      // Determine if this is an update or create based on whether we have initial values
      const isUpdate = !!initialTitle || !!initialDescription;

      // Keep tags as comma-separated string
      const tagsString = tags.trim();

      const taskData = isUpdate ? {
        title: title.trim() || undefined,
        description: description.trim() || undefined,
        url: url.trim() || undefined,
        priority: priority || undefined,
        tags: tagsString || undefined,
        due_date: dueDate || undefined,
      } : {
        title: title.trim(),
        description: description.trim() || undefined,
        url: url.trim() || undefined,
        priority,
        tags: tagsString || undefined,
        due_date: dueDate || undefined,
      };

      await onSubmit(taskData);

      // Reset form after successful submission (only for create)
      if (!isUpdate) {
        setTitle('');
        setDescription('');
        setUrl('');
        setPriority('medium');
        setTags('');
        setDueDate('');
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
    <form onSubmit={handleSubmit} className="mb-6 w-full">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden w-full">
        <div className="px-3 sm:px-4 py-3 sm:py-4 md:px-6">
          <div className="grid grid-cols-1 gap-3 sm:gap-4">
            <div className="grid w-full max-w-sm items-center gap-1.5">
              <Label htmlFor="title">Task Title *</Label>
              <Input
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
                placeholder="What needs to be done?"
                disabled={isLoading}
                className={errors.title ? 'border-red-500' : ''}
              />
              {errors.title && (
                <p className="text-xs md:text-sm text-red-600 flex items-center">
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
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Description
              </label>
              <Textarea
                id="description"
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
                placeholder="Add details about this task..."
                disabled={isLoading}
                className={errors.description ? 'border-red-500' : ''}
              />
              {errors.description && (
                <p className="text-xs md:text-sm text-red-600 flex items-center">
                  <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  {errors.description}
                </p>
              )}
            </div>

            {/* Priority Selection */}
            <div className="grid w-full max-w-sm items-center gap-1.5">
              <Label htmlFor="priority">Priority</Label>
              <select
                id="priority"
                value={priority}
                onChange={(e) => setPriority(e.target.value as TaskPriority)}
                disabled={isLoading}
                className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            {/* Tags Input */}
            <div className="grid w-full max-w-sm items-center gap-1.5">
              <Label htmlFor="tags">Tags (comma-separated)</Label>
              <Input
                type="text"
                id="tags"
                value={tags}
                onChange={(e) => {
                  setTags(e.target.value);
                }}
                placeholder="work, urgent, home"
                disabled={isLoading}
              />
              <p className="text-xs text-gray-500">Separate multiple tags with commas</p>
            </div>

            {/* Due Date */}
            <div className="grid w-full max-w-sm items-center gap-1.5">
              <Label htmlFor="dueDate">Due Date (Optional)</Label>
              <Input
                type="date"
                id="dueDate"
                value={dueDate}
                onChange={(e) => {
                  setDueDate(e.target.value);
                  if (errors.dueDate) {
                    setErrors((prev) => {
                      const newErrors = { ...prev };
                      delete newErrors.dueDate;
                      return newErrors;
                    });
                  }
                }}
                disabled={isLoading}
                className={errors.dueDate ? 'border-red-500' : ''}
              />
              {errors.dueDate && (
                <p className="text-xs md:text-sm text-red-600 flex items-center">
                  <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  {errors.dueDate}
                </p>
              )}
            </div>

            <div className="grid w-full max-w-sm items-center gap-1.5">
              <Label htmlFor="url">URL (Optional)</Label>
              <Input
                type="url"
                id="url"
                value={url}
                onChange={(e) => {
                  setUrl(e.target.value);
                  if (errors.url) {
                    setErrors((prev) => {
                      const newErrors = { ...prev };
                      delete newErrors.url;
                      return newErrors;
                    });
                  }
                }}
                placeholder="https://example.com"
                disabled={isLoading}
                className={errors.url ? 'border-red-500' : ''}
              />
              {errors.url && (
                <p className="text-xs md:text-sm text-red-600 flex items-center">
                  <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  {errors.url}
                </p>
              )}
            </div>
          </div>

          {error && (
            <div className="mt-3 rounded-md bg-red-50 border border-red-200 p-3">
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
                  <h3 className="text-sm font-medium text-red-800">{error}</h3>
                </div>
              </div>
            </div>
          )}
        </div>
        <div className="bg-gray-50 px-3 sm:px-4 py-3 flex flex-col md:flex-row justify-end items-stretch md:items-center gap-2 md:gap-3 pt-3 pb-3">
          {(onCancel || initialTitle) && (
            <Button
              type="button"
              onClick={handleReset}
              disabled={isLoading}
              variant="outline"
              className="w-full md:w-auto"
            >
              Cancel
            </Button>
          )}
          <Button
            type="submit"
            disabled={isLoading}
            className="w-full md:w-auto"
          >
            {isLoading && (
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            )}
            {isLoading ? 'Saving...' : submitButtonText}
          </Button>
        </div>
      </div>
    </form>
  );
};
