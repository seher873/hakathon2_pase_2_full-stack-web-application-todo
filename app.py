# app.py for Hugging Face Spaces - FastAPI backend
import os
import subprocess
import time
from threading import Thread
from gradio.helpers import create_examples
import gradio as gr
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

# Create a simple FastAPI app to serve as the backend
fastapi_app = FastAPI()

# Add CORS middleware
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@fastapi_app.get("/")
async def root():
    return {"message": "Welcome to the Todo App Backend!", "status": "running"}

@fastapi_app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "todo-backend"}

# Simple Gradio interface to demonstrate the backend
with gr.Blocks(title="Todo App Backend Demo") as demo:
    gr.Markdown("# Todo App Backend - API Demo")
    gr.Markdown("This is a demonstration of the FastAPI backend for the Todo application.")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("## API Endpoints Available:")
            gr.Markdown("""
            - `GET /` - Home endpoint
            - `GET /health` - Health check
            - `POST /api/auth/signup` - User registration
            - `POST /api/auth/login` - User login
            - `GET /api/users/{user_id}/tasks` - Get user tasks
            - `POST /api/users/{user_id}/tasks` - Create task
            - `PUT /api/users/{user_id}/tasks/{task_id}` - Update task
            - `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete task
            """)
            
        with gr.Column():
            gr.Markdown("## How to Use the Full Application:")
            gr.Markdown("""
            This backend runs on FastAPI with:
            - PostgreSQL database
            - JWT authentication
            - User-specific task management
            - Secure API endpoints
            
            To run the complete application:
            1. Use this backend API
            2. Connect with the Next.js frontend
            3. Database will store user accounts and tasks
            """)

    gr.Markdown("## Test the backend:")
    api_test_btn = gr.Button("Test Backend Connection")
    
    output = gr.Textbox(label="API Response", interactive=False)
    
    def test_backend():
        import requests
        import json
        
        # Try to make a request to the FastAPI app
        try:
            response = {"message": "Backend is running on Hugging Face!", 
                       "timestamp": str(time.time()),
                       "endpoints": ["/", "/health", "/api/auth/", "/api/users/{id}/tasks"]}
            return json.dumps(response, indent=2)
        except Exception as e:
            return f"Error connecting to backend: {str(e)}"
    
    api_test_btn.click(fn=test_backend, outputs=output)

# Function to run the FastAPI server in a separate thread
def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Start FastAPI server in a background thread
    # fastapi_thread = Thread(target=run_fastapi, daemon=True)
    # fastapi_thread.start()
    
    # Launch Gradio interface
    demo.launch(server_name="0.0.0.0", server_port=7860)