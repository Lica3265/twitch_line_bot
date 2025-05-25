#!/bin/bash

# 啟動 Flask Webhook 伺服器
python main.py &

# 啟動 Ngrok 隧道
ngrok http 8080 > /dev/null &
sleep 2

# 取得 Ngrok 產生的 URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

echo "Ngrok URL: $NGROK_URL"

# 設定環境變數，讓 Webhook 訂閱時使用正確的 URL
export CALLBACK_URL=$NGROK_URL/webhook

# 訂閱 Twitch Webhook
python twitch.py