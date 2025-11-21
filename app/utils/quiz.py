"""
クイズ関連のユーティリティ関数
"""
import random
from app.models import Quiz


def select_quiz_questions(category_id, num_questions=10):
    """
    カテゴリから指定数の問題をランダムに選択
    
    Args:
        category_id: カテゴリID
        num_questions: 選択する問題数（デフォルト: 10）
    
    Returns:
        list: 選択されたQuizオブジェクトのリスト
    """
    # カテゴリに属するすべての問題を取得
    all_quizzes = Quiz.query.filter_by(category_id=category_id).all()
    
    if not all_quizzes:
        return []
    
    # 問題数が指定数以下の場合は重複を許可して選択
    if len(all_quizzes) <= num_questions:
        # 重複を許可してランダムに選択
        selected = random.choices(all_quizzes, k=num_questions)
    else:
        # 重複なしでランダムに選択
        selected = random.sample(all_quizzes, num_questions)
    
    # 順番をシャッフル
    random.shuffle(selected)
    
    return selected


def get_review_questions(quiz_result_id):
    """
    復習モード用に間違えた問題を取得
    
    Args:
        quiz_result_id: クイズ結果ID
    
    Returns:
        list: 間違えた問題のQuizオブジェクトのリスト
    """
    from app.models import QuizAnswer
    
    # 間違えた問題のIDを取得
    wrong_answers = QuizAnswer.query.filter_by(
        quiz_result_id=quiz_result_id,
        is_correct=False
    ).all()
    
    # 問題IDのリストを作成
    quiz_ids = [answer.quiz_id for answer in wrong_answers]
    
    # 問題を取得
    quizzes = Quiz.query.filter(Quiz.id.in_(quiz_ids)).all()
    
    return quizzes

