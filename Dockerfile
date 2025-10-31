FROM python:3.11-slim

WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係をインストール
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY app/ .

# ポート5000を公開
EXPOSE 5000

# Flaskアプリケーションを起動
CMD ["python", "app.py"]

