#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
既存のinit_data.pyからデータを抽出してJSONファイルに変換するスクリプト
"""
import json
import os
import sys

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from migrations.seeds.init_data import (
    init_security_questions,
    init_security_terms,
    init_it_basics_questions,
    init_it_basics_terms,
    init_programming_questions,
    init_programming_terms,
    init_project_management_questions,
    init_project_management_terms
)
from app import create_app, db
from app.models import Category, Question, Choice, TermReference

def extract_questions(category_name, output_file):
    """指定カテゴリの問題を抽出してJSONに保存"""
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        print(f"{category_name}カテゴリが見つかりません")
        return
    
    questions = Question.query.filter_by(category_id=category.id).order_by(Question.id).all()
    questions_data = []
    
    for question in questions:
        choices_data = []
        for choice in question.choices.order_by(Choice.display_order).all():
            choices_data.append({
                "choice_text": choice.choice_text,
                "is_correct": choice.is_correct,
                "display_order": choice.display_order
            })
        
        questions_data.append({
            "question_text": question.question_text,
            "explanation": question.explanation,
            "difficulty": question.difficulty,
            "choices": choices_data
        })
    
    # JSONファイルに保存
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ {category_name}: {len(questions_data)}問を {output_file} に保存")

def extract_terms(category_name, output_file):
    """指定カテゴリの用語を抽出してJSONに保存"""
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        print(f"{category_name}カテゴリが見つかりません")
        return
    
    terms = TermReference.query.filter_by(category_id=category.id).order_by(TermReference.display_order).all()
    terms_data = []
    
    for term in terms:
        terms_data.append({
            "term_name": term.term_name,
            "description": term.description,
            "url": term.url,
            "display_order": term.display_order
        })
    
    # JSONファイルに保存
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(terms_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ {category_name}用語: {len(terms_data)}件を {output_file} に保存")

def main():
    """メイン処理"""
    app = create_app('development')
    
    with app.app_context():
        # データベースが存在するか確認
        try:
            category_count = Category.query.count()
            if category_count == 0:
                print("データベースにデータがありません。先にinit_data.pyを実行してください。")
                return
        except Exception as e:
            print(f"データベースエラー: {e}")
            print("先にinit_data.pyを実行してデータベースを初期化してください。")
            return
        
        print("=" * 60)
        print("データ抽出開始")
        print("=" * 60)
        print()
        
        # 問題を抽出
        print("【問題の抽出】")
        extract_questions("セキュリティ", "data/questions/security.json")
        extract_questions("IT基礎", "data/questions/it_basics.json")
        extract_questions("プログラミング", "data/questions/programming.json")
        extract_questions("プロジェクトマネージメント", "data/questions/project_management.json")
        print()
        
        # 用語を抽出
        print("【用語の抽出】")
        extract_terms("セキュリティ", "data/terms/security.json")
        extract_terms("IT基礎", "data/terms/it_basics.json")
        extract_terms("プログラミング", "data/terms/programming.json")
        extract_terms("プロジェクトマネージメント", "data/terms/project_management.json")
        print()
        
        print("=" * 60)
        print("✓ データ抽出が完了しました！")
        print("=" * 60)

if __name__ == '__main__':
    main()


