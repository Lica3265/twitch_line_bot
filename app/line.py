import requests
import config

def send_line_message(streamer_name, stream_url):
    headers = {
        "Authorization": f"Bearer {config.LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": config.GROUP_ID,
        "messages": [{"type": "text", "text": f"{streamer_name} 開台啦！快來看：{stream_url}"}]
    }

    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=data)
    return response.json()


def send_group_id():
    payload = {
        "to": "GROUP_ID",
        "messages": [{"type": "text", "text": "這是你的群組 ID"}]
    }

    headers = {
        "Authorization": f"Bearer {config.LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
    print(response.json())

