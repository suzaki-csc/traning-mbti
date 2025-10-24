"""採点・判定ロジック"""


def calculate_mbti_type(scores: dict) -> str:
    """
    4軸のスコアからMBTIタイプを判定
    
    Args:
        scores: {
            'E': 6, 'I': 0,
            'S': 4, 'N': 2,
            'T': 4, 'F': 2,
            'J': 4, 'P': 2
        }
    
    Returns:
        str: 'INTJ', 'ENFP' など
    """
    result = ""
    
    # 1軸目: E vs I
    result += "E" if scores.get('E', 0) >= scores.get('I', 0) else "I"
    
    # 2軸目: S vs N
    result += "S" if scores.get('S', 0) >= scores.get('N', 0) else "N"
    
    # 3軸目: T vs F
    result += "T" if scores.get('T', 0) >= scores.get('F', 0) else "F"
    
    # 4軸目: J vs P
    result += "J" if scores.get('J', 0) >= scores.get('P', 0) else "P"
    
    return result


def calculate_percentage(axis_score: int, total_questions_per_axis: int) -> float:
    """
    各軸の傾向を百分率で計算
    
    Args:
        axis_score: その軸のスコア（例: E=6）
        total_questions_per_axis: その軸の質問数（通常3問）
    
    Returns:
        float: 傾向の強さ（0〜100%）
    """
    max_score = total_questions_per_axis * 2  # 各質問で最大2点
    return (axis_score / max_score) * 100 if max_score > 0 else 50.0


def get_axis_percentages(scores: dict) -> dict:
    """
    全軸の百分率を計算
    
    Args:
        scores: 各軸のスコア辞書
    
    Returns:
        dict: 各軸の百分率
    """
    # 各軸の質問数（12問を4軸で分けるので各3問）
    questions_per_axis = 3
    
    return {
        'E': calculate_percentage(scores.get('E', 0), questions_per_axis),
        'I': calculate_percentage(scores.get('I', 0), questions_per_axis),
        'S': calculate_percentage(scores.get('S', 0), questions_per_axis),
        'N': calculate_percentage(scores.get('N', 0), questions_per_axis),
        'T': calculate_percentage(scores.get('T', 0), questions_per_axis),
        'F': calculate_percentage(scores.get('F', 0), questions_per_axis),
        'J': calculate_percentage(scores.get('J', 0), questions_per_axis),
        'P': calculate_percentage(scores.get('P', 0), questions_per_axis)
    }

