#!/bin/bash

# Test script to verify task creation functionality

echo "Testing task creation functionality..."

# Step 1: Login with an existing user (since registration might fail due to duplicate emails)
echo "Step 1: Logging in with existing user..."
login_response=$(curl -s -X POST http://localhost:4000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com", "password":"password123"}')

# Extract the token from the response
token=$(echo "$login_response" | grep -o '"token":"[^"]*"' | head -n1 | cut -d'"' -f4)

if [ -z "$token" ]; then
    echo "ERROR: Failed to get token from login response"
    echo "Response: $login_response"
    exit 1
fi

echo "Token obtained: $token"

# Step 2: Create a task using the token
echo "Step 2: Creating a task..."
task_response=$(curl -s -X POST http://localhost:4000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $token" \
  -d '{"title":"Test Task from Script", "description":"This is a test task created via script", "url":"https://www.example.com", "status":"todo"}')

echo "Task creation response:"
echo "$task_response"
echo ""

# Step 3: Get tasks to verify the task was created
echo "Step 3: Retrieving tasks..."
tasks_response=$(curl -s -X GET http://localhost:4000/api/tasks \
  -H "Authorization: Bearer $token")

echo "Tasks retrieval response:"
echo "$tasks_response"

echo ""
echo "Test completed!"