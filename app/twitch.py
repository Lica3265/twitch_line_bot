import requests
import os

CALLBACK_URL = os.getenv("CALLBACK_URL")  # 取得 Ngrok URL

def subscribe_twitch_webhook(broadcaster_id):
    headers = {
        "Client-ID": os.getenv("TWITCH_CLIENT_ID"),
        "Authorization": f"Bearer {os.getenv('TWITCH_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "stream.online",
        "version": "1",
        "condition": {"broadcaster_user_id": broadcaster_id},
        "transport": {"method": "webhook", "callback": CALLBACK_URL, "secret": "your_secret"}
    }
    response = requests.post("https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers, json=data)
    return response.json()

print(subscribe_twitch_webhook("實況主ID"))