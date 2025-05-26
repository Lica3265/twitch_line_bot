#!/bin/bash

echo "🔄 啟動 Ngrok 隧道..."
start ngrok http 8080 > NUL 2>&1  # ✅ Windows 正確啟動 Ngrok

# ✅ 嘗試獲取 Ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*' | cut -d'"' -f4)

# ✅ 確保 URL 取得成功
if [[ -z "$NGROK_URL" ]]; then
    echo "❌ 無法取得 Ngrok URL，請檢查 Ngrok 是否正常運行！"
    exit 1
fi

echo "✅ Ngrok URL: $NGROK_URL"

# ✅ 設定環境變數，使 Webhook 訂閱時使用正確的 URL
export CALLBACK_URL="$NGROK_URL/webhook"
echo "✅ 訂閱用的 Webhook URL: $CALLBACK_URL"

# ✅ 獲取 Twitch 數字 ID
broadcaster_id=$(curl -s -X GET "https://api.twitch.tv/helix/users?login=使用者名稱" \
       -H "Client-ID: your_twitch_client_id" \
       -H "Authorization: Bearer your_twitch_access_token" | grep -o '"id":"[^"]*' | cut -d'"' -f4)

echo "✅ 獲取數字 ID: $broadcaster_id"

echo "🔄 啟動 Flask Webhook 伺服器..."
python app/main.py &

echo "🚀 Webhook 服務啟動完成！"