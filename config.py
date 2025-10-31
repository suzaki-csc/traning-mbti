import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-learning'
    
    # SQLAlchemy設定
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_USER = os.environ.get('DB_USER', 'mbti_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mbti_password')
    DB_NAME = os.environ.get('DB_NAME', 'mbti_db')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 管理者設定
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'

