"""
アプリケーション設定ファイル

環境変数や設定値を管理します。
"""
import os
from datetime import timedelta


class Config:
    """基本設定クラス"""
    
    # Flaskの基本設定
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'
    
    # データベース設定
    # 開発時はSQLite、本番時はMySQLを使用
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///quiz_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # SQLのログを表示（開発時はTrue推奨）
    
    # セッション設定
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CSRF保護
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # トークンの有効期限なし
    
    # クイズアプリ固有の設定
    QUIZ_DEFAULT_QUESTIONS = 10  # デフォルトの出題数
    QUIZ_DEFAULT_TIMER_SECONDS = 30  # デフォルトのタイマー秒数
    QUIZ_MIN_TIMER_SECONDS = 15  # 最小タイマー秒数
    QUIZ_MAX_TIMER_SECONDS = 60  # 最大タイマー秒数
    
    # ページネーション
    ITEMS_PER_PAGE = 20
    
    # ログ設定
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'


class DevelopmentConfig(Config):
    """開発環境設定"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """本番環境設定"""
    DEBUG = False
    
    # 本番環境では必ず環境変数から取得
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # セキュリティ強化
    SESSION_COOKIE_SECURE = True  # HTTPS必須
    
    # MySQL設定例
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://user:password@localhost:3306/quiz_app'


class TestingConfig(Config):
    """テスト環境設定"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# 環境に応じた設定の選択
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

