import os
from gradio.helpers import create_examples
import gradio as gr
import subprocess
import time

# Since this is a full-stack application with both frontend and backend,
# we'll create a simple interface that explains how to run the application

def run_application():
    """Instructions for running the full-stack application"""
    instructions = """
    # Full-Stack Todo Application
    
    This is a complete full-stack application with:
    - Frontend: Next.js application
    - Backend: FastAPI server
    - Database: PostgreSQL
    
    ## To run this application locally:
    
    1. Clone the repository
    2. Navigate to the backend directory and install dependencies:
       ```bash
       cd backend
       pip install -r requirements.txt
       ```
    3. Set up environment variables in a `.env` file
    4. Start the backend:
       ```bash
       cd backend
       python main.py
       ```
    5. In a new terminal, navigate to the frontend directory:
       ```bash
       cd frontend
       npm install
       npm run dev
       ```
    
    The application will be available at http://localhost:3000
    
    ## Backend API
    The backend runs on http://localhost:8000 and provides:
    - User authentication endpoints
    - Task management endpoints
    - JWT-based authentication
    
    ## Frontend
    The frontend is built with Next.js and provides:
    - User registration and login
    - Dashboard for managing tasks
    - Responsive UI with Tailwind CSS
    """
    
    return instructions

with gr.Blocks(title="Full-Stack Todo Application") as demo:
    gr.Markdown("# Full-Stack Todo Application")
    gr.Markdown("This is a complete full-stack application with Next.js frontend and FastAPI backend.")
    
    output = gr.Textbox(label="Application Information", lines=20)
    
    btn = gr.Button("Show Application Details")
    btn.click(run_application, outputs=output)
    
    gr.Markdown("## Note")
    gr.Markdown("This Hugging Face Space serves as a demonstration of the code. "
                "To run the full application, please clone the repository and follow "
                "the instructions provided.")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)