from flask import Flask, request, jsonify, render_template
import requests
import config
import twitch
import line

app = Flask(__name__)

# ✅ 已訂閱的 Twitch 實況主清單（存放頻道名稱）
subscribed_streamers = []

# ✅ 取得 Twitch 頻道帳號名稱
def get_streamer_name(broadcaster_id):
    headers = {
        "Client-ID": config.TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {config.TWITCH_ACCESS_TOKEN}"
    }

    response = requests.get(f"https://api.twitch.tv/helix/users?id={broadcaster_id}", headers=headers)
    data = response.json()

    if "data" in data and len(data["data"]) > 0:
        return data["data"][0]["login"]  # ✅ 取得 Twitch 頻道名稱

    return None

@app.route("/unsubscribe", methods=["POST"])
def unsubscribe_streamer():
    data = request.form
    broadcaster_id = data.get("broadcaster_id")

    if broadcaster_id:
        headers = {
            "Client-ID": config.TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {config.TWITCH_ACCESS_TOKEN}"
        }

        # ✅ 先查詢目前的 Webhook 訂閱 ID
        response = requests.get("https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers)
        subscriptions = response.json().get("data", [])

        # ✅ 找到對應的 `broadcaster_id`
        for sub in subscriptions:
            if sub["type"] == "stream.online" and sub["condition"]["broadcaster_user_id"] == broadcaster_id:
                sub_id = sub["id"]

                # ✅ 取消 Webhook 訂閱
                delete_response = requests.delete(f"https://api.twitch.tv/helix/eventsub/subscriptions?id={sub_id}", headers=headers)
                
                if delete_response.status_code == 204:  # Twitch 成功刪除訂閱
                    subscribed_streamers.remove(broadcaster_id)  # ✅ 從本地清單移除
                    return jsonify({"status": "success", "message": f"已取消訂閱 {broadcaster_id}"}), 200

    return jsonify({"status": "error", "message": "取消訂閱失敗"}), 400

# ✅ 啟動 Flask 時，自動載入已訂閱的 Twitch 頻道
def load_subscriptions():
    headers = {
        "Client-ID": config.TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {config.TWITCH_ACCESS_TOKEN}"
    }

    response = requests.get("https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers)
    data = response.json()

    if "data" in data:
        for sub in data["data"]:
            if sub["type"] == "stream.online":
                channel_name = get_streamer_name(sub["condition"]["broadcaster_user_id"])
                if channel_name:
                    subscribed_streamers.append(channel_name)  # ✅ 儲存頻道名稱

    print(f"已載入 {len(subscribed_streamers)} 位已訂閱的實況主")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # ✅ 回應 Twitch 的 `challenge`
    if "challenge" in data:
        return data["challenge"], 200

    # ✅ 處理 Twitch Webhook 事件
    if data["subscription"]["type"] == "stream.online":
        streamer_name = data["event"]["broadcaster_user_name"]
        stream_url = f"https://www.twitch.tv/{streamer_name}"
        line.send_line_message(streamer_name, stream_url)

    return jsonify({"status": "received"}), 200

@app.route("/", methods=["GET"])
def show_subscriptions():
    return render_template("subscriptions.html", streamers=subscribed_streamers)

@app.route("/subscribe", methods=["POST"])
def subscribe_streamer():
    data = request.json
    broadcaster_id = data.get("broadcaster_id")

    if broadcaster_id:
        response = twitch.subscribe_twitch_webhook(broadcaster_id)
        if response.get("data"):
            channel_name = get_streamer_name(broadcaster_id)
            if channel_name:
                subscribed_streamers.append(channel_name)  # ✅ 儲存新的訂閱
                return jsonify({"status": "success", "message": f"已訂閱 {channel_name}"}), 200

    return jsonify({"status": "error", "message": "訂閱失敗"}), 400

if __name__ == "__main__":
    load_subscriptions()  # ✅ 啟動時自動查詢 Webhook 訂閱
    app.run(host="0.0.0.0", port=8080)