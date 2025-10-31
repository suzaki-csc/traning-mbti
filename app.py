from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from models.models import db, DiagnosisResult, Answer, Question

app = Flask(__name__)
app.config.from_object(Config)

# データベース初期化
db.init_app(app)

# 質問データ
QUESTIONS = [
    # E/I軸（外向-内向）
    {'id': 1, 'text': '人と会うことでエネルギーが湧いてくる', 'axis': 'EI'},
    {'id': 2, 'text': '一人でじっくり考える時間が必要だ', 'axis': 'EI', 'reverse': True},
    {'id': 3, 'text': '初対面の人とも気軽に話せる', 'axis': 'EI'},
    
    # S/N軸（感覚-直感）
    {'id': 4, 'text': '現実的で具体的な情報を重視する', 'axis': 'SN'},
    {'id': 5, 'text': '抽象的な概念やアイデアに興味がある', 'axis': 'SN', 'reverse': True},
    {'id': 6, 'text': '細かいディテールに気づきやすい', 'axis': 'SN'},
    
    # T/F軸（思考-感情）
    {'id': 7, 'text': '論理的な分析を重視して判断する', 'axis': 'TF'},
    {'id': 8, 'text': '人の気持ちを考えて行動する', 'axis': 'TF', 'reverse': True},
    {'id': 9, 'text': '客観的な事実を感情より優先する', 'axis': 'TF'},
    
    # J/P軸（判断-知覚）
    {'id': 10, 'text': '計画を立てて物事を進めるのが好きだ', 'axis': 'JP'},
    {'id': 11, 'text': '柔軟に対応できる自由さが重要だ', 'axis': 'JP', 'reverse': True},
    {'id': 12, 'text': '締め切りを守ることを優先する', 'axis': 'JP'}
]

MBTI_DESCRIPTIONS = {
    'INTJ': '戦略家 - 独創的で戦略的な思考を持つ完璧主義者。長期的なビジョンを持ち、論理的に物事を分析します。独立心が強く、知的好奇心に満ちた革新的な問題解決者です。効率性と改善を重視し、目標達成のために計画的に行動します。',
    'INTP': '論理学者 - 知識を追求する革新的な発明家。抽象的な理論や複雑なシステムを理解することに長けています。独立的で分析的、客観的な視点から物事を捉えます。新しいアイデアを探求し、論理的な一貫性を大切にします。',
    'ENTJ': '指揮官 - 大胆で想像力豊かな強い意志を持つ指導者。目標達成に向けて組織を動かす天性のリーダーです。効率的で決断力があり、戦略的思考に優れています。困難な課題にも果敢に挑戦し、チームを成功へと導きます。',
    'ENTP': '討論者 - 賢くて好奇心旺盛な思想家。新しい可能性を探求し、知的な議論を楽しみます。機知に富み、創造的で、既成概念にとらわれない柔軟な発想を持ちます。変化を好み、革新的なアイデアを生み出すことに喜びを感じます。',
    'INFJ': '提唱者 - 理想主義的で静かながらも積極的な人。深い洞察力を持ち、人々の成長を支援することに情熱を注ぎます。共感力が高く、他者の感情を理解し、調和を大切にします。理想を実現するために献身的に努力します。',
    'INFP': '仲介者 - 詩的で親切な利他主義者。内面の価値観を大切にし、真実と調和を追求します。創造的で想像力豊かで、理想主義的な世界観を持ちます。他者への思いやりに満ち、自分の信念に忠実に生きようとします。',
    'ENFJ': '主人公 - カリスマ性があり人を励ます指導者。人々の可能性を信じ、成長を支援することに喜びを感じます。共感力が高く、コミュニケーション能力に優れています。調和を重視し、グループをまとめ、前向きな雰囲気を作り出します。',
    'ENFP': '運動家 - 情熱的で創造的な社交的な自由人。新しい経験と可能性を探求することを愛します。熱意と想像力に満ち、人々を鼓舞する力を持ちます。柔軟で適応力があり、変化を楽しむ楽観的な性格です。',
    'ISTJ': '管理者 - 実用的で事実に基づいた信頼できる人。責任感が強く、組織的で几帳面です。伝統と秩序を尊重し、確立された方法を守ります。誠実で忠実、約束を必ず守る信頼できるパートナーです。詳細に注意を払い、計画的に物事を進めます。',
    'ISFJ': '擁護者 - 献身的で温かい防衛者。他者への奉仕と支援に喜びを見出します。思いやり深く、責任感が強く、細やかな気配りができます。伝統を大切にし、調和を保つことを重視します。信頼できる誠実な支援者です。',
    'ESTJ': '幹部 - 優れた管理能力を持つ代表者。組織的で実用的、効率的に物事を管理します。明確なルールと秩序を重視し、リーダーシップを発揮します。責任感が強く、決断力があり、目標達成に向けて着実に進みます。',
    'ESFJ': '領事 - 非常に思いやりがあり社交的で人気者。人々との調和を大切にし、他者の幸福を気にかけます。協力的で責任感が強く、グループの雰囲気作りが得意です。伝統を尊重し、社会的な期待に応えようと努力します。',
    'ISTP': '巨匠 - 大胆で実践的な実験者。機械的なことや技術的なことに興味を持ち、実際に手を動かして学びます。論理的で分析的、問題解決能力に優れています。柔軟で適応力があり、現実的なアプローチを取ります。',
    'ISFP': '冒険家 - 柔軟で魅力的な芸術家。美的感覚に優れ、現在の瞬間を大切にします。思いやりがあり、調和を重視し、自分の価値観に忠実です。創造的で表現力豊かで、新しい経験を通じて自己を表現します。',
    'ESTP': '起業家 - 賢くてエネルギッシュで知覚的な人。行動的で大胆、リスクを恐れません。現実的で実践的な問題解決を得意とし、状況に素早く適応します。社交的で機転が利き、スリルと興奮を求めます。',
    'ESFP': 'エンターテイナー - 自発的でエネルギッシュで熱心な人。人生を楽しみ、他者と喜びを分かち合うことを愛します。社交的で友好的、周囲を明るくする存在です。現在の瞬間を大切にし、柔軟で適応力があります。'
}

def calculate_mbti_type(answers):
    """回答からMBTIタイプを判定"""
    scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    
    for question in QUESTIONS:
        question_id = question['id']
        axis = question['axis']
        answer_value = int(answers.get(str(question_id), 0))
        
        # reverse質問の場合は値を反転
        if question.get('reverse'):
            answer_value = -answer_value
        
        # 正の値: 軸の前者にポイント、負の値: 軸の後者にポイント
        if answer_value > 0:
            scores[axis[0]] += answer_value
        elif answer_value < 0:
            scores[axis[1]] += abs(answer_value)
    
    # 各軸で優勢な方を選択
    mbti_type = ''
    mbti_type += 'E' if scores['E'] >= scores['I'] else 'I'
    mbti_type += 'S' if scores['S'] >= scores['N'] else 'N'
    mbti_type += 'T' if scores['T'] >= scores['F'] else 'F'
    mbti_type += 'J' if scores['J'] >= scores['P'] else 'P'
    
    return {'type': mbti_type, 'scores': scores}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnosis')
def diagnosis():
    return render_template('diagnosis.html', questions=QUESTIONS)

@app.route('/submit', methods=['POST'])
def submit():
    answers = request.form.to_dict()
    user_name = answers.pop('user_name', '')
    
    # MBTI判定
    result = calculate_mbti_type(answers)
    mbti_type = result['type']
    scores = result['scores']
    
    # データベースに保存
    try:
        user_ip = request.remote_addr
        
        # 診断結果を保存
        diagnosis_result = DiagnosisResult(
            user_name=user_name,
            mbti_type=mbti_type,
            e_score=scores['E'],
            i_score=scores['I'],
            s_score=scores['S'],
            n_score=scores['N'],
            t_score=scores['T'],
            f_score=scores['F'],
            j_score=scores['J'],
            p_score=scores['P'],
            user_ip=user_ip
        )
        db.session.add(diagnosis_result)
        db.session.flush()  # IDを取得するためにflush
        
        # 回答詳細を保存
        for question_id, answer_value in answers.items():
            if question_id.isdigit():
                answer = Answer(
                    result_id=diagnosis_result.id,
                    question_id=int(question_id),
                    answer_value=int(answer_value)
                )
                db.session.add(answer)
        
        db.session.commit()
        
        return redirect(url_for('result', id=diagnosis_result.id))
    except Exception as e:
        db.session.rollback()
        return f"エラーが発生しました: {str(e)}", 500

@app.route('/result/<int:id>')
def result(id):
    try:
        diagnosis_result = DiagnosisResult.query.get_or_404(id)
        
        mbti_type = diagnosis_result.mbti_type
        description = MBTI_DESCRIPTIONS.get(mbti_type, 'タイプの説明はありません')
        scores = {
            'E': diagnosis_result.e_score,
            'I': diagnosis_result.i_score,
            'S': diagnosis_result.s_score,
            'N': diagnosis_result.n_score,
            'T': diagnosis_result.t_score,
            'F': diagnosis_result.f_score,
            'J': diagnosis_result.j_score,
            'P': diagnosis_result.p_score
        }
        
        return render_template('result.html', mbti_type=mbti_type, description=description, scores=scores, result_id=id)
    except Exception as e:
        return f"エラーが発生しました: {str(e)}", 500

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 認証チェック
        if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin/login.html', error='ユーザー名またはパスワードが間違っています')
    
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    try:
        search = request.args.get('search', '')
        
        if search:
            results = DiagnosisResult.query.filter(
                (DiagnosisResult.user_name.like(f'%{search}%')) |
                (DiagnosisResult.mbti_type.like(f'%{search}%'))
            ).order_by(DiagnosisResult.diagnosed_at.desc()).all()
        else:
            results = DiagnosisResult.query.order_by(DiagnosisResult.diagnosed_at.desc()).all()
        
        return render_template('admin/dashboard.html', results=results, search=search)
    except Exception as e:
        return f"エラーが発生しました: {str(e)}", 500

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
