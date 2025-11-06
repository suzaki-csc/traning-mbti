FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新とインストール
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN pip install --no-cache-dir poetry

# プロジェクトファイルをコピー
COPY pyproject.toml poetry.lock ./

# 依存関係のインストール（仮想環境を作成せず、システム全体にインストール）
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# アプリケーションコードをコピー
COPY . .

# ポートを公開
EXPOSE 5000

# アプリケーションを起動
CMD ["python", "run.py"]

