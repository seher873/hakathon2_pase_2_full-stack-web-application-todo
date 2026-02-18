/**
 * Utility functions for formatting chat messages and responses
 */

/**
 * Format a message for display in the chat interface
 * @param {string} content - The raw message content
 * @param {string} type - The type of message (user, ai, system)
 * @param {Object} data - Optional structured data from the response
 * @returns {string} Formatted content for display
 */
export function formatMessageContent(content, type, data) {
  if (type === 'ai' && data) {
    return formatAIResponse(content, data);
  }

  return content;
}

/**
 * Format an AI response based on its structured data
 * @param {string} content - The AI's text response
 * @param {Object} data - Structured data from tool results
 * @returns {string} Enhanced response with formatted data
 */
export function formatAIResponse(content, data) {
  let formattedResponse = content;

  if (data && typeof data === 'object') {
    // Check if it's a task creation response
    if (data.created_task || hasTaskData(data)) {
      const taskData = data.created_task || extractTaskFromData(data);
      if (taskData) {
        formattedResponse += `\n\n✅ Task created: ${taskData.title || taskData.name || 'Untitled task'}`;
        if (taskData.description) {
          formattedResponse += `\n📝 ${taskData.description}`;
        }
        if (taskData.due_date) {
          formattedResponse += `\n📅 Due: ${formatDate(taskData.due_date)}`;
        }
      }
    }
    // Check if it's a task update response
    else if (data.updated_task || hasTaskUpdateData(data)) {
      const taskData = data.updated_task || extractTaskFromData(data);
      if (taskData) {
        formattedResponse += `\n\n🔄 Task updated: ${taskData.title || 'Untitled task'}`;
        if (taskData.status) {
          formattedResponse += `\n>Status: ${taskData.status}`;
        }
      }
    }
    // Check if it's a task listing response
    else if (Array.isArray(data) || data.task_list || hasTaskListData(data)) {
      const tasks = data.task_list || data;
      if (Array.isArray(tasks) && tasks.length > 0) {
        const completedCount = tasks.filter(t => t.status === 'completed').length;
        const pendingCount = tasks.length - completedCount;

        formattedResponse += `\n\n📋 Found ${tasks.length} tasks: ${pendingCount} pending, ${completedCount} completed`;

        // Add previews of the tasks if there aren't too many
        if (tasks.length <= 5) {
          const taskPreviews = tasks.map(task =>
            `• ${task.title} ${task.status === 'completed' ? '✅' : '⏳'}`
          ).join('\n');
          formattedResponse += `\n\n${taskPreviews}`;
        }
      }
    }
    // Check if it's a deletion response
    else if (data.deleted_task_id || hasDeletionData(data)) {
      const taskId = data.deleted_task_id || extractTaskIdFromData(data);
      formattedResponse += `\n\n🗑️ Task deleted (ID: ${taskId})`;
    }
    // Check if it's a toggle response
    else if (data.toggled_task || hasToggleData(data)) {
      const taskData = data.toggled_task || extractTaskFromData(data);
      if (taskData) {
        const status = taskData.status === 'completed' ? 'completed' : 'pending';
        formattedResponse += `\n\n🔄 Task marked as ${status}: ${taskData.title || 'Untitled task'}`;
      }
    }
  }

  return formattedResponse;
}

/**
 * Extract task information from response data
 * @param {Object} data - Response data that may contain task information
 * @returns {Object|null} Task object if found
 */
function extractTaskFromData(data) {
  if (!data || typeof data !== 'object') return null;

  // Look for common task properties
  if (data.title || data.description || data.due_date || data.status || data.id || data.task_id) {
    return data;
  }

  // Look in nested properties
  for (const key of Object.keys(data)) {
    if (data[key] && typeof data[key] === 'object' &&
        (data[key].title || data[key].description || data[key].due_date || data[key].status)) {
      return data[key];
    }
  }

  return null;
}

/**
 * Extract task ID from deletion response data
 * @param {Object} data - Response data that may contain a task ID
 * @returns {number|null} Task ID if found
 */
function extractTaskIdFromData(data) {
  if (!data) return null;

  if (typeof data === 'object') {
    if (data.task_id) return data.task_id;
    if (data.id) return data.id;
  }

  if (typeof data === 'number') return data;

  return null;
}

/**
 * Check if data contains task creation properties
 * @param {Object} data - Data to check
 * @returns {boolean} True if data looks like a task creation response
 */
function hasTaskData(data) {
  return data && typeof data === 'object' &&
    (data.title || data.description || data.due_date);
}

/**
 * Check if data contains task update properties
 * @param {Object} data - Data to check
 * @returns {boolean} True if data looks like a task update response
 */
function hasTaskUpdateData(data) {
  return data && typeof data === 'object' &&
    (data.title || data.description || data.due_date || data.status);
}

/**
 * Check if data contains a task list
 * @param {Object} data - Data to check
 * @returns {boolean} True if data looks like a task list response
 */
function hasTaskListData(data) {
  if (!data || typeof data !== 'object') return false;

  // Check if it's an array of tasks
  if (Array.isArray(data) && data.length > 0) {
    return data.every(task =>
      typeof task === 'object' &&
      (task.title || task.description || task.due_date || task.status || task.id)
    );
  }

  // Check for object with task array
  return Array.isArray(data.tasks) || Array.isArray(data.task_list);
}

/**
 * Check if data contains deletion information
 * @param {Object} data - Data to check
 * @returns {boolean} True if data looks like a deletion response
 */
function hasDeletionData(data) {
  return data && typeof data === 'object' &&
    (data.deleted_task_id || typeof data === 'number' ||
     (typeof data === 'object' && data.success === true && data.task_id));
}

/**
 * Check if data contains toggle information
 * @param {Object} data - Data to check
 * @returns {boolean} True if data looks like a toggle response
 */
function hasToggleData(data) {
  return data && typeof data === 'object' &&
    (data.status || data.toggled_task ||
     (data.title && (data.status === 'completed' || data.status === 'pending')));
}

/**
 * Format a date string for display
 * @param {string|Date} date - Date to format
 * @returns {string} Formatted date string
 */
export function formatDate(date) {
  if (!date) return '';

  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    if (isNaN(dateObj.getTime())) return date; // Return original if invalid date

    return dateObj.toLocaleDateString();
  } catch (e) {
    return date; // Return original on error
  }
}

/**
 * Format a list of tasks for display
 * @param {Array} tasks - Array of task objects
 * @param {string} filter - Optional filter ('all', 'pending', 'completed')
 * @returns {string} Formatted list of tasks
 */
export function formatTaskList(tasks, filter = 'all') {
  if (!Array.isArray(tasks)) return '';

  let filteredTasks = tasks;
  if (filter === 'pending') {
    filteredTasks = tasks.filter(task => task.status !== 'completed');
  } else if (filter === 'completed') {
    filteredTasks = tasks.filter(task => task.status === 'completed');
  }

  if (filteredTasks.length === 0) {
    return 'No tasks found.';
  }

  return filteredTasks
    .map((task, index) => `${index + 1}. ${task.title || 'Untitled'}${task.status === 'completed' ? ' ✅' : ' ⏳'}`)
    .join('\n');
}