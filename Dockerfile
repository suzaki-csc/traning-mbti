FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 環境変数の設定
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# システムパッケージの更新とビルドツールのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN pip install --upgrade pip && \
    pip install poetry

# Poetry設定（仮想環境を作成しない）
RUN poetry config virtualenvs.create false

# 依存関係ファイルをコピー
COPY pyproject.toml poetry.lock* ./

# 依存関係のインストール
RUN poetry install --no-interaction --no-ansi --no-root

# アプリケーションファイルをコピー
COPY . .

# ポートを公開
EXPOSE 5000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/', timeout=5)" || exit 1

# アプリケーションの起動
CMD ["python", "run.py"]

