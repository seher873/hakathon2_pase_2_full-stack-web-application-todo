import requests

BASE_URL = "http://localhost:4001"

print("=" * 50)
print("Phase 3 Chatbot - Comprehensive Test")
print("=" * 50)

# Test 1: Add task
print("\n1. Add Task: 'Add buy groceries'")
r = requests.post(f"{BASE_URL}/api/chat", json={"message": "Add buy groceries"})
print(f"   Response: {r.json()['response']}")
conv_id = r.json().get('conversation_id')

# Test 2: List tasks
print("\n2. List Tasks: 'Show my tasks'")
r = requests.post(f"{BASE_URL}/api/chat", json={"message": "Show my tasks", "conversation_id": conv_id})
print(f"   Response: {r.json()['response']}")

# Test 3: Complete task
print("\n3. Complete Task: 'Complete buy groceries'")
r = requests.post(f"{BASE_URL}/api/chat", json={"message": "Complete buy groceries", "conversation_id": conv_id})
print(f"   Response: {r.json()['response']}")

# Test 4: Add another task
print("\n4. Add Task: 'Remember to call mom'")
r = requests.post(f"{BASE_URL}/api/chat", json={"message": "Remember to call mom", "conversation_id": conv_id})
print(f"   Response: {r.json()['response']}")

# Test 5: List pending tasks
print("\n5. List Pending: 'Show pending tasks'")
r = requests.post(f"{BASE_URL}/api/chat", json={"message": "Show pending tasks", "conversation_id": conv_id})
print(f"   Response: {r.json()['response']}")

# Test 6: Delete task
print("\n6. Delete Task: 'Delete call mom'")
r = requests.post(f"{BASE_URL}/api/chat", json={"message": "Delete call mom", "conversation_id": conv_id})
print(f"   Response: {r.json()['response']}")

# Test 7: Unknown command
print("\n7. Unknown Command: 'What is the weather'")
r = requests.post(f"{BASE_URL}/api/chat", json={"message": "What is the weather", "conversation_id": conv_id})
print(f"   Response: {r.json()['response']}")

# Test 8: Get conversation messages
print("\n8. Get Conversation History:")
r = requests.get(f"{BASE_URL}/api/chat/help")
print(f"   Help: {r.json()['description']}")

print("\n" + "=" * 50)
print("All Chatbot Tests Complete!")
print("=" * 50)
