"""
診断用の質問データ
"""


def get_questions():
    """
    MBTI診断の質問リストを取得
    
    Returns:
        list: 質問データのリスト（12問）
    """
    questions = [
        # E/I軸 - 外向性/内向性（3問）
        {
            "id": 1,
            "text": "初対面の人との会話は楽しいですか？",
            "options": [
                {"text": "とても楽しい", "axis": "E", "score": 3},
                {"text": "まあまあ楽しい", "axis": "E", "score": 1},
                {"text": "少し苦手", "axis": "I", "score": 1},
                {"text": "かなり苦手", "axis": "I", "score": 3}
            ]
        },
        {
            "id": 2,
            "text": "大勢の集まりと少人数の集まり、どちらが好きですか？",
            "options": [
                {"text": "大勢の集まりが好き", "axis": "E", "score": 3},
                {"text": "どちらかといえば大勢", "axis": "E", "score": 1},
                {"text": "どちらかといえば少人数", "axis": "I", "score": 1},
                {"text": "少人数の集まりが好き", "axis": "I", "score": 3}
            ]
        },
        {
            "id": 3,
            "text": "休日は外出するのと家でゆっくり過ごすのとどちらが好きですか？",
            "options": [
                {"text": "外出することが多い", "axis": "E", "score": 3},
                {"text": "どちらかといえば外出", "axis": "E", "score": 1},
                {"text": "どちらかといえば家", "axis": "I", "score": 1},
                {"text": "家でゆっくりが好き", "axis": "I", "score": 3}
            ]
        },
        
        # S/N軸 - 感覚/直観（3問）
        {
            "id": 4,
            "text": "新しいことを学ぶとき、具体例と理論、どちらから入りたいですか？",
            "options": [
                {"text": "具体例から学びたい", "axis": "S", "score": 3},
                {"text": "どちらかといえば具体例", "axis": "S", "score": 1},
                {"text": "どちらかといえば理論", "axis": "N", "score": 1},
                {"text": "理論から学びたい", "axis": "N", "score": 3}
            ]
        },
        {
            "id": 5,
            "text": "物事を説明するとき、詳細な事実と全体像、どちらを重視しますか？",
            "options": [
                {"text": "詳細な事実を重視", "axis": "S", "score": 3},
                {"text": "どちらかといえば事実", "axis": "S", "score": 1},
                {"text": "どちらかといえば全体像", "axis": "N", "score": 1},
                {"text": "全体像を重視", "axis": "N", "score": 3}
            ]
        },
        {
            "id": 6,
            "text": "現実的で実用的なアイデアと、革新的で未来志向のアイデア、どちらに惹かれますか？",
            "options": [
                {"text": "現実的・実用的", "axis": "S", "score": 3},
                {"text": "どちらかといえば実用的", "axis": "S", "score": 1},
                {"text": "どちらかといえば革新的", "axis": "N", "score": 1},
                {"text": "革新的・未来志向", "axis": "N", "score": 3}
            ]
        },
        
        # T/F軸 - 思考/感情（3問）
        {
            "id": 7,
            "text": "意思決定をするとき、論理と感情、どちらを重視しますか？",
            "options": [
                {"text": "論理を重視", "axis": "T", "score": 3},
                {"text": "どちらかといえば論理", "axis": "T", "score": 1},
                {"text": "どちらかといえば感情", "axis": "F", "score": 1},
                {"text": "感情を重視", "axis": "F", "score": 3}
            ]
        },
        {
            "id": 8,
            "text": "友人が悩みを相談してきたとき、解決策と共感、どちらを優先しますか？",
            "options": [
                {"text": "解決策を提示する", "axis": "T", "score": 3},
                {"text": "どちらかといえば解決策", "axis": "T", "score": 1},
                {"text": "どちらかといえば共感", "axis": "F", "score": 1},
                {"text": "共感を示す", "axis": "F", "score": 3}
            ]
        },
        {
            "id": 9,
            "text": "批判的に分析することと、調和を保つこと、どちらが得意ですか？",
            "options": [
                {"text": "批判的に分析", "axis": "T", "score": 3},
                {"text": "どちらかといえば分析", "axis": "T", "score": 1},
                {"text": "どちらかといえば調和", "axis": "F", "score": 1},
                {"text": "調和を保つ", "axis": "F", "score": 3}
            ]
        },
        
        # J/P軸 - 判断/知覚（3問）
        {
            "id": 10,
            "text": "計画を立てて行動するのと、その場の流れに任せるのと、どちらが好きですか？",
            "options": [
                {"text": "計画を立てる", "axis": "J", "score": 3},
                {"text": "どちらかといえば計画", "axis": "J", "score": 1},
                {"text": "どちらかといえば流れに任せる", "axis": "P", "score": 1},
                {"text": "流れに任せる", "axis": "P", "score": 3}
            ]
        },
        {
            "id": 11,
            "text": "仕事や勉強は、締め切り前に余裕を持って終わらせますか？",
            "options": [
                {"text": "いつも余裕を持って終わらせる", "axis": "J", "score": 3},
                {"text": "だいたい余裕がある", "axis": "J", "score": 1},
                {"text": "ギリギリになることが多い", "axis": "P", "score": 1},
                {"text": "いつもギリギリ", "axis": "P", "score": 3}
            ]
        },
        {
            "id": 12,
            "text": "決定を下すことと、選択肢を開いておくこと、どちらが好きですか？",
            "options": [
                {"text": "早く決定を下す", "axis": "J", "score": 3},
                {"text": "どちらかといえば決定", "axis": "J", "score": 1},
                {"text": "どちらかといえば選択肢を残す", "axis": "P", "score": 1},
                {"text": "選択肢を開いておく", "axis": "P", "score": 3}
            ]
        }
    ]
    
    return questions

