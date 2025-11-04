FROM python:3.12-slim

WORKDIR /app

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN pip install poetry

# 依存関係ファイルのコピー
COPY pyproject.toml poetry.lock ./

# 依存関係のインストール（仮想環境を作らない）
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# アプリケーションコードのコピー
COPY . .

# ポート公開
EXPOSE 5000

# 起動コマンド
CMD ["flask", "run", "--host=0.0.0.0"]

