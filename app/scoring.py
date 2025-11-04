"""採点ロジック"""


def calculate_scores(answers):
    """
    回答からMBTIスコアを計算
    
    Args:
        answers: list of dict
            [{"question_id": 1, "axis": "E", "score": 2}, ...]
    
    Returns:
        dict: {"E": 6, "I": 0, "S": 4, "N": 2, ...}
    """
    scores = {
        "E": 0, "I": 0,
        "S": 0, "N": 0,
        "T": 0, "F": 0,
        "J": 0, "P": 0
    }
    
    for answer in answers:
        axis = answer.get("axis")
        score = answer.get("score", 0)
        if axis in scores:
            scores[axis] += score
    
    return scores


def determine_type(scores):
    """
    スコアからMBTIタイプを判定
    
    Args:
        scores: dict {"E": 6, "I": 0, ...}
    
    Returns:
        str: MBTIタイプ（例: "INTJ"）
    """
    mbti_type = ""
    
    # E vs I
    mbti_type += "E" if scores["E"] >= scores["I"] else "I"
    
    # S vs N
    mbti_type += "S" if scores["S"] >= scores["N"] else "N"
    
    # T vs F
    mbti_type += "T" if scores["T"] >= scores["F"] else "F"
    
    # J vs P
    mbti_type += "J" if scores["J"] >= scores["P"] else "P"
    
    return mbti_type


def get_score_percentages(scores):
    """
    各軸のスコアをパーセンテージに変換
    
    Args:
        scores: dict {"E": 6, "I": 0, ...}
    
    Returns:
        dict: {"E/I": {"E": 75, "I": 25}, ...}
    """
    percentages = {}
    
    axes = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
    
    for axis1, axis2 in axes:
        total = scores[axis1] + scores[axis2]
        if total > 0:
            percentages[f"{axis1}/{axis2}"] = {
                axis1: round((scores[axis1] / total) * 100),
                axis2: round((scores[axis2] / total) * 100)
            }
        else:
            # スコアが0の場合は50:50
            percentages[f"{axis1}/{axis2}"] = {
                axis1: 50,
                axis2: 50
            }
    
    return percentages


def get_axis_descriptions():
    """
    各軸の説明を取得
    
    Returns:
        dict: 軸の説明
    """
    return {
        "E/I": {
            "name": "外向型 / 内向型",
            "E": "外向型（Extraversion）",
            "I": "内向型（Introversion）"
        },
        "S/N": {
            "name": "感覚型 / 直観型",
            "S": "感覚型（Sensing）",
            "N": "直観型（iNtuition）"
        },
        "T/F": {
            "name": "思考型 / 感情型",
            "T": "思考型（Thinking）",
            "F": "感情型（Feeling）"
        },
        "J/P": {
            "name": "判断型 / 知覚型",
            "J": "判断型（Judging）",
            "P": "知覚型（Perceiving）"
        }
    }

