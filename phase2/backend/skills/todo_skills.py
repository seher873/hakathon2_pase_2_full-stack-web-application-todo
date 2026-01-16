"""
AI Skills for Todo application.
Implements create_task, list_tasks, and complete_task skills with natural language processing.
"""
import json
import re
from typing import Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class TodoSkills:
    """
    AI Skills for Todo application.
    Handles natural language processing and API calls to the backend.
    """

    def __init__(self, base_url: str = "http://localhost:8000/api"):
        """
        Initialize the TodoSkills instance.

        Args:
            base_url: Base URL for the backend API
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

        # Define retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _make_request(self, method: str, endpoint: str, jwt_token: str, data: Optional[Dict] = None) -> Dict[Any, Any]:
        """
        Internal method to make HTTP requests to the API.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint
            jwt_token: JWT token for authorization
            data: Request data (for POST/PATCH requests)

        Returns:
            Response JSON data
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt_token}"
        }

        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            json=data
        )

        response.raise_for_status()
        return response.json()

    def create_task(self, user_id: str, title: str, description: Optional[str], jwt_token: str) -> Dict[Any, Any]:
        """
        Create a new task for the user.

        Args:
            user_id: User ID
            title: Task title
            description: Task description (optional)
            jwt_token: JWT token for authorization

        Returns:
            Created task data
        """
        endpoint = f"/users/{user_id}/tasks"
        data = {"title": title}
        if description:
            data["description"] = description

        return self._make_request("POST", endpoint, jwt_token, data)

    def list_tasks(self, user_id: str, jwt_token: str) -> Dict[Any, Any]:
        """
        List all tasks for the user.

        Args:
            user_id: User ID
            jwt_token: JWT token for authorization

        Returns:
            List of user's tasks
        """
        endpoint = f"/users/{user_id}/tasks"
        return self._make_request("GET", endpoint, jwt_token)

    def complete_task(self, user_id: str, task_id: str, completed: bool, jwt_token: str) -> Dict[Any, Any]:
        """
        Mark a task as complete/incomplete.

        Args:
            user_id: User ID
            task_id: Task ID to update
            completed: Whether the task is completed
            jwt_token: JWT token for authorization

        Returns:
            Updated task data
        """
        endpoint = f"/users/{user_id}/tasks/{task_id}/complete"
        data = {"completed": completed}
        return self._make_request("PATCH", endpoint, jwt_token, data)

    def _extract_task_info(self, user_input: str) -> Dict[str, str]:
        """
        Extract task information from natural language input.
        This is a simple implementation - in a real app, this would use NLP.

        Args:
            user_input: Natural language input from user

        Returns:
            Dictionary with extracted task info (title, description)
        """
        # Normalize the input
        normalized = user_input.lower().strip()

        # Remove common prefixes/suffixes
        patterns_to_remove = [
            r'^add\s+', r'^create\s+', r'^make\s+', r'^please\s+', r'\s+please$', r'\s+now$',
            r'^can you\s+', r'^could you\s+', r'^i want to\s+', r'^i need to\s+'
        ]

        for pattern in patterns_to_remove:
            normalized = re.sub(pattern, '', normalized)

        # Extract the core task information
        # Remove common verbs and phrases
        verb_patterns = [
            r'add\s+', r'create\s+', r'make\s+', r'do\s+', r'perform\s+', r'execute\s+',
            r'complete\s+', r'finish\s+', r'start\s+', r'begin\s+', r'stop\s+', r'end\s+',
            r'buy\s+', r'get\s+', r'purchase\s+', r'obtain\s+', r'prepare\s+', r'ready\s+',
            r'work on\s+', r'focus on\s+', r'take care of\s+', r'handle\s+'
        ]

        for pattern in verb_patterns:
            normalized = re.sub(pattern, '', normalized)

        # Clean up extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized).strip()

        # If the result is too short, return the original cleaned version
        if len(normalized) < 2:
            normalized = user_input.strip()

        return {
            "title": normalized[:255],  # Limit to 255 chars as per API
            "description": f"Task created from AI command: '{user_input}'"
        }

    def _identify_intent(self, user_input: str) -> str:
        """
        Identify the intent from user input.
        This is a simple keyword-based implementation.

        Args:
            user_input: Natural language input from user

        Returns:
            Intent (create_task, list_tasks, complete_task, etc.)
        """
        normalized = user_input.lower()

        # Create task intents
        create_keywords = [
            'add', 'create', 'make', 'new', 'do', 'perform', 'add task', 'create task',
            'make task', 'add todo', 'create todo', 'make todo', 'add kaam', 'create kaam',
            'add karo', 'create karo', 'kal ka kaam', 'tomorrow task', 'next task'
        ]

        # List tasks intents
        list_keywords = [
            'show', 'list', 'display', 'see', 'view', 'my tasks', 'pending tasks',
            'open tasks', 'incomplete tasks', 'dikhao', 'dekhao', 'show me',
            'what are', 'tell me', 'list tasks', 'show tasks', 'pending kaam',
            'kya hai', 'hai kya'
        ]

        # Complete task intents
        complete_keywords = [
            'complete', 'finish', 'done', 'completed', 'mark done', 'mark complete',
            'close', 'end', 'finish up', 'complete task', 'finish task', 'done task',
            'ho gaya', 'ho gya', 'khtm', 'khatam', 'done karo', 'finish karo'
        ]

        # Count keyword matches for each intent
        create_matches = sum(1 for keyword in create_keywords if keyword in normalized)
        list_matches = sum(1 for keyword in list_keywords if keyword in normalized)
        complete_matches = sum(1 for keyword in complete_keywords if keyword in normalized)

        # Determine intent based on highest match
        if create_matches >= list_matches and create_matches >= complete_matches and create_matches > 0:
            return "create_task"
        elif list_matches >= complete_matches and list_matches > 0:
            return "list_tasks"
        elif complete_matches > 0:
            return "complete_task"
        else:
            # Additional check for completion by task name
            if any(word in normalized for word in ['complete ', 'finish ', 'done ', 'mark done', 'ho gaya', 'done karo']):
                return "complete_task"
            else:
                return "unknown"

    def process_request(self, user_input: str, user_id: str, jwt_token: str) -> Dict[str, Any]:
        """
        Process a natural language request from the user.

        Args:
            user_input: Natural language input from user
            user_id: User ID
            jwt_token: JWT token for authorization

        Returns:
            Result dictionary with success status and message
        """
        try:
            # Identify the intent
            intent = self._identify_intent(user_input)

            if intent == "create_task":
                # Extract task information from the input
                task_info = self._extract_task_info(user_input)

                # Create the task
                result = self.create_task(
                    user_id=user_id,
                    title=task_info["title"],
                    description=task_info["description"],
                    jwt_token=jwt_token
                )

                return {
                    "skill": "create_task",
                    "success": True,
                    "message": f"Task '{task_info['title']}' created successfully!",
                    "data": result
                }

            elif intent == "list_tasks":
                # List the user's tasks
                result = self.list_tasks(user_id=user_id, jwt_token=jwt_token)

                tasks = result.get("data", {}).get("tasks", [])
                task_count = len(tasks)

                if task_count == 0:
                    message = "You have no tasks."
                elif task_count == 1:
                    message = f"You have 1 task."
                else:
                    message = f"You have {task_count} tasks."

                return {
                    "skill": "list_tasks",
                    "success": True,
                    "message": message,
                    "data": result
                }

            elif intent == "complete_task":
                # First, list tasks to find the one to complete
                tasks_result = self.list_tasks(user_id=user_id, jwt_token=jwt_token)
                tasks = tasks_result.get("data", {}).get("tasks", [])

                # Extract potential task reference from user input
                normalized_input = user_input.lower()
                task_to_complete = None

                # Look for task by title or keywords
                for task in tasks:
                    if not task.get('completed', False):  # Only look at incomplete tasks
                        task_title_lower = task.get('title', '').lower()

                        # Check if the task title is mentioned in the input
                        if task_title_lower in normalized_input or any(keyword in normalized_input for keyword in task_title_lower.split()):
                            task_to_complete = task
                            break

                if task_to_complete:
                    # Complete the found task
                    result = self.complete_task(
                        user_id=user_id,
                        task_id=task_to_complete['id'],
                        completed=True,
                        jwt_token=jwt_token
                    )

                    return {
                        "skill": "complete_task",
                        "success": True,
                        "message": f"Task '{task_to_complete['title']}' marked as complete!",
                        "data": result
                    }
                else:
                    # If no specific task was found, complete the most recent incomplete task
                    incomplete_tasks = [t for t in tasks if not t.get('completed', False)]
                    if incomplete_tasks:
                        most_recent = incomplete_tasks[-1]  # Most recent is typically last in list

                        result = self.complete_task(
                            user_id=user_id,
                            task_id=most_recent['id'],
                            completed=True,
                            jwt_token=jwt_token
                        )

                        return {
                            "skill": "complete_task",
                            "success": True,
                            "message": f"Task '{most_recent['title']}' marked as complete!",
                            "data": result
                        }
                    else:
                        return {
                            "skill": "complete_task",
                            "success": False,
                            "message": "No incomplete tasks found to mark as complete.",
                            "data": None
                        }

            else:
                # Unknown intent
                return {
                    "skill": "unknown",
                    "success": False,
                    "message": f"I could not understand your request: '{user_input}'. Try commands like 'add buy milk' or 'show my tasks'.",
                    "data": None
                }

        except requests.exceptions.RequestException as e:
            # Handle API request errors
            return {
                "skill": intent,
                "success": False,
                "message": f"Error communicating with the API: {str(e)}",
                "data": None
            }
        except Exception as e:
            # Handle other errors
            return {
                "skill": intent,
                "success": False,
                "message": f"An error occurred processing your request: {str(e)}",
                "data": None
            }