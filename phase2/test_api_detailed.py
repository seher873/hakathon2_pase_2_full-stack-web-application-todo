import requests
import json

print("Testing API endpoints with details...")

# Test health endpoint
r = requests.get('http://localhost:4000/health')
print(f'\n=== Health ===')
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')

# Test tasks endpoint with detailed error
print(f'\n=== Tasks ===')
try:
    r = requests.get('http://localhost:4000/api/tasks')
    print(f'Status: {r.status_code}')
    print(f'Headers: {dict(r.headers)}')
    print(f'Content: {r.text}')
except Exception as e:
    print(f'Exception: {e}')

# Test create task
print(f'\n=== Create Task ===')
try:
    r = requests.post('http://localhost:4000/api/tasks', json={
        'title': 'Test Task',
        'description': 'Test Description',
        'priority': 'high'
    })
    print(f'Status: {r.status_code}')
    print(f'Content: {r.text[:500]}')
except Exception as e:
    print(f'Exception: {e}')

print("\nDone!")
