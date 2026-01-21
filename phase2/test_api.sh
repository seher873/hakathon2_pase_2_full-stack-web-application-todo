#!/bin/bash

# Register a new user
echo "Registering new user..."
response=$(curl -s -X POST http://localhost:4000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com", "password":"password123"}')

# Extract the token from the response
token=$(echo "$response" | grep -o '"token":"[^"]*"' | head -n1 | cut -d'"' -f4)

echo "Token: $token"

# Create a task with a URL
echo "Creating a task with URL..."
task_response=$(curl -s -X POST http://localhost:4000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $token" \
  -d '{"title":"Test Task with URL", "description":"This is a test task with a URL", "url":"https://www.google.com", "status":"todo"}')

echo "Task creation response:"
echo "$task_response"
echo ""

# Get the tasks to verify
echo "Getting tasks to verify..."
tasks_response=$(curl -s -X GET http://localhost:4000/api/tasks \
  -H "Authorization: Bearer $token")

echo "Tasks response:"
echo "$tasks_response"