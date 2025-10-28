"""
データベースモデル定義
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """ユーザーモデル"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('user', 'admin'), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # リレーション
    test_results = db.relationship('TestResult', backref='user', lazy='dynamic', 
                                   cascade='all, delete-orphan')
    
    def set_password(self, password):
        """パスワードをハッシュ化して保存"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """パスワードの検証"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """管理者かどうかを判定"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'


class TestResult(db.Model):
    """診断結果モデル"""
    __tablename__ = 'test_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    mbti_type = db.Column(db.String(4), nullable=False, index=True)
    
    # 各軸のスコア
    e_score = db.Column(db.Integer, nullable=False, default=0)
    i_score = db.Column(db.Integer, nullable=False, default=0)
    s_score = db.Column(db.Integer, nullable=False, default=0)
    n_score = db.Column(db.Integer, nullable=False, default=0)
    t_score = db.Column(db.Integer, nullable=False, default=0)
    f_score = db.Column(db.Integer, nullable=False, default=0)
    j_score = db.Column(db.Integer, nullable=False, default=0)
    p_score = db.Column(db.Integer, nullable=False, default=0)
    
    # 回答データ（JSON形式）
    answers = db.Column(db.Text, nullable=False)
    
    taken_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def set_answers(self, answers_list):
        """回答データをJSON文字列として保存"""
        self.answers = json.dumps(answers_list, ensure_ascii=False)
    
    def get_answers(self):
        """JSON文字列から回答データを取得"""
        return json.loads(self.answers)
    
    def get_scores_dict(self):
        """スコアを辞書形式で取得"""
        return {
            'E': self.e_score,
            'I': self.i_score,
            'S': self.s_score,
            'N': self.n_score,
            'T': self.t_score,
            'F': self.f_score,
            'J': self.j_score,
            'P': self.p_score
        }
    
    def __repr__(self):
        return f'<TestResult {self.mbti_type} - User {self.user_id}>'

