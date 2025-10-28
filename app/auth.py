"""
認証関連のヘルパー関数とデコレーター
"""
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def admin_required(f):
    """
    管理者権限が必要なビューを保護するデコレーター
    
    使用例:
        @app.route('/admin')
        @login_required
        @admin_required
        def admin_page():
            return 'Admin page'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('ログインが必要です。', 'warning')
            return redirect(url_for('main.login'))
        
        if not current_user.is_admin():
            flash('管理者権限が必要です。', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_mbti_description(mbti_type):
    """
    MBTIタイプの説明を取得
    
    Args:
        mbti_type: MBTIタイプ（4文字の文字列）
    
    Returns:
        str: タイプの説明
    """
    descriptions = {
        'INTJ': '独創的な戦略家。論理的思考と長期計画を重視し、目標達成に向けて効率的に行動します。',
        'INTP': '理論的な革新者。知的好奇心が強く、複雑な問題を分析し解決策を見出すことを楽しみます。',
        'ENTJ': 'カリスマ的な指導者。大胆で想像力豊かなリーダーで、障害を乗り越える方法を常に見つけます。',
        'ENTP': '賢い討論者。知的挑戦を愛し、新しいアイデアや可能性を追求することに情熱を注ぎます。',
        'INFJ': '理想主義的な助言者。深い洞察力を持ち、他者の成長を支援することに喜びを感じます。',
        'INFP': '献身的な仲介者。理想と価値観を大切にし、調和と真実性を追求します。',
        'ENFJ': '情熱的な主人公。カリスマ性があり、他者を鼓舞し導くことに長けています。',
        'ENFP': '熱狂的な活動家。創造的で社交的。新しい可能性や人間関係を大切にします。',
        'ISTJ': '実務的な管理者。事実と詳細を重視し、信頼性と責任感が強い性格です。',
        'ISFJ': '献身的な擁護者。思いやりがあり、他者のニーズに敏感で支援することを喜びます。',
        'ESTJ': '優秀な管理者。組織力と決断力があり、物事を効率的に進めることが得意です。',
        'ESFJ': '思いやりのある世話役。協調性が高く、他者との調和を重視し支援します。',
        'ISTP': '大胆な職人。実践的で論理的。手を動かして問題を解決することが得意です。',
        'ISFP': '柔軟な芸術家。感受性豊かで、美と調和を大切にする自由な精神の持ち主です。',
        'ESTP': '活発な起業家。エネルギッシュで行動的。リスクを恐れず新しい経験を求めます。',
        'ESFP': '陽気なエンターテイナー。社交的で楽観的。周囲を楽しませることが得意です。',
    }
    
    return descriptions.get(mbti_type, 'あなた独自の魅力的な性格です。')


def get_mbti_name(mbti_type):
    """
    MBTIタイプの名称を取得
    
    Args:
        mbti_type: MBTIタイプ（4文字の文字列）
    
    Returns:
        str: タイプの名称
    """
    names = {
        'INTJ': '建築家',
        'INTP': '論理学者',
        'ENTJ': '指揮官',
        'ENTP': '討論者',
        'INFJ': '提唱者',
        'INFP': '仲介者',
        'ENFJ': '主人公',
        'ENFP': '広報運動家',
        'ISTJ': '管理者',
        'ISFJ': '擁護者',
        'ESTJ': '幹部',
        'ESFJ': '領事官',
        'ISTP': '巨匠',
        'ISFP': '冒険家',
        'ESTP': '起業家',
        'ESFP': 'エンターテイナー',
    }
    
    return names.get(mbti_type, 'ユニーク')

