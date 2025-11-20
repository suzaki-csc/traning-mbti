"""
データモデル定義モジュール

このモジュールでは、SQLAlchemyを使用してデータベースのテーブル構造を定義します。
Category, Question, QuizResult, AnswerDetailの4つのモデルを定義しています。
"""

from app import db
from datetime import datetime


class Category(db.Model):
    """
    カテゴリモデル
    
    クイズのカテゴリ（セキュリティ、IT基礎、プログラミングなど）を表すモデルです。
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, comment='カテゴリ名（例: セキュリティ）')
    description = db.Column(db.Text, comment='カテゴリの説明')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション: このカテゴリに属する問題のリスト
    questions = db.relationship('Question', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        """
        カテゴリ情報を辞書形式で返す
        
        Returns:
            dict: カテゴリ情報の辞書
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'question_count': len(self.questions)
        }


class Question(db.Model):
    """
    問題モデル
    
    クイズの問題を表すモデルです。4択形式の問題とその解説を保持します。
    """
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False, comment='問題文')
    option_a = db.Column(db.String(255), nullable=False, comment='選択肢A')
    option_b = db.Column(db.String(255), nullable=False, comment='選択肢B')
    option_c = db.Column(db.String(255), nullable=False, comment='選択肢C')
    option_d = db.Column(db.String(255), nullable=False, comment='選択肢D')
    correct_answer = db.Column(db.Enum('A', 'B', 'C', 'D'), nullable=False, comment='正解')
    explanation = db.Column(db.Text, nullable=False, comment='解説')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:50]}...>'
    
    def to_dict(self):
        """
        問題情報を辞書形式で返す
        
        Returns:
            dict: 問題情報の辞書
        """
        return {
            'id': self.id,
            'category_id': self.category_id,
            'question_text': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation
        }
    
    def check_answer(self, user_answer):
        """
        ユーザーの回答が正解かどうかを判定
        
        Args:
            user_answer: ユーザーが選択した回答（'A', 'B', 'C', 'D'のいずれか）
        
        Returns:
            bool: 正解の場合True、不正解の場合False
        """
        return user_answer.upper() == self.correct_answer


class QuizResult(db.Model):
    """
    クイズ結果モデル
    
    クイズの実行結果を保存するモデルです。スコアやかかった時間などの情報を保持します。
    """
    __tablename__ = 'quiz_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True, index=True, comment='ユーザーID（ログイン機能実装時に使用）')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    total_questions = db.Column(db.Integer, nullable=False, comment='総問題数')
    correct_answers = db.Column(db.Integer, nullable=False, comment='正解数')
    score_percentage = db.Column(db.Numeric(5, 2), nullable=False, comment='正答率')
    time_taken = db.Column(db.Integer, comment='かかった時間（秒）')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # リレーション: このクイズ結果に紐づく回答詳細のリスト
    answer_details = db.relationship('AnswerDetail', backref='quiz_result', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<QuizResult {self.id}: {self.correct_answers}/{self.total_questions}>'
    
    def to_dict(self):
        """
        クイズ結果情報を辞書形式で返す
        
        Returns:
            dict: クイズ結果情報の辞書
        """
        return {
            'id': self.id,
            'category_id': self.category_id,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'score_percentage': float(self.score_percentage),
            'time_taken': self.time_taken,
            'created_at': self.created_at.isoformat()
        }
    
    def get_incorrect_questions(self):
        """
        間違えた問題のIDリストを取得
        
        Returns:
            list: 間違えた問題のIDのリスト
        """
        incorrect_details = [detail for detail in self.answer_details if not detail.is_correct]
        return [detail.question_id for detail in incorrect_details]


class AnswerDetail(db.Model):
    """
    回答詳細モデル
    
    各問題に対するユーザーの回答を詳細に記録するモデルです。
    """
    __tablename__ = 'answer_details'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_result_id = db.Column(db.Integer, db.ForeignKey('quiz_results.id'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False, index=True)
    user_answer = db.Column(db.Enum('A', 'B', 'C', 'D'), nullable=False, comment='ユーザーの回答')
    is_correct = db.Column(db.Boolean, nullable=False, comment='正解かどうか')
    time_taken = db.Column(db.Integer, comment='回答にかかった時間（秒）')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AnswerDetail {self.id}: Question {self.question_id}, Answer {self.user_answer}, Correct: {self.is_correct}>'
    
    def to_dict(self):
        """
        回答詳細情報を辞書形式で返す
        
        Returns:
            dict: 回答詳細情報の辞書
        """
        return {
            'id': self.id,
            'quiz_result_id': self.quiz_result_id,
            'question_id': self.question_id,
            'user_answer': self.user_answer,
            'is_correct': self.is_correct,
            'time_taken': self.time_taken
        }

