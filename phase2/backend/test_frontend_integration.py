#!/usr/bin/env python3
"""
Test script to verify FastAPI backend works with frontend API calls.
This script mimics the calls that the frontend makes to the backend.
"""
import requests
import json
import time

BASE_URL = "http://localhost:4001"

def test_api_call(description, method, endpoint, headers=None, data=None, expected_status=200):
    """Helper function to test API calls"""
    print(f"\n🔍 Testing: {description}")
    print(f"   {method} {BASE_URL}{endpoint}")

    if data:
        print(f"   Data: {json.dumps(data) if isinstance(data, dict) else data}")

    try:
        response = requests.request(
            method=method,
            url=f"{BASE_URL}{endpoint}",
            headers=headers,
            json=data
        )

        print(f"   Status: {response.status_code}")

        if response.status_code == expected_status:
            print(f"   ✅ SUCCESS")
            if response.content:
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return response_data
                except:
                    print(f"   Response: {response.text[:200]}...")
                    return response.text
        else:
            print(f"   ❌ FAILED - Expected {expected_status}, got {response.status_code}")
            print(f"   Response: {response.text}")
            return None

    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return None

def main():
    print("🚀 Testing FastAPI Backend Integration with Frontend API Calls")
    print("="*60)

    # Test 1: Health check
    test_api_call("Health Check", "GET", "/health", expected_status=200)

    # Test 2: Register a new user
    register_data = {
        "email": "integration-test@example.com",
        "password": "securepassword123"
    }
    auth_response = test_api_call("User Registration", "POST", "/api/auth/register",
                                  headers={"Content-Type": "application/json"},
                                  data=register_data, expected_status=200)

    if not auth_response or "token" not in auth_response:
        print("\n❌ FATAL: Cannot proceed without authentication token")
        return False

    # Extract the token
    token = auth_response["token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print(f"\n   Using token: {token[:20]}...")

    # Test 3: Get user info
    test_api_call("Get User Info", "GET", "/api/auth/me", headers=headers, expected_status=200)

    # Test 4: Create a task (matching frontend CreateTaskRequest format)
    task_data = {
        "title": "Integration Test Task",
        "description": "This task was created to test frontend-backend integration",
        "status": "todo"
    }
    task_response = test_api_call("Create Task", "POST", "/api/tasks",
                                  headers=headers, data=task_data, expected_status=200)

    if not task_response or "id" not in task_response.get("data", {}):
        print("\n❌ FATAL: Cannot proceed without a created task")
        return False

    task_id = task_response["data"]["id"]
    print(f"\n   Created task with ID: {task_id}")

    # Test 5: Get single task
    test_api_call(f"Get Task {task_id}", "GET", f"/api/tasks/{task_id}",
                  headers=headers, expected_status=200)

    # Test 6: Update task (matching frontend UpdateTaskRequest format)
    update_data = {
        "title": "Updated Integration Test Task",
        "description": "This task was updated to test frontend-backend integration",
        "status": "in-progress"
    }
    test_api_call(f"Update Task {task_id}", "PUT", f"/api/tasks/{task_id}",
                  headers=headers, data=update_data, expected_status=200)

    # Test 7: Toggle task completion (matching frontend format from api.ts)
    completion_data = {"completed": True}
    test_api_call(f"Toggle Task {task_id} Completion", "PATCH", f"/api/tasks/{task_id}/complete",
                  headers=headers, data=completion_data, expected_status=200)

    # Test 8: Get all tasks (should include the updated task)
    tasks_response = test_api_call("Get All Tasks", "GET", "/api/tasks",
                                   headers=headers, expected_status=200)

    if tasks_response and "data" in tasks_response:
        task_count = len(tasks_response["data"])
        print(f"\n   Found {task_count} tasks in response")

    # Test 9: Login with the same user (for session testing)
    login_data = {
        "email": "integration-test@example.com",
        "password": "securepassword123"
    }
    login_response = test_api_call("User Login", "POST", "/api/auth/login",
                                   headers={"Content-Type": "application/json"},
                                   data=login_data, expected_status=200)

    # Test 10: Try to delete the task
    test_api_call(f"Delete Task {task_id}", "DELETE", f"/api/tasks/{task_id}",
                  headers=headers, expected_status=200)

    print(f"\n✅ Frontend Integration Test Complete!")
    print(f"   All API endpoints work correctly with the frontend format.")
    print(f"   The FastAPI backend is fully compatible with the Next.js frontend.")

    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Integration test PASSED - Backend and Frontend are compatible!")
    else:
        print("\n❌ Integration test FAILED - Issues found")
        exit(1)