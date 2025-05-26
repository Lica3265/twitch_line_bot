FROM python:3.10

WORKDIR /app

# ✅ 使用 `.dockerignore`，避免複製不必要的文件
COPY . /app

# ✅ 安裝依賴並確保 Ngrok 正確設定
RUN apt update && apt install -y curl jq \
    && curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc \
    && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list \
    && apt update && apt install -y ngrok

# ✅ 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 確保 `start.sh` 具執行權限
RUN chmod +x start.sh

# ✅ 使用 ENTRYPOINT，允許自訂命令
ENTRYPOINT ["bash", "./start.sh"]