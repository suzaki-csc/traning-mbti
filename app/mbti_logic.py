"""
MBTI判定ロジック
"""


def calculate_mbti_type(answers):
    """
    回答からMBTIタイプを判定する

    Args:
        answers: list of dict [{'axis': str, 'score': int}, ...]

    Returns:
        dict: {
            'type': str,  # 例: 'INTJ'
            'scores': {
                'E': int, 'I': int,
                'S': int, 'N': int,
                'T': int, 'F': int,
                'J': int, 'P': int
            }
        }
    """
    # 各軸のスコアを初期化
    scores = {
        'E': 0, 'I': 0,
        'S': 0, 'N': 0,
        'T': 0, 'F': 0,
        'J': 0, 'P': 0
    }

    # 回答からスコアを合算
    for answer in answers:
        axis = answer['axis']
        score = answer['score']
        scores[axis] += score

    # 各軸ペアで優位な軸を判定
    mbti_type = ''
    mbti_type += 'E' if scores['E'] >= scores['I'] else 'I'
    mbti_type += 'S' if scores['S'] >= scores['N'] else 'N'
    mbti_type += 'T' if scores['T'] >= scores['F'] else 'F'
    mbti_type += 'J' if scores['J'] >= scores['P'] else 'P'

    return {
        'type': mbti_type,
        'scores': scores
    }


def get_type_description(mbti_type):
    """
    MBTIタイプの説明を返す

    Args:
        mbti_type: str (例: 'INTJ')

    Returns:
        dict: {
            'name': str,
            'description': str
        }
    """
    descriptions = {
        'INTJ': {
            'name': '建築家',
            'description': (
                '戦略的な思考と高い独立性を持つタイプ。'
                '長期的なビジョンを持ち、効率的に目標を達成します。'
                '論理的で分析的、常に知識を深めることを好みます。'
            )
        },
        'INTP': {
            'name': '論理学者',
            'description': (
                '知的好奇心が旺盛で、理論や抽象的な概念を探求するタイプ。'
                '柔軟な思考で問題を分析し、独創的な解決策を見出します。'
                '客観的で論理的な思考を重視します。'
            )
        },
        'ENTJ': {
            'name': '指揮官',
            'description': (
                'リーダーシップと決断力に優れたタイプ。'
                '明確なビジョンを持ち、効率的に組織を動かします。'
                '論理的で戦略的、目標達成に向けて積極的に行動します。'
            )
        },
        'ENTP': {
            'name': '討論者',
            'description': (
                '知的な議論と新しいアイデアを楽しむタイプ。'
                '創造的で革新的、様々な可能性を探求します。'
                '柔軟な思考で問題解決に取り組みます。'
            )
        },
        'INFJ': {
            'name': '提唱者',
            'description': (
                '理想主義的で思慮深いタイプ。'
                '他者への深い共感力を持ち、人々を励まし導きます。'
                '内省的でありながら、強い信念に基づいて行動します。'
            )
        },
        'INFP': {
            'name': '仲介者',
            'description': (
                '理想主義的で創造的なタイプ。'
                '自分の価値観を大切にし、調和を求めます。'
                '想像力豊かで、他者の可能性を信じ、'
                '支援することを喜びとします。'
            )
        },
        'ENFJ': {
            'name': '主人公',
            'description': (
                'カリスマ性とリーダーシップを持つタイプ。'
                '他者の成長を支援し、調和的なコミュニティを築きます。'
                '共感力が高く、人々を励まし導くことに情熱を注ぎます。'
            )
        },
        'ENFP': {
            'name': '運動家',
            'description': (
                '熱意と創造性に満ちたタイプ。'
                '新しい可能性を探求し、人々とのつながりを大切にします。'
                '自由な発想で、周囲を励まし、楽しい雰囲気を作ります。'
            )
        },
        'ISTJ': {
            'name': '管理者',
            'description': (
                '責任感が強く、実直なタイプ。'
                '伝統と秩序を重んじ、計画的に物事を進めます。'
                '信頼性が高く、着実に目標を達成する実務家です。'
            )
        },
        'ISFJ': {
            'name': '擁護者',
            'description': (
                '献身的で思いやり深いタイプ。'
                '他者のニーズに敏感で、サポートすることに喜びを感じます。'
                '責任感が強く、調和的な環境を大切にします。'
            )
        },
        'ESTJ': {
            'name': '幹部',
            'description': (
                '実務的で組織的なタイプ。'
                '明確なルールと秩序を重視し、効率的に物事を管理します。'
                'リーダーシップがあり、責任感を持って目標を達成します。'
            )
        },
        'ESFJ': {
            'name': '領事官',
            'description': (
                '社交的で協調性の高いタイプ。'
                '他者との調和を重視し、コミュニティに貢献します。'
                '思いやりがあり、'
                '人々のニーズに応えることに喜びを感じます。'
            )
        },
        'ISTP': {
            'name': '巨匠',
            'description': (
                '実践的で分析的なタイプ。'
                '手を動かして問題を解決することを好みます。'
                '柔軟で適応力があり、冷静に状況を判断します。'
            )
        },
        'ISFP': {
            'name': '冒険家',
            'description': (
                '芸術的で柔軟なタイプ。'
                '美的センスに優れ、今を楽しむことを大切にします。'
                '控えめでありながら、自分の価値観に忠実に生きます。'
            )
        },
        'ESTP': {
            'name': '起業家',
            'description': (
                '行動的で現実的なタイプ。'
                'リスクを恐れず、素早く決断し行動します。'
                '社交的でエネルギッシュ、刺激的な経験を求めます。'
            )
        },
        'ESFP': {
            'name': 'エンターテイナー',
            'description': (
                '陽気で社交的なタイプ。'
                '人々を楽しませることが得意で、場を盛り上げます。'
                '今を楽しみ、周囲にポジティブなエネルギーを与えます。'
            )
        }
    }

    return descriptions.get(mbti_type, {
        'name': '未定義',
        'description': 'このタイプの説明はまだ用意されていません。'
    })


def get_axis_percentages(scores):
    """
    各軸ペアのパーセンテージを計算

    Args:
        scores: dict {'E': int, 'I': int, ...}

    Returns:
        dict: {
            'EI': {'E': percentage, 'I': percentage},
            'SN': {'S': percentage, 'N': percentage},
            'TF': {'T': percentage, 'F': percentage},
            'JP': {'J': percentage, 'P': percentage}
        }
    """
    result = {}

    # E-I軸
    ei_total = scores['E'] + scores['I']
    result['EI'] = {
        'E': round(
            (scores['E'] / ei_total * 100) if ei_total > 0 else 0, 1),
        'I': round(
            (scores['I'] / ei_total * 100) if ei_total > 0 else 0, 1)
    }

    # S-N軸
    sn_total = scores['S'] + scores['N']
    result['SN'] = {
        'S': round(
            (scores['S'] / sn_total * 100) if sn_total > 0 else 0, 1),
        'N': round(
            (scores['N'] / sn_total * 100) if sn_total > 0 else 0, 1)
    }

    # T-F軸
    tf_total = scores['T'] + scores['F']
    result['TF'] = {
        'T': round(
            (scores['T'] / tf_total * 100) if tf_total > 0 else 0, 1),
        'F': round(
            (scores['F'] / tf_total * 100) if tf_total > 0 else 0, 1)
    }

    # J-P軸
    jp_total = scores['J'] + scores['P']
    result['JP'] = {
        'J': round(
            (scores['J'] / jp_total * 100) if jp_total > 0 else 0, 1),
        'P': round(
            (scores['P'] / jp_total * 100) if jp_total > 0 else 0, 1)
    }

    return result
