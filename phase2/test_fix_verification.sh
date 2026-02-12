#!/bin/bash

# Test script to verify the fix for the task completion issue

echo "Testing task completion fix..."

# Step 1: Register a new user or login if user already exists
echo "Step 1: Attempting to register/login user..."
response=$(curl -s -X POST http://localhost:4000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"testfix@example.com", "password":"password123"}')

# Check if registration failed due to existing user, then try login
if [[ "$response" == *"duplicate"* ]] || [[ "$response" == *"exists"* ]]; then
    echo "User already exists, attempting login..."
    response=$(curl -s -X POST http://localhost:4000/api/auth/login \
      -H "Content-Type: application/json" \
      -d '{"email":"testfix@example.com", "password":"password123"}')
fi

# Extract the token from the response
token=$(echo "$response" | grep -o '"token":"[^"]*"' | head -n1 | cut -d'"' -f4)

if [ -z "$token" ]; then
    echo "ERROR: Failed to get token from response"
    echo "Response: $response"
    exit 1
fi

echo "Token obtained: ${token:0:20}..."

# Step 2: Create a task using the token
echo "Step 2: Creating a task..."
task_response=$(curl -s -X POST http://localhost:4000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $token" \
  -d '{"title":"Test Task for Fix Verification", "description":"This task is to verify the fix for the disappearing tasks issue", "status":"todo"}')

echo "Task creation response status: $(echo $task_response | jq -r '.status // "missing"')"

# Extract task ID
task_id=$(echo "$task_response" | jq -r '.data.id // empty')
if [ -z "$task_id" ] || [ "$task_id" = "null" ]; then
    echo "ERROR: Failed to get task ID from creation response"
    echo "Response: $task_response"
    exit 1
fi

echo "Created task with ID: $task_id"

# Step 3: Get tasks to verify the task was created
echo "Step 3: Retrieving tasks to verify creation..."
tasks_response=$(curl -s -X GET http://localhost:4000/api/tasks \
  -H "Authorization: Bearer $token")

task_count_before=$(echo "$tasks_response" | jq -r '.data | length')
echo "Number of tasks before completion: $task_count_before"

# Find our specific task in the response
our_task=$(echo "$tasks_response" | jq -r ".data[] | select(.id == \"$task_id\")")
if [ -z "$our_task" ]; then
    echo "ERROR: Created task not found in task list"
    exit 1
else
    echo "Task found in list, status: $(echo $our_task | jq -r '.status')"
fi

# Step 4: Mark the task as completed
echo "Step 4: Marking task as completed..."
completion_response=$(curl -s -X PATCH http://localhost:4000/api/tasks/$task_id/complete \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $token" \
  -d '{"completed": true}')

echo "Completion response status: $(echo $completion_response | jq -r '.status // "missing"')"

# Check if the response contains the updated task
updated_task=$(echo "$completion_response" | jq -r '.data // empty')
if [ -z "$updated_task" ] || [ "$updated_task" = "null" ]; then
    echo "ERROR: Failed to get updated task from completion response"
    echo "Response: $completion_response"
    exit 1
fi

echo "Received updated task from completion endpoint"
echo "Updated task status: $(echo $updated_task | jq -r '.status')"
echo "Updated task completed flag: $(echo $updated_task | jq -r '.completed')"

# Step 5: Get tasks again to verify the task is still there and marked as completed
echo "Step 5: Retrieving tasks to verify completion..."
tasks_after_completion=$(curl -s -X GET http://localhost:4000/api/tasks \
  -H "Authorization: Bearer $token")

task_count_after=$(echo "$tasks_after_completion" | jq -r '.data | length')
echo "Number of tasks after completion: $task_count_after"

# Find our specific task in the response after completion
our_task_after=$(echo "$tasks_after_completion" | jq -r ".data[] | select(.id == \"$task_id\")")
if [ -z "$our_task_after" ]; then
    echo "ERROR: Task disappeared after completion - the bug still exists!"
    exit 1
else
    task_status=$(echo $our_task_after | jq -r '.status')
    task_completed=$(echo $our_task_after | jq -r '.completed')
    echo "Task still exists after completion"
    echo "Task status: $task_status"
    echo "Task completed flag: $task_completed"
    
    if [ "$task_completed" = "true" ] && [ "$task_status" = "completed" ]; then
        echo "SUCCESS: Task was properly marked as completed and did not disappear!"
    else
        echo "ERROR: Task was not properly marked as completed"
        exit 1
    fi
fi

# Step 6: Mark the task as incomplete again to test the reverse operation
echo "Step 6: Marking task as incomplete again..."
incomplete_response=$(curl -s -X PATCH http://localhost:4000/api/tasks/$task_id/complete \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $token" \
  -d '{"completed": false}')

echo "Mark incomplete response status: $(echo $incomplete_response | jq -r '.status // "missing"')"

# Verify the task is still there and marked as incomplete
tasks_after_incomplete=$(curl -s -X GET http://localhost:4000/api/tasks \
  -H "Authorization: Bearer $token")

our_task_after_incomplete=$(echo "$tasks_after_incomplete" | jq -r ".data[] | select(.id == \"$task_id\")")
if [ -z "$our_task_after_incomplete" ]; then
    echo "ERROR: Task disappeared after marking as incomplete!"
    exit 1
else
    task_status_incomplete=$(echo $our_task_after_incomplete | jq -r '.status')
    task_completed_incomplete=$(echo $our_task_after_incomplete | jq -r '.completed')
    echo "Task still exists after marking as incomplete"
    echo "Task status: $task_status_incomplete"
    echo "Task completed flag: $task_completed_incomplete"
    
    if [ "$task_completed_incomplete" = "false" ] && [ "$task_status_incomplete" = "todo" ]; then
        echo "SUCCESS: Task was properly marked as incomplete and did not disappear!"
    else
        echo "ERROR: Task was not properly marked as incomplete"
        exit 1
    fi
fi

echo ""
echo "VERIFICATION COMPLETE: The fix is working correctly!"
echo "- Tasks are properly updated when marked as complete/incomplete"
echo "- Tasks do not disappear after status changes"
echo "- Both completion directions (todo↔completed) work correctly"