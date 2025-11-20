#!/bin/bash
# Dockerコンテナを完全にクリーンアップして再ビルドするスクリプト

set -e

# スクリプトのディレクトリからプロジェクトルートに移動
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Docker Composeコマンドの確認
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    DOCKER_COMPOSE_CMD="docker-compose"
fi

echo "=========================================="
echo "Dockerコンテナを完全にクリーンアップします"
echo "=========================================="
echo ""

# コンテナを停止して削除
echo "1. コンテナを停止・削除..."
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml down -v

# イメージを削除
echo "2. イメージを削除..."
docker rmi quiz-app-web 2>/dev/null || echo "   quiz-app-webイメージが見つかりません（スキップ）"
docker rmi mysql:8.0 2>/dev/null || echo "   mysqlイメージが見つかりません（スキップ）"

# ビルドキャッシュをクリア
echo "3. ビルドキャッシュをクリア..."
docker builder prune -f

# 再ビルド
echo "4. イメージを再ビルド..."
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml build --no-cache --pull

echo ""
echo "=========================================="
echo "再ビルドが完了しました。起動します..."
echo "=========================================="
echo "MySQLの初期化には30秒程度かかります。"
echo ""

# 起動
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml up

