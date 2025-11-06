#!/bin/bash

# クイズアプリケーション停止スクリプト

echo "=========================================="
echo "  クイズアプリケーション停止"
echo "=========================================="
echo ""

# docker-compose.ymlの存在確認
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ エラー: docker-compose.ymlが見つかりません"
    echo "   プロジェクトのルートディレクトリで実行してください"
    exit 1
fi

# コンテナを停止
echo "🛑 Dockerコンテナを停止しています..."
docker-compose down

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ アプリケーションを停止しました"
    echo ""
else
    echo ""
    echo "❌ エラー: アプリケーションの停止に失敗しました"
    exit 1
fi

