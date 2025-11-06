"""
データベース接続待機スクリプト

MySQLデータベースが準備できるまで待機します。
"""
import time
import sys
from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'mysql+pymysql://quizuser:quizpass@db:3306/quiz_app')
MAX_RETRIES = 30
RETRY_INTERVAL = 2

def wait_for_db():
    """データベースが利用可能になるまで待機"""
    print("データベース接続を待機中...")
    
    for attempt in range(MAX_RETRIES):
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("✓ データベース接続成功！")
            return True
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print(f"接続試行 {attempt + 1}/{MAX_RETRIES} 失敗。{RETRY_INTERVAL}秒後に再試行... ({str(e)[:50]})")
                time.sleep(RETRY_INTERVAL)
            else:
                print(f"✗ データベース接続失敗: {e}")
                return False
    
    return False

if __name__ == '__main__':
    if not wait_for_db():
        sys.exit(1)
    sys.exit(0)

