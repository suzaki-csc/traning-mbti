#!/usr/bin/env python
"""
init_data.pyからデータを抽出してJSONファイルに変換するスクリプト
"""
import json
import re
import sys

def extract_questions_data(file_path, function_name):
    """指定された関数からquestions_dataを抽出"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 関数の開始位置を見つける
    pattern = rf'def {function_name}\(\):.*?questions_data = \[(.*?)\]'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"Warning: {function_name} not found")
        return []
    
    questions_str = '[' + match.group(1) + ']'
    
    # Pythonコードとして評価（安全性のため実際の環境では注意が必要）
    try:
        questions_data = eval(questions_str)
        return questions_data
    except Exception as e:
        print(f"Error parsing {function_name}: {e}")
        return []

def extract_terms_data(file_path, function_name):
    """指定された関数からtermsを抽出"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 関数の開始位置を見つける
    pattern = rf'def {function_name}\(\):.*?terms = \[(.*?)\]'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"Warning: {function_name} not found")
        return []
    
    terms_str = '[' + match.group(1) + ']'
    
    try:
        terms_data = eval(terms_str)
        return terms_data
    except Exception as e:
        print(f"Error parsing {function_name}: {e}")
        return []

def main():
    init_file = 'migrations/seeds/init_data.py'
    
    # セキュリティ
    print("Extracting security questions...")
    security_questions = extract_questions_data(init_file, 'init_security_questions')
    with open('data/security_questions.json', 'w', encoding='utf-8') as f:
        json.dump(security_questions, f, ensure_ascii=False, indent=2)
    print(f"✓ security_questions.json: {len(security_questions)} questions")
    
    print("Extracting security terms...")
    security_terms = extract_terms_data(init_file, 'init_security_terms')
    with open('data/security_terms.json', 'w', encoding='utf-8') as f:
        json.dump(security_terms, f, ensure_ascii=False, indent=2)
    print(f"✓ security_terms.json: {len(security_terms)} terms")
    
    # IT基礎
    print("Extracting IT basics questions...")
    it_questions = extract_questions_data(init_file, 'init_it_basics_questions')
    with open('data/it_basics_questions.json', 'w', encoding='utf-8') as f:
        json.dump(it_questions, f, ensure_ascii=False, indent=2)
    print(f"✓ it_basics_questions.json: {len(it_questions)} questions")
    
    print("Extracting IT basics terms...")
    it_terms = extract_terms_data(init_file, 'init_it_basics_terms')
    with open('data/it_basics_terms.json', 'w', encoding='utf-8') as f:
        json.dump(it_terms, f, ensure_ascii=False, indent=2)
    print(f"✓ it_basics_terms.json: {len(it_terms)} terms")
    
    # プログラミング
    print("Extracting programming questions...")
    prog_questions = extract_questions_data(init_file, 'init_programming_questions')
    with open('data/programming_questions.json', 'w', encoding='utf-8') as f:
        json.dump(prog_questions, f, ensure_ascii=False, indent=2)
    print(f"✓ programming_questions.json: {len(prog_questions)} questions")
    
    print("Extracting programming terms...")
    prog_terms = extract_terms_data(init_file, 'init_programming_terms')
    with open('data/programming_terms.json', 'w', encoding='utf-8') as f:
        json.dump(prog_terms, f, ensure_ascii=False, indent=2)
    print(f"✓ programming_terms.json: {len(prog_terms)} terms")
    
    # プロジェクトマネージメント
    print("Extracting project management questions...")
    pm_questions = extract_questions_data(init_file, 'init_project_management_questions')
    with open('data/project_management_questions.json', 'w', encoding='utf-8') as f:
        json.dump(pm_questions, f, ensure_ascii=False, indent=2)
    print(f"✓ project_management_questions.json: {len(pm_questions)} questions")
    
    print("Extracting project management terms...")
    pm_terms = extract_terms_data(init_file, 'init_project_management_terms')
    with open('data/project_management_terms.json', 'w', encoding='utf-8') as f:
        json.dump(pm_terms, f, ensure_ascii=False, indent=2)
    print(f"✓ project_management_terms.json: {len(pm_terms)} terms")
    
    print("\n✅ All data extracted successfully!")

if __name__ == '__main__':
    main()

