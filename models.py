"""
パスワード強度チェッカー - データベースモデル

パスワードチェックの履歴を保存するためのモデル定義
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import hashlib

db = SQLAlchemy()


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
    
    def to_dict(self):
        """
        モデルオブジェクトを辞書形式に変換
        
        Returns:
            dict: モデルのデータを含む辞書
        """
        return {
            'id': self.id,
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

