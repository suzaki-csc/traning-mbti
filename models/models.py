from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class DiagnosisResult(db.Model):
    """診断結果モデル"""
    __tablename__ = 'diagnosis_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    mbti_type = db.Column(db.String(4), nullable=False)
    e_score = db.Column(db.Integer, nullable=False)
    i_score = db.Column(db.Integer, nullable=False)
    s_score = db.Column(db.Integer, nullable=False)
    n_score = db.Column(db.Integer, nullable=False)
    t_score = db.Column(db.Integer, nullable=False)
    f_score = db.Column(db.Integer, nullable=False)
    j_score = db.Column(db.Integer, nullable=False)
    p_score = db.Column(db.Integer, nullable=False)
    diagnosed_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_ip = db.Column(db.String(45))
    
    # リレーション
    answers = db.relationship('Answer', backref='diagnosis', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<DiagnosisResult {self.id}: {self.mbti_type}>'


class Answer(db.Model):
    """回答モデル"""
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('diagnosis_results.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_value = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Answer {self.id}: Q{self.question_id}={self.answer_value}>'


class Question(db.Model):
    """質問モデル"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    axis = db.Column(db.String(10), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # リレーション
    answers = db.relationship('Answer', backref='question', lazy=True)
    
    def __repr__(self):
        return f'<Question {self.id}: {self.axis}>'

