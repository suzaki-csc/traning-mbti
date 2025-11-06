"""
データベースモデル定義

アプリケーションで使用するデータモデルを定義します。
"""
from datetime import datetime
from flask_login import UserMixin
import bcrypt
from app import db


class User(UserMixin, db.Model):
    """ユーザーテーブル"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'user' or 'admin'
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)
    
    # リレーションシップ
    quiz_sessions = db.relationship('QuizSession', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """パスワードをハッシュ化して保存"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """パスワードを検証"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def is_admin(self):
        """管理者かどうかを判定"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'quiz_count': self.quiz_sessions.count()
        }


class Category(db.Model):
    """カテゴリテーブル"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    display_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーションシップ
    questions = db.relationship('Question', backref='category', lazy='dynamic', cascade='all, delete-orphan')
    quiz_sessions = db.relationship('QuizSession', backref='category', lazy='dynamic')
    term_references = db.relationship('TermReference', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'display_order': self.display_order,
            'question_count': self.questions.filter_by(is_active=True).count()
        }


class Question(db.Model):
    """問題テーブル"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False, default=1)  # 1-5
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーションシップ
    choices = db.relationship('Choice', backref='question', lazy='dynamic', cascade='all, delete-orphan')
    user_answers = db.relationship('UserAnswer', backref='question', lazy='dynamic')
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:30]}...>'
    
    def get_correct_choice(self):
        """正解の選択肢を取得"""
        return self.choices.filter_by(is_correct=True).first()
    
    def to_dict(self, include_choices=False, shuffle_choices=False):
        """辞書形式に変換"""
        data = {
            'id': self.id,
            'category_id': self.category_id,
            'question_text': self.question_text,
            'explanation': self.explanation,
            'difficulty': self.difficulty
        }
        
        if include_choices:
            choices = list(self.choices.all())
            if shuffle_choices:
                import random
                random.shuffle(choices)
            data['choices'] = [choice.to_dict() for choice in choices]
        
        return data


class Choice(db.Model):
    """選択肢テーブル"""
    __tablename__ = 'choices'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    choice_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)
    display_order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Choice {self.id}: {self.choice_text[:20]}...>'
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'choice_text': self.choice_text,
            'is_correct': self.is_correct
        }


class QuizSession(db.Model):
    """クイズセッションテーブル"""
    __tablename__ = 'quiz_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # ログインユーザー用
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    session_key = db.Column(db.String(64), unique=True, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_count = db.Column(db.Integer, nullable=False, default=0)
    is_review_mode = db.Column(db.Boolean, nullable=False, default=False)
    parent_session_id = db.Column(db.Integer, db.ForeignKey('quiz_sessions.id'), nullable=True)
    timer_seconds = db.Column(db.Integer, nullable=False, default=30)
    sound_enabled = db.Column(db.Boolean, nullable=False, default=True)
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # リレーションシップ
    user_answers = db.relationship('UserAnswer', backref='session', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<QuizSession {self.session_key}>'
    
    def is_completed(self):
        """完了しているかチェック"""
        return self.completed_at is not None
    
    def get_accuracy_rate(self):
        """正答率を計算"""
        if self.total_questions == 0:
            return 0.0
        return (self.correct_count / self.total_questions) * 100
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'session_key': self.session_key,
            'category_id': self.category_id,
            'category_name': self.category.name,
            'total_questions': self.total_questions,
            'correct_count': self.correct_count,
            'accuracy_rate': self.get_accuracy_rate(),
            'is_review_mode': self.is_review_mode,
            'timer_seconds': self.timer_seconds,
            'sound_enabled': self.sound_enabled,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class UserAnswer(db.Model):
    """回答履歴テーブル"""
    __tablename__ = 'user_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('quiz_sessions.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey('choices.id'))
    is_correct = db.Column(db.Boolean, nullable=False)
    time_spent_seconds = db.Column(db.Integer, nullable=False)
    answered_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserAnswer session={self.session_id} question={self.question_id}>'
    
    def to_dict(self):
        """辞書形式に変換"""
        choice = Choice.query.get(self.choice_id) if self.choice_id else None
        return {
            'id': self.id,
            'question_id': self.question_id,
            'choice_id': self.choice_id,
            'choice_text': choice.choice_text if choice else '未回答',
            'is_correct': self.is_correct,
            'time_spent_seconds': self.time_spent_seconds,
            'answered_at': self.answered_at.isoformat()
        }


class TermReference(db.Model):
    """用語参考リンクテーブル"""
    __tablename__ = 'term_references'
    
    id = db.Column(db.Integer, primary_key=True)
    term_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    display_order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TermReference {self.term_name}>'
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'term_name': self.term_name,
            'description': self.description,
            'url': self.url,
            'category_id': self.category_id
        }

