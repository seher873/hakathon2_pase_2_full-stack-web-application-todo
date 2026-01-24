import requests
import json

# Test the AI chatbot functionality
def test_chatbot():
    print("Testing AI Chatbot functionality...")
    
    # This is a mock token for testing purposes
    # In a real scenario, you would need to authenticate first
    mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    
    headers = {
        "Authorization": f"Bearer {mock_token}",
        "Content-Type": "application/json"
    }
    
    # Test data
    test_message = {
        "message": "Hello, how are you?",
        "conversation_id": None
    }
    
    try:
        # Send request to the chatbot endpoint
        response = requests.post(
            "http://localhost:8001/api/chatbot/chat",
            headers=headers,
            json=test_message
        )
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Chatbot endpoint is working!")
            data = response.json()
            print(f"Response: {data.get('response', 'N/A')}")
            print(f"Intent: {data.get('intent', 'N/A')}")
        else:
            print("❌ Chatbot endpoint returned an error.")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the chatbot service. Is it running?")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")

if __name__ == "__main__":
    test_chatbot()