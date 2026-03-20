import requests
import traceback

BASE_URL = "http://localhost:4000"

print("Debug: Create task with tags")

try:
    r = requests.post(f"{BASE_URL}/api/tasks", json={
        "title": "Task with tags",
        "tags": ["work", "urgent"],
        "priority": "high"
    })
    print(f"Status: {r.status_code}")
    print(f"Headers: {dict(r.headers)}")
    print(f"Content: {r.text}")
except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()
