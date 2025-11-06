#!/bin/bash

# データベース初期化スクリプト

echo "=========================================="
echo "  データベース初期化"
echo "=========================================="
echo ""

# docker-compose.ymlの存在確認
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ エラー: docker-compose.ymlが見つかりません"
    echo "   プロジェクトのルートディレクトリで実行してください"
    exit 1
fi

# コンテナが起動しているか確認
if ! docker-compose ps | grep -q "Up"; then
    echo "⚠️  警告: コンテナが起動していません"
    read -p "コンテナを起動しますか？ (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./start.sh
        echo ""
        echo "⏳ データベースの起動を待っています（10秒）..."
        sleep 10
    else
        echo "❌ 中止しました"
        exit 1
    fi
fi

# 確認メッセージ
echo "⚠️  警告: この操作は既存のデータをすべて削除します"
read -p "データベースを初期化してもよろしいですか？ (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 中止しました"
    exit 0
fi

echo ""
echo "🔄 データベースを初期化しています..."

# Webコンテナ内でPythonスクリプトを実行
docker-compose exec -T web python migrations/seeds/init_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ データベースの初期化が完了しました！"
    echo ""
    echo "📊 初期データ:"
    echo "   - カテゴリ: セキュリティ、IT基礎、プログラミング"
    echo "   - 問題数: 各カテゴリ10問ずつ"
    echo "   - 用語参考: セキュリティ関連用語"
    echo ""
else
    echo ""
    echo "❌ エラー: データベースの初期化に失敗しました"
    echo "   詳細を確認: docker-compose logs web"
    exit 1
fi

