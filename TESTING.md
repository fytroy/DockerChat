# Quick Test Guide

## Running the Tests

### 1. Make sure the app is running
```bash
docker-compose up -d
```

### 2. Install test dependencies (one-time setup)
```bash
pip install python-socketio[client] requests python-engineio
```

### 3. Run the test suite
```bash
python test_chat.py
```

## What Gets Tested

1. ✅ Server connectivity
2. ✅ API endpoints (rooms, users, messages)
3. ✅ Single user connection
4. ✅ User joining rooms
5. ✅ Sending/receiving messages
6. ✅ **Two users chatting simultaneously** 👥
7. ✅ Message persistence in database
8. ✅ Multiple room support
9. ✅ Typing indicators

## Expected Output

```
🧪 PROCHAT - COMPREHENSIVE TEST SUITE
======================================================================
✅ PASSED: 11
❌ FAILED: 0
📈 SUCCESS RATE: 100.0%
```

## Two-User Chat Simulation

The test automatically simulates Alice and Bob chatting:

```
Alice: Hello Bob! 👋
Bob: Hi Alice! How are you?
Alice: I'm great! Testing the chat app 🚀
Bob: Awesome! It's working perfectly! ✨
```

Both users receive all messages in real-time!

## Viewing Detailed Results

See [TEST_RESULTS.md](TEST_RESULTS.md) for complete test report.

## Troubleshooting

**Problem:** Tests fail to connect  
**Solution:** Make sure docker containers are running (`docker ps`)

**Problem:** Import errors  
**Solution:** Install dependencies: `pip install python-socketio[client] requests`

**Problem:** Database errors  
**Solution:** Restart containers: `docker-compose restart`
