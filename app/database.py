"""
データベースとモデルの定義
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """ユーザーモデル"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), default='user', nullable=False)  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # リレーション
    diagnosis_results = db.relationship('DiagnosisResult', backref='user', lazy=True)
    
    def set_password(self, password):
        """パスワードをハッシュ化"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """パスワードを検証"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """管理者かチェック"""
        return self.role == 'admin'


class DiagnosisResult(db.Model):
    """診断結果モデル"""
    __tablename__ = 'diagnosis_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    mbti_type = db.Column(db.String(4), nullable=False)
    score_ei = db.Column(db.Integer)
    score_sn = db.Column(db.Integer)
    score_tf = db.Column(db.Integer)
    score_jp = db.Column(db.Integer)
    answers = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_type_name(self):
        """タイプ名を取得"""
        from app.mbti import get_mbti_info
        return get_mbti_info(self.mbti_type)['name']

