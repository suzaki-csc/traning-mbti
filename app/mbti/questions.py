"""
質問データと軸マッピング
"""

QUESTIONS = [
    {
        "id": 1,
        "text": "パーティーや集まりでは、積極的に多くの人と話すほうだ",
        "axis": "EI",  # E/I軸
        "direction": "E"  # Eに寄せる質問（肯定的回答でEスコア増加）
    },
    {
        "id": 2,
        "text": "一人で静かに過ごす時間が大切だ",
        "axis": "EI",
        "direction": "I"  # Iに寄せる質問
    },
    {
        "id": 3,
        "text": "具体的な事実やデータを重視する",
        "axis": "SN",
        "direction": "S"
    },
    {
        "id": 4,
        "text": "将来の可能性や全体像を考えることが好きだ",
        "axis": "SN",
        "direction": "N"
    },
    {
        "id": 5,
        "text": "論理的で客観的な判断を重視する",
        "axis": "TF",
        "direction": "T"
    },
    {
        "id": 6,
        "text": "人の感情や気持ちを考慮して決断する",
        "axis": "TF",
        "direction": "F"
    },
    {
        "id": 7,
        "text": "計画を立てて、順序立てて物事を進めたい",
        "axis": "JP",
        "direction": "J"
    },
    {
        "id": 8,
        "text": "柔軟に対応し、臨機応変に行動したい",
        "axis": "JP",
        "direction": "P"
    },
    {
        "id": 9,
        "text": "グループで活動することでエネルギーが湧く",
        "axis": "EI",
        "direction": "E"
    },
    {
        "id": 10,
        "text": "抽象的な概念や理論を考えることが楽しい",
        "axis": "SN",
        "direction": "N"
    },
    {
        "id": 11,
        "text": "決定する前に、じっくり考える時間が必要だ",
        "axis": "EI",
        "direction": "I"
    },
    {
        "id": 12,
        "text": "スケジュールよりも、その場の流れを大事にする",
        "axis": "JP",
        "direction": "P"
    }
]

# 5段階評価の選択肢
ANSWER_OPTIONS = [
    {"value": 5, "label": "強くそう思う"},
    {"value": 4, "label": "そう思う"},
    {"value": 3, "label": "どちらでもない"},
    {"value": 2, "label": "そう思わない"},
    {"value": 1, "label": "全くそう思わない"}
]


def get_question_by_id(question_id):
    """
    IDから質問を取得する
    """
    for q in QUESTIONS:
        if q["id"] == question_id:
            return q
    return None


def get_total_questions():
    """
    総質問数を返す
    """
    return len(QUESTIONS)

