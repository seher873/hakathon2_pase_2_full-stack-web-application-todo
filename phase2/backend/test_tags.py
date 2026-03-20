import requests

BASE_URL = "http://localhost:4000"

print("Testing task creation with tags...")

# Test 1: Create task with tags as list
print("\n1. Create with tags as list")
r = requests.post(f"{BASE_URL}/api/tasks", json={
    "title": "Task with tags",
    "tags": ["work", "urgent"]
})
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:300]}")

# Test 2: Create task with tags as string
print("\n2. Create with tags as comma-separated string")
r = requests.post(f"{BASE_URL}/api/tasks", json={
    "title": "Task with tags string",
    "tags": "work,urgent"
})
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:300]}")

# Test 3: Create task without tags
print("\n3. Create without tags")
r = requests.post(f"{BASE_URL}/api/tasks", json={
    "title": "Task without tags"
})
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:300]}")

# Test 4: Create task with priority high
print("\n4. Create with priority high")
r = requests.post(f"{BASE_URL}/api/tasks", json={
    "title": "High priority task",
    "priority": "high"
})
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:300]}")
