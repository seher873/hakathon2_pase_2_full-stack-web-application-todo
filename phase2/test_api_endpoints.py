import requests

print("Testing API endpoints...")

# Test health endpoint
try:
    r = requests.get('http://localhost:4000/health')
    print(f'Health: {r.status_code}')
    print(f'Health Response: {r.json()}')
except Exception as e:
    print(f'Health Error: {e}')

# Test tasks endpoint
try:
    r = requests.get('http://localhost:4000/api/tasks')
    print(f'Tasks Status: {r.status_code}')
    print(f'Tasks Content: {r.text}')
except Exception as e:
    print(f'Tasks Error: {e}')

print("Done!")
