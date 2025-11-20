"""
初期データ投入スクリプト

このモジュールは、アプリケーションの初期データ（カテゴリと問題）を
データベースに投入するための関数を提供します。
"""

from app import db
from app.models import Category, Question


def create_initial_categories():
    """
    初期カテゴリを作成します。
    
    Returns:
        dict: カテゴリ名をキー、Categoryオブジェクトを値とする辞書
    """
    categories_data = [
        {
            'name': 'セキュリティ',
            'description': '情報セキュリティに関する基礎知識を学びます'
        },
        {
            'name': 'IT基礎',
            'description': 'ITの基礎的な知識を学びます'
        },
        {
            'name': 'プログラミング',
            'description': 'プログラミングの基礎知識を学びます'
        }
    ]
    
    categories = {}
    for cat_data in categories_data:
        # 既に存在する場合はスキップ
        category = Category.query.filter_by(name=cat_data['name']).first()
        if not category:
            category = Category(
                name=cat_data['name'],
                description=cat_data['description']
            )
            db.session.add(category)
        categories[cat_data['name']] = category
    
    db.session.commit()
    return categories


def create_security_questions(category):
    """
    セキュリティカテゴリの問題を作成します。
    
    Args:
        category: Categoryオブジェクト
    """
    questions_data = [
        {
            'question_text': 'XSS（Cross-Site Scripting）攻撃とは何ですか？',
            'option_a': 'データベースに不正なSQL文を注入する攻撃',
            'option_b': 'Webページに悪意のあるスクリプトを注入する攻撃',
            'option_c': 'パスワードを総当たりで試行する攻撃',
            'option_d': 'ネットワーク経由でコンピュータに侵入する攻撃',
            'correct_answer': 'B',
            'explanation': 'XSSは、Webアプリケーションの脆弱性を利用して、悪意のあるJavaScriptコードをWebページに注入する攻撃です。ユーザーのブラウザでスクリプトが実行され、セッション情報の窃取などが行われます。'
        },
        {
            'question_text': 'CSRF（Cross-Site Request Forgery）攻撃を防ぐ方法として最も効果的なのはどれですか？',
            'option_a': 'パスワードを複雑にする',
            'option_b': 'CSRFトークンを使用する',
            'option_c': 'HTTPSを使用する',
            'option_d': 'ファイアウォールを設置する',
            'correct_answer': 'B',
            'explanation': 'CSRFトークンは、リクエストの正当性を検証するための一意のトークンです。各フォームにトークンを埋め込み、サーバー側で検証することで、第三者が勝手にリクエストを送信することを防ぎます。'
        },
        {
            'question_text': 'SQLインジェクション攻撃とは何ですか？',
            'option_a': 'Webページにスクリプトを注入する攻撃',
            'option_b': 'データベースに不正なSQL文を注入する攻撃',
            'option_c': 'メールにウイルスを添付する攻撃',
            'option_d': 'パスワードを推測する攻撃',
            'correct_answer': 'B',
            'explanation': 'SQLインジェクションは、アプリケーションの入力フィールドに悪意のあるSQL文を入力し、データベースを不正に操作する攻撃です。パラメータ化クエリやプリペアドステートメントを使用することで防ぐことができます。'
        },
        {
            'question_text': 'パスワードリスト攻撃とは何ですか？',
            'option_a': '辞書に載っている単語をパスワードとして試行する攻撃',
            'option_b': '過去に漏洩したパスワードのリストを使用する攻撃',
            'option_c': 'パスワードを総当たりで試行する攻撃',
            'option_d': 'パスワードを推測する攻撃',
            'correct_answer': 'B',
            'explanation': 'パスワードリスト攻撃は、過去の情報漏洩事件で流出したユーザーIDとパスワードの組み合わせリストを使用して、他のサービスへの不正ログインを試みる攻撃です。同じパスワードを複数のサービスで使い回していると被害を受けやすくなります。'
        },
        {
            'question_text': 'レインボーテーブルとは何ですか？',
            'option_a': 'パスワードのハッシュ値と平文の対応表',
            'option_b': 'ネットワークの接続状態を表示する表',
            'option_c': 'セキュリティイベントを記録する表',
            'option_d': 'ユーザーの権限を管理する表',
            'correct_answer': 'A',
            'explanation': 'レインボーテーブルは、ハッシュ値から元のパスワードを逆引きするための事前計算済みのテーブルです。ソルト（salt）を使用することで、レインボーテーブル攻撃を防ぐことができます。'
        },
        {
            'question_text': 'ゼロトラストセキュリティモデルの基本原則は何ですか？',
            'option_a': 'すべての通信を信頼する',
            'option_b': '内部ネットワークは安全と仮定する',
            'option_c': 'すべてのアクセスを検証し、信頼しない',
            'option_d': '外部からのアクセスのみを監視する',
            'correct_answer': 'C',
            'explanation': 'ゼロトラストは「信頼しない、常に検証する」という考え方です。内部ネットワークであっても、すべてのアクセスを検証し、最小権限の原則に基づいてアクセスを制御します。'
        },
        {
            'question_text': '多要素認証（MFA）に含まれる要素として正しい組み合わせはどれですか？',
            'option_a': 'パスワードとユーザー名',
            'option_b': '知識（パスワード）、所有物（スマートフォン）、生体認証（指紋）のうち2つ以上',
            'option_c': 'メールアドレスとパスワード',
            'option_d': 'IPアドレスとユーザー名',
            'correct_answer': 'B',
            'explanation': '多要素認証は、知識（知っているもの）、所有物（持っているもの）、生体認証（本人であること）の3つの要素のうち、2つ以上を組み合わせて認証する方式です。セキュリティを大幅に向上させることができます。'
        },
        {
            'question_text': 'DPIA（Data Protection Impact Assessment）とは何ですか？',
            'option_a': 'データベースのパフォーマンスを評価する手法',
            'option_b': '個人データの処理がプライバシーに与える影響を評価する手法',
            'option_c': 'ネットワークのセキュリティを評価する手法',
            'option_d': 'アプリケーションの脆弱性を評価する手法',
            'correct_answer': 'B',
            'explanation': 'DPIAは、個人データの処理が個人のプライバシーや権利に与える影響を事前に評価する手法です。GDPR（EU一般データ保護規則）などで義務付けられています。'
        },
        {
            'question_text': 'SAST（Static Application Security Testing）とは何ですか？',
            'option_a': '実行中のアプリケーションをテストする手法',
            'option_b': 'ソースコードを静的解析して脆弱性を検出する手法',
            'option_c': 'ネットワーク経由でアプリケーションをテストする手法',
            'option_d': 'データベースのセキュリティをテストする手法',
            'correct_answer': 'B',
            'explanation': 'SASTは、ソースコードを実行せずに静的解析を行い、潜在的な脆弱性を検出する手法です。開発の早期段階で問題を発見できるため、コストを抑えながらセキュリティを向上させることができます。'
        },
        {
            'question_text': 'DAST（Dynamic Application Security Testing）とは何ですか？',
            'option_a': 'ソースコードを静的解析する手法',
            'option_b': '実行中のアプリケーションを外部からテストする手法',
            'option_c': 'データベースの構造を分析する手法',
            'option_d': 'ネットワークの設定を確認する手法',
            'correct_answer': 'B',
            'explanation': 'DASTは、実行中のアプリケーションに対して外部から攻撃を試み、実際の動作環境で脆弱性を検出する手法です。SASTと組み合わせることで、より包括的なセキュリティテストが可能になります。'
        },
        {
            'question_text': 'CVE（Common Vulnerabilities and Exposures）とは何ですか？',
            'option_a': 'セキュリティパッチの配布システム',
            'option_b': '脆弱性に一意の識別番号を付与するシステム',
            'option_c': 'ウイルス対策ソフトのデータベース',
            'option_d': 'ファイアウォールの設定ファイル',
            'correct_answer': 'B',
            'explanation': 'CVEは、公開されているソフトウェアの脆弱性に一意の識別番号（CVE-ID）を付与するシステムです。脆弱性の情報共有や管理を容易にします。'
        },
        {
            'question_text': 'CVSS（Common Vulnerability Scoring System）とは何ですか？',
            'option_a': '脆弱性の深刻度を数値化するシステム',
            'option_b': 'セキュリティパッチの優先順位を決めるシステム',
            'option_c': 'ウイルスの検出率を測定するシステム',
            'option_d': 'ネットワークの帯域幅を測定するシステム',
            'correct_answer': 'A',
            'explanation': 'CVSSは、脆弱性の深刻度を0.0から10.0のスコアで評価するシステムです。スコアが高いほど深刻な脆弱性とされ、対応の優先順位を決める際の指標として使用されます。'
        },
        {
            'question_text': 'フィッシング攻撃とは何ですか？',
            'option_a': '物理的にコンピュータに侵入する攻撃',
            'option_b': '偽のWebサイトやメールで個人情報を詐取する攻撃',
            'option_c': 'パスワードを総当たりで試行する攻撃',
            'option_d': 'ネットワークを経由してデータを窃取する攻撃',
            'correct_answer': 'B',
            'explanation': 'フィッシングは、正規の組織を装った偽のメールやWebサイトを使用して、ユーザーから個人情報や認証情報を詐取する攻撃です。URLや送信元アドレスを注意深く確認することが重要です。'
        },
        {
            'question_text': 'スミッシング（Smishing）とは何ですか？',
            'option_a': 'メールを使用したフィッシング攻撃',
            'option_b': 'SMS（ショートメッセージ）を使用したフィッシング攻撃',
            'option_c': 'ソーシャルメディアを使用した攻撃',
            'option_d': '電話を使用した詐欺',
            'correct_answer': 'B',
            'explanation': 'スミッシングは、SMS（ショートメッセージ）を使用したフィッシング攻撃です。スマートフォンの普及に伴い、この手の攻撃が増加しています。不審なリンクをクリックしないことが重要です。'
        },
        {
            'question_text': 'スピアフィッシングとは何ですか？',
            'option_a': '不特定多数を対象としたフィッシング攻撃',
            'option_b': '特定の個人や組織を標的としたフィッシング攻撃',
            'option_c': '自動化されたフィッシング攻撃',
            'option_d': '物理的な侵入を伴う攻撃',
            'correct_answer': 'B',
            'explanation': 'スピアフィッシングは、特定の個人や組織を標的とした、より高度なフィッシング攻撃です。標的の情報を事前に収集し、より信頼性の高い偽装を行うため、通常のフィッシングよりも危険です。'
        },
        {
            'question_text': 'ランサムウェアとは何ですか？',
            'option_a': 'コンピュータの動作を監視するマルウェア',
            'option_b': 'データを暗号化し、身代金を要求するマルウェア',
            'option_c': 'パスワードを窃取するマルウェア',
            'option_d': '広告を表示するマルウェア',
            'correct_answer': 'B',
            'explanation': 'ランサムウェアは、コンピュータのファイルを暗号化し、復号化のための身代金を要求するマルウェアです。定期的なバックアップを取得することで、被害を最小限に抑えることができます。'
        },
        {
            'question_text': 'サプライチェーン攻撃とは何ですか？',
            'option_a': '直接的な攻撃手法',
            'option_b': '信頼できるサプライヤーやパートナーを経由した攻撃',
            'option_c': 'ネットワーク経由の攻撃',
            'option_d': '物理的な侵入を伴う攻撃',
            'correct_answer': 'B',
            'explanation': 'サプライチェーン攻撃は、信頼できるサプライヤーやパートナーのシステムに侵入し、そこを経由して最終的な標的を攻撃する手法です。ソフトウェアの更新やサプライヤーのセキュリティ管理が重要です。'
        },
        {
            'question_text': 'ソーシャルエンジニアリングとは何ですか？',
            'option_a': '技術的な脆弱性を利用する攻撃',
            'option_b': '人間の心理的な弱点を利用する攻撃',
            'option_c': 'ネットワークの脆弱性を利用する攻撃',
            'option_d': '物理的な侵入を伴う攻撃',
            'correct_answer': 'B',
            'explanation': 'ソーシャルエンジニアリングは、技術的な脆弱性ではなく、人間の心理的な弱点（好奇心、信頼、恐怖など）を利用して情報を入手する攻撃手法です。セキュリティ教育が重要です。'
        },
        {
            'question_text': 'セキュアコーディングとは何ですか？',
            'option_a': '高速なコードを書くこと',
            'option_b': 'セキュリティを考慮したコードを書くこと',
            'option_c': '短いコードを書くこと',
            'option_d': 'コメントが多いコードを書くこと',
            'correct_answer': 'B',
            'explanation': 'セキュアコーディングは、セキュリティを考慮したコードを書くことです。入力検証、適切なエラーハンドリング、暗号化の使用など、脆弱性を生み出さないコーディング手法を実践します。'
        },
        {
            'question_text': '侵入テスト（Penetration Testing）とは何ですか？',
            'option_a': 'ソースコードを静的解析すること',
            'option_b': '実際に攻撃を試みて脆弱性を検証すること',
            'option_c': 'ネットワークの設定を確認すること',
            'option_d': 'ログファイルを分析すること',
            'correct_answer': 'B',
            'explanation': '侵入テストは、実際に攻撃者の視点からシステムに侵入を試み、脆弱性を発見・検証するテストです。定期的に実施することで、セキュリティの向上が期待できます。'
        },
        {
            'question_text': 'WAF（Web Application Firewall）とは何ですか？',
            'option_a': 'データベースを保護するファイアウォール',
            'option_b': 'Webアプリケーションへの攻撃を検出・防御するシステム',
            'option_c': 'ネットワーク全体を保護するファイアウォール',
            'option_d': 'メールをフィルタリングするシステム',
            'correct_answer': 'B',
            'explanation': 'WAFは、WebアプリケーションへのHTTP/HTTPS通信を監視し、SQLインジェクションやXSSなどの攻撃を検出・防御するシステムです。アプリケーションの前段に配置されます。'
        },
        {
            'question_text': 'IAM（Identity and Access Management）とは何ですか？',
            'option_a': 'ネットワークの管理システム',
            'option_b': 'ユーザーの認証とアクセス権限を管理するシステム',
            'option_c': 'データベースの管理システム',
            'option_d': 'サーバーの監視システム',
            'correct_answer': 'B',
            'explanation': 'IAMは、ユーザーの認証（本人確認）と認可（アクセス権限の管理）を統合的に管理するシステムです。適切なIAMの実装により、最小権限の原則に基づいたアクセス制御が可能になります。'
        }
    ]
    
    # 既存の問題数を確認
    existing_count = Question.query.filter_by(category_id=category.id).count()
    
    # 既に問題が存在する場合はスキップ
    if existing_count >= len(questions_data):
        return
    
    # 問題を作成
    for q_data in questions_data:
        # 既に同じ問題が存在するかチェック
        existing = Question.query.filter_by(
            category_id=category.id,
            question_text=q_data['question_text']
        ).first()
        
        if not existing:
            question = Question(
                category_id=category.id,
                question_text=q_data['question_text'],
                option_a=q_data['option_a'],
                option_b=q_data['option_b'],
                option_c=q_data['option_c'],
                option_d=q_data['option_d'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation']
            )
            db.session.add(question)
    
    db.session.commit()


def create_it_basic_questions(category):
    """
    IT基礎カテゴリの問題を作成します。
    
    Args:
        category: Categoryオブジェクト
    """
    # IT基礎カテゴリの問題は後で追加可能
    # 現在は空の実装
    pass


def create_programming_questions(category):
    """
    プログラミングカテゴリの問題を作成します。
    
    Args:
        category: Categoryオブジェクト
    """
    # プログラミングカテゴリの問題は後で追加可能
    # 現在は空の実装
    pass


def init_data():
    """
    すべての初期データを作成します。
    """
    print('初期カテゴリを作成中...')
    categories = create_initial_categories()
    
    print('セキュリティカテゴリの問題を作成中...')
    create_security_questions(categories['セキュリティ'])
    
    print('IT基礎カテゴリの問題を作成中...')
    create_it_basic_questions(categories['IT基礎'])
    
    print('プログラミングカテゴリの問題を作成中...')
    create_programming_questions(categories['プログラミング'])
    
    print('初期データの作成が完了しました。')

