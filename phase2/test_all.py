import requests
import json

print("Testing with detailed error output")

# Test 1: Simple task (should work)
print("\n1. Simple task")
r = requests.post('http://localhost:4000/api/tasks', json={
    'title': 'Simple Task'
})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print(f"Response: {json.dumps(r.json(), indent=2)}")
else:
    print(f"Error: {r.text}")

# Test 2: Task with priority (should work)
print("\n2. Task with priority")
r = requests.post('http://localhost:4000/api/tasks', json={
    'title': 'Priority Task',
    'priority': 'high'
})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print(f"Response: {json.dumps(r.json(), indent=2)}")
else:
    print(f"Error: {r.text}")

# Test 3: Task with tags (problematic)
print("\n3. Task with tags (as comma-separated string)")
r = requests.post('http://localhost:4000/api/tasks', json={
    'title': 'Tag Task',
    'tags': 'work,urgent'
})
print(f"Status: {r.status_code}")
print(f"Headers: {dict(r.headers)}")
print(f"Full Response: {r.text}")
if r.status_code == 200:
    data = r.json()['data']
    print(f"Tags stored as: {data.get('tags')}")

# Test 4: Task with all fields
print("\n4. Task with all fields")
r = requests.post('http://localhost:4000/api/tasks', json={
    'title': 'Complete Task',
    'description': 'A complete task',
    'priority': 'high',
    'tags': ['work', 'important'],
    'url': 'https://example.com'
})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print(f"Response: {json.dumps(r.json(), indent=2)}")
else:
    print(f"Error: {r.text}")
