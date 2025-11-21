# Flaskアプリケーション用Dockerfile
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージのインストール
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN pip install poetry

# Poetryの設定（仮想環境を作成しない）
RUN poetry config virtualenvs.create false

# 依存関係ファイルをコピー
COPY pyproject.toml poetry.lock ./

# 依存関係のインストール
RUN poetry install --no-dev

# アプリケーションコードをコピー
COPY . .

# ポートを公開
EXPOSE 5000

# アプリケーションを起動
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:create_app()"]

