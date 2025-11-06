#!/bin/bash

# ログ表示スクリプト

echo "=========================================="
echo "  アプリケーションログ"
echo "=========================================="
echo ""
echo "📝 ログをリアルタイムで表示します（Ctrl+Cで終了）"
echo ""

# docker-compose.ymlの存在確認
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ エラー: docker-compose.ymlが見つかりません"
    echo "   プロジェクトのルートディレクトリで実行してください"
    exit 1
fi

# ログを表示
docker-compose logs -f --tail=100

