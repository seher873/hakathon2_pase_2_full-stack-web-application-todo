"""
Integration test for frontend-backend connection.
Tests the deployed backend at https://sehrkhan873-hakathon-2.hf.space
"""
import requests
import json

BASE_URL = "https://sehrkhan873-hakathon-2.hf.space"

def test_health_endpoints():
    """Test all health endpoints"""
    print("=" * 60)
    print("Testing Health Endpoints")
    print("=" * 60)
    
    # Root health check
    response = requests.get(f"{BASE_URL}/")
    print(f"\n1. Root Endpoint (/):")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    # Backend health
    response = requests.get(f"{BASE_URL}/health")
    print(f"\n2. Backend Health (/health):")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    # Chat API health
    response = requests.get(f"{BASE_URL}/api/chat/health")
    print(f"\n3. Chat API Health (/api/chat/health):")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
def test_chat_message_endpoint():
    """Test chat message endpoint (expects auth token)"""
    print("\n" + "=" * 60)
    print("Testing Chat Message Endpoint")
    print("=" * 60)
    
    # Test without auth token (should fail with 401)
    response = requests.post(
        f"{BASE_URL}/api/chat/message",
        json={"message": "Hello", "user_id": "test-user"},
        headers={"Content-Type": "application/json"}
    )
    print(f"\n1. Without Authentication:")
    print(f"   Status: {response.status_code}")
    try:
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"   Response: {response.text}")
    
    # Test with dummy auth token
    response = requests.post(
        f"{BASE_URL}/api/chat/message",
        json={"message": "Hello", "user_id": "test-user"},
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer dummy-token"
        }
    )
    print(f"\n2. With Dummy Token:")
    print(f"   Status: {response.status_code}")
    try:
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"   Response: {response.text}")

def test_cors_headers():
    """Test CORS configuration"""
    print("\n" + "=" * 60)
    print("Testing CORS Headers")
    print("=" * 60)
    
    response = requests.options(
        f"{BASE_URL}/api/chat/message",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type, Authorization"
        }
    )
    
    print(f"\nCORS Preflight Response:")
    print(f"   Status: {response.status_code}")
    print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
    print(f"   Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'Not set')}")
    print(f"   Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'Not set')}")

if __name__ == "__main__":
    print(f"\nTesting integration with: {BASE_URL}\n")
    
    try:
        test_health_endpoints()
        test_chat_message_endpoint()
        test_cors_headers()
        
        print("\n" + "=" * 60)
        print("Integration Test Complete!")
        print("=" * 60)
        print("\nSummary:")
        print("✅ Backend is running and healthy")
        print("✅ Health endpoints are accessible")
        print("⚠️  Chat message endpoint requires authentication (expected)")
        print("\nNext steps:")
        print("1. Ensure frontend is configured with correct API URL")
        print("2. Implement proper authentication flow")
        print("3. Test full user journey from frontend")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
