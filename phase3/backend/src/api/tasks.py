from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import os
import jwt

router = APIRouter()
security = HTTPBearer()

# Secret key for JWT decoding (should match Phase-2)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-default-secret-key")
ALGORITHM = "HS256"

def verify_token(token: str):
    """Verify JWT token and return user info"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

@router.get("/")
async def get_tasks(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get all tasks for the authenticated user by calling Phase-2 backend
    """
    # Verify the token
    user_payload = verify_token(credentials.credentials)
    
    # Get the Phase-2 backend URL from environment
    backend_url = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
    
    try:
        # Make a request to the Phase-2 tasks API
        headers = {
            'Authorization': f'Bearer {credentials.credentials}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{backend_url}/api/tasks", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from Phase-2 backend: {response.text}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling Phase-2 backend: {str(e)}"
        )

@router.post("/")
async def create_task(task_data: dict, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Create a new task by calling Phase-2 backend
    """
    # Verify the token
    user_payload = verify_token(credentials.credentials)
    
    # Get the Phase-2 backend URL from environment
    backend_url = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
    
    try:
        # Make a request to the Phase-2 tasks API
        headers = {
            'Authorization': f'Bearer {credentials.credentials}',
            'Content-Type': 'application/json'
        }
        response = requests.post(f"{backend_url}/api/tasks", json=task_data, headers=headers)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from Phase-2 backend: {response.text}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling Phase-2 backend: {str(e)}"
        )

@router.put("/{task_id}")
async def update_task(task_id: str, task_data: dict, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Update a task by calling Phase-2 backend
    """
    # Verify the token
    user_payload = verify_token(credentials.credentials)
    
    # Get the Phase-2 backend URL from environment
    backend_url = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
    
    try:
        # Make a request to the Phase-2 tasks API
        headers = {
            'Authorization': f'Bearer {credentials.credentials}',
            'Content-Type': 'application/json'
        }
        response = requests.put(f"{backend_url}/api/tasks/{task_id}", json=task_data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from Phase-2 backend: {response.text}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling Phase-2 backend: {str(e)}"
        )

@router.delete("/{task_id}")
async def delete_task(task_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Delete a task by calling Phase-2 backend
    """
    # Verify the token
    user_payload = verify_token(credentials.credentials)
    
    # Get the Phase-2 backend URL from environment
    backend_url = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
    
    try:
        # Make a request to the Phase-2 tasks API
        headers = {
            'Authorization': f'Bearer {credentials.credentials}',
            'Content-Type': 'application/json'
        }
        response = requests.delete(f"{backend_url}/api/tasks/{task_id}", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from Phase-2 backend: {response.text}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling Phase-2 backend: {str(e)}"
        )

@router.get("/{task_id}")
async def get_task(task_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get a specific task by calling Phase-2 backend
    """
    # Verify the token
    user_payload = verify_token(credentials.credentials)
    
    # Get the Phase-2 backend URL from environment
    backend_url = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
    
    try:
        # Make a request to the Phase-2 tasks API
        headers = {
            'Authorization': f'Bearer {credentials.credentials}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{backend_url}/api/tasks/{task_id}", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from Phase-2 backend: {response.text}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling Phase-2 backend: {str(e)}"
        )