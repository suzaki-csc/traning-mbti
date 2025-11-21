#!/bin/bash

# クイズアプリケーション停止スクリプト
# Docker Composeを使用してアプリケーションとデータベースを停止します

set -e

echo "クイズアプリケーションを停止します..."

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

# Dockerの確認
if ! command -v docker &> /dev/null; then
    echo "エラー: Dockerがインストールされていません"
    exit 1
fi

# docker-composeコマンドの確認（docker compose または docker-compose）
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Docker Composeでサービスを停止
echo "Docker Composeでサービスを停止しています..."
$DOCKER_COMPOSE -f docker/docker-compose.dev.yml stop

echo "停止が完了しました。"

# コンテナを削除するか確認（オプション）
read -p "コンテナも削除しますか？ (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "コンテナを削除しています..."
    $DOCKER_COMPOSE -f docker/docker-compose.dev.yml down
    echo "コンテナの削除が完了しました。"
    echo "注意: データベースのデータは保持されています（ボリュームは削除されません）"
fi

