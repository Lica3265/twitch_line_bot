FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# 安裝 Ngrok
RUN apt update && apt install -y curl && \
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt update && apt install -y ngrok

CMD ["./start.sh"]