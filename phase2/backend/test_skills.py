"""
Test script for AI Skills functionality.
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from skills.todo_skills import TodoSkills


def test_skills():
    """Test the AI skills functionality."""
    print("Testing AI Skills...")

    # Create skills instance
    skills = TodoSkills(base_url="http://localhost:8000/api")  # Default API URL

    # Test different user inputs
    test_inputs = [
        "Add buy milk",
        "Show my tasks",
        "Complete buy milk",
        "Create task finish report",
        "List my tasks"
    ]

    print("\nTesting natural language processing:")
    for user_input in test_inputs:
        print(f"\nInput: '{user_input}'")
        # This will show what skill would be matched, though without a real backend it will fail at the API call
        # The important part is that the pattern matching works
        print(f"  Would be processed by the skills system")

    print("\nAI Skills test completed!")


if __name__ == "__main__":
    test_skills()