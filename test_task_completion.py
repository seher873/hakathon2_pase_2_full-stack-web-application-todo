#!/usr/bin/env python3
"""
Test script to verify task completion functionality
"""
import requests
import json
import os

def test_task_completion():
    """
    Test that task completion works properly through the PUT endpoint
    """
    print("Testing task completion functionality...")
    
    # Base URL for the backend
    BASE_URL = "http://localhost:4000/api"
    
    # Mock token for testing (this would normally come from a login)
    # Note: This is just for testing - in a real scenario, you'd need to register/login first
    mock_token = os.getenv("TEST_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
    
    headers = {
        "Authorization": f"Bearer {mock_token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Create a new task
    print("\n1. Creating a new task...")
    task_data = {
        "title": "Test task for completion",
        "description": "This is a test task to verify completion functionality"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/tasks", headers=headers, json=task_data)
        print(f"Create task response: {response.status_code}")
        
        if response.status_code == 201:
            task = response.json()["data"]
            task_id = task["id"]
            print(f"Created task with ID: {task_id}")
            print(f"Initial status: {task['status']}, completed: {task['completed']}")
        else:
            print(f"Failed to create task: {response.text}")
            return False
    except Exception as e:
        print(f"Error creating task: {e}")
        return False
    
    # Test 2: Update the task to mark as completed using PUT endpoint
    print("\n2. Updating task to mark as completed...")
    update_data = {
        "completed": True
    }
    
    try:
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", headers=headers, json=update_data)
        print(f"Update task response: {response.status_code}")
        
        if response.status_code == 200:
            updated_task = response.json()["data"]
            print(f"Updated status: {updated_task['status']}, completed: {updated_task['completed']}")
            
            if updated_task['status'] == 'completed' and updated_task['completed'] is True:
                print("✅ Task completion via PUT endpoint works correctly!")
            else:
                print("❌ Task completion via PUT endpoint failed!")
                return False
        else:
            print(f"Failed to update task: {response.text}")
            return False
    except Exception as e:
        print(f"Error updating task: {e}")
        return False
    
    # Test 3: Update the task to mark as incomplete using PUT endpoint
    print("\n3. Updating task to mark as incomplete...")
    update_data = {
        "completed": False
    }
    
    try:
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", headers=headers, json=update_data)
        print(f"Update task response: {response.status_code}")
        
        if response.status_code == 200:
            updated_task = response.json()["data"]
            print(f"Updated status: {updated_task['status']}, completed: {updated_task['completed']}")
            
            if updated_task['status'] == 'todo' and updated_task['completed'] is False:
                print("✅ Task incompletion via PUT endpoint works correctly!")
            else:
                print("❌ Task incompletion via PUT endpoint failed!")
                return False
        else:
            print(f"Failed to update task: {response.text}")
            return False
    except Exception as e:
        print(f"Error updating task: {e}")
        return False
    
    # Test 4: Use the dedicated PATCH endpoint to toggle completion
    print("\n4. Using PATCH endpoint to mark as completed...")
    patch_data = {
        "completed": True
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/tasks/{task_id}/complete", headers=headers, json=patch_data)
        print(f"Patch task completion response: {response.status_code}")
        
        if response.status_code == 200:
            patched_task = response.json()["data"]
            print(f"Patched status: {patched_task['status']}, completed: {patched_task['completed']}")
            
            if patched_task['status'] == 'completed' and patched_task['completed'] is True:
                print("✅ Task completion via PATCH endpoint works correctly!")
            else:
                print("❌ Task completion via PATCH endpoint failed!")
                return False
        else:
            print(f"Failed to patch task: {response.text}")
            return False
    except Exception as e:
        print(f"Error patching task: {e}")
        return False
    
    # Test 5: Verify we can retrieve the task and it shows as completed
    print("\n5. Retrieving the task to verify completion status...")
    try:
        response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        print(f"Get task response: {response.status_code}")
        
        if response.status_code == 200:
            retrieved_task = response.json()["data"]
            print(f"Retrieved status: {retrieved_task['status']}, completed: {retrieved_task['completed']}")
            
            if retrieved_task['status'] == 'completed' and retrieved_task['completed'] is True:
                print("✅ Task retrieval shows correct completion status!")
            else:
                print("❌ Task retrieval shows incorrect completion status!")
                return False
        else:
            print(f"Failed to retrieve task: {response.text}")
            return False
    except Exception as e:
        print(f"Error retrieving task: {e}")
        return False
    
    print("\n🎉 All tests passed! Task completion functionality is working correctly.")
    return True

if __name__ == "__main__":
    test_task_completion()