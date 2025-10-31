import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-learning'
    
    # MySQL設定
    MYSQL_HOST = os.environ.get('DB_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('DB_PORT', 3306))
    MYSQL_USER = os.environ.get('DB_USER', 'mbti_user')
    MYSQL_PASSWORD = os.environ.get('DB_PASSWORD', 'mbti_password')
    MYSQL_DB = os.environ.get('DB_NAME', 'mbti_db')
    
    # 管理者設定
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'

