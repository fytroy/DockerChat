 💬 ProChat - Real-Time Chat Application

Chat with your friends in real-time! A professional, feature-rich chat application that lets multiple people communicate instantly through their web browsers.

![1](1.png)

---

 🎯 What is This?

ProChat is a modern chat application where you and your friends can:
- 💬 Send messages to each other instantly
- 👥 See who's online
- 🏠 Chat in different topic-based channels
- 💾 Keep all your chat history saved
- 😊 Send emojis, images, videos, and links
- 🔒 Send private messages to specific people

No sign-up required! Just enter a username and start chatting.

---

 📋 What You Need (Prerequisites)

Before you start, make sure you have:

1. Docker Desktop installed on your computer
   - Windows/Mac: Download from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Install it and make sure it's running (you'll see a whale icon in your taskbar/menu bar)

2. This project folder (DockerChat) with all its files

That's it! Docker will handle everything else automatically.

---

 🚀 Quick Start Guide (For You - The Host)

 Step 1: Get the Project Running

1. Open your terminal/command prompt
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Mac: Press `Cmd + Space`, type `terminal`, press Enter

2. Navigate to the project folder
   ```bash
   cd path/to/DockerChat
   ```
   Example (Windows): `cd C:\Users\YourName\Desktop\DockerChat`

3. Start the application
   ```bash
   docker-compose up --build -d
   ```
   
   ⏳ First time? This will take 2-3 minutes to download and build everything.
   
   ✅ When you see: `Container dockerchat-chat_app-1  Started` - you're ready!

4. Open your browser and go to:
   ```
   http://localhost:5000
   ```

5. Test it!
   - Enter a username (e.g., "Alice")
   - Type a message and hit Enter
   - Open another browser tab (or incognito window) with a different username
   - Watch messages appear in real-time! 🎉

---

 👥 Inviting Your Friend to Chat

Your friend has two options to join:

 Option A: Same Wi-Fi Network (Easiest)

Perfect if you're in the same location (home, office, café)

Your Steps:

1. Find your computer's IP address
   
   Windows:
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., `192.168.1.100`)
   
   Mac/Linux:
   ```bash
   ifconfig
   ```
   or
   ```bash
   hostname -I
   ```

2. Share this URL with your friend:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: `http://192.168.1.100:5000`

Your Friend's Steps:

1. Make sure they're on the same Wi-Fi network as you
2. Open their web browser
3. Type the URL you gave them (e.g., `http://192.168.1.100:5000`)
4. Enter their username
5. Start chatting! 🎊

---

 Option B: Over the Internet (Using ngrok)

Perfect if your friend is in a different location

Your Steps:

1. Install ngrok (one-time setup)
   - Go to [https://ngrok.com/download](https://ngrok.com/download)
   - Download and install it
   - Sign up for a free account and follow their setup instructions

2. Start ngrok
   ```bash
   ngrok http 5000
   ```

3. Copy the HTTPS URL that ngrok shows (looks like: `https://abc123.ngrok.io`)

4. Share that URL with your friend

Your Friend's Steps:

1. Open their web browser (can be anywhere in the world!)
2. Go to the URL you shared (e.g., `https://abc123.ngrok.io`)
3. Enter their username
4. Start chatting! 🌍

---

 📖 How to Use the Chat

 For Everyone (You and Your Friends)

1. When you first open the chat:
   - A popup will ask for your username
   - Choose any name you like (e.g., "Alice", "Bob", "YourName")
   - Click "Join Chat"

2. Sending Messages:
   - Type in the message box at the bottom
   - Press Enter or click Send
   - Your message appears instantly for everyone! ⚡

3. Switching Channels:
   - See the sidebar on the left? Click any channel:
     - general - Main chat room
     - random - Random conversations
     - tech - Tech discussions
     - gaming - Gaming chat
   - Each channel has separate conversations

4. Using Emojis:
   - Click the 😊 smiley face button
   - Pick any emoji from the grid
   - It appears in your message!

5. Sending Images/Videos:
   - Click the 🖼️ image or 🎥 video icon
   - Select a file from your computer
   - It appears in the chat for everyone to see!

6. Adding Links:
   - Click the 🔗 link icon
   - Paste any URL
   - It becomes a clickable link in the chat

7. Private Messages:
   - See the online users list on the left?
   - Click any user's name
   - Type your private message in the popup
   - Only that person will see it! 🤫

---

 💾 Your Messages Are Saved!

Good news: All your conversations are automatically saved!

- Close your browser and come back later - your messages are still there
- Restart the app - chat history remains
- Your friend can see what was discussed before they joined

---

 🛠️ Managing the Application

 Checking if it's running:
```bash
docker ps
```
You should see `dockerchat-chat_app-1` in the list.

 Viewing logs (if something goes wrong):
```bash
docker logs dockerchat-chat_app-1
```

 Restarting the chat:
```bash
docker-compose restart
```

 Stopping the chat:
```bash
docker-compose down
```

 Starting it again:
```bash
docker-compose up -d
```

 Completely reset everything (deletes all messages):
```bash
docker-compose down -v
docker-compose up --build -d
```

---

 🎨 Features Overview

| Feature | Description |
|---------|-------------|
| 💬 Real-time Chat | Messages appear instantly for all users |
| 👥 Multi-user | Chat with unlimited friends simultaneously |
| 🏠 Multiple Channels | 4 topic-based chat rooms (general, random, tech, gaming) |
| 💾 Message History | All messages saved and loaded when you join |
| 😊 Emoji Support | 100+ emojis to express yourself |
| 🖼️ Rich Media | Share images, videos, and links |
| 🔒 Private Messages | Send DMs to specific users |
| 👀 Online Status | See who's currently in the chat |
| ⌨️ Typing Indicators | Know when someone is typing |
| 📱 Responsive Design | Works on desktop, tablet, and mobile |
| 🎨 Professional UI | Beautiful modern interface |

---

 ❓ Troubleshooting

 "Can't connect to the chat!"

For the host (you):
- ✅ Is Docker Desktop running? Check for the whale icon
- ✅ Did you run `docker-compose up -d`?
- ✅ Check: `docker ps` - is the container running?
- ✅ Try: `docker-compose restart`

For your friend (same network):
- ✅ Are they on the SAME Wi-Fi as you?
- ✅ Did you give them the correct IP address?
- ✅ Did you include `:5000` at the end? (e.g., `http://192.168.1.100:5000`)
- ✅ Check Windows Firewall - it might be blocking port 5000

For your friend (using ngrok):
- ✅ Is ngrok running on your computer?
- ✅ Did you share the HTTPS URL (not HTTP)?
- ✅ Is the URL still valid? (ngrok URLs change when you restart it)

 "Messages aren't sending!"

- ✅ Check browser console for errors (F12 → Console tab)
- ✅ Refresh the page
- ✅ Make sure your username was entered
- ✅ Check: `docker logs dockerchat-chat_app-1` for server errors

 "Can't see other users' messages!"

- ✅ Make sure you're in the same channel
- ✅ Refresh the page
- ✅ Check if you're both connected (look at online users list)

 "Docker isn't working!"

- ✅ Restart Docker Desktop
- ✅ Update Docker Desktop to the latest version
- ✅ On Windows: Make sure WSL 2 is installed and enabled

---

 🎓 For Developers

 Tech Stack
- Backend: Flask 2.3.3, Flask-SocketIO 5.3.4, SQLAlchemy
- Database: SQLite (persistent Docker volume)
- Real-time: Socket.IO v4 with eventlet
- Frontend: HTML5, CSS3, JavaScript (vanilla)
- Deployment: Docker + Docker Compose

 Project Structure
```
DockerChat/
├── app.py                  Flask backend + Socket.IO + Database
├── docker-compose.yml      Container orchestration
├── Dockerfile             Container image
├── requirements.txt       Python dependencies
├── README.md             This file
└── templates/
    └── index.html        Frontend UI
```

 Testing
```bash
python test_chat.py
```

See `TEST_RESULTS.txt` for complete test documentation.

---

 📞 Need Help?

If you're stuck:
1. Check the Troubleshooting section above
2. Look at the logs: `docker logs dockerchat-chat_app-1`
3. Make sure Docker is running
4. Try restarting: `docker-compose restart`

---

 🎉 Quick Reference Card

Share this with your friend:

```
╔════════════════════════════════════════════════════╗
║         HOW TO JOIN THE CHAT (FOR FRIENDS)        ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  1. Ask the host for the chat URL                 ║
║                                                    ║
║  2. Open it in your web browser                   ║
║     Chrome, Firefox, Safari, Edge - any works!    ║
║                                                    ║
║  3. Enter your username when asked                ║
║                                                    ║
║  4. Start chatting! 🎉                            ║
║                                                    ║
║  That's it - no downloads or sign-ups needed!     ║
║                                                    ║
╚════════════════════════════════════════════════════╝
```

---

 📜 License

Open source - use freely for personal or educational purposes!

---

Happy Chatting! 💬✨

Built with ❤️ using Flask, Socket.IO, and Docker

 For Multiple Users

To test with multiple users:

1. Open multiple browser tabs or windows
2. Each tab can join with a different username
3. All users will see messages in real-time
4. Users joining and leaving are announced to everyone

 Sharing with Others

 On Local Network

Other users on your local network can access the chat by:

1. Find your computer's IP address:
   - Windows: Run `ipconfig` and look for IPv4 Address
   - Mac/Linux: Run `ifconfig` or `ip addr`

2. Share this URL with others:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: `http://192.168.1.100:5000`

 Over the Internet

To make the chat accessible over the internet:

1. Using ngrok (easiest):
   ```bash
    Install ngrok from https://ngrok.com
   ngrok http 5000
   ```
   Share the generated HTTPS URL

2. Port forwarding: Configure your router to forward port 5000 to your computer

 Available Channels

- general - General discussion
- random - Random chat
- tech - Technology discussion  
- gaming - Gaming chat

 Data Persistence

All messages and user data are stored in a SQLite database that persists in a Docker volume (`chat_data`). This means:

- Messages remain even if you restart the containers
- Users can see message history when they return
- Chat history is preserved across sessions

 Stopping the Application

```bash
docker-compose down
```

To also remove the database volume:
```bash
docker-compose down -v
```

 Rebuilding After Changes

If you modify the code:

```bash
docker-compose up --build -d
```

 Viewing Logs

```bash
 View all logs
docker-compose logs

 Follow logs in real-time
docker-compose logs -f

 View app logs only
docker logs dockerchat-chat_app-1
```

 Tech Stack

- Backend: Flask, Flask-SocketIO, SQLAlchemy
- Database: SQLite
- Real-time: Socket.IO with eventlet
- Frontend: HTML5, CSS3, JavaScript
- Deployment: Docker, Docker Compose

 Troubleshooting

 Can't send messages?
- Check if the containers are running: `docker ps`
- View logs: `docker logs dockerchat-chat_app-1`
- Restart containers: `docker-compose restart`

 Lost connection?
- Refresh the browser
- Check if containers are still running
- Restart the application

 Database errors?
- Stop containers: `docker-compose down`
- Remove volume: `docker volume rm dockerchat_chat_data`
- Rebuild: `docker-compose up --build -d`

 Project Structure

```
DockerChat/
├── app.py                  Main Flask application
├── requirements.txt        Python dependencies
├── Dockerfile             Docker image definition
├── docker-compose.yml     Docker services configuration
├── README.md             This file
└── templates/
    └── index.html        Frontend UI
```

 Contributing

Feel free to fork this project and add your own features!

 License

Open source - use freely!
