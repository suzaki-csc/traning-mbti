"""
アプリケーション設定ファイル
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """基本設定クラス"""
    
    # セキュリティ
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # データベース
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://mbti_user:mbti_password@localhost:3306/mbti_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True,
    }
    
    # セッション
    PERMANENT_SESSION_LIFETIME = 3600  # 1時間
    SESSION_COOKIE_SECURE = False  # 本番環境ではTrueに
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CSRF保護
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None


class DevelopmentConfig(Config):
    """開発環境設定"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """本番環境設定"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """テスト環境設定"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# 環境に応じた設定を選択
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

