"""
採点ロジック・判定処理
"""

from .questions import QUESTIONS


def calculate_scores(answers):
    """
    回答から各軸のスコアを計算する
    
    Args:
        answers: 回答データの辞書 {question_id: answer_value}
    
    Returns:
        各軸のスコア辞書 {"EI": score, "SN": score, "TF": score, "JP": score}
    """
    scores = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}
    
    for question in QUESTIONS:
        q_id = question["id"]
        q_id_str = str(q_id)
        if q_id_str in answers:
            answer_value = answers[q_id_str]
            # 中央値3を基準に-2〜+2のスコアに変換
            base_score = answer_value - 3
            
            axis = question["axis"]
            direction = question["direction"]
            
            # 方向性に基づいてスコアを加算
            # E, S, T, Jの場合: 正のスコアでその方向に寄る
            # I, N, F, Pの場合: 正のスコアでその方向に寄るので、軸スコアからは減算
            if direction in ["E", "S", "T", "J"]:
                scores[axis] += base_score
            else:  # direction in ["I", "N", "F", "P"]
                scores[axis] -= base_score
    
    return scores


def determine_mbti_type(scores):
    """
    各軸のスコアからMBTIタイプを判定する
    
    Args:
        scores: 各軸のスコア辞書
    
    Returns:
        MBTIタイプ（4文字の文字列）
    """
    mbti_type = ""
    
    # E/I軸: 正ならE、負またはゼロならI
    mbti_type += "E" if scores["EI"] > 0 else "I"
    
    # S/N軸: 正ならS、負またはゼロならN
    mbti_type += "S" if scores["SN"] > 0 else "N"
    
    # T/F軸: 正ならT、負またはゼロならF
    mbti_type += "T" if scores["TF"] > 0 else "F"
    
    # J/P軸: 正ならJ、負またはゼロならP
    mbti_type += "J" if scores["JP"] > 0 else "P"
    
    return mbti_type


def get_axis_percentages(scores):
    """
    各軸のスコアをパーセンテージに変換する
    
    Args:
        scores: 各軸のスコア辞書
    
    Returns:
        各軸のパーセンテージ辞書（左側の特性が強い場合に正の値）
    """
    # 最大スコア（質問数×2）から計算
    # EI軸は4問、SN軸は3問、TF軸は2問、JP軸は3問
    axis_max_scores = {
        "EI": 4 * 2,  # 8
        "SN": 3 * 2,  # 6
        "TF": 2 * 2,  # 4
        "JP": 3 * 2   # 6
    }
    
    percentages = {}
    for axis, score in scores.items():
        max_score = axis_max_scores[axis]
        # スコアをパーセンテージに変換（-100〜100）
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        percentages[axis] = round(percentage, 1)
    
    return percentages


def get_axis_labels(mbti_type):
    """
    MBTIタイプから各軸のラベルを取得する
    
    Args:
        mbti_type: MBTIタイプ（4文字）
    
    Returns:
        各軸のラベル辞書
    """
    labels = {
        "EI": ("外向型 (E)", "内向型 (I)"),
        "SN": ("感覚型 (S)", "直感型 (N)"),
        "TF": ("思考型 (T)", "感情型 (F)"),
        "JP": ("判断型 (J)", "知覚型 (P)")
    }
    
    return labels

