#!/bin/bash
# クイズアプリ起動スクリプト（Docker Compose使用）

set -e

# スクリプトのディレクトリからプロジェクトルートに移動
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# DockerとDocker Composeがインストールされているか確認
if ! command -v docker &> /dev/null; then
    echo "エラー: Dockerがインストールされていません。"
    echo "Dockerのインストール方法: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "エラー: Docker Composeがインストールされていません。"
    echo "Docker Composeのインストール方法: https://docs.docker.com/compose/install/"
    exit 1
fi

# Docker Composeコマンドの確認（新バージョンは 'docker compose'、旧バージョンは 'docker-compose'）
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    DOCKER_COMPOSE_CMD="docker-compose"
fi

# データベースが存在しない場合は初期化（初回起動時）
# 注意: app.pyで自動的に初期化されるため、ここではスキップ
# 手動で初期化する場合は以下を実行:
# $DOCKER_COMPOSE_CMD exec web poetry run python -m app.data.init_questions

# アプリケーションを起動
echo "クイズアプリを起動します..."
echo "ブラウザで http://localhost:5000 にアクセスしてください。"
echo "停止するには Ctrl+C を押すか、別のターミナルで './stop.sh' を実行してください。"
echo ""

$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml up

