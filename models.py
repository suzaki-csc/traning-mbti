"""
パスワード強度チェッカー - データベースモデル

パスワードチェックの履歴を保存するためのモデル定義
ユーザー認証とロール管理機能を含む
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import json

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    ユーザーテーブル
    
    認証情報とロール管理を行います。
    """
    
    __tablename__ = 'users'
    
    # 主キー
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 認証情報
    email = db.Column(db.String(255), unique=True, nullable=False, index=True, comment='メールアドレス')
    password_hash = db.Column(db.String(255), nullable=False, comment='パスワードハッシュ')
    
    # ユーザー情報
    username = db.Column(db.String(100), nullable=True, comment='ユーザー名')
    
    # ロール管理
    role = db.Column(db.String(20), nullable=False, default='user', comment='ロール（user/admin）')
    
    # アカウント状態
    is_active = db.Column(db.Boolean, default=True, comment='アカウント有効状態')
    
    # タイムスタンプ
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='作成日時')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新日時')
    last_login = db.Column(db.DateTime, nullable=True, comment='最終ログイン日時')
    
    # リレーション
    password_checks = db.relationship('PasswordCheck', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User id={self.id} email={self.email} role={self.role}>'
    
    def set_password(self, password):
        """
        パスワードをハッシュ化して保存
        
        Args:
            password (str): 平文パスワード
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        パスワードを検証
        
        Args:
            password (str): 検証するパスワード
            
        Returns:
            bool: パスワードが正しい場合True
        """
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """
        管理者かどうかを判定
        
        Returns:
            bool: 管理者の場合True
        """
        return self.role == 'admin'
    
    def to_dict(self, include_checks=False):
        """
        モデルオブジェクトを辞書形式に変換
        
        Args:
            include_checks (bool): チェック履歴を含めるか
            
        Returns:
            dict: ユーザー情報を含む辞書
        """
        data = {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'total_checks': self.password_checks.count()
        }
        
        if include_checks:
            data['recent_checks'] = [check.to_dict() for check in self.password_checks.order_by(PasswordCheck.created_at.desc()).limit(10)]
        
        return data


class PasswordCheck(db.Model):
    """
    パスワードチェック履歴テーブル
    
    パスワードの強度評価結果を保存します。
    パスワード自体は以下の2形式で保存：
    1. SHA-256ハッシュ値（復号不可）
    2. 先頭1文字 + マスク文字（例: "P***********"）
    """
    
    __tablename__ = 'password_checks'
    
    # 主キー
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # ユーザーID（外部キー）
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True, comment='ユーザーID（NULL可：未ログイン時）')
    
    # パスワード情報（2種類の形式）
    password_hash = db.Column(db.String(64), nullable=False, index=True, comment='SHA-256ハッシュ値')
    password_masked = db.Column(db.String(50), nullable=False, comment='先頭1文字+マスク表示')
    
    # パスワード評価結果
    score = db.Column(db.Integer, nullable=False, comment='スコア（0-100）')
    strength_level = db.Column(db.String(20), nullable=False, comment='強度レベル（very-weak, weak, fair, strong, very-strong）')
    entropy = db.Column(db.Float, nullable=False, comment='エントロピー（bits）')
    crack_time = db.Column(db.String(100), nullable=False, comment='総当たり攻撃想定時間')
    
    # 文字種情報
    has_lowercase = db.Column(db.Boolean, default=False, comment='小文字を含むか')
    has_uppercase = db.Column(db.Boolean, default=False, comment='大文字を含むか')
    has_digit = db.Column(db.Boolean, default=False, comment='数字を含むか')
    has_symbol = db.Column(db.Boolean, default=False, comment='記号を含むか')
    
    # パターン検出結果
    has_common_word = db.Column(db.Boolean, default=False, comment='よくある単語を含むか')
    has_repeating = db.Column(db.Boolean, default=False, comment='繰り返しパターンがあるか')
    has_sequential = db.Column(db.Boolean, default=False, comment='連番パターンがあるか')
    has_keyboard_pattern = db.Column(db.Boolean, default=False, comment='キーボード並びがあるか')
    
    # パスワードの長さ
    password_length = db.Column(db.Integer, nullable=False, comment='パスワード文字数')
    
    # タイムスタンプ
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='チェック実行日時')
    
    # インデックス
    __table_args__ = (
        db.Index('idx_user_id', 'user_id'),
        db.Index('idx_score', 'score'),
        db.Index('idx_strength_level', 'strength_level'),
        db.Index('idx_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f'<PasswordCheck id={self.id} level={self.strength_level} score={self.score}>'
    
    @staticmethod
    def hash_password(password):
        """
        パスワードをSHA-256でハッシュ化
        
        Args:
            password (str): 元のパスワード
            
        Returns:
            str: SHA-256ハッシュ値（64文字の16進数文字列）
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @staticmethod
    def mask_password(password):
        """
        パスワードをマスク表示形式に変換
        先頭1文字 + アスタリスク
        
        Args:
            password (str): 元のパスワード
            
        Returns:
            str: マスク表示されたパスワード（例: "P***********"）
        """
        if len(password) == 0:
            return ''
        elif len(password) == 1:
            return password
        else:
            return password[0] + '*' * (len(password) - 1)
    
    def to_dict(self, include_user=False):
        """
        モデルオブジェクトを辞書形式に変換
        
        Args:
            include_user (bool): ユーザー情報を含めるか
        
        Returns:
            dict: モデルのデータを含む辞書
        """
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'password_masked': self.password_masked,
            'score': self.score,
            'strength_level': self.strength_level,
            'entropy': self.entropy,
            'crack_time': self.crack_time,
            'has_lowercase': self.has_lowercase,
            'has_uppercase': self.has_uppercase,
            'has_digit': self.has_digit,
            'has_symbol': self.has_symbol,
            'has_common_word': self.has_common_word,
            'has_repeating': self.has_repeating,
            'has_sequential': self.has_sequential,
            'has_keyboard_pattern': self.has_keyboard_pattern,
            'password_length': self.password_length,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_user and self.user:
            data['user'] = {
                'id': self.user.id,
                'email': self.user.email,
                'username': self.user.username
            }
        
        return data


class PasswordPolicy(db.Model):
    """
    パスワード強度ポリシーテーブル
    
    組織のセキュリティポリシーに応じたパスワード要件を定義します。
    """
    
    __tablename__ = 'password_policies'
    
    # 主キー
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # ポリシー名
    name = db.Column(db.String(100), nullable=False, comment='ポリシー名')
    description = db.Column(db.Text, nullable=True, comment='説明')
    
    # アクティブフラグ（1つだけアクティブにできる）
    is_active = db.Column(db.Boolean, default=False, comment='アクティブ')
    
    # 長さ要件
    min_length = db.Column(db.Integer, default=8, comment='最小文字数')
    max_length = db.Column(db.Integer, default=128, comment='最大文字数')
    
    # 文字種要件
    require_lowercase = db.Column(db.Boolean, default=True, comment='小文字必須')
    require_uppercase = db.Column(db.Boolean, default=True, comment='大文字必須')
    require_digit = db.Column(db.Boolean, default=True, comment='数字必須')
    require_symbol = db.Column(db.Boolean, default=False, comment='記号必須')
    
    # 禁止パターン
    block_common_words = db.Column(db.Boolean, default=True, comment='よくある単語を禁止')
    block_repeating = db.Column(db.Boolean, default=True, comment='繰り返しパターンを禁止')
    block_sequential = db.Column(db.Boolean, default=True, comment='連番パターンを禁止')
    block_keyboard_patterns = db.Column(db.Boolean, default=True, comment='キーボード並びを禁止')
    
    # カスタム禁止単語（JSON形式）
    custom_blocked_words = db.Column(db.Text, nullable=True, comment='カスタム禁止単語（JSON配列）')
    
    # スコア閾値
    min_score_required = db.Column(db.Integer, default=50, comment='必要最低スコア')
    
    # タイムスタンプ
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='作成日時')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新日時')
    
    def __repr__(self):
        return f'<PasswordPolicy id={self.id} name={self.name} active={self.is_active}>'
    
    def get_custom_blocked_words(self):
        """
        カスタム禁止単語をリストで取得
        
        Returns:
            list: 禁止単語のリスト
        """
        if not self.custom_blocked_words:
            return []
        try:
            return json.loads(self.custom_blocked_words)
        except:
            return []
    
    def set_custom_blocked_words(self, words_list):
        """
        カスタム禁止単語を設定
        
        Args:
            words_list (list): 禁止単語のリスト
        """
        if isinstance(words_list, list):
            self.custom_blocked_words = json.dumps(words_list, ensure_ascii=False)
        else:
            self.custom_blocked_words = None
    
    def to_dict(self):
        """
        モデルオブジェクトを辞書形式に変換
        
        Returns:
            dict: ポリシー情報を含む辞書
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'min_length': self.min_length,
            'max_length': self.max_length,
            'require_lowercase': self.require_lowercase,
            'require_uppercase': self.require_uppercase,
            'require_digit': self.require_digit,
            'require_symbol': self.require_symbol,
            'block_common_words': self.block_common_words,
            'block_repeating': self.block_repeating,
            'block_sequential': self.block_sequential,
            'block_keyboard_patterns': self.block_keyboard_patterns,
            'custom_blocked_words': self.get_custom_blocked_words(),
            'min_score_required': self.min_score_required,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_active_policy():
        """
        アクティブなポリシーを取得
        
        Returns:
            PasswordPolicy: アクティブなポリシー、なければNone
        """
        return PasswordPolicy.query.filter_by(is_active=True).first()
    
    @staticmethod
    def get_default_policy():
        """
        デフォルトポリシーを取得または作成
        
        Returns:
            PasswordPolicy: デフォルトポリシー
        """
        default = PasswordPolicy.query.filter_by(name='デフォルト').first()
        if not default:
            default = PasswordPolicy(
                name='デフォルト',
                description='標準的なパスワード要件',
                is_active=True,
                min_length=8,
                max_length=128,
                require_lowercase=True,
                require_uppercase=True,
                require_digit=True,
                require_symbol=False,
                block_common_words=True,
                block_repeating=True,
                block_sequential=True,
                block_keyboard_patterns=True,
                min_score_required=50
            )
            db.session.add(default)
            try:
                db.session.commit()
            except:
                db.session.rollback()
        return default

