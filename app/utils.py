"""
ユーティリティ関数モジュール

クイズアプリケーションで使用する共通のユーティリティ関数を定義します。
問題の選択、スコア計算、セッション管理などの機能を提供します。
"""

import random
from typing import List, Dict, Any


def select_questions(question_ids: List[int], max_questions: int = 10) -> List[int]:
    """
    問題IDリストから指定数の問題をランダムに選択します。
    問題数が指定数より少ない場合は、重複を許可して指定数まで出題します。
    
    Args:
        question_ids: 選択可能な問題IDのリスト
        max_questions: 選択する最大問題数（デフォルト: 10）
    
    Returns:
        List[int]: 選択された問題IDのリスト（シャッフル済み）
    
    Example:
        >>> question_ids = [1, 2, 3, 4, 5]
        >>> selected = select_questions(question_ids, max_questions=10)
        >>> len(selected)  # 5問しかないので、重複して10問になる
        10
    """
    if not question_ids:
        return []
    
    # 問題数が指定数以下の場合は重複を許可
    if len(question_ids) <= max_questions:
        # 指定数になるまでランダムに選択（重複あり）
        selected = []
        while len(selected) < max_questions:
            selected.append(random.choice(question_ids))
        # シャッフルして返す
        random.shuffle(selected)
        return selected
    else:
        # 問題数が十分にある場合は、重複なしでランダムに選択
        selected = random.sample(question_ids, max_questions)
        # シャッフルして返す
        random.shuffle(selected)
        return selected


def calculate_score(answers: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
    """
    回答履歴からスコアを計算します。
    
    Args:
        answers: 回答履歴の辞書
            {
                question_id: {
                    'is_correct': bool,
                    'time_taken': int
                }
            }
    
    Returns:
        Dict[str, Any]: スコア情報の辞書
            {
                'total_questions': int,
                'correct_answers': int,
                'score_percentage': float,
                'incorrect_question_ids': List[int]
            }
    """
    total_questions = len(answers)
    correct_answers = sum(1 for answer in answers.values() if answer.get('is_correct', False))
    
    if total_questions == 0:
        score_percentage = 0.0
    else:
        score_percentage = (correct_answers / total_questions) * 100
    
    # 間違えた問題のIDリスト
    incorrect_question_ids = [
        question_id
        for question_id, answer in answers.items()
        if not answer.get('is_correct', False)
    ]
    
    return {
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score_percentage': round(score_percentage, 2),
        'incorrect_question_ids': incorrect_question_ids
    }


def format_score_string(category_name: str, correct_answers: int, total_questions: int, score_percentage: float) -> str:
    """
    スコア情報を共有用の文字列形式にフォーマットします。
    
    Args:
        category_name: カテゴリ名
        correct_answers: 正解数
        total_questions: 総問題数
        score_percentage: 正答率（パーセンテージ）
    
    Returns:
        str: フォーマットされたスコア文字列
    
    Example:
        >>> format_score_string('セキュリティ', 8, 10, 80.0)
        'セキュリティクイズ: 8/10問正解 (80.0%)'
    """
    return f'{category_name}クイズ: {correct_answers}/{total_questions}問正解 ({score_percentage}%)'


def shuffle_list(items: List[Any]) -> List[Any]:
    """
    リストをシャッフルして返します（元のリストは変更しません）。
    
    Args:
        items: シャッフルするリスト
    
    Returns:
        List[Any]: シャッフルされた新しいリスト
    """
    shuffled = items.copy()
    random.shuffle(shuffled)
    return shuffled

