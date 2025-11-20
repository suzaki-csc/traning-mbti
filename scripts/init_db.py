#!/usr/bin/env python
"""
データベース初期化スクリプト

このスクリプトは、データベースのテーブルを作成し、初期データを投入します。
"""

import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.data.initial_data import init_data

def main():
    """メイン処理"""
    app = create_app()
    
    with app.app_context():
        print('データベースのテーブルを作成中...')
        db.create_all()
        print('テーブルの作成が完了しました。')
        
        print('初期データを投入中...')
        init_data()
        print('データベースの初期化が完了しました。')

if __name__ == '__main__':
    main()

