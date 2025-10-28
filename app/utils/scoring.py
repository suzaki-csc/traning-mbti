"""
MBTIスコア計算ロジック
"""


def calculate_mbti_type(answers):
    """
    回答からMBTIタイプを判定する
    
    Args:
        answers: list of dict
            [{"question_id": 1, "axis": "E", "score": 3}, ...]
    
    Returns:
        dict: {
            "mbti_type": "INTJ",
            "scores": {
                "E": 2, "I": 7,
                "S": 3, "N": 6,
                "T": 8, "F": 1,
                "J": 7, "P": 2
            }
        }
    """
    # 各軸のスコアを初期化
    scores = {
        "E": 0, "I": 0,
        "S": 0, "N": 0,
        "T": 0, "F": 0,
        "J": 0, "P": 0
    }
    
    # 各回答のスコアを合算
    for answer in answers:
        axis = answer["axis"]
        score = answer["score"]
        if axis in scores:
            scores[axis] += score
    
    # 各軸で優勢な方を判定
    mbti_type = ""
    
    # E/I軸
    if scores["E"] > scores["I"]:
        mbti_type += "E"
    else:
        mbti_type += "I"  # 同点の場合はIを選択
    
    # S/N軸
    if scores["S"] > scores["N"]:
        mbti_type += "S"
    else:
        mbti_type += "N"  # 同点の場合はNを選択
    
    # T/F軸
    if scores["T"] > scores["F"]:
        mbti_type += "T"
    else:
        mbti_type += "F"  # 同点の場合はFを選択
    
    # J/P軸
    if scores["J"] > scores["P"]:
        mbti_type += "J"
    else:
        mbti_type += "P"  # 同点の場合はPを選択
    
    return {
        "mbti_type": mbti_type,
        "scores": scores
    }


def get_axis_percentages(scores):
    """
    各軸のスコアをパーセンテージに変換
    
    Args:
        scores: dict スコア辞書
    
    Returns:
        dict: パーセンテージ辞書
    """
    percentages = {}
    
    # E/I軸
    total_ei = scores["E"] + scores["I"]
    if total_ei > 0:
        percentages["E"] = round((scores["E"] / total_ei) * 100)
        percentages["I"] = round((scores["I"] / total_ei) * 100)
    else:
        percentages["E"] = percentages["I"] = 50
    
    # S/N軸
    total_sn = scores["S"] + scores["N"]
    if total_sn > 0:
        percentages["S"] = round((scores["S"] / total_sn) * 100)
        percentages["N"] = round((scores["N"] / total_sn) * 100)
    else:
        percentages["S"] = percentages["N"] = 50
    
    # T/F軸
    total_tf = scores["T"] + scores["F"]
    if total_tf > 0:
        percentages["T"] = round((scores["T"] / total_tf) * 100)
        percentages["F"] = round((scores["F"] / total_tf) * 100)
    else:
        percentages["T"] = percentages["F"] = 50
    
    # J/P軸
    total_jp = scores["J"] + scores["P"]
    if total_jp > 0:
        percentages["J"] = round((scores["J"] / total_jp) * 100)
        percentages["P"] = round((scores["P"] / total_jp) * 100)
    else:
        percentages["J"] = percentages["P"] = 50
    
    return percentages

