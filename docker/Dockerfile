# Flaskアプリケーション用Dockerfile

FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Poetryをインストール
RUN pip install --no-cache-dir poetry

# Poetryの設定（仮想環境を作成しない）
RUN poetry config virtualenvs.create false

# プロジェクトファイルをコピー
COPY pyproject.toml poetry.lock ./

# 依存関係をインストール（開発依存関係を除く、プロジェクト自体はインストールしない）
RUN poetry install --without dev --no-interaction --no-ansi --no-root

# アプリケーションコードをコピー
COPY . .

# 環境変数を設定
ENV FLASK_APP=wsgi.py
ENV PYTHONUNBUFFERED=1

# ポートを公開
EXPOSE 5000

# アプリケーションを起動
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "wsgi:app"]

