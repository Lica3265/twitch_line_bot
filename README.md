# Twitch Line Bot

## Overview
Twitch Line Bot is an automated notification system that alerts a LINE group when a specific Twitch streamer goes live. It integrates **Twitch's EventSub Webhook API** with **LINE Messaging API** to provide real-time updates.

## Features
- 🟣 **Live Stream Detection**: Monitors Twitch `stream.online` events.
- 💬 **LINE Notifications**: Sends messages to a designated LINE group.
- ⚙️ **Easy Deployment**: Packaged with Docker for quick setup.
- 🔧 **Customizable Alerts**: Supports message formatting and multi-streamer tracking.

## Installation & Setup

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/twitch-line-bot.git
cd twitch-line-bot

### **2. Install Dependencies**
pip install -r requirements.txt
### **3. Set Up Environment Variables**
TWITCH_CLIENT_ID=your_twitch_client_id
TWITCH_ACCESS_TOKEN=your_twitch_access_token
CALLBACK_URL=https://your-domain.com/webhook
LINE_ACCESS_TOKEN=your_line_channel_token
GROUP_ID=your_line_group_id
### **4. Run Webhook Server**
python webhook.py
### **5. Subscribe to Twitch EventSub**
python subscribe.py

### **6. Docker Deployment**
docker build -t twitch-line-bot .
docker run -d -p 8080:8080 --env-file .env twitch-line-bot

##Usage
Once deployed, the bot will automatically send LINE notifications when a Twitch streamer goes live.
Future Enhancements
- ✅ Support multiple streamers
- ✅ Add rich media notifications (stream thumbnail, title, etc.)
- ✅ Implement a web dashboard for managing subscriptions
##License
MIT License
