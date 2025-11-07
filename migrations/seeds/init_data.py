#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
データベース初期データ投入スクリプト（JSON読み込み版）
"""
import sys
import os
import json

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app, db
from app.models import Category, Question, Choice, TermReference, User
from datetime import datetime


def load_json(file_path):
    """JSONファイルを読み込む"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def init_categories():
    """カテゴリの初期データ"""
    categories_data = load_json('data/categories.json')
    
    created_count = 0
    for cat_data in categories_data:
        category = Category.query.filter_by(name=cat_data['name']).first()
        if not category:
            category = Category(**cat_data)
            db.session.add(category)
            created_count += 1
    
    db.session.commit()
    
    total_categories = Category.query.count()
    print(f"カテゴリ: {total_categories}件 (新規作成: {created_count}件)")


def init_questions(category_name, json_file):
    """指定カテゴリの問題を投入"""
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        print(f"  ⚠️  {category_name}カテゴリが見つかりません")
        return
    
    questions_data = load_json(json_file)
    created_count = 0
    
    for q_data in questions_data:
        # 既存チェック
        existing = Question.query.filter_by(
            category_id=category.id,
            question_text=q_data['question_text']
        ).first()
        
        if not existing:
            choices_data = q_data.pop('choices')
            question = Question(category_id=category.id, **q_data)
            db.session.add(question)
            db.session.flush()  # IDを取得するため
            
            for choice_data in choices_data:
                choice = Choice(question_id=question.id, **choice_data)
                db.session.add(choice)
            
            created_count += 1
    
    db.session.commit()
    
    total_questions = Question.query.filter_by(category_id=category.id).count()
    print(f"  ✓ {category_name}: {total_questions}問 (新規作成: {created_count}問)")


def init_terms(category_name, json_file):
    """指定カテゴリの用語参考を投入"""
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        print(f"  ⚠️  {category_name}カテゴリが見つかりません")
        return
    
    terms_data = load_json(json_file)
    created_count = 0
    
    for term_data in terms_data:
        existing = TermReference.query.filter_by(
            term_name=term_data['term_name'],
            category_id=category.id
        ).first()
        
        if not existing:
            term = TermReference(category_id=category.id, **term_data)
            db.session.add(term)
            created_count += 1
    
    db.session.commit()
    
    total_terms = TermReference.query.filter_by(category_id=category.id).count()
    print(f"  ✓ {category_name}用語: {total_terms}件 (新規作成: {created_count}件)")


def init_users():
    """ユーザーの初期データ（デフォルト管理者）"""
    admin_email = 'admin@example.com'
    admin_password = 'admin123'
    
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            role='admin',
            is_active=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print(f"✓ デフォルト管理者を作成: {admin_email} / {admin_password}")
    else:
        print("✓ デフォルト管理者は既に存在します")


def main():
    """メイン処理"""
    app = create_app('development')
    
    with app.app_context():
        # データベーステーブルを作成
        db.create_all()
        print("=" * 60)
        print("データベース初期化スクリプト")
        print("=" * 60)
        print()
        
        # ユーザー初期化
        print("【ユーザー】")
        init_users()
        print()
        
        # カテゴリ初期化
        print("【カテゴリ】")
        init_categories()
        print()
        
        # 問題初期化
        print("【問題】")
        init_questions("セキュリティ", "data/questions/security.json")
        init_questions("IT基礎", "data/questions/it_basics.json")
        init_questions("プログラミング", "data/questions/programming.json")
        init_questions("プロジェクトマネージメント", "data/questions/project_management.json")
        print()
        
        # 用語初期化
        print("【用語参考】")
        init_terms("セキュリティ", "data/terms/security.json")
        init_terms("IT基礎", "data/terms/it_basics.json")
        init_terms("プログラミング", "data/terms/programming.json")
        init_terms("プロジェクトマネージメント", "data/terms/project_management.json")
        print()
        
        print("=" * 60)
        print("✓ 初期データの投入が完了しました！")
        print("=" * 60)
        print()
        print("アプリケーション起動: ./start.sh")


if __name__ == '__main__':
    main()
