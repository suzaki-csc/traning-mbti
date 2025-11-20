"""
アプリケーション設定ファイル
環境変数から設定を読み込む
"""
import os
from pathlib import Path

# ベースディレクトリ（プロジェクトルート）
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """基本設定クラス"""
    # セキュリティキー（本番環境では環境変数から取得）
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # データベース設定
    # 環境変数DATABASE_URLが設定されている場合はそれを使用
    # なければSQLiteを使用（ローカル開発用）
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{BASE_DIR / "quiz.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    
    # セッション設定
    SESSION_COOKIE_SECURE = False  # HTTPS使用時はTrueに
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # クイズ設定
    QUIZ_TIMER_SECONDS = 30  # 1問あたりの制限時間（秒）
    QUESTIONS_PER_QUIZ = 10  # 1回のクイズで出題する問題数
    MAX_QUESTIONS_PER_CATEGORY = 20  # カテゴリあたりの最大問題数

class DevelopmentConfig(Config):
    """開発環境用設定"""
    DEBUG = True

class ProductionConfig(Config):
    """本番環境用設定"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_SECURE = True

# 環境に応じた設定を選択
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

