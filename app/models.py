from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """ユーザーモデル"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # リレーション
    diagnoses = db.relationship(
        'DiagnosisSession',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def set_password(self, password):
        """パスワードをハッシュ化して保存"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """パスワードを検証"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """管理者権限チェック"""
        return self.role == 'admin'
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<User {self.email} - {self.role}>'


class DiagnosisSession(db.Model):
    """診断セッションモデル"""
    
    __tablename__ = 'diagnosis_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 認証ユーザーの場合のみ
    mbti_type = db.Column(db.String(4), nullable=False)
    scores_json = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)
    
    # リレーション
    answers = db.relationship(
        'DiagnosisAnswer',
        backref='session',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'mbti_type': self.mbti_type,
            'scores': self.scores_json,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'ip_address': self.ip_address,
            'answers': [answer.to_dict() for answer in self.answers]
        }
    
    def __repr__(self):
        return f'<DiagnosisSession {self.session_id} - {self.mbti_type}>'


class DiagnosisAnswer(db.Model):
    """診断回答モデル"""
    
    __tablename__ = 'diagnosis_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.Integer,
        db.ForeignKey('diagnosis_sessions.id'),
        nullable=False
    )
    question_id = db.Column(db.Integer, nullable=False)
    axis = db.Column(db.String(1), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'question_id': self.question_id,
            'axis': self.axis,
            'score': self.score,
            'answer_text': self.answer_text,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<DiagnosisAnswer Q{self.question_id} - {self.axis}>'

