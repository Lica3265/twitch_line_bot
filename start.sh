#!/bin/bash

echo "🔄 啟動 Flask Webhook 伺服器..."
python main.py &

echo "🔄 啟動 Ngrok 隧道..."
ngrok http 8080 > /dev/null &
sleep 3  # ✅ 多等一秒，確保 Ngrok 連線成功

# ✅ 取得 Ngrok 產生的 URL（並檢查是否成功）
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

# ✅ 檢查 URL 是否有效
if [[ -z "$NGROK_URL" ]]; then
    echo "❌ 無法取得 Ngrok URL，請檢查 Ngrok 是否正常運行！"
    exit 1
fi

echo "✅ Ngrok URL: $NGROK_URL"

# ✅ 設定環境變數，讓 Webhook 訂閱時使用正確的 URL
export CALLBACK_URL="$NGROK_URL/webhook"

echo "🔄 訂閱 Twitch Webhook..."
python twitch.py

echo "🚀 Webhook 服務啟動完成！"