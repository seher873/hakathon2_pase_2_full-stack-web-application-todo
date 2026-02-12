#!/bin/bash

# Test script to verify the fix for the task completion issue

echo "Testing task completion fix..."

# Step 1: Login with test user
echo "Step 1: Logging in with test user..."
response=$(curl -s -X POST http://localhost:4000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"password123"}')

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

echo "Task creation response received."

# Extract task ID using grep and sed
task_id=$(echo "$task_response" | grep -o '"id":[^,}]*' | head -n1 | sed 's/"id"://' | sed 's/"//g' | tr -d '\n\r ')

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

# Count tasks by counting 'id' fields
task_count_before=$(echo "$tasks_response" | grep -o '"id"' | wc -l)
echo "Number of tasks before completion: $task_count_before"

# Find our specific task in the response
if echo "$tasks_response" | grep -q "$task_id"; then
    echo "Task found in list"
    # Extract status
    task_status=$(echo "$tasks_response" | grep -A 10 "$task_id" | grep -o '"status":"[^"]*"' | head -n1 | cut -d'"' -f4)
    echo "Task status: $task_status"
else
    echo "ERROR: Created task not found in task list"
    exit 1
fi

# Step 4: Mark the task as completed
echo "Step 4: Marking task as completed..."
completion_response=$(curl -s -X PATCH http://localhost:4000/api/tasks/$task_id/complete \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $token" \
  -d '{"completed": true}')

echo "Completion response received."

# Check if the response contains the updated task data
if echo "$completion_response" | grep -q "$task_id"; then
    echo "Received updated task from completion endpoint"
    # Extract status and completed flag
    updated_status=$(echo "$completion_response" | grep -o '"status":"[^"]*"' | head -n1 | cut -d'"' -f4)
    updated_completed=$(echo "$completion_response" | grep -o '"completed":[^,}]*' | head -n1 | cut -d':' -f2 | tr -d ' ')
    echo "Updated task status: $updated_status"
    echo "Updated task completed flag: $updated_completed"
else
    echo "ERROR: Failed to get updated task from completion response"
    echo "Response: $completion_response"
    exit 1
fi

# Step 5: Get tasks again to verify the task is still there and marked as completed
echo "Step 5: Retrieving tasks to verify completion..."
tasks_after_completion=$(curl -s -X GET http://localhost:4000/api/tasks \
  -H "Authorization: Bearer $token")

task_count_after=$(echo "$tasks_after_completion" | grep -o '"id"' | wc -l)
echo "Number of tasks after completion: $task_count_after"

# Find our specific task in the response after completion
if echo "$tasks_after_completion" | grep -q "$task_id"; then
    echo "Task still exists after completion"
    # Extract status and completed flag
    final_status=$(echo "$tasks_after_completion" | grep -A 10 "$task_id" | grep -o '"status":"[^"]*"' | head -n1 | cut -d'"' -f4)
    final_completed=$(echo "$tasks_after_completion" | grep -A 10 "$task_id" | grep -o '"completed":[^,}]*' | head -n1 | cut -d':' -f2 | tr -d ' ')
    echo "Final task status: $final_status"
    echo "Final task completed flag: $final_completed"
    
    if [ "$final_completed" = "true" ] && [ "$final_status" = "completed" ]; then
        echo "SUCCESS: Task was properly marked as completed and did not disappear!"
    else
        echo "ERROR: Task was not properly marked as completed"
        exit 1
    fi
else
    echo "ERROR: Task disappeared after completion - the bug still exists!"
    exit 1
fi

# Step 6: Mark the task as incomplete again to test the reverse operation
echo "Step 6: Marking task as incomplete again..."
incomplete_response=$(curl -s -X PATCH http://localhost:4000/api/tasks/$task_id/complete \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $token" \
  -d '{"completed": false}')

echo "Mark incomplete response received."

# Verify the task is still there and marked as incomplete
tasks_after_incomplete=$(curl -s -X GET http://localhost:4000/api/tasks \
  -H "Authorization: Bearer $token")

if echo "$tasks_after_incomplete" | grep -q "$task_id"; then
    echo "Task still exists after marking as incomplete"
    # Extract status and completed flag
    final_status_incomplete=$(echo "$tasks_after_incomplete" | grep -A 10 "$task_id" | grep -o '"status":"[^"]*"' | head -n1 | cut -d'"' -f4)
    final_completed_incomplete=$(echo "$tasks_after_incomplete" | grep -A 10 "$task_id" | grep -o '"completed":[^,}]*' | head -n1 | cut -d':' -f2 | tr -d ' ')
    echo "Final task status after marking incomplete: $final_status_incomplete"
    echo "Final task completed flag after marking incomplete: $final_completed_incomplete"
    
    if [ "$final_completed_incomplete" = "false" ] && [ "$final_status_incomplete" = "todo" ]; then
        echo "SUCCESS: Task was properly marked as incomplete and did not disappear!"
    else
        echo "ERROR: Task was not properly marked as incomplete"
        exit 1
    fi
else
    echo "ERROR: Task disappeared after marking as incomplete!"
    exit 1
fi

echo ""
echo "VERIFICATION COMPLETE: The fix is working correctly!"
echo "- Tasks are properly updated when marked as complete/incomplete"
echo "- Tasks do not disappear after status changes"
echo "- Both completion directions (todo↔completed) work correctly"