"""
MBTI診断の質問データ
"""

# 質問データ
QUESTIONS = [
    {
        "id": 1,
        "text": "パーティーや集まりで、あなたは...",
        "options": [
            {"text": "積極的に新しい人と交流する", "axis": "E", "score": 2},
            {"text": "知っている人と話す", "axis": "E", "score": 1},
            {"text": "静かに観察していることが多い", "axis": "I", "score": 1},
            {"text": "一人で過ごす方が好き", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 2,
        "text": "問題に直面したとき、あなたは...",
        "options": [
            {"text": "具体的な事実とデータを重視する", "axis": "S", "score": 2},
            {"text": "過去の経験を参考にする", "axis": "S", "score": 1},
            {"text": "直感的に解決策を探る", "axis": "N", "score": 1},
            {"text": "可能性や全体像を考える", "axis": "N", "score": 2}
        ]
    },
    {
        "id": 3,
        "text": "決断を下すとき、あなたは...",
        "options": [
            {"text": "論理的な分析を優先する", "axis": "T", "score": 2},
            {"text": "客観的に判断する", "axis": "T", "score": 1},
            {"text": "人への影響を考える", "axis": "F", "score": 1},
            {"text": "感情や価値観を重視する", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 4,
        "text": "計画について、あなたは...",
        "options": [
            {"text": "詳細な計画を立てて実行する", "axis": "J", "score": 2},
            {"text": "大まかな予定を決める", "axis": "J", "score": 1},
            {"text": "柔軟に対応したい", "axis": "P", "score": 1},
            {"text": "流れに任せる方が好き", "axis": "P", "score": 2}
        ]
    },
    {
        "id": 5,
        "text": "週末の過ごし方として好きなのは...",
        "options": [
            {"text": "友人と外出して活動的に過ごす", "axis": "E", "score": 2},
            {"text": "少人数で楽しく過ごす", "axis": "E", "score": 1},
            {"text": "一人で趣味に没頭する", "axis": "I", "score": 1},
            {"text": "静かに自宅でリラックスする", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 6,
        "text": "新しいことを学ぶとき、あなたは...",
        "options": [
            {"text": "段階的に実践しながら学ぶ", "axis": "S", "score": 2},
            {"text": "具体例から理解する", "axis": "S", "score": 1},
            {"text": "理論や概念から理解する", "axis": "N", "score": 1},
            {"text": "全体像を把握してから深掘りする", "axis": "N", "score": 2}
        ]
    },
    {
        "id": 7,
        "text": "意見の対立があったとき、あなたは...",
        "options": [
            {"text": "論理的に正しい方を選ぶ", "axis": "T", "score": 2},
            {"text": "効率性を優先する", "axis": "T", "score": 1},
            {"text": "調和を大切にする", "axis": "F", "score": 1},
            {"text": "みんなの気持ちを優先する", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 8,
        "text": "仕事の進め方について、あなたは...",
        "options": [
            {"text": "締切前に余裕を持って完成させる", "axis": "J", "score": 2},
            {"text": "計画的に進める", "axis": "J", "score": 1},
            {"text": "柔軟に調整しながら進める", "axis": "P", "score": 1},
            {"text": "締切ギリギリまで粘る", "axis": "P", "score": 2}
        ]
    },
    {
        "id": 9,
        "text": "エネルギーを充電するには...",
        "options": [
            {"text": "人と話すことでエネルギーを得る", "axis": "E", "score": 2},
            {"text": "グループ活動が好き", "axis": "E", "score": 1},
            {"text": "一人の時間が必要", "axis": "I", "score": 1},
            {"text": "孤独な時間で回復する", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 10,
        "text": "情報を受け取るとき、あなたは...",
        "options": [
            {"text": "詳細や具体的な情報を好む", "axis": "S", "score": 2},
            {"text": "現実的な情報を重視する", "axis": "S", "score": 1},
            {"text": "抽象的なアイデアが好き", "axis": "N", "score": 1},
            {"text": "可能性や意味を探る", "axis": "N", "score": 2}
        ]
    },
    {
        "id": 11,
        "text": "批判を受けたとき、あなたは...",
        "options": [
            {"text": "客観的に分析する", "axis": "T", "score": 2},
            {"text": "改善点を探す", "axis": "T", "score": 1},
            {"text": "個人的に受け止める", "axis": "F", "score": 1},
            {"text": "感情的に反応する", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 12,
        "text": "日常生活において、あなたは...",
        "options": [
            {"text": "ルーティンを守る", "axis": "J", "score": 2},
            {"text": "整理整頓を好む", "axis": "J", "score": 1},
            {"text": "自由に行動する", "axis": "P", "score": 1},
            {"text": "予定を変更することを楽しむ", "axis": "P", "score": 2}
        ]
    }
]


# 軸の説明
AXES_DESCRIPTION = {
    "E": "外向型 (Extraversion) - エネルギーを外部から得る",
    "I": "内向型 (Introversion) - エネルギーを内面から得る",
    "S": "感覚型 (Sensing) - 具体的な事実を重視",
    "N": "直感型 (Intuition) - 可能性やパターンを重視",
    "T": "思考型 (Thinking) - 論理と客観性を重視",
    "F": "感情型 (Feeling) - 価値観と調和を重視",
    "J": "判断型 (Judging) - 計画的で組織的",
    "P": "知覚型 (Perceiving) - 柔軟で適応的"
}


def get_question(question_id):
    """
    指定されたIDの質問を取得

    Args:
        question_id: 質問ID（1-12）

    Returns:
        dict: 質問データ、存在しない場合はNone
    """
    for question in QUESTIONS:
        if question['id'] == question_id:
            return question
    return None


def get_total_questions():
    """
    質問の総数を取得

    Returns:
        int: 質問の総数
    """
    return len(QUESTIONS)
