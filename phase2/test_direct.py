import requests

r = requests.post('http://localhost:4000/api/tasks', json={
    'title': 'Task with tags',
    'tags': ['work', 'urgent'],
    'priority': 'high'
})
print(f'Status: {r.status_code}')
print(f'Content: {r.text}')

with open('result.txt', 'w') as f:
    f.write(f'Status: {r.status_code}\n')
    f.write(f'Content: {r.text}')
