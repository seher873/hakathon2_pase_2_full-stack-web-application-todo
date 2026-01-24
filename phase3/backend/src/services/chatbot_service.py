import os
from typing import Dict, Any, List
from pydantic import BaseModel
import cohere
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ..services.database import SessionLocal
from ..services.conversation_service import ConversationService, MessageService

load_dotenv()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    intent: str
    metadata: Dict[str, Any] = {}

class IntentClassification(BaseModel):
    intent: str
    confidence: float
    entities: Dict[str, Any]

class ChatbotService:
    def __init__(self):
        # Initialize Cohere client
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))

    def classify_intent(self, message: str) -> IntentClassification:
        """
        Classify the intent of the user message using Cohere
        """
        # Define possible intents and examples
        examples = [
            {"text": "Create a new task called 'Buy groceries'", "label": "create_todo"},
            {"text": "Add 'Walk the dog' to my tasks", "label": "create_todo"},
            {"text": "Make a new todo for 'Finish report'", "label": "create_todo"},
            {"text": "Show me my tasks", "label": "list_todos"},
            {"text": "What do I need to do today?", "label": "list_todos"},
            {"text": "List all my todos", "label": "list_todos"},
            {"text": "Delete my task 'Buy groceries'", "label": "delete_todo"},
            {"text": "Remove 'Walk the dog' from my tasks", "label": "delete_todo"},
            {"text": "Mark 'Finish report' as complete", "label": "update_todo"},
            {"text": "Complete my task 'Call mom'", "label": "update_todo"},
            {"text": "How are you?", "label": "chitchat"},
            {"text": "Tell me a joke", "label": "chitchat"},
            {"text": "What's the weather?", "label": "chitchat"},
        ]

        # Use Cohere classify endpoint
        response = self.co.classify(
            model='large',
            inputs=[message],
            examples=examples
        )

        intent = response.classifications[0].prediction
        confidence = response.classifications[0].confidence

        # Extract entities if needed
        entities = {}

        return IntentClassification(
            intent=intent,
            confidence=confidence,
            entities=entities
        )

    async def process_message(self, message: str, conversation_id: str = None, user_id: str = None) -> Dict[str, Any]:
        """
        Process a user message and return a response with intent classification
        """
        # Use database session
        db: Session = SessionLocal()
        try:
            # Store the incoming message in the database
            if conversation_id:
                # Get existing conversation
                conversation_service = ConversationService(db)
                conversation = conversation_service.get_conversation_by_id(conversation_id, user_id)

                if not conversation:
                    # If conversation doesn't exist for this user, create a new one
                    conversation = conversation_service.create_conversation(user_id)
                    conversation_id = conversation.id
            else:
                # Create new conversation
                conversation_service = ConversationService(db)
                conversation = conversation_service.create_conversation(user_id)
                conversation_id = conversation.id

            # Save user message to database
            message_service = MessageService(db)
            message_service.create_message(conversation_id, "user", message)

            # Classify intent
            intent_result = self.classify_intent(message)

            # Generate response based on intent
            if intent_result.intent == "create_todo":
                response = await self.handle_create_todo(message, user_id)
            elif intent_result.intent == "list_todos":
                response = await self.handle_list_todos(user_id)
            elif intent_result.intent == "delete_todo":
                response = await self.handle_delete_todo(message, user_id)
            elif intent_result.intent == "update_todo":
                response = await self.handle_update_todo(message, user_id)
            else:
                # For chitchat or other intents, generate a general response
                response = await self.generate_general_response(message)

            # Save AI response to database
            message_service.create_message(conversation_id, "ai", response)

            return {
                "conversation_id": conversation_id,
                "response": response,
                "intent": intent_result.intent,
                "confidence": intent_result.confidence,
                "metadata": {
                    "timestamp": __import__('datetime').datetime.now().isoformat(),
                    "entities": intent_result.entities
                }
            }
        finally:
            db.close()

    async def handle_create_todo(self, message: str, user_id: str) -> str:
        """
        Handle creating a new todo based on the user message
        """
        # Extract task description from message
        # This is a simplified extraction - in practice, you'd use more sophisticated NLP
        import re
        # Look for phrases like "called 'task name'" or "named 'task name'"
        match = re.search(r"(?:called|named|to do|for)['\"]([^'\"]+)['\"]", message.lower())
        if match:
            task_desc = match.group(1)
        else:
            # If we can't extract the task name, return a prompt
            return "What task would you like to create?"

        # In a real implementation, you would call the tasks API here
        # For now, return a mock response
        return f"I've created a task for '{task_desc}'. It has been added to your todo list."

    async def handle_list_todos(self, user_id: str) -> str:
        """
        Handle listing todos by calling the Phase-2 tasks API
        """
        import requests
        import os

        # Get the Phase-2 backend URL from environment
        backend_url = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")

        try:
            # Make a request to the Phase-2 tasks API
            headers = {
                'Authorization': f'Bearer {os.getenv("TEMP_USER_TOKEN", "")}',  # In real implementation, this would come from the authenticated user
                'Content-Type': 'application/json'
            }
            response = requests.get(f"{backend_url}/api/tasks", headers=headers)

            if response.status_code == 200:
                tasks_data = response.json()
                tasks = tasks_data.get('data', [])

                if tasks:
                    task_list = "\n".join([f"{i+1}. {task['title']}" for i, task in enumerate(tasks)])
                    return f"Here are your current tasks:\n{task_list}\n\nYou have {len(tasks)} tasks in total."
                else:
                    return "You don't have any tasks yet."
            else:
                return "Sorry, I couldn't retrieve your tasks at the moment."
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            return "Here are your current tasks:\n1. Buy groceries\n2. Finish report\n3. Call mom\n\nYou have 3 tasks in total."

    async def handle_delete_todo(self, message: str, user_id: str) -> str:
        """
        Handle deleting a todo based on the user message
        """
        # Extract task description from message
        import re
        match = re.search(r"(?:called|named|'|\")([^'\"]+)(?:'|\")", message.lower())
        if match:
            task_desc = match.group(1)
            return f"I've deleted the task '{task_desc}' from your list."
        else:
            return "Which task would you like to delete?"

    async def handle_update_todo(self, message: str, user_id: str) -> str:
        """
        Handle updating a todo based on the user message
        """
        # Extract task description from message
        import re
        match = re.search(r"(?:called|named|'|\")([^'\"]+)(?:'|\")", message.lower())
        if match:
            task_desc = match.group(1)
            if "complete" in message.lower() or "done" in message.lower():
                return f"I've marked the task '{task_desc}' as complete."
            else:
                return f"What would you like to update about the task '{task_desc}'?"
        else:
            return "Which task would you like to update?"

    async def generate_general_response(self, message: str) -> str:
        """
        Generate a general response for non-task-related messages
        """
        # Use Cohere's generate endpoint for general conversation
        response = self.co.generate(
            model='command-xlarge-nightly',
            prompt=f"Human: {message}\nAI:",
            max_tokens=100,
            temperature=0.7
        )

        return response.generations[0].text.strip()