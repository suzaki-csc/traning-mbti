"""
クイズサービス

問題選択、採点などのクイズロジックを提供します。
"""
import random
import secrets
from app import db
from app.models import Question, Choice, QuizSession, UserAnswer, Category


def generate_session_key():
    """セッションキーを生成"""
    return secrets.token_urlsafe(32)


def select_questions(category_id, num_questions=10):
    """
    指定カテゴリから問題をランダムに選択
    
    Args:
        category_id: カテゴリID
        num_questions: 出題数（デフォルト10問）
    
    Returns:
        選択された問題IDのリスト
    """
    # カテゴリ内の有効な問題を取得
    available_questions = Question.query.filter_by(
        category_id=category_id,
        is_active=True
    ).all()
    
    question_ids = [q.id for q in available_questions]
    
    # 問題がない場合
    if not question_ids:
        return []
    
    # 問題数が足りない場合は重複を許可
    if len(question_ids) < num_questions:
        # 重複を許可してランダムサンプリング
        selected = random.choices(question_ids, k=num_questions)
    else:
        # 重複なしでランダムサンプリング
        selected = random.sample(question_ids, num_questions)
    
    # 順番をシャッフル
    random.shuffle(selected)
    
    return selected


def get_shuffled_choices(question_id):
    """
    問題の選択肢をシャッフルして返す
    
    Args:
        question_id: 問題ID
    
    Returns:
        シャッフルされた選択肢のリスト
    """
    choices = Choice.query.filter_by(question_id=question_id).all()
    choices_list = list(choices)
    random.shuffle(choices_list)
    
    return choices_list


def create_quiz_session(category_id, timer_seconds=30, sound_enabled=True, 
                        is_review_mode=False, parent_session_key=None, user_id=None):
    """
    新しいクイズセッションを作成
    
    Args:
        category_id: カテゴリID
        timer_seconds: タイマー秒数
        sound_enabled: 効果音の有効/無効
        is_review_mode: 復習モードかどうか
        parent_session_key: 復習モード時の元セッションキー
        user_id: ログインユーザーのID（オプション）
    
    Returns:
        作成されたQuizSessionオブジェクト
    """
    # セッションキーを生成
    session_key = generate_session_key()
    
    # 復習モードの場合は間違えた問題を選択
    if is_review_mode and parent_session_key:
        parent_session = QuizSession.query.filter_by(
            session_key=parent_session_key
        ).first()
        
        if parent_session:
            # 間違えた問題のIDを取得
            incorrect_answers = UserAnswer.query.filter_by(
                session_id=parent_session.id,
                is_correct=False
            ).all()
            question_ids = [ans.question_id for ans in incorrect_answers]
            parent_session_id = parent_session.id
        else:
            # 親セッションが見つからない場合は通常モード
            question_ids = select_questions(category_id)
            parent_session_id = None
    else:
        # 通常モード：ランダムに問題を選択
        question_ids = select_questions(category_id)
        parent_session_id = None
    
    # セッションを作成
    session = QuizSession(
        user_id=user_id,
        category_id=category_id,
        session_key=session_key,
        total_questions=len(question_ids),
        timer_seconds=timer_seconds,
        sound_enabled=sound_enabled,
        is_review_mode=is_review_mode,
        parent_session_id=parent_session_id
    )
    
    db.session.add(session)
    db.session.commit()
    
    # セッションと問題の紐付けを保存（session_keyを使って後で取得）
    # ここでは一時的にセッション情報として保存
    # 実際の実装では中間テーブルを使うか、JSONフィールドに保存
    # 簡易実装として、最初の問題からの順序で管理
    
    return session, question_ids


def get_question_for_session(session_key, question_number, question_ids):
    """
    セッションの特定の問題番号の問題を取得
    
    Args:
        session_key: セッションキー
        question_number: 問題番号（1から開始）
        question_ids: 問題IDのリスト
    
    Returns:
        Question オブジェクトと選択肢のリスト
    """
    if question_number < 1 or question_number > len(question_ids):
        return None, []
    
    question_id = question_ids[question_number - 1]
    question = Question.query.get(question_id)
    
    if not question:
        return None, []
    
    choices = get_shuffled_choices(question_id)
    
    return question, choices


def submit_answer(session_key, question_id, choice_id, time_spent_seconds):
    """
    回答を送信して採点
    
    Args:
        session_key: セッションキー
        question_id: 問題ID
        choice_id: 選択した選択肢ID（タイムアウトの場合はNone）
        time_spent_seconds: 回答にかかった時間（秒）
    
    Returns:
        (is_correct, explanation, correct_choice_id) のタプル
    """
    session = QuizSession.query.filter_by(session_key=session_key).first()
    
    if not session:
        return None, None, None
    
    # 選択肢をチェック
    if choice_id:
        selected_choice = Choice.query.get(choice_id)
        is_correct = selected_choice.is_correct if selected_choice else False
    else:
        # タイムアウト（未回答）
        is_correct = False
    
    # 正解の選択肢を取得
    question = Question.query.get(question_id)
    correct_choice = question.get_correct_choice()
    
    # 回答履歴を保存
    user_answer = UserAnswer(
        session_id=session.id,
        question_id=question_id,
        choice_id=choice_id,
        is_correct=is_correct,
        time_spent_seconds=time_spent_seconds
    )
    
    db.session.add(user_answer)
    
    # セッションの正解数を更新
    if is_correct:
        session.correct_count += 1
    
    db.session.commit()
    
    return is_correct, question.explanation, correct_choice.id if correct_choice else None


def complete_session(session_key):
    """
    セッションを完了状態にする
    
    Args:
        session_key: セッションキー
    
    Returns:
        完了したQuizSessionオブジェクト
    """
    from datetime import datetime
    
    session = QuizSession.query.filter_by(session_key=session_key).first()
    
    if session and not session.is_completed():
        session.completed_at = datetime.utcnow()
        db.session.commit()
    
    return session


def get_session_by_key(session_key):
    """
    セッションキーからセッションを取得
    
    Args:
        session_key: セッションキー
    
    Returns:
        QuizSessionオブジェクト
    """
    return QuizSession.query.filter_by(session_key=session_key).first()

