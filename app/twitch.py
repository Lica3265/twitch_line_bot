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
def get_broadcaster_id(username):
    """ 使用 Twitch API 取得使用者的數字 ID """
    headers = {
        "Client-ID": os.getenv("TWITCH_CLIENT_ID"),
        "Authorization": f"Bearer {os.getenv('TWITCH_ACCESS_TOKEN')}",
    }
    response = requests.get(f"https://api.twitch.tv/helix/users?login={username}", headers=headers)
    data = response.json()
    return data["data"][0]["id"] if "data" in data and data["data"] else None
