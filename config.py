"""
アプリケーション設定ファイル
"""
import os
from datetime import timedelta


class Config:
    """基本設定"""
    # セキュリティ
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'dev-secret-key-change-in-production'

    # セッション設定
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # データベース設定（Phase 2で使用）
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///mbti.db'  # 開発用はSQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # アプリケーション設定
    MAX_QUESTIONS = 12


class DevelopmentConfig(Config):
    """開発環境設定"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """本番環境設定"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """テスト環境設定"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# 設定の選択
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
