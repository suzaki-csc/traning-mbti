#!/bin/bash
# クイズアプリケーション停止用ラッパーシェル
#
# このスクリプトは、Docker Composeで起動したアプリケーションを停止します。
#
# 使用方法:
#   ./scripts/stop.sh
#
# オプション:
#   -v, --volumes    データベースのボリュームも削除します（すべてのデータが削除されます）

set -e

# プロジェクトルートディレクトリに移動
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "クイズアプリケーション 停止スクリプト"
echo "=========================================="
echo ""

# オプションの解析
REMOVE_VOLUMES=false
for arg in "$@"; do
    case $arg in
        -v|--volumes)
            REMOVE_VOLUMES=true
            shift
            ;;
        *)
            ;;
    esac
done

# Docker Composeを使用しているか確認
if [ ! -d "docker" ]; then
    echo "❌ エラー: dockerディレクトリが見つかりません。"
    exit 1
fi

# Dockerの確認
if ! command -v docker &> /dev/null; then
    echo "❌ エラー: Dockerがインストールされていません。"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ エラー: Docker Composeがインストールされていません。"
    exit 1
fi

cd docker

if [ "$REMOVE_VOLUMES" = true ]; then
    echo "⚠️  警告: データベースのボリュームも削除します。"
    echo "   すべてのデータが失われます。"
    echo ""
    echo "続行しますか？ (y/n)"
    read -r response
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        echo "🛑 コンテナとボリュームを停止・削除します..."
        docker-compose down -v
        echo "✅ コンテナとボリュームを削除しました。"
    else
        echo "❌ 操作をキャンセルしました。"
        exit 0
    fi
else
    echo "🛑 コンテナを停止します..."
    docker-compose down
    echo "✅ コンテナを停止しました。"
    echo ""
    echo "💡 データベースのボリュームも削除する場合は、以下を実行してください:"
    echo "   ./scripts/stop.sh --volumes"
fi

