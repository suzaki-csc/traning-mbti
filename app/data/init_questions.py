"""
初期問題データを登録するスクリプト
セキュリティカテゴリの問題20問を登録

注意: このモジュールの関数は app.app_context() 内で呼び出される必要があります
関数の引数として db, Category, Question を受け取ります
"""

def init_security_questions(db, Category, Question):
    """セキュリティカテゴリの問題を登録"""
    
    # 既存のカテゴリを確認
    existing_cat = Category.query.filter_by(name='セキュリティ').first()
    if existing_cat:
        print('セキュリティカテゴリは既に存在します。')
        return existing_cat
    
    # カテゴリを作成
    security_cat = Category(
        name='セキュリティ',
        description='情報セキュリティに関する基礎的な用語と概念を学習します'
    )
    db.session.add(security_cat)
    db.session.commit()
    
    # 問題リスト
    questions = [
        {
            'question_text': 'XSS（クロスサイトスクリプティング）とは何ですか？',
            'option_a': 'データベースに不正なSQLを送信する攻撃',
            'option_b': 'Webサイトに悪意のあるスクリプトを埋め込む攻撃',
            'option_c': 'パスワードを総当たりで解読する攻撃',
            'option_d': 'ネットワーク通信を傍受する攻撃',
            'correct_answer': 'B',
            'explanation': 'XSSは、攻撃者が悪意のあるスクリプト（主にJavaScript）をWebページに埋め込み、他のユーザーのブラウザで実行させる攻撃です。これにより、セッション情報の盗取やフィッシングなどが可能になります。'
        },
        {
            'question_text': 'SQLインジェクションを防ぐ最も効果的な方法は？',
            'option_a': 'ファイアウォールを導入する',
            'option_b': 'パスワードを複雑にする',
            'option_c': 'プリペアドステートメントを使用する',
            'option_d': 'HTTPSを使用する',
            'correct_answer': 'C',
            'explanation': 'プリペアドステートメント（パラメータ化クエリ）を使用することで、SQLとデータを分離し、SQLインジェクション攻撃を防ぐことができます。これは最も基本的で効果的な対策方法です。'
        },
        {
            'question_text': 'CSRF（クロスサイトリクエストフォージェリ）攻撃の説明として正しいものは？',
            'option_a': 'ユーザーの意図しない操作を強制的に実行させる攻撃',
            'option_b': 'パスワードを盗み取る攻撃',
            'option_c': 'ウイルスをダウンロードさせる攻撃',
            'option_d': 'ネットワークを過負荷にする攻撃',
            'correct_answer': 'A',
            'explanation': 'CSRFは、ログイン中のユーザーに対して、本人の意図しない送金や設定変更などの操作を強制的に実行させる攻撃です。CSRFトークンを使用することで防ぐことができます。'
        },
        {
            'question_text': 'パスワードリスト攻撃とは何ですか？',
            'option_a': '辞書にある単語を順番に試す攻撃',
            'option_b': '他サイトから流出したID/パスワードを使い回す攻撃',
            'option_c': 'ランダムな文字列を総当たりで試す攻撃',
            'option_d': 'パスワード管理ソフトを攻撃する手法',
            'correct_answer': 'B',
            'explanation': 'パスワードリスト攻撃は、他のサービスから流出したIDとパスワードのリストを使って不正ログインを試みる攻撃です。多くのユーザーが複数のサービスで同じパスワードを使い回していることを悪用します。'
        },
        {
            'question_text': 'レインボーテーブルとは何ですか？',
            'option_a': '様々な文字列とそのハッシュ値を事前計算したテーブル',
            'option_b': 'ネットワーク通信を色分けして表示するツール',
            'option_c': 'セキュリティリスクを評価する表',
            'option_d': 'パスワードの強度を表示する表',
            'correct_answer': 'A',
            'explanation': 'レインボーテーブルは、パスワードとそのハッシュ値を大量に事前計算して保存したテーブルです。これを使うとハッシュ値からパスワードを高速に逆算できます。ソルトを使用することで対策できます。'
        },
        {
            'question_text': 'ゼロトラストセキュリティモデルの基本原則は？',
            'option_a': '社内ネットワークは全て信頼する',
            'option_b': 'VPNさえ使えば安全',
            'option_c': '全てのアクセスを検証し、何も信頼しない',
            'option_d': 'ファイアウォールだけで防御する',
            'correct_answer': 'C',
            'explanation': 'ゼロトラストは「決して信頼せず、常に検証する」という原則に基づくセキュリティモデルです。社内外を問わず、全てのアクセスを毎回検証することで、より高いセキュリティを実現します。'
        },
        {
            'question_text': '多要素認証（MFA）で使われる「要素」として正しくないものは？',
            'option_a': '知識要素（パスワードなど）',
            'option_b': '所有要素（スマホなど）',
            'option_c': '生体要素（指紋など）',
            'option_d': '時間要素（ログイン時刻など）',
            'correct_answer': 'D',
            'explanation': '多要素認証の3要素は、知識要素（知っているもの）、所有要素（持っているもの）、生体要素（その人自身）です。時間要素は一般的な要素ではありません。'
        },
        {
            'question_text': 'DPIA（データ保護影響評価）の主な目的は？',
            'option_a': 'システムの処理速度を評価する',
            'option_b': '個人データ処理によるプライバシーリスクを評価する',
            'option_c': 'ネットワーク帯域を評価する',
            'option_d': 'データベースの容量を評価する',
            'correct_answer': 'B',
            'explanation': 'DPIAは、個人データの処理活動がプライバシーに与える影響とリスクを事前に評価する手法です。GDPRなどのプライバシー規制で要求されることがあります。'
        },
        {
            'question_text': 'SASTとDASTの違いとして正しいものは？',
            'option_a': 'SASTはソースコード解析、DASTは実行時テスト',
            'option_b': 'SASTは動的解析、DASTは静的解析',
            'option_c': 'SASTは手動テスト、DASTは自動テスト',
            'option_d': 'SASTは本番環境、DASTは開発環境',
            'correct_answer': 'A',
            'explanation': 'SAST（Static Application Security Testing）はソースコードを解析する静的テスト、DAST（Dynamic Application Security Testing）は実際にアプリを動かして脆弱性を探す動的テストです。'
        },
        {
            'question_text': 'CVEとは何を表しますか？',
            'option_a': '暗号化アルゴリズムの略称',
            'option_b': '脆弱性に付与される共通識別子',
            'option_c': 'セキュリティ製品の認証規格',
            'option_d': 'ネットワークプロトコルの名称',
            'correct_answer': 'B',
            'explanation': 'CVE（Common Vulnerabilities and Exposures）は、公開されている脆弱性に付与される共通の識別子です。CVE番号により、脆弱性を一意に特定し、情報共有が容易になります。'
        },
        {
            'question_text': 'CVSSの主な用途は？',
            'option_a': 'ネットワーク速度の測定',
            'option_b': '脆弱性の深刻度を数値化する',
            'option_c': 'データ容量の計算',
            'option_d': 'パスワードの強度評価',
            'correct_answer': 'B',
            'explanation': 'CVSS（Common Vulnerability Scoring System）は、脆弱性の深刻度を0.0〜10.0のスコアで評価する標準的な指標です。優先的に対処すべき脆弱性を判断するのに役立ちます。'
        },
        {
            'question_text': 'フィッシング攻撃の説明として最も適切なものは？',
            'option_a': '偽のWebサイトやメールで個人情報を騙し取る',
            'option_b': 'ネットワークを監視して情報を盗む',
            'option_c': 'ウイルスを使ってファイルを暗号化する',
            'option_d': 'システムに大量のリクエストを送る',
            'correct_answer': 'A',
            'explanation': 'フィッシングは、本物そっくりの偽サイトやメールを使って、ユーザーをだましてパスワードやクレジットカード情報などを入力させる攻撃手法です。'
        },
        {
            'question_text': 'スミッシングとは何ですか？',
            'option_a': 'SMSを使ったフィッシング攻撃',
            'option_b': 'スマートフォンのウイルス',
            'option_c': 'SNSでの誹謗中傷',
            'option_d': 'スパムメールのフィルタリング技術',
            'correct_answer': 'A',
            'explanation': 'スミッシングは、SMS（ショートメッセージ）を使ったフィッシング攻撃です。SMS + Phishing = Smishingという造語で、宅配業者などを装ったメッセージが多く見られます。'
        },
        {
            'question_text': 'スピアフィッシングの特徴は？',
            'option_a': '不特定多数に送信される',
            'option_b': '特定の個人や組織を狙う',
            'option_c': 'ウイルスを添付しない',
            'option_d': '必ず電話で確認される',
            'correct_answer': 'B',
            'explanation': 'スピアフィッシングは、特定の個人や組織を標的にした精巧なフィッシング攻撃です。事前に標的の情報を収集し、信憑性の高いメールを作成するため、見破るのが困難です。'
        },
        {
            'question_text': 'ランサムウェアの主な特徴は？',
            'option_a': 'ファイルを暗号化して身代金を要求する',
            'option_b': 'パスワードを盗み出す',
            'option_c': 'Webサイトを改ざんする',
            'option_d': 'ネットワークを監視する',
            'correct_answer': 'A',
            'explanation': 'ランサムウェアは、感染したコンピュータのファイルを暗号化し、復号のために身代金（Ransom）を要求するマルウェアです。定期的なバックアップが重要な対策となります。'
        },
        {
            'question_text': 'サプライチェーン攻撃とは？',
            'option_a': '物流システムを停止させる攻撃',
            'option_b': '信頼されているソフトウェアや業者を経由した攻撃',
            'option_c': 'ネットワーク機器を直接攻撃する手法',
            'option_d': 'ECサイトのカート機能を狙う攻撃',
            'correct_answer': 'B',
            'explanation': 'サプライチェーン攻撃は、標的企業が信頼している外部ベンダーやソフトウェアを侵害し、それを足がかりに本来の標的を攻撃する手法です。防御が難しい高度な攻撃です。'
        },
        {
            'question_text': 'ソーシャルエンジニアリングとは？',
            'option_a': '人の心理的な隙を突いて情報を得る手法',
            'option_b': 'SNSの機能を開発する技術',
            'option_c': 'ソフトウェアの脆弱性を突く攻撃',
            'option_d': '社会インフラを管理する技術',
            'correct_answer': 'A',
            'explanation': 'ソーシャルエンジニアリングは、技術的な手段ではなく、人間の心理的な隙や信頼関係を悪用して機密情報を入手する手法です。技術的な対策だけでは防げないため、教育が重要です。'
        },
        {
            'question_text': 'セキュアコーディングの主な目的は？',
            'option_a': 'コードの実行速度を上げる',
            'option_b': 'セキュリティ脆弱性を作り込まない',
            'option_c': 'コードの行数を減らす',
            'option_d': 'デザインパターンを適用する',
            'correct_answer': 'B',
            'explanation': 'セキュアコーディングは、開発段階からセキュリティを考慮し、脆弱性を作り込まないようにするプログラミング手法です。入力値の検証やエラー処理などが含まれます。'
        },
        {
            'question_text': '侵入テスト（ペネトレーションテスト）の目的は？',
            'option_a': 'システムの処理速度を測定する',
            'option_b': '実際に攻撃を試してセキュリティの弱点を発見する',
            'option_c': 'ユーザビリティを評価する',
            'option_d': 'データベースの整合性を確認する',
            'correct_answer': 'B',
            'explanation': '侵入テストは、実際の攻撃者の視点でシステムに侵入を試み、セキュリティ上の弱点を発見する手法です。脆弱性診断よりも実践的なアプローチです。'
        },
        {
            'question_text': 'WAF（Web Application Firewall）の主な機能は？',
            'option_a': 'Webアプリケーションへの攻撃を検知・防御する',
            'option_b': 'Webページの表示速度を上げる',
            'option_c': 'データベースをバックアップする',
            'option_d': 'HTTPSを自動設定する',
            'correct_answer': 'A',
            'explanation': 'WAFは、Webアプリケーションへの攻撃（SQLインジェクション、XSSなど）を検知・防御する専用のファイアウォールです。アプリケーション層での防御を提供します。'
        }
    ]
    
    # 問題を登録
    for q_data in questions:
        question = Question(
            category_id=security_cat.id,
            **q_data
        )
        db.session.add(question)
    
    db.session.commit()
    print(f'セキュリティカテゴリに{len(questions)}問を登録しました。')
    return security_cat

def init_it_basics_questions(db, Category, Question):
    """IT基礎カテゴリの問題を登録（サンプル）"""
    existing_cat = Category.query.filter_by(name='IT基礎').first()
    if existing_cat:
        print('IT基礎カテゴリは既に存在します。')
        return existing_cat
    
    it_cat = Category(
        name='IT基礎',
        description='ITの基礎的な知識と用語を学習します'
    )
    db.session.add(it_cat)
    db.session.commit()
    print('IT基礎カテゴリを作成しました。（問題は後で追加してください）')
    return it_cat

def init_programming_questions(db, Category, Question):
    """プログラミングカテゴリの問題を登録（サンプル）"""
    existing_cat = Category.query.filter_by(name='プログラミング').first()
    if existing_cat:
        print('プログラミングカテゴリは既に存在します。')
        return existing_cat
    
    prog_cat = Category(
        name='プログラミング',
        description='プログラミングの基本概念を学習します'
    )
    db.session.add(prog_cat)
    db.session.commit()
    print('プログラミングカテゴリを作成しました。（問題は後で追加してください）')
    return prog_cat

if __name__ == '__main__':
    with app.app_context():
        # データベーステーブルを作成
        db.create_all()
        
        # 初期データを登録
        print('初期データの登録を開始します...')
        init_security_questions()
        init_it_basics_questions()
        init_programming_questions()
        print('初期データの登録が完了しました。')

