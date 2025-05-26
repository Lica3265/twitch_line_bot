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
    """ 取消 Twitch 訂閱 (使用實況主名稱查詢 ID) """
    data = request.get_json()
    if not data or "broadcaster_username" not in data:
        return jsonify({"status": "error", "message": "缺少 Twitch 使用者名稱"}), 400

    broadcaster_username = data["broadcaster_username"]
    broadcaster_id = str(twitch.get_broadcaster_id(broadcaster_username))
    print(f"🔍 {broadcaster_username} 的 broadcaster_id: {broadcaster_id}")

    if not broadcaster_id:
        return jsonify({"status": "error", "message": f"無法獲取 {broadcaster_username} 的數字 ID"}), 400

    headers = {
        "Client-ID": config.TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {config.TWITCH_ACCESS_TOKEN}"
    }

    response = requests.get("https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers)
    try:
        subscriptions = response.json().get("data", [])
    except Exception as e:
        print(f"❌ 無法解析 Twitch 訂閱列表: {e}")
        return jsonify({"status": "error", "message": "無法獲取訂閱列表"}), 500

    for sub in subscriptions:
        if sub["type"] == "stream.online" and sub["condition"]["broadcaster_user_id"] == broadcaster_id:
            sub_id = sub["id"]

            delete_response = requests.delete(f"https://api.twitch.tv/helix/eventsub/subscriptions?id={sub_id}", headers=headers)
            if delete_response.status_code == 204:
                if broadcaster_username in subscribed_streamers:
                    subscribed_streamers.remove(broadcaster_username)
                print(f"✅ 成功取消訂閱 {broadcaster_username}")
                return jsonify({"status": "success", "message": f"已取消訂閱 {broadcaster_username}"}), 200
            else:
                print(f"❌ 取消訂閱失敗：{delete_response.status_code}, {delete_response.text}")
                return jsonify({"status": "error", "message": "取消訂閱失敗"}), 400

    return jsonify({"status": "error", "message": f"找不到 {broadcaster_username} 的訂閱，可能未訂閱"}), 400
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
    """ 訂閱 Twitch Webhook """
    data = request.json
    if not data or "broadcaster_username" not in data:
        return jsonify({"status": "error", "message": "缺少 Twitch 使用者名稱"}), 400

    broadcaster_username = data["broadcaster_username"]
    broadcaster_id = twitch.get_broadcaster_id(broadcaster_username)
    if not broadcaster_id:
        return jsonify({"status": "error", "message": f"無法獲取 {broadcaster_username} 的數字 ID"}), 400

    success = twitch.subscribe_twitch_webhook(broadcaster_id)
    if success:
        subscribed_streamers.append(broadcaster_username)
        return jsonify({"status": "success", "message": f"已訂閱 {broadcaster_username}"}), 200
    else:
        return jsonify({"status": "error", "message": "訂閱失敗"}), 400


if __name__ == "__main__":
    load_subscriptions()  # ✅ 啟動時自動查詢 Webhook 訂閱
    app.run(host="0.0.0.0", port=8080)