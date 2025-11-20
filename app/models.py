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
    クイズセッションの履歴を保存するモデル（オプション機能）
    
    Attributes:
        id: セッションID（主キー）
        category_id: カテゴリID（外部キー）
        score: 正解数
        total_questions: 総問題数
        completed_at: 完了日時
    """
    __tablename__ = 'quiz_session'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<QuizSession {self.id}: {self.score}/{self.total_questions}>'

