"""
データベースモデル定義
Category、Question、QuizSessionのモデルを定義
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# dbオブジェクトはapp.pyで初期化される
db = SQLAlchemy()

class Category(db.Model):
    """
    クイズのカテゴリを管理するモデル
    
    Attributes:
        id: カテゴリID（主キー）
        name: カテゴリ名（一意）
        description: カテゴリの説明
        created_at: 作成日時
        questions: このカテゴリに属する問題（リレーション）
    """
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # リレーション: このカテゴリに属する問題
    questions = db.relationship('Question', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Question(db.Model):
    """
    クイズの問題を管理するモデル
    
    Attributes:
        id: 問題ID（主キー）
        category_id: カテゴリID（外部キー）
        question_text: 問題文
        option_a, option_b, option_c, option_d: 選択肢
        correct_answer: 正解（'A', 'B', 'C', 'D'のいずれか）
        explanation: 解説文
        created_at: 作成日時
    """
    __tablename__ = 'question'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', 'D'
    explanation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:30]}...>'

class QuizSession(db.Model):
    """
    クイズセッションの履歴を保存するモデル
    
    Attributes:
        id: セッションID（主キー）
        user_id: ユーザID（外部キー、オプション）
        category_id: カテゴリID（外部キー）
        score: 正解数
        total_questions: 総問題数
        completed_at: 完了日時
    """
    __tablename__ = 'quiz_session'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<QuizSession {self.id}: {self.score}/{self.total_questions}>'

class User(db.Model):
    """
    ユーザを管理するモデル
    
    Attributes:
        id: ユーザID（主キー）
        user_id: ユーザID（ログイン用、一意）
        email: メールアドレス（一意）
        password_hash: パスワードハッシュ
        role: ロール（'user' または 'admin'）
        created_at: 作成日時
        quiz_sessions: このユーザのクイズセッション履歴（リレーション）
    """
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'user' または 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # リレーション: このユーザのクイズセッション履歴
    quiz_sessions = db.relationship('QuizSession', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.user_id} ({self.role})>'
    
    def set_password(self, password):
        """パスワードをハッシュ化して設定"""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """パスワードが正しいかチェック"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """管理者かどうかを判定"""
        return self.role == 'admin'

