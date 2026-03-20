import requests
import json

BASE_URL = "http://localhost:4000"

print("=" * 60)
print("COMPREHENSIVE API TEST")
print("=" * 60)

# 1. Health Check
print("\n1. Health Check")
r = requests.get(f"{BASE_URL}/health")
print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")

# 2. Create Task with all fields
print("\n2. Create Task (with priority, tags, due_date)")
task_data = {
    "title": "Complete Hackathon Project",
    "description": "Finish all intermediate features",
    "priority": "high",
    "tags": "work,urgent,hackathon",  # Comma-separated string
    "url": "https://github.com/hackathon"
}
r = requests.post(f"{BASE_URL}/api/tasks", json=task_data)
print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")
if r.status_code == 200:
    task = r.json()["data"]
    task_id = task["id"]
    print(f"   Task ID: {task_id}")
    print(f"   Priority: {task['priority']}")
    print(f"   Tags: {task['tags']}")
else:
    print(f"   Error: {r.text}")
    task_id = None

# 3. Create another task with medium priority
print("\n3. Create Task (medium priority)")
task_data2 = {
    "title": "Review Code",
    "description": "Review the implemented features",
    "priority": "medium",
    "tags": "review,code"  # Comma-separated string
}
r = requests.post(f"{BASE_URL}/api/tasks", json=task_data2)
print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")

# 4. Create task with low priority
print("\n4. Create Task (low priority)")
task_data3 = {
    "title": "Write Documentation",
    "priority": "low"
}
r = requests.post(f"{BASE_URL}/api/tasks", json=task_data3)
print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")

# 5. Get All Tasks
print("\n5. Get All Tasks")
r = requests.get(f"{BASE_URL}/api/tasks")
print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")
if r.status_code == 200:
    tasks = r.json()["data"]
    print(f"   Total Tasks: {len(tasks)}")

# 6. Filter by Priority
print("\n6. Filter by Priority (high)")
r = requests.get(f"{BASE_URL}/api/tasks?priority=high")
print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")
if r.status_code == 200:
    tasks = r.json()["data"]
    print(f"   High Priority Tasks: {len(tasks)}")

# 7. Search Tasks
print("\n7. Search Tasks ('code')")
r = requests.get(f"{BASE_URL}/api/tasks?search=code")
print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")
if r.status_code == 200:
    tasks = r.json()["data"]
    print(f"   Matching Tasks: {len(tasks)}")

# 8. Sort by Priority
print("\n8. Sort by Priority (descending)")
r = requests.get(f"{BASE_URL}/api/tasks?sort_by=priority&sort_order=desc")
print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")
if r.status_code == 200:
    tasks = r.json()["data"]
    print(f"   First task priority: {tasks[0]['priority'] if tasks else 'N/A'}")

# 9. Filter by Tags
print("\n9. Filter by Tags ('work')")
r = requests.get(f"{BASE_URL}/api/tasks?tags=work")
print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")
if r.status_code == 200:
    tasks = r.json()["data"]
    print(f"   Tasks with 'work' tag: {len(tasks)}")

# 10. Update Task
print("\n10. Update Task")
if task_id:
    update_data = {
        "title": "Complete Hackathon Project - UPDATED",
        "priority": "medium"
    }
    r = requests.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_data)
    print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")
    if r.status_code == 200:
        print(f"   Updated Title: {r.json()['data']['title']}")
        print(f"   Updated Priority: {r.json()['data']['priority']}")

# 11. Mark Task Complete
print("\n11. Mark Task Complete")
if task_id:
    r = requests.patch(f"{BASE_URL}/api/tasks/{task_id}/complete")
    print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")
    if r.status_code == 200:
        print(f"   Completed: {r.json()['data']['completed']}")

# 12. Filter by Status
print("\n12. Filter by Status (completed)")
r = requests.get(f"{BASE_URL}/api/tasks?status=completed")
print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")
if r.status_code == 200:
    tasks = r.json()["data"]
    print(f"   Completed Tasks: {len(tasks)}")

# 13. Filter by Status (pending)
print("\n13. Filter by Status (pending)")
r = requests.get(f"{BASE_URL}/api/tasks?status=pending")
print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")
if r.status_code == 200:
    tasks = r.json()["data"]
    print(f"   Pending Tasks: {len(tasks)}")

# 14. Delete Task
print("\n14. Delete Task")
if task_id:
    r = requests.delete(f"{BASE_URL}/api/tasks/{task_id}")
    print(f"   Status: {r.status_code} ✓" if r.status_code == 200 else f"   Status: {r.status_code} ✗")

# 15. Verify Deletion
print("\n15. Verify Deletion")
r = requests.get(f"{BASE_URL}/api/tasks")
if r.status_code == 200:
    tasks = r.json()["data"]
    deleted = not any(t["id"] == task_id for t in tasks)
    print(f"   Task Deleted: {'✓' if deleted else '✗'}")
    print(f"   Remaining Tasks: {len(tasks)}")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED")
print("=" * 60)
