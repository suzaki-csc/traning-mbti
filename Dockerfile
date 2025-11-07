# パスワード強度チェッカー - Dockerfile
#
# Python 3.12ベースのFlaskアプリケーション用コンテナ

FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新と必要なツールのインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Poetry設定: 仮想環境を作成しない（コンテナ内では不要）
RUN poetry config virtualenvs.create false

# 依存関係ファイルをコピー
COPY pyproject.toml poetry.lock ./

# 依存関係をインストール（開発用パッケージは除外）
# Poetry 1.2以降では --without dev を使用
RUN poetry install --no-root --without dev --no-interaction --no-ansi

# アプリケーションファイルをコピー
COPY password_checker_app.py ./
COPY models.py ./
COPY templates ./templates
COPY static ./static

# ポート5000を公開
EXPOSE 5000

# 非rootユーザーを作成して切り替え（セキュリティ向上）
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# アプリケーションを起動
CMD ["python", "password_checker_app.py"]

