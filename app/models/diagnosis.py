from datetime import datetime
from . import db


class Diagnosis(db.Model):
    """診断結果モデル"""
    
    __tablename__ = 'diagnoses'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    user_name = db.Column(db.String(100))
    user_email = db.Column(db.String(255))
    
    # 各軸のスコア
    e_score = db.Column(db.Integer, default=0)
    i_score = db.Column(db.Integer, default=0)
    s_score = db.Column(db.Integer, default=0)
    n_score = db.Column(db.Integer, default=0)
    t_score = db.Column(db.Integer, default=0)
    f_score = db.Column(db.Integer, default=0)
    j_score = db.Column(db.Integer, default=0)
    p_score = db.Column(db.Integer, default=0)
    
    # 判定結果
    mbti_type = db.Column(db.String(4), nullable=False, index=True)
    
    # 回答データ（JSON形式）
    answers = db.Column(db.JSON)
    
    # タイムスタンプ
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Diagnosis {self.id}: {self.mbti_type}>'
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_name': self.user_name,
            'user_email': self.user_email,
            'mbti_type': self.mbti_type,
            'scores': {
                'E': self.e_score,
                'I': self.i_score,
                'S': self.s_score,
                'N': self.n_score,
                'T': self.t_score,
                'F': self.f_score,
                'J': self.j_score,
                'P': self.p_score
            },
            'answers': self.answers,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

