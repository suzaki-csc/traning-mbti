# MBTI風性格診断アプリケーション Dockerfile
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# システムパッケージの更新と必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Poetryをインストール
RUN pip install poetry==1.7.1

# Poetry設定（仮想環境を作成しない）
RUN poetry config virtualenvs.create false

# 依存関係ファイルをコピー
COPY pyproject.toml poetry.lock* ./

# 依存パッケージをインストール
RUN poetry install --no-interaction --no-ansi --no-root --only main

# アプリケーションのソースコードをコピー
COPY . .

# 非rootユーザーを作成
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# 非rootユーザーに切り替え
USER appuser

# ポート5000を公開
EXPOSE 5000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000', timeout=2)" || exit 1

# アプリケーションを起動
CMD ["python", "app.py"]

