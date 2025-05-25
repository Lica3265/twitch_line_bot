from flask import Flask, request, jsonify
import twitch
import line

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # ✅ 回應 Twitch 的 `challenge`
    if "challenge" in data:
        return data["challenge"], 200  # Twitch 需要這個值才能啟用 Webhook

    # ✅ 處理 Twitch Webhook 事件
    if data["subscription"]["type"] == "stream.online":
        streamer_name = data["event"]["broadcaster_user_name"]
        stream_url = f"https://www.twitch.tv/{streamer_name}"
        line.send_line_message(streamer_name, stream_url)

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)