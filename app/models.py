"""
データベースモデル定義
"""
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """ユーザーテーブル"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='user_role'), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """パスワードをハッシュ化して設定"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """パスワードを検証"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """管理者かどうかを判定"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.user_id}>'


class Category(db.Model):
    """カテゴリテーブル"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション
    quizzes = db.relationship('Quiz', backref='category', lazy=True, cascade='all, delete-orphan')
    quiz_results = db.relationship('QuizResult', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Quiz(db.Model):
    """クイズテーブル"""
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)  # 1-4
    explanation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション
    quiz_answers = db.relationship('QuizAnswer', backref='quiz', lazy=True)
    
    def get_option(self, option_num):
        """選択肢を取得（1-4）"""
        options = {
            1: self.option1,
            2: self.option2,
            3: self.option3,
            4: self.option4
        }
        return options.get(option_num, '')
    
    def __repr__(self):
        return f'<Quiz {self.id}: {self.question[:50]}...>'


class QuizResult(db.Model):
    """クイズ結果テーブル"""
    __tablename__ = 'quiz_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    is_review_mode = db.Column(db.Boolean, default=False, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # リレーション
    quiz_answers = db.relationship('QuizAnswer', backref='quiz_result', lazy=True, cascade='all, delete-orphan')
    
    def get_percentage(self):
        """正答率を計算"""
        if self.total_questions == 0:
            return 0
        return round((self.score / self.total_questions) * 100, 1)
    
    def __repr__(self):
        return f'<QuizResult {self.id}: {self.score}/{self.total_questions}>'


class QuizAnswer(db.Model):
    """回答詳細テーブル"""
    __tablename__ = 'quiz_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_result_id = db.Column(db.Integer, db.ForeignKey('quiz_results.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_answer = db.Column(db.Integer, nullable=False)  # 1-4
    is_correct = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<QuizAnswer {self.id}: {self.user_answer} (correct: {self.is_correct})>'


class Review(db.Model):
    """レビューテーブル"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id}: {self.title}>'

