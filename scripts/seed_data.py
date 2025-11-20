#!/usr/bin/env python
"""
初期データ投入スクリプト

このスクリプトは、既存のデータベースに初期データを投入します。
既にデータが存在する場合は、重複を避けて追加します。
"""

import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.data.initial_data import init_data

def main():
    """メイン処理"""
    app = create_app()
    
    with app.app_context():
        print('初期データを投入中...')
        init_data()
        print('初期データの投入が完了しました。')

if __name__ == '__main__':
    main()

