"""質問データ定義"""

QUESTIONS = [
    {
        "id": 1,
        "text": "初対面の人と会うとき、あなたは...",
        "options": [
            {"value": "A", "text": "積極的に話しかける", "axis": "E", "score": 2},
            {"value": "B", "text": "相手から話しかけてくれるのを待つ", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 2,
        "text": "新しいプロジェクトを始めるとき、あなたは...",
        "options": [
            {"value": "A", "text": "まず全体像を把握してから細部を詰める", "axis": "N", "score": 2},
            {"value": "B", "text": "具体的な事実やデータから積み上げる", "axis": "S", "score": 2}
        ]
    },
    {
        "id": 3,
        "text": "友人が悩みを相談してきたとき、あなたは...",
        "options": [
            {"value": "A", "text": "解決策を論理的に提案する", "axis": "T", "score": 2},
            {"value": "B", "text": "共感して気持ちに寄り添う", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 4,
        "text": "旅行の計画を立てるとき、あなたは...",
        "options": [
            {"value": "A", "text": "詳細なスケジュールを事前に決める", "axis": "J", "score": 2},
            {"value": "B", "text": "大まかに決めて現地で柔軟に対応する", "axis": "P", "score": 2}
        ]
    },
    {
        "id": 5,
        "text": "週末の過ごし方として、あなたは...",
        "options": [
            {"value": "A", "text": "友人と外出してエネルギーをチャージする", "axis": "E", "score": 2},
            {"value": "B", "text": "一人でゆっくり過ごしてリフレッシュする", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 6,
        "text": "本を読むとき、あなたは...",
        "options": [
            {"value": "A", "text": "実用書やハウツー本を好む", "axis": "S", "score": 2},
            {"value": "B", "text": "哲学書や抽象的な概念の本を好む", "axis": "N", "score": 2}
        ]
    },
    {
        "id": 7,
        "text": "意思決定をするとき、あなたは...",
        "options": [
            {"value": "A", "text": "客観的な基準と論理を重視する", "axis": "T", "score": 2},
            {"value": "B", "text": "関係者の感情や価値観を考慮する", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 8,
        "text": "仕事のデスク周りは...",
        "options": [
            {"value": "A", "text": "いつも整理整頓されている", "axis": "J", "score": 2},
            {"value": "B", "text": "必要なものが見つかればOK", "axis": "P", "score": 2}
        ]
    },
    {
        "id": 9,
        "text": "グループディスカッションでは...",
        "options": [
            {"value": "A", "text": "積極的に発言してリードする", "axis": "E", "score": 2},
            {"value": "B", "text": "じっくり考えてから発言する", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 10,
        "text": "問題解決のアプローチとして...",
        "options": [
            {"value": "A", "text": "過去の経験や実績を参考にする", "axis": "S", "score": 2},
            {"value": "B", "text": "新しい視点や可能性を探る", "axis": "N", "score": 2}
        ]
    },
    {
        "id": 11,
        "text": "批判を受けたとき、あなたは...",
        "options": [
            {"value": "A", "text": "客観的に内容を分析する", "axis": "T", "score": 2},
            {"value": "B", "text": "まず感情的に受け止める", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 12,
        "text": "締め切りに対して、あなたは...",
        "options": [
            {"value": "A", "text": "早めに終わらせて余裕を持ちたい", "axis": "J", "score": 2},
            {"value": "B", "text": "締め切り間際の集中力を活用する", "axis": "P", "score": 2}
        ]
    }
]


MBTI_TYPES = {
    "INTJ": {
        "name": "建築家",
        "description": "戦略的な思考と独立性を持つ完璧主義者。長期的なビジョンを持ち、効率的に目標を達成します。",
        "strengths": ["分析力", "戦略的思考", "独立性"],
        "careers": ["科学者", "エンジニア", "戦略コンサルタント"]
    },
    "INTP": {
        "name": "論理学者",
        "description": "革新的で独創的な思考を持つ知的探求者。理論と抽象的概念を探求することを好みます。",
        "strengths": ["論理的思考", "創造性", "分析力"],
        "careers": ["研究者", "プログラマー", "哲学者"]
    },
    "ENTJ": {
        "name": "指揮官",
        "description": "生まれながらのリーダー。大胆で想像力豊かに、常に道を見つけるか作り出します。",
        "strengths": ["リーダーシップ", "戦略的思考", "決断力"],
        "careers": ["経営者", "弁護士", "起業家"]
    },
    "ENTP": {
        "name": "討論者",
        "description": "賢く好奇心旺盛な思考家。知的挑戦に抵抗できません。",
        "strengths": ["創造性", "柔軟性", "問題解決能力"],
        "careers": ["起業家", "マーケター", "発明家"]
    },
    "INFJ": {
        "name": "提唱者",
        "description": "理想主義者で直観的。世界を変えることを夢見る静かで神秘的な存在。",
        "strengths": ["共感力", "洞察力", "理想主義"],
        "careers": ["カウンセラー", "作家", "人事"]
    },
    "INFP": {
        "name": "仲介者",
        "description": "詩的で親切で利他的。良い目的のためなら全力を尽くします。",
        "strengths": ["創造性", "共感力", "柔軟性"],
        "careers": ["作家", "芸術家", "心理学者"]
    },
    "ENFJ": {
        "name": "主人公",
        "description": "カリスマ的で鼓舞的なリーダー。聴衆を魅了する能力があります。",
        "strengths": ["リーダーシップ", "共感力", "コミュニケーション"],
        "careers": ["教師", "政治家", "人事マネージャー"]
    },
    "ENFP": {
        "name": "運動家",
        "description": "熱心で創造的で社交的な自由人。常に笑顔の理由を見つけます。",
        "strengths": ["創造性", "熱意", "コミュニケーション"],
        "careers": ["マーケター", "俳優", "カウンセラー"]
    },
    "ISTJ": {
        "name": "管理者",
        "description": "実用的で事実重視。信頼性こそが何よりも重要です。",
        "strengths": ["責任感", "組織力", "実用性"],
        "careers": ["会計士", "管理職", "軍人"]
    },
    "ISFJ": {
        "name": "擁護者",
        "description": "非常に献身的で温かい守護者。愛する人を守る準備が常にできています。",
        "strengths": ["献身性", "責任感", "共感力"],
        "careers": ["看護師", "教師", "図書館司書"]
    },
    "ESTJ": {
        "name": "幹部",
        "description": "優れた管理者。物事や人々を管理することに比類なき能力を持ちます。",
        "strengths": ["組織力", "リーダーシップ", "実行力"],
        "careers": ["経営管理", "警察官", "裁判官"]
    },
    "ESFJ": {
        "name": "領事官",
        "description": "非常に思いやりがあり、社交的で人気者。常に助ける準備ができています。",
        "strengths": ["協調性", "責任感", "思いやり"],
        "careers": ["営業", "イベントプランナー", "教師"]
    },
    "ISTP": {
        "name": "巨匠",
        "description": "大胆で実践的な実験者。あらゆる種類の道具の達人です。",
        "strengths": ["実用性", "柔軟性", "問題解決"],
        "careers": ["エンジニア", "整備士", "パイロット"]
    },
    "ISFP": {
        "name": "冒険家",
        "description": "柔軟で魅力的な芸術家。常に新しい経験を探求する準備ができています。",
        "strengths": ["創造性", "柔軟性", "美的センス"],
        "careers": ["芸術家", "デザイナー", "音楽家"]
    },
    "ESTP": {
        "name": "起業家",
        "description": "賢く、エネルギッシュで非常に知覚的。人生を危険と隣り合わせで生きます。",
        "strengths": ["行動力", "柔軟性", "現実的"],
        "careers": ["営業", "起業家", "救急隊員"]
    },
    "ESFP": {
        "name": "エンターテイナー",
        "description": "自発的でエネルギッシュで熱心なエンターテイナー。退屈な瞬間はありません。",
        "strengths": ["社交性", "柔軟性", "楽観性"],
        "careers": ["俳優", "イベントプランナー", "営業"]
    }
}


def get_question_by_id(question_id):
    """IDから質問を取得"""
    for question in QUESTIONS:
        if question['id'] == question_id:
            return question
    return None


def get_total_questions():
    """総質問数を取得"""
    return len(QUESTIONS)

