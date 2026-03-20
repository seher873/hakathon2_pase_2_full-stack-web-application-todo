import requests
import json

data = {'title': 'Tag Task', 'tags': 'work,urgent'}
print(f"Sending: {json.dumps(data)}")

r = requests.post('http://localhost:4000/api/tasks', json=data)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}")
