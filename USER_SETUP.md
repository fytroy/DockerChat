 📥 Instructions for Your User to Clone

Share these instructions with your User:

 For Your User (To Install on Their Laptop)

 Step 1: Install Prerequisites

1. Install Docker Desktop
   - Windows/Mac: https://www.docker.com/products/docker-desktop
   - Make sure it's running (whale icon visible)

2. Install Git (if not already installed)
   - Windows: https://git-scm.com/download/win
   - Mac: Run `git --version` (it will prompt to install if needed)
   - Linux: `sudo apt install git` or `sudo yum install git`

 Step 2: Clone the Project

```bash
 Open terminal and navigate to where you want the project
cd Desktop   or any folder you prefer

 Clone the repository (replace YOUR_USERNAME)
git clone https://github.com/YOUR_USERNAME/ProChat.git

 Enter the project folder
cd ProChat
```

 Step 3: Start the Application

```bash
 Start the chat application
docker-compose up --build -d

 Wait 2-3 minutes for first-time setup
```

 Step 4: Access the Chat

Open your browser and go to:
```
http://localhost:5000
```

Enter a username and start chatting!

---

 🌐 To Chat Together

 Option A: Same Network (Easiest)

Your User's Steps:
1. Find their IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Mac/Linux: `ifconfig` or `hostname -I`

2. Share with you: `http://THEIR_IP:5000`

3. You open that URL in your browser

Now you're both chatting! 🎉

 Option B: Different Locations (Using ngrok)

One of you runs:
```bash
 Install ngrok from https://ngrok.com
ngrok http 5000
```

Then share the HTTPS URL with the other person!

---

 🛠️ Managing the App

View logs:
```bash
docker logs dockerchat-chat_app-1
```

Stop the app:
```bash
docker-compose down
```

Restart the app:
```bash
docker-compose up -d
```

Update from GitHub (if you make changes):
```bash
git pull origin main
docker-compose up --build -d
```

---

 ✅ That's It!

Both of you now have the same chat app running, and you can connect to each other!

All your messages will be saved in the database, so you can continue conversations anytime.

Happy Chatting! 💬
