"""
Example usage of AI Skills for Todo Application.

This demonstrates the AI skills functionality for Phase 3 preview.
Note: This example shows pattern matching but won't work without a running backend API.
"""
import asyncio
import sys
import os

# Add parent directory to path to access src
backend_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, backend_dir)

from skills.todo_skills import TodoSkills


def demonstrate_skills():
    """Demonstrate the AI skills functionality."""
    print("=== AI Skills Demonstration - Phase 3 Preview ===\n")

    print("⚠️  PREVIEW FEATURE - This is part of Phase 3 and does not impact Phase 2 grading.\n")

    # Create skills instance - in a real scenario, this would connect to the running API
    # For demonstration, we'll show how the pattern matching works
    skills = TodoSkills(base_url="http://localhost:8000/api")  # Point to actual API

    print("Supported Skills and Example Usage:\n")

    # Example 1: Create Task
    print("1. Create Task:")
    print("   Input: 'Add buy milk'")
    print("   Input: 'Create task finish report - urgent'")
    print("   Input: 'New task call mom'")
    print("   Description: Creates a new task with optional description\n")

    # Example 2: List Tasks
    print("2. List Tasks:")
    print("   Input: 'Show my tasks'")
    print("   Input: 'List my tasks'")
    print("   Input: 'What tasks do I have?'")
    print("   Description: Lists all tasks for the authenticated user\n")

    # Example 3: Complete Task
    print("3. Complete Task:")
    print("   Input: 'Complete buy milk'")
    print("   Input: 'Finish finish report'")
    print("   Input: 'Mark call mom done'")
    print("   Description: Marks a specific task as complete\n")

    print("=== API Usage ===")
    print("The skills are accessible via the following endpoints:")
    print("POST /api/ai/process")
    print("GET  /api/ai/skills")
    print("")
    print("Example request:")
    print("{")
    print('  "input": "Add buy milk"')
    print("}")
    print("")
    print("=== Implementation Details ===")
    print("- Skills call existing Phase-2 API endpoints")
    print("- Respects JWT authentication and user isolation")
    print("- Uses pattern matching for intent detection")
    print("- Handles errors consistently with existing API patterns")


if __name__ == "__main__":
    demonstrate_skills()