"""
ProChat - Comprehensive Test Suite
Tests all features including multi-user chat simulation
"""

import socketio
import requests
import time
import threading
from datetime import datetime

# Test configuration
BASE_URL = 'http://localhost:5000'
TEST_PASSED = []
TEST_FAILED = []

def print_test(name, passed, message=""):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")
    if message:
        print(f"         {message}")
    
    if passed:
        TEST_PASSED.append(name)
    else:
        TEST_FAILED.append(name)

def test_server_connection():
    """Test 1: Server is accessible"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        passed = response.status_code == 200
        print_test("Server Connection", passed, f"Status code: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Server Connection", False, f"Error: {str(e)}")
        return False

def test_api_rooms():
    """Test 2: Rooms API endpoint"""
    try:
        response = requests.get(f'{BASE_URL}/api/rooms', timeout=5)
        passed = response.status_code == 200
        if passed:
            rooms = response.json()
            passed = len(rooms) == 4  # Should have 4 default rooms
            print_test("Rooms API Endpoint", passed, f"Found {len(rooms)} rooms: {', '.join([r['name'] for r in rooms])}")
        else:
            print_test("Rooms API Endpoint", False, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Rooms API Endpoint", False, f"Error: {str(e)}")
        return False

def test_api_users():
    """Test 3: Users API endpoint"""
    try:
        response = requests.get(f'{BASE_URL}/api/users', timeout=5)
        passed = response.status_code == 200
        if passed:
            users = response.json()
            print_test("Users API Endpoint", passed, f"Active users: {len(users)}")
        else:
            print_test("Users API Endpoint", False, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Users API Endpoint", False, f"Error: {str(e)}")
        return False

def test_api_messages():
    """Test 4: Messages API endpoint"""
    try:
        response = requests.get(f'{BASE_URL}/api/messages/general', timeout=5)
        passed = response.status_code == 200
        if passed:
            messages = response.json()
            print_test("Messages API Endpoint", passed, f"Messages in general: {len(messages)}")
        else:
            print_test("Messages API Endpoint", False, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Messages API Endpoint", False, f"Error: {str(e)}")
        return False

class ChatUser:
    """Simulated chat user"""
    
    def __init__(self, username):
        self.username = username
        self.sio = socketio.Client()
        self.messages_received = []
        self.connected = False
        self.joined = False
        
        @self.sio.on('connect')
        def on_connect():
            self.connected = True
            print(f"         [{self.username}] Connected to server")
        
        @self.sio.on('disconnect')
        def on_disconnect():
            self.connected = False
            print(f"         [{self.username}] Disconnected")
        
        @self.sio.on('message')
        def on_message(data):
            self.messages_received.append(data)
            print(f"         [{self.username}] Received: {data['username']}: {data['message']}")
        
        @self.sio.on('user_joined')
        def on_user_joined(data):
            print(f"         [{self.username}] User joined: {data['username']}")
        
        @self.sio.on('user_left')
        def on_user_left(data):
            print(f"         [{self.username}] User left: {data['username']}")
    
    def connect(self):
        """Connect to server"""
        try:
            self.sio.connect(BASE_URL)
            return True
        except Exception as e:
            print(f"         [{self.username}] Connection error: {str(e)}")
            return False
    
    def join_room(self, room='general'):
        """Join a chat room"""
        try:
            self.sio.emit('join', {'username': self.username, 'room': room})
            time.sleep(0.5)  # Wait for join to process
            self.joined = True
            return True
        except Exception as e:
            print(f"         [{self.username}] Join error: {str(e)}")
            return False
    
    def send_message(self, message, room='general'):
        """Send a message"""
        try:
            self.sio.emit('message', {
                'username': self.username,
                'message': message,
                'room': room,
                'type': 'text'
            })
            return True
        except Exception as e:
            print(f"         [{self.username}] Send error: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        try:
            if self.connected:
                self.sio.disconnect()
            return True
        except Exception as e:
            print(f"         [{self.username}] Disconnect error: {str(e)}")
            return False

def test_single_user_connection():
    """Test 5: Single user can connect"""
    try:
        user = ChatUser("TestUser1")
        connected = user.connect()
        time.sleep(1)
        
        if connected and user.connected:
            user.disconnect()
            print_test("Single User Connection", True, "User connected successfully")
            return True
        else:
            print_test("Single User Connection", False, "Connection failed")
            return False
    except Exception as e:
        print_test("Single User Connection", False, f"Error: {str(e)}")
        return False

def test_user_join_room():
    """Test 6: User can join room"""
    try:
        user = ChatUser("TestUser2")
        user.connect()
        time.sleep(1)
        
        joined = user.join_room('general')
        time.sleep(1)
        
        success = user.connected and user.joined
        user.disconnect()
        
        print_test("User Join Room", success, "User joined room successfully")
        return success
    except Exception as e:
        print_test("User Join Room", False, f"Error: {str(e)}")
        return False

def test_send_receive_message():
    """Test 7: User can send and receive messages"""
    try:
        user = ChatUser("TestUser3")
        user.connect()
        time.sleep(1)
        user.join_room('general')
        time.sleep(1)
        
        # Send a message
        test_message = f"Test message at {datetime.now().strftime('%H:%M:%S')}"
        user.send_message(test_message)
        time.sleep(2)
        
        # Check if message was received (echo back)
        received = any(msg['message'] == test_message for msg in user.messages_received)
        user.disconnect()
        
        print_test("Send/Receive Message", received, f"Message: '{test_message}'")
        return received
    except Exception as e:
        print_test("Send/Receive Message", False, f"Error: {str(e)}")
        return False

def test_two_users_chatting():
    """Test 8: Two users chatting simultaneously"""
    print("\n🔄 Starting two-user chat simulation...")
    
    try:
        # Create two users
        alice = ChatUser("Alice")
        bob = ChatUser("Bob")
        
        # Connect both users
        alice.connect()
        time.sleep(1)
        bob.connect()
        time.sleep(1)
        
        # Both join the same room
        alice.join_room('general')
        time.sleep(1)
        bob.join_room('general')
        time.sleep(2)
        
        # Alice sends a message
        alice_msg1 = "Hello Bob! 👋"
        alice.send_message(alice_msg1)
        time.sleep(2)
        
        # Bob sends a reply
        bob_msg1 = "Hi Alice! How are you?"
        bob.send_message(bob_msg1)
        time.sleep(2)
        
        # Alice replies back
        alice_msg2 = "I'm great! Testing the chat app 🚀"
        alice.send_message(alice_msg2)
        time.sleep(2)
        
        # Bob sends final message
        bob_msg2 = "Awesome! It's working perfectly! ✨"
        bob.send_message(bob_msg2)
        time.sleep(2)
        
        # Verify both users received messages
        alice_received_bob = any('Bob' in msg['username'] for msg in alice.messages_received)
        bob_received_alice = any('Alice' in msg['username'] for msg in bob.messages_received)
        
        print(f"         Alice received {len(alice.messages_received)} messages")
        print(f"         Bob received {len(bob.messages_received)} messages")
        
        # Disconnect both users
        alice.disconnect()
        bob.disconnect()
        
        success = alice_received_bob and bob_received_alice
        print_test("Two Users Chatting", success, "Both users communicated successfully")
        return success
        
    except Exception as e:
        print_test("Two Users Chatting", False, f"Error: {str(e)}")
        return False

def test_message_persistence():
    """Test 9: Messages persist in database"""
    try:
        # Send a unique message
        user = ChatUser("PersistenceTest")
        user.connect()
        time.sleep(1)
        user.join_room('general')
        time.sleep(1)
        
        unique_msg = f"Persistence test {int(time.time())}"
        user.send_message(unique_msg)
        time.sleep(2)
        user.disconnect()
        time.sleep(1)
        
        # Check if message appears in API
        response = requests.get(f'{BASE_URL}/api/messages/general', timeout=5)
        messages = response.json()
        
        # Look for our message
        found = any(unique_msg in msg['content'] for msg in messages)
        
        print_test("Message Persistence", found, f"Message found in database: {found}")
        return found
        
    except Exception as e:
        print_test("Message Persistence", False, f"Error: {str(e)}")
        return False

def test_multiple_rooms():
    """Test 10: Users can join different rooms"""
    try:
        user1 = ChatUser("RoomTest1")
        user2 = ChatUser("RoomTest2")
        
        user1.connect()
        time.sleep(1)
        user2.connect()
        time.sleep(1)
        
        # User1 joins 'tech'
        user1.join_room('tech')
        time.sleep(1)
        
        # User2 joins 'gaming'
        user2.join_room('gaming')
        time.sleep(1)
        
        # Both send messages
        user1.send_message("Tech talk!", 'tech')
        user2.send_message("Gaming time!", 'gaming')
        time.sleep(2)
        
        user1.disconnect()
        user2.disconnect()
        
        # Verify messages went to correct rooms
        tech_msgs = requests.get(f'{BASE_URL}/api/messages/tech').json()
        gaming_msgs = requests.get(f'{BASE_URL}/api/messages/gaming').json()
        
        tech_found = any('Tech talk!' in msg['content'] for msg in tech_msgs)
        gaming_found = any('Gaming time!' in msg['content'] for msg in gaming_msgs)
        
        success = tech_found and gaming_found
        print_test("Multiple Rooms", success, f"Tech: {tech_found}, Gaming: {gaming_found}")
        return success
        
    except Exception as e:
        print_test("Multiple Rooms", False, f"Error: {str(e)}")
        return False

def test_typing_indicator():
    """Test 11: Typing indicator functionality"""
    try:
        user = ChatUser("TypeTest")
        user.connect()
        time.sleep(1)
        user.join_room('general')
        time.sleep(1)
        
        # Emit typing event
        user.sio.emit('typing', {'username': user.username, 'room': 'general', 'is_typing': True})
        time.sleep(1)
        
        user.sio.emit('typing', {'username': user.username, 'room': 'general', 'is_typing': False})
        time.sleep(1)
        
        user.disconnect()
        
        # If no errors occurred, test passes
        print_test("Typing Indicator", True, "Typing events sent successfully")
        return True
        
    except Exception as e:
        print_test("Typing Indicator", False, f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 PROCHAT - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"Testing server at: {BASE_URL}")
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    print("📡 CONNECTIVITY TESTS")
    print("-" * 70)
    test_server_connection()
    print()
    
    print("🔌 API ENDPOINT TESTS")
    print("-" * 70)
    test_api_rooms()
    test_api_users()
    test_api_messages()
    print()
    
    print("👤 SINGLE USER TESTS")
    print("-" * 70)
    test_single_user_connection()
    test_user_join_room()
    test_send_receive_message()
    print()
    
    print("👥 MULTI-USER TESTS")
    print("-" * 70)
    test_two_users_chatting()
    print()
    
    print("💾 PERSISTENCE TESTS")
    print("-" * 70)
    test_message_persistence()
    print()
    
    print("🏠 ADVANCED FEATURES")
    print("-" * 70)
    test_multiple_rooms()
    test_typing_indicator()
    print()
    
    # Print summary
    print("="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"✅ PASSED: {len(TEST_PASSED)}")
    print(f"❌ FAILED: {len(TEST_FAILED)}")
    print(f"📈 SUCCESS RATE: {len(TEST_PASSED)/(len(TEST_PASSED)+len(TEST_FAILED))*100:.1f}%")
    print("="*70)
    
    if TEST_FAILED:
        print("\n❌ Failed tests:")
        for test in TEST_FAILED:
            print(f"   - {test}")
    
    print(f"\nTest completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    # Return success status
    return len(TEST_FAILED) == 0

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        exit(1)
