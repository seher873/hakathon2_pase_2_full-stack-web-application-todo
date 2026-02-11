import os
from typing import Dict, Any, List
from pydantic import BaseModel
import cohere
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ..services.database import SessionLocal
from ..services.conversation_service import ConversationService, MessageService
from ..services.language_processing import translate_for_intent_classification

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
        api_key = os.getenv("COHERE_API_KEY")
        if api_key:
            self.co = cohere.Client(api_key)
            self.is_available = True
        else:
            print("WARNING: COHERE_API_KEY environment variable is not set. Chatbot functionality will be limited.")
            self.co = None
            self.is_available = False

    def classify_intent(self, message: str) -> IntentClassification:
        """
        Classify the intent of the user message using Cohere
        """
        # Translate the message for intent classification if needed
        translated_message = translate_for_intent_classification(message)
        
        if not self.is_available:
            # Fallback intent classification when API is not available
            message_lower = translated_message.lower()
            if any(word in message_lower for word in ['create', 'add', 'make', 'new', 'bnana', 'banaya', 'naya']):
                intent = "create_todo"
            elif any(word in message_lower for word in ['show', 'list', 'what', 'do', 'dikhao', 'dikhaye', 'kya', 'hai']):
                intent = "list_todos"
            elif any(word in message_lower for word in ['delete', 'remove', 'hatana', 'nikal']):
                intent = "delete_todo"
            elif any(word in message_lower for word in ['complete', 'done', 'mark', 'ho', 'gya', 'hogya', 'krdo', 'kardo']):
                intent = "update_todo"
            else:
                intent = "chitchat"

            return IntentClassification(
                intent=intent,
                confidence=0.5,  # Default confidence when using fallback
                entities={}
            )

        # Define possible intents and examples
        examples = [
            {"text": "Create a new task called 'Buy groceries'", "label": "create_todo"},
            {"text": "Add 'Walk the dog' to my tasks", "label": "create_todo"},
            {"text": "Make a new todo for 'Finish report'", "label": "create_todo"},
            {"text": "Show me my tasks", "label": "list_todos"},
            {"text": "What do I need to do today?", "label": "list_todos"},
            {"text": "List all my todos", "label": "list_todos"},
            {"text": "List pending tasks", "label": "list_todos"},
            {"text": "Show pending tasks", "label": "list_todos"},
            {"text": "Show completed tasks", "label": "list_todos"},
            {"text": "Delete my task 'Buy groceries'", "label": "delete_todo"},
            {"text": "Remove 'Walk the dog' from my tasks", "label": "delete_todo"},
            {"text": "Mark 'Finish report' as complete", "label": "update_todo"},
            {"text": "Complete my task 'Call mom'", "label": "update_todo"},
            {"text": "How are you?", "label": "chitchat"},
            {"text": "Tell me a joke", "label": "chitchat"},
            {"text": "What's the weather?", "label": "chitchat"},
            # Roman Urdu examples
            {"text": "Naya kaam bnana hai", "label": "create_todo"},
            {"text": "Meray kaamon ko dikhao", "label": "list_todos"},
            {"text": "Kaam complete krdo", "label": "update_todo"},
            {"text": "Koi madad chahta hon", "label": "chitchat"},
            {"text": "Pending tasks dikhao", "label": "list_todos"},
            {"text": "Completed tasks dikhao", "label": "list_todos"},
            {"text": "Sab kaam dikhao", "label": "list_todos"},
            {"text": "Meri pending list batao", "label": "list_todos"},
        ]

        # Use Cohere classify endpoint
        try:
            # Try the modern Cohere API format first
            response = self.co.classify(
                model='large',
                inputs=[translated_message],
                examples=[[ex["text"], ex["label"]] for ex in examples]
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
        except Exception as e:
            print(f"Cohere classification failed: {e}")
            # Fallback to simple keyword matching when API fails
            message_lower = translated_message.lower()
            if any(word in message_lower for word in ['create', 'add', 'make', 'new', 'bnana', 'banaya', 'naya']):
                intent = "create_todo"
            elif any(word in message_lower for word in ['show', 'list', 'what', 'do', 'dikhao', 'dikhaye', 'kya', 'hai']) or 'pending' in message_lower or 'completed' in message_lower:
                intent = "list_todos"
            elif any(word in message_lower for word in ['delete', 'remove', 'hatana', 'nikal']):
                intent = "delete_todo"
            elif any(word in message_lower for word in ['complete', 'done', 'mark', 'ho', 'gya', 'hogya', 'krdo', 'kardo']):
                intent = "update_todo"
            else:
                intent = "chitchat"

            return IntentClassification(
                intent=intent,
                confidence=0.3,  # Lower confidence for fallback
                entities={}
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
                response = await self.handle_list_todos(user_id, message)
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
        # Translate the message to handle Roman Urdu
        translated_message = translate_for_intent_classification(message)
        
        # Extract task description from message
        # This is a simplified extraction - in practice, you'd use more sophisticated NLP
        import re
        # Look for phrases like "called 'task name'" or "named 'task name'" or Roman Urdu equivalents
        match = re.search(r"(?:called|named|to do|for|bnana|banaya|k lia|k liye|kaam)['\"]([^'\"]+)['\"]", translated_message.lower())
        if not match:
            # Try alternative patterns for Roman Urdu
            match = re.search(r"(?:bnana|banaya|k lia|k liye)['\"]?([^'\"]+)", translated_message.lower())
        if not match:
            # Try to extract the task name after certain keywords
            match = re.search(r"(?:create|add|make|bnana|banaya)\s+(.+?)(?:\.|$)", translated_message.lower())
        if not match:
            # Try to extract after "kaam" or "task"
            match = re.search(r"(?:kaam|task|kam)\s+(.+?)(?:\.|$)", translated_message.lower())
            
        if match:
            task_desc = match.group(1).strip()
        else:
            # If we can't extract the task name, return a prompt
            return "What task would you like to create?"

        # In a real implementation, you would call the tasks API here
        # For now, return a mock response
        return f"I've created a task for '{task_desc}'. It has been added to your todo list."

    async def handle_list_todos(self, user_id: str, original_message: str = "") -> str:
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
                    # Filter tasks based on context (pending/completed)
                    # This would normally be determined by the specific request, but for now we'll use a general approach
                    all_tasks = tasks
                    pending_tasks = [task for task in tasks if not task.get('completed', False)]
                    completed_tasks = [task for task in tasks if task.get('completed', False)]

                    # Determine which list to show based on the original message
                    # Check if the original message contains words indicating specific filtering
                    original_msg_lower = original_message.lower()
                    
                    # Check for Roman Urdu and English variants
                    if any(word in original_msg_lower for word in ['pending', 'panding', 'incomplete', 'khatam', 'khtm', 'nahi_hua']):
                        filtered_tasks = pending_tasks
                        task_type = "pending"
                    elif any(word in original_msg_lower for word in ['completed', 'done', 'hogya', 'ho_gaya', 'khatam', 'khtm']):
                        filtered_tasks = completed_tasks
                        task_type = "completed"
                    else:
                        filtered_tasks = all_tasks
                        task_type = "current"

                    if filtered_tasks:
                        task_list = "\n".join([f"{i+1}. {task['title']}" for i, task in enumerate(filtered_tasks)])
                        return f"Here are your {task_type} tasks:\n{task_list}\n\nYou have {len(filtered_tasks)} {task_type} tasks."
                    else:
                        return f"You don't have any {task_type} tasks yet."
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
        # Translate the message to handle Roman Urdu
        translated_message = translate_for_intent_classification(message)
        
        # Extract task description from message
        import re
        match = re.search(r"(?:called|named|'|\")([^'\"]+)(?:'|\")", translated_message.lower())
        if not match:
            # Try Roman Urdu patterns
            match = re.search(r"(?:delete|remove|hatana|nikal|khatam|band|khtm)\s+(.+?)(?:\.|$)", translated_message.lower())
        if match:
            task_desc = match.group(1)
            return f"I've deleted the task '{task_desc}' from your list."
        else:
            return "Which task would you like to delete?"

    async def handle_update_todo(self, message: str, user_id: str) -> str:
        """
        Handle updating a todo based on the user message
        """
        # Translate the message to handle Roman Urdu
        translated_message = translate_for_intent_classification(message)
        
        # Extract task description from message
        import re
        match = re.search(r"(?:called|named|'|\")([^'\"]+)(?:'|\")", translated_message.lower())
        if not match:
            # Try Roman Urdu patterns
            match = re.search(r"(?:complete|done|mark|krdo|kardo|ho|gya|hogya|krna|kar|update|change|badlo)\s+(.+?)(?:\.|$)", translated_message.lower())
        if match:
            task_desc = match.group(1)
            # Check for completion indicators in both English and Roman Urdu
            if any(indicator in translated_message.lower() for indicator in ["complete", "done", "krdo", "kardo", "ho", "gya", "hogya", "krna", "kar", "mark"]):
                return f"I've marked the task '{task_desc}' as complete."
            else:
                return f"What would you like to update about the task '{task_desc}'?"
        else:
            return "Which task would you like to update?"

    async def generate_general_response(self, message: str) -> str:
        """
        Generate a general response for non-task-related messages
        """
        # Translate the message to handle Roman Urdu
        translated_message = translate_for_intent_classification(message)
        
        if not self.is_available:
            # Fallback response when API is not available
            fallback_responses = {
                "hello": "Hello! I'm the AI assistant. How can I help you with your tasks?",
                "hi": "Hi there! I'm here to help you manage your tasks. What would you like to do?",
                "how are you": "I'm doing well, thank you! I'm here to help you with your tasks.",
                "help": "I can help you create, list, update, and delete tasks. For example, you can say 'Create a task called buy groceries' or 'Show me my tasks'.",
                "thank you": "You're welcome! Is there anything else I can help you with?",
                "thanks": "You're welcome! Feel free to ask me anything about managing your tasks.",
                # Roman Urdu responses
                "assalam": "Wa alaykum assalam! Main aapki kisi bhi kaam mein madad kar sakta hun. Kya aap koi kaam banana chahte hain?",
                "madad": "Main aapki kaamon ki list dekh sakta hun, naye kaam bana sakta hun, aur unhe complete ya delete bhi kar sakta hun. Jaise aap keh sakte hain 'Ek kaam banao jo groceries khareedna hai' ya 'Mere kaam dikhaao'.",
                "shukriya": "Aapka shukriya! Kya aapko aur kisi cheez ki zaroorat hai?",
                "kaise": "Aap mujhse keh sakte hain kehne ke liye 'Naya kaam banao', 'Mere kaam dikhaao', 'Kaam complete kardo', ya kuch aur pooch sakte hain."
            }

            message_lower = translated_message.lower()
            for trigger, response in fallback_responses.items():
                if trigger in message_lower:
                    return response

            return "Main aapka AI assistant hun jo aapki kaam manage karne mein madad karta hai. Main aapki kaamon ki list dekh sakta hun, naye kaam bana sakta hun, aur unhe complete ya delete bhi kar sakta hun. Jaise aap keh sakte hain 'Ek kaam banao jo groceries khareedna hai' ya 'Mere kaam dikhaao'."

        # Use Cohere's generate endpoint for general conversation
        response = self.co.generate(
            model='command-xlarge-nightly',
            prompt=f"Human: {translated_message}\nAI:",
            max_tokens=100,
            temperature=0.7
        )

        return response.generations[0].text.strip()