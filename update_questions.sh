#!/bin/bash

# 色付けのための変数
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  問題データ更新スクリプト (JSON版)${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Dockerコンテナが起動しているか確認
echo -e "${YELLOW}Dockerコンテナの状態を確認中...${NC}"
if ! docker-compose ps web | grep -q "Up"; then
    echo -e "${RED}エラー: Dockerコンテナ (webサービス) が起動していません。${NC}"
    echo -e "${YELLOW}./start.sh を実行してコンテナを起動してください。${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Dockerコンテナは起動しています${NC}"
echo ""

# 確認メッセージ
echo -e "${YELLOW}⚠️  注意事項:${NC}"
echo -e "  - data/ディレクトリのJSONファイルから問題をロード"
echo -e "  - 既存の問題・選択肢・用語を削除して再作成"
echo -e "  - ${GREEN}クイズ履歴は保持されます${NC}"
echo -e "  - ${GREEN}ユーザーアカウント情報は保持されます${NC}"
echo ""
echo -e "${YELLOW}この操作を実行しますか？ (y/N): ${NC}"
read -r response

if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo -e "${RED}操作をキャンセルしました。${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  問題データの更新を開始します${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# 既存の問題データを削除して再投入
echo -e "${YELLOW}既存データを削除して、JSONから再投入中...${NC}"
docker-compose exec -T web python << 'PYTHON_SCRIPT'
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, '/app')

from app import create_app, db
from app.models import Question, Choice, TermReference, Category
import json

print("=" * 60)
print("問題データの更新を開始します...")
print("=" * 60)
print("")
print("※ 外部キー制約を一時的に無効化してデータを更新します")
print("※ クイズ履歴は保持されます")
print("")

app = create_app('development')

with app.app_context():
    categories = Category.query.all()
    
    # 外部キー制約を一時的に無効化
    db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 0"))
    
    # カテゴリごとに既存の問題・選択肢・用語を削除
    for category in categories:
        # 用語参考を削除
        terms_count = TermReference.query.filter_by(category_id=category.id).count()
        TermReference.query.filter_by(category_id=category.id).delete()
        
        # 選択肢と問題を削除
        questions = Question.query.filter_by(category_id=category.id).all()
        choices_count = 0
        for question in questions:
            choices_count += Choice.query.filter_by(question_id=question.id).count()
            Choice.query.filter_by(question_id=question.id).delete()
        
        questions_count = Question.query.filter_by(category_id=category.id).count()
        Question.query.filter_by(category_id=category.id).delete()
        
        print(f"✓ {category.name}カテゴリの既存データを削除:")
        print(f"  - 問題: {questions_count}件")
        print(f"  - 選択肢: {choices_count}件")
        print(f"  - 用語参考: {terms_count}件")
    
    # 外部キー制約を再有効化
    db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 1"))
    db.session.commit()
    print("")
    print("✓ 既存データの削除が完了しました")
    print("")
PYTHON_SCRIPT

if [ $? -ne 0 ]; then
    echo -e "${RED}エラー: 既存データの削除に失敗しました${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}JSONファイルから新しい問題データを投入中...${NC}"
docker-compose exec -T web python migrations/seeds/init_data.py

if [ $? -ne 0 ]; then
    echo -e "${RED}エラー: 問題データの投入に失敗しました${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}✓ 問題データの更新が完了しました！${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${GREEN}更新内容:${NC}"
echo -e "  ✓ ユーザーアカウント: ${GREEN}保持${NC}"
echo -e "  ✓ クイズ履歴: ${GREEN}保持${NC}"
echo -e "  ✓ 問題データ: ${GREEN}JSONファイルから読み込み${NC}"
echo ""
echo -e "${BLUE}データソース:${NC}"
echo -e "  📁 data/categories.json"
echo -e "  📁 data/questions/*.json"
echo -e "  📁 data/terms/*.json"
echo ""
echo -e "${YELLOW}⚠️  注意:${NC}"
echo -e "  過去のクイズ履歴は保持されていますが、問題内容が変わったため"
echo -e "  履歴の詳細表示で不整合が発生する可能性があります"
echo ""
echo -e "${GREEN}ブラウザで以下のURLにアクセスしてください:${NC}"
echo -e "  ${BLUE}http://localhost:5000${NC}"
echo ""
echo -e "${YELLOW}※ ブラウザのキャッシュをクリアしてください (Cmd + Shift + R)${NC}"
echo ""
