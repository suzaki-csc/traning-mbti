"""
結果サービス

クイズ結果の集計や復習リスト生成を提供します。
"""
from app.models import QuizSession, UserAnswer, Question, Choice


def get_session_result(session_key):
    """
    セッションの結果を取得
    
    Args:
        session_key: セッションキー
    
    Returns:
        結果データの辞書
    """
    session = QuizSession.query.filter_by(session_key=session_key).first()
    
    if not session:
        return None
    
    # 間違えた問題のリストを取得
    incorrect_answers = UserAnswer.query.filter_by(
        session_id=session.id,
        is_correct=False
    ).all()
    
    incorrect_questions = []
    for answer in incorrect_answers:
        question = Question.query.get(answer.question_id)
        user_choice = Choice.query.get(answer.choice_id) if answer.choice_id else None
        correct_choice = question.get_correct_choice()
        
        incorrect_questions.append({
            'question_id': question.id,
            'question_text': question.question_text,
            'user_choice_text': user_choice.choice_text if user_choice else '未回答（時間切れ）',
            'correct_choice_text': correct_choice.choice_text if correct_choice else '',
            'explanation': question.explanation
        })
    
    # スコア共有用テキストを生成
    share_text = generate_share_text(session)
    
    result = {
        'session_key': session.session_key,
        'category_name': session.category.name,
        'total_questions': session.total_questions,
        'correct_count': session.correct_count,
        'accuracy_rate': session.get_accuracy_rate(),
        'completed_at': session.completed_at.isoformat() if session.completed_at else None,
        'incorrect_questions': incorrect_questions,
        'share_text': share_text,
        'has_incorrect': len(incorrect_questions) > 0
    }
    
    return result


def generate_share_text(session):
    """
    スコア共有用のテキストを生成
    
    Args:
        session: QuizSessionオブジェクト
    
    Returns:
        共有用テキスト
    """
    accuracy = int(session.get_accuracy_rate())
    
    share_text = f"""【クイズ結果】
カテゴリ: {session.category.name}
スコア: {session.correct_count}/{session.total_questions} ({accuracy}%)
#ITクイズアプリ"""
    
    return share_text


def get_review_questions(session_key):
    """
    復習対象の問題IDリストを取得
    
    Args:
        session_key: セッションキー
    
    Returns:
        問題IDのリスト
    """
    session = QuizSession.query.filter_by(session_key=session_key).first()
    
    if not session:
        return []
    
    # 間違えた問題のIDを取得
    incorrect_answers = UserAnswer.query.filter_by(
        session_id=session.id,
        is_correct=False
    ).all()
    
    question_ids = [answer.question_id for answer in incorrect_answers]
    
    return question_ids


def get_evaluation_message(accuracy_rate):
    """
    正答率に応じた評価メッセージを取得
    
    Args:
        accuracy_rate: 正答率（0-100）
    
    Returns:
        評価メッセージ
    """
    if accuracy_rate == 100:
        return "完璧です！🎉 すべての問題に正解しました！"
    elif accuracy_rate >= 80:
        return "素晴らしい！😊 よく理解できています！"
    elif accuracy_rate >= 60:
        return "良い成績です！💪 もう少しで完璧です！"
    elif accuracy_rate >= 40:
        return "まずまずです！📚 復習して理解を深めましょう！"
    else:
        return "頑張りましょう！✨ 復習モードで再挑戦してみてください！"

