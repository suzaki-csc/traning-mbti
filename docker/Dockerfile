# Python 3.12のベースイメージを使用
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新とPoetryのインストールに必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ヘルスチェック用にcurlを保持（本番環境では削除可能）

# Poetryをインストール
RUN curl -sSL https://install.python-poetry.org | python3 -

# Poetryのパスを環境変数に追加
ENV PATH="/root/.local/bin:$PATH"

# Poetryの設定（仮想環境を無効化 - Docker内では不要）
RUN poetry config virtualenvs.create false

# プロジェクトファイルをコピー
COPY pyproject.toml poetry.lock* ./

# README.mdもコピー（pyproject.tomlで参照されている場合）
COPY README.md* ./

# 依存関係をインストール（--no-rootでプロジェクト自体はインストールしない）
RUN poetry install --no-interaction --no-ansi --no-root

# アプリケーションのコードをコピー
# .dockerignoreで除外されたファイルはコピーされない
COPY app/ /app/app/
COPY pyproject.toml poetry.lock* README.md* ./

# 不要なディレクトリを削除（念のため）
# ビルド時にroutes/ディレクトリが存在する場合は削除
RUN find /app -type d -name "routes" -exec rm -rf {} + 2>/dev/null || true

# コピーされたファイルを確認（デバッグ用）
RUN echo "=== コピーされたファイル一覧 ===" && \
    find /app/app -maxdepth 2 -type f -name "*.py" | sort && \
    echo "=== ディレクトリ一覧 ===" && \
    ls -la /app/

# ポート5000を公開
EXPOSE 5000

# 環境変数の設定
ENV FLASK_APP=app.app:app
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONWARNINGS=ignore::RuntimeWarning

# アプリケーションを起動
CMD ["poetry", "run", "python", "-m", "app.app"]

