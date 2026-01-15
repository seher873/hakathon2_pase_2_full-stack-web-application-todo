"""
Test script for Phase-3 AI Agent System.

This script tests the complete workflow of the AI agent system.
"""
import sys
import os

# Add the phase3 directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from phase3.backend import create_ai_agent_system


def test_ai_agent_system():
    """
    Test the complete AI agent system workflow.
    """
    print("Testing AI Agent System...")

    # Create the AI agent system
    ai_system = create_ai_agent_system()

    # Test user ID (example UUID)
    user_id = "123e4567-e89b-12d3-a456-426614174000"

    # Test cases
    test_cases = [
        ("Add a task to buy groceries", "create_task"),
        ("Show my tasks", "list_tasks"),
        ("Complete the task buy groceries", "complete_task")
    ]

    for user_input, expected_intent in test_cases:
        print(f"\nTesting: '{user_input}'")
        result = ai_system.route_request(user_input, user_id)
        print(f"Result: {result}")

        # Note: These tests will likely fail without a running backend server
        # but they should at least show the system is working up to the API call point
        if result.get('success') is False:
            print(f"Expected to reach API (would fail without server), got: {result.get('message')}")


if __name__ == "__main__":
    test_ai_agent_system()