import os

class Config:
    """アプリケーション設定"""
    
    # Flask設定
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-learning'
    DEBUG = True
    
    # データベース設定
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'mbti_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mbti_pass')
    DB_NAME = os.environ.get('DB_NAME', 'mbti_db')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    
    # ページネーション設定
    ITEMS_PER_PAGE = 10

