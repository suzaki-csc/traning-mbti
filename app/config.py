import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """アプリケーション設定"""
    
    # Flask設定
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # データベース設定
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://mbti_user:mbti_password@localhost:3306/mbti_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # セッション設定
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 1800  # 30分
    
    # JSON設定（日本語文字化け対策）
    JSON_AS_ASCII = False


class DevelopmentConfig(Config):
    """開発環境設定"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """本番環境設定"""
    DEBUG = False
    FLASK_ENV = 'production'


# 設定の選択
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

