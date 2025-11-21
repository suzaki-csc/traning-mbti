"""
初期データ投入スクリプト
"""
from app import create_app, db
from app.models import User, Category, Quiz


def create_initial_data():
    """初期データを作成"""
    app = create_app()
    
    with app.app_context():
        # データベーステーブルを作成
        db.create_all()
        
        # デフォルト管理者の作成
        admin = User.query.filter_by(user_id='admin').first()
        if not admin:
            admin = User(user_id='admin', email='admin@example.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            print("デフォルト管理者を作成しました: admin / admin123")
        
        # カテゴリの作成
        categories_data = [
            {
                'name': 'セキュリティ',
                'description': '情報セキュリティに関する知識を学びます',
                'quizzes': create_security_quizzes()
            },
            {
                'name': 'IT基礎',
                'description': 'ITの基礎知識を学びます',
                'quizzes': create_it_basic_quizzes()
            },
            {
                'name': 'プログラミング',
                'description': 'プログラミングの基礎知識を学びます',
                'quizzes': create_programming_quizzes()
            }
        ]
        
        for cat_data in categories_data:
            category = Category.query.filter_by(name=cat_data['name']).first()
            if not category:
                category = Category(name=cat_data['name'], description=cat_data['description'])
                db.session.add(category)
                db.session.flush()  # IDを取得するためにflush
                
                # クイズを作成
                for quiz_data in cat_data['quizzes']:
                    quiz = Quiz(
                        category_id=category.id,
                        question=quiz_data['question'],
                        option1=quiz_data['option1'],
                        option2=quiz_data['option2'],
                        option3=quiz_data['option3'],
                        option4=quiz_data['option4'],
                        correct_answer=quiz_data['correct_answer'],
                        explanation=quiz_data['explanation']
                    )
                    db.session.add(quiz)
                
                print(f"カテゴリ '{cat_data['name']}' と {len(cat_data['quizzes'])} 問のクイズを作成しました")
        
        db.session.commit()
        print("初期データの投入が完了しました")


def create_security_quizzes():
    """セキュリティカテゴリのクイズデータ"""
    return [
        {
            'question': 'XSS (Cross-Site Scripting) とは何ですか？',
            'option1': 'Webサイトに悪意のあるスクリプトを注入する攻撃',
            'option2': 'データベースにSQLクエリを注入する攻撃',
            'option3': 'パスワードを総当たりで試行する攻撃',
            'option4': 'ネットワークを経由した通信を傍受する攻撃',
            'correct_answer': 1,
            'explanation': 'XSSは、Webアプリケーションに悪意のあるJavaScriptコードを注入し、ユーザーのブラウザで実行させる攻撃です。適切な入力検証とエスケープ処理で防ぐことができます。'
        },
        {
            'question': 'CSRF (Cross-Site Request Forgery) とは何ですか？',
            'option1': 'ユーザーが意図しないリクエストを送信させる攻撃',
            'option2': 'セッション情報を盗む攻撃',
            'option3': 'パスワードを推測する攻撃',
            'option4': 'ファイルをアップロードする攻撃',
            'correct_answer': 1,
            'explanation': 'CSRFは、ユーザーがログインしている状態で、悪意のあるサイトからユーザーが意図しないリクエストを送信させる攻撃です。CSRFトークンを使用して防ぐことができます。'
        },
        {
            'question': 'SQLインジェクションとは何ですか？',
            'option1': 'データベースに悪意のあるSQLクエリを注入する攻撃',
            'option2': 'WebページにJavaScriptを注入する攻撃',
            'option3': 'メールにウイルスを添付する攻撃',
            'option4': 'ネットワークパケットを改ざんする攻撃',
            'correct_answer': 1,
            'explanation': 'SQLインジェクションは、アプリケーションの入力フィールドに悪意のあるSQLコードを注入し、データベースを操作する攻撃です。パラメータ化クエリを使用して防ぐことができます。'
        },
        {
            'question': 'パスワードリスト攻撃とは何ですか？',
            'option1': '既に漏洩したパスワードのリストを使用してログインを試みる攻撃',
            'option2': 'パスワードを総当たりで試行する攻撃',
            'option3': 'パスワードを推測する攻撃',
            'option4': 'パスワードをハッシュ化する攻撃',
            'correct_answer': 1,
            'explanation': 'パスワードリスト攻撃は、他のサービスから漏洩したユーザーIDとパスワードの組み合わせを使用して、別のサービスへのログインを試みる攻撃です。多要素認証で防ぐことができます。'
        },
        {
            'question': 'レインボーテーブルとは何ですか？',
            'option1': 'ハッシュ値から元のパスワードを逆引きするためのテーブル',
            'option2': 'パスワードの強度を判定するテーブル',
            'option3': 'ユーザー情報を保存するテーブル',
            'option4': 'ログイン履歴を記録するテーブル',
            'correct_answer': 1,
            'explanation': 'レインボーテーブルは、事前に計算したハッシュ値と元のパスワードの対応表です。ソルト（salt）を使用することで、レインボーテーブル攻撃を防ぐことができます。'
        },
        {
            'question': 'ゼロトラストとは何ですか？',
            'option1': 'すべての通信を信頼せず、常に検証するセキュリティモデル',
            'option2': 'ネットワークの境界でセキュリティを確保するモデル',
            'option3': 'パスワードを一切使用しない認証モデル',
            'option4': 'すべての通信を暗号化するモデル',
            'correct_answer': 1,
            'explanation': 'ゼロトラストは、「信頼しない、常に検証する」という考え方に基づくセキュリティモデルです。ネットワークの内外に関わらず、すべてのアクセスを検証します。'
        },
        {
            'question': '多要素認証（MFA）とは何ですか？',
            'option1': '複数の認証要素を組み合わせた認証方式',
            'option2': 'パスワードを複数回入力する認証方式',
            'option3': '複数のパスワードを使用する認証方式',
            'option4': '複数のユーザーで認証する方式',
            'correct_answer': 1,
            'explanation': '多要素認証は、知識（パスワード）、所持（スマートフォン）、生体（指紋）など、異なる種類の認証要素を組み合わせて認証する方式です。セキュリティが向上します。'
        },
        {
            'question': 'DPIA (Data Protection Impact Assessment) とは何ですか？',
            'option1': '個人データの処理が個人に与える影響を評価する手続き',
            'option2': 'データベースのパフォーマンスを評価する手続き',
            'option3': 'データのバックアップ計画を評価する手続き',
            'option4': 'データの暗号化方法を評価する手続き',
            'correct_answer': 1,
            'explanation': 'DPIAは、個人データの処理が個人の権利や自由に与えるリスクを事前に評価し、対策を講じるための手続きです。GDPRで義務付けられています。'
        },
        {
            'question': 'SAST/DASTとは何ですか？',
            'option1': '静的/動的アプリケーションセキュリティテスト',
            'option2': 'サーバー/データベース管理システム',
            'option3': 'セキュア/暗号化通信プロトコル',
            'option4': 'セキュリティ/データ分析ツール',
            'correct_answer': 1,
            'explanation': 'SAST（静的解析）はソースコードを解析し、DAST（動的解析）は実行中のアプリケーションをテストします。両方を組み合わせることで、より包括的なセキュリティテストが可能です。'
        },
        {
            'question': 'CVE/CVSSとは何ですか？',
            'option1': '脆弱性の識別番号と深刻度評価システム',
            'option2': '暗号化通信プロトコル',
            'option3': 'セキュリティ監視システム',
            'option4': 'データベース管理システム',
            'correct_answer': 1,
            'explanation': 'CVE（Common Vulnerabilities and Exposures）は脆弱性の識別番号、CVSS（Common Vulnerability Scoring System）は脆弱性の深刻度を評価するシステムです。'
        },
        {
            'question': 'フィッシングとは何ですか？',
            'option1': '偽のWebサイトやメールで個人情報を詐取する攻撃',
            'option2': 'パスワードを総当たりで試行する攻撃',
            'option3': 'ネットワーク通信を傍受する攻撃',
            'option4': 'マルウェアを配布する攻撃',
            'correct_answer': 1,
            'explanation': 'フィッシングは、正規の組織を装った偽のWebサイトやメールを使用して、ユーザーから個人情報や認証情報を詐取する攻撃です。送信元を確認することが重要です。'
        },
        {
            'question': 'スミッシングとは何ですか？',
            'option1': 'SMS（ショートメッセージ）を使用したフィッシング攻撃',
            'option2': 'メールを使用したフィッシング攻撃',
            'option3': '電話を使用した詐欺攻撃',
            'option4': 'ソーシャルメディアを使用した攻撃',
            'correct_answer': 1,
            'explanation': 'スミッシングは、SMS（ショートメッセージサービス）を使用して、ユーザーを偽のWebサイトに誘導し、個人情報を詐取する攻撃です。SMS版のフィッシングです。'
        },
        {
            'question': 'スピアフィッシングとは何ですか？',
            'option1': '特定の個人や組織を標的としたフィッシング攻撃',
            'option2': '不特定多数を標的としたフィッシング攻撃',
            'option3': '企業の内部ネットワークを標的とした攻撃',
            'option4': '政府機関を標的とした攻撃',
            'correct_answer': 1,
            'explanation': 'スピアフィッシングは、特定の個人や組織を標的として、その人物に関する情報を収集し、より信頼性の高い偽のメールやWebサイトを作成する攻撃です。'
        },
        {
            'question': 'ランサムウェアとは何ですか？',
            'option1': 'データを暗号化して身代金を要求するマルウェア',
            'option2': 'パスワードを盗むマルウェア',
            'option3': 'システムを破壊するマルウェア',
            'option4': '個人情報を収集するマルウェア',
            'correct_answer': 1,
            'explanation': 'ランサムウェアは、ユーザーのデータを暗号化し、復号化のための身代金を要求するマルウェアです。定期的なバックアップが有効な対策です。'
        },
        {
            'question': 'サプライチェーン攻撃とは何ですか？',
            'option1': 'ソフトウェアの開発・配布プロセスを経由した攻撃',
            'option2': 'ネットワーク経由での直接攻撃',
            'option3': '物理的なアクセスによる攻撃',
            'option4': '内部関係者による攻撃',
            'correct_answer': 1,
            'explanation': 'サプライチェーン攻撃は、ソフトウェアの開発や配布プロセスに侵入し、正規のソフトウェアにマルウェアを混入させる攻撃です。信頼できるソースからのみソフトウェアを入手することが重要です。'
        },
        {
            'question': 'ソーシャルエンジニアリングとは何ですか？',
            'option1': '人間の心理的な弱点を利用した情報取得手法',
            'option2': 'ソーシャルメディアを使用した攻撃',
            'option3': 'ネットワークを経由した攻撃',
            'option4': '物理的な侵入による攻撃',
            'correct_answer': 1,
            'explanation': 'ソーシャルエンジニアリングは、技術的な脆弱性ではなく、人間の心理的な弱点（信頼、好奇心など）を利用して情報を取得する手法です。セキュリティ教育が重要です。'
        },
        {
            'question': 'セキュアコーディングとは何ですか？',
            'option1': 'セキュリティを考慮した安全なコードを書くこと',
            'option2': '暗号化されたコードを書くこと',
            'option3': '複雑なコードを書くこと',
            'option4': '高速なコードを書くこと',
            'correct_answer': 1,
            'explanation': 'セキュアコーディングは、セキュリティの脆弱性を防ぐためのコーディング手法です。入力検証、エスケープ処理、適切なエラーハンドリングなどが含まれます。'
        },
        {
            'question': '侵入テスト（ペネトレーションテスト）とは何ですか？',
            'option1': '実際に攻撃を試みてセキュリティを評価するテスト',
            'option2': 'コードを解析して脆弱性を発見するテスト',
            'option3': 'パフォーマンスを評価するテスト',
            'option4': 'ユーザビリティを評価するテスト',
            'correct_answer': 1,
            'explanation': '侵入テストは、実際に攻撃者の視点からシステムへの侵入を試み、セキュリティの脆弱性を発見・評価するテストです。定期的な実施が推奨されます。'
        },
        {
            'question': 'WAF (Web Application Firewall) とは何ですか？',
            'option1': 'Webアプリケーションを保護するファイアウォール',
            'option2': 'ネットワーク全体を保護するファイアウォール',
            'option3': 'データベースを保護するファイアウォール',
            'option4': 'メールサーバーを保護するファイアウォール',
            'correct_answer': 1,
            'explanation': 'WAFは、WebアプリケーションへのHTTP/HTTPS通信を監視し、悪意のあるリクエストをブロックするファイアウォールです。XSSやSQLインジェクションなどの攻撃を防ぎます。'
        },
        {
            'question': 'IAM (Identity and Access Management) とは何ですか？',
            'option1': 'ユーザーの認証とアクセス権限を管理するシステム',
            'option2': 'データベースを管理するシステム',
            'option3': 'ネットワークを管理するシステム',
            'option4': 'サーバーを管理するシステム',
            'correct_answer': 1,
            'explanation': 'IAMは、ユーザーの認証（本人確認）と認可（アクセス権限の管理）を統合的に管理するシステムです。適切な権限管理により、セキュリティを向上させます。'
        }
    ]


def create_it_basic_quizzes():
    """IT基礎カテゴリのクイズデータ"""
    return [
        {
            'question': 'HTTPとHTTPSの主な違いは何ですか？',
            'option1': 'HTTPSは通信を暗号化する',
            'option2': 'HTTPはより高速である',
            'option3': 'HTTPSはより多くのデータを送信できる',
            'option4': 'HTTPはより安全である',
            'correct_answer': 1,
            'explanation': 'HTTPSはHTTPにSSL/TLS暗号化を追加したプロトコルです。通信内容が暗号化されるため、機密情報の送信に適しています。'
        },
        {
            'question': 'DNS (Domain Name System) の主な役割は何ですか？',
            'option1': 'ドメイン名をIPアドレスに変換する',
            'option2': 'メールを送信する',
            'option3': 'Webページを表示する',
            'option4': 'ファイルを転送する',
            'correct_answer': 1,
            'explanation': 'DNSは、人間が覚えやすいドメイン名（例: example.com）を、コンピュータが理解できるIPアドレス（例: 192.0.2.1）に変換するシステムです。'
        },
        {
            'question': 'TCP/IPとは何ですか？',
            'option1': 'インターネットで使用される通信プロトコルのセット',
            'option2': 'データベース管理システム',
            'option3': 'Webサーバーソフトウェア',
            'option4': 'プログラミング言語',
            'correct_answer': 1,
            'explanation': 'TCP/IPは、インターネットで使用される通信プロトコルのセットです。TCP（伝送制御プロトコル）とIP（インターネットプロトコル）を中心としたプロトコル群です。'
        },
        {
            'question': 'OSI参照モデルは何層で構成されていますか？',
            'option1': '7層',
            'option2': '5層',
            'option3': '3層',
            'option4': '9層',
            'correct_answer': 1,
            'explanation': 'OSI参照モデルは、ネットワーク通信を7つの層（物理層、データリンク層、ネットワーク層、トランスポート層、セッション層、プレゼンテーション層、アプリケーション層）に分けて説明するモデルです。'
        },
        {
            'question': 'クラウドコンピューティングの主な利点は何ですか？',
            'option1': 'スケーラビリティとコスト削減',
            'option2': '物理的なサーバーが必要',
            'option3': 'インターネット接続が不要',
            'option4': 'セキュリティが不要',
            'correct_answer': 1,
            'explanation': 'クラウドコンピューティングは、必要な時に必要な分だけリソースを利用でき、初期投資を抑えながらスケールアップ・ダウンが可能です。'
        },
        {
            'question': '仮想化とは何ですか？',
            'option1': '物理的なリソースを論理的に分割して利用すること',
            'option2': 'データを暗号化すること',
            'option3': 'ネットワークを構築すること',
            'option4': 'データベースを作成すること',
            'correct_answer': 1,
            'explanation': '仮想化は、物理的なハードウェアリソース（CPU、メモリ、ストレージなど）を論理的に分割し、複数の仮想環境として利用できるようにする技術です。'
        },
        {
            'question': 'コンテナとは何ですか？',
            'option1': 'アプリケーションとその依存関係をパッケージ化したもの',
            'option2': 'データを保存する箱',
            'option3': 'ネットワークの接続点',
            'option4': 'データベースのテーブル',
            'correct_answer': 1,
            'explanation': 'コンテナは、アプリケーションとその実行に必要なライブラリや設定をまとめてパッケージ化したものです。Dockerが代表的なコンテナ技術です。'
        },
        {
            'question': 'API (Application Programming Interface) とは何ですか？',
            'option1': 'アプリケーション間でデータを交換するためのインターフェース',
            'option2': 'データベース管理システム',
            'option3': 'プログラミング言語',
            'option4': 'Webブラウザ',
            'correct_answer': 1,
            'explanation': 'APIは、異なるアプリケーションやサービス間でデータや機能を交換するためのインターフェースです。RESTful APIが広く使用されています。'
        },
        {
            'question': 'RESTfulとは何ですか？',
            'option1': 'Webサービスの設計原則の一つ',
            'option2': 'データベースの設計方法',
            'option3': 'プログラミングのパラダイム',
            'option4': 'ネットワークプロトコル',
            'correct_answer': 1,
            'explanation': 'RESTfulは、HTTPメソッド（GET、POST、PUT、DELETEなど）を使用してリソースを操作するWebサービスの設計原則です。シンプルで拡張性が高い設計です。'
        },
        {
            'question': 'JSONとは何ですか？',
            'option1': 'データを表現するための軽量なテキスト形式',
            'option2': 'データベース管理システム',
            'option3': 'プログラミング言語',
            'option4': 'ネットワークプロトコル',
            'correct_answer': 1,
            'explanation': 'JSON（JavaScript Object Notation）は、データを表現するための軽量なテキスト形式です。人間が読み書きしやすく、機械でも処理しやすい形式です。'
        },
        {
            'question': 'XMLとは何ですか？',
            'option1': '構造化されたデータを表現するマークアップ言語',
            'option2': 'プログラミング言語',
            'option3': 'データベース管理システム',
            'option4': 'Webブラウザ',
            'correct_answer': 1,
            'explanation': 'XML（eXtensible Markup Language）は、構造化されたデータを表現するためのマークアップ言語です。タグを使用してデータの構造を定義します。'
        },
        {
            'question': 'データベースとは何ですか？',
            'option1': 'データを効率的に保存・管理するシステム',
            'option2': 'ファイルを保存する場所',
            'option3': 'ネットワークの接続点',
            'option4': 'Webサーバー',
            'correct_answer': 1,
            'explanation': 'データベースは、大量のデータを効率的に保存・管理・検索するためのシステムです。MySQL、PostgreSQL、MongoDBなどが代表的なデータベースです。'
        },
        {
            'question': 'リレーショナルデータベースとは何ですか？',
            'option1': 'テーブル間の関係を定義してデータを管理するデータベース',
            'option2': 'ファイルベースのデータベース',
            'option3': 'メモリベースのデータベース',
            'option4': 'クラウドベースのデータベース',
            'correct_answer': 1,
            'explanation': 'リレーショナルデータベースは、テーブル（表）の形式でデータを保存し、テーブル間の関係（リレーション）を定義してデータを管理するデータベースです。SQLを使用して操作します。'
        },
        {
            'question': 'NoSQLとは何ですか？',
            'option1': 'SQLを使用しないデータベースの総称',
            'option2': 'SQLのみを使用するデータベース',
            'option3': 'ネットワークプロトコル',
            'option4': 'プログラミング言語',
            'correct_answer': 1,
            'explanation': 'NoSQLは、SQLを使用しないデータベースの総称です。ドキュメント型、キー・バリュー型、カラム型など、様々なデータモデルがあります。'
        },
        {
            'question': 'バックアップとは何ですか？',
            'option1': 'データの複製を作成して保存すること',
            'option2': 'データを削除すること',
            'option3': 'データを暗号化すること',
            'option4': 'データを転送すること',
            'correct_answer': 1,
            'explanation': 'バックアップは、データの複製を作成して別の場所に保存することです。データ損失に備えて定期的に実施することが重要です。'
        },
        {
            'question': 'ディザスタリカバリとは何ですか？',
            'option1': '災害時にシステムを復旧する計画と手順',
            'option2': 'データをバックアップすること',
            'option3': 'システムを停止すること',
            'option4': 'ネットワークを構築すること',
            'correct_answer': 1,
            'explanation': 'ディザスタリカバリは、災害や障害が発生した際に、システムやデータを迅速に復旧するための計画と手順です。BCP（事業継続計画）の一部です。'
        },
        {
            'question': 'ロードバランサーとは何ですか？',
            'option1': '複数のサーバーに負荷を分散する装置',
            'option2': 'データを保存する装置',
            'option3': 'ネットワークを接続する装置',
            'option4': 'データを暗号化する装置',
            'correct_answer': 1,
            'explanation': 'ロードバランサーは、複数のサーバーにリクエストを分散し、負荷を均等に配分する装置です。可用性とパフォーマンスの向上に役立ちます。'
        },
        {
            'question': 'CDN (Content Delivery Network) とは何ですか？',
            'option1': 'コンテンツを地理的に分散して配信するネットワーク',
            'option2': 'データベース管理ネットワーク',
            'option3': 'セキュリティ監視ネットワーク',
            'option4': 'ファイル転送ネットワーク',
            'correct_answer': 1,
            'explanation': 'CDNは、コンテンツを複数の地理的に分散したサーバーに配置し、ユーザーに最も近いサーバーから配信するネットワークです。配信速度の向上に役立ちます。'
        },
        {
            'question': 'DevOpsとは何ですか？',
            'option1': '開発と運用を統合する開発手法',
            'option2': 'データベース管理手法',
            'option3': 'ネットワーク構築手法',
            'option4': 'セキュリティ監視手法',
            'correct_answer': 1,
            'explanation': 'DevOpsは、開発（Development）と運用（Operations）を統合し、継続的な開発・テスト・デプロイを実現する開発手法です。CI/CDパイプラインが重要です。'
        },
        {
            'question': 'CI/CDとは何ですか？',
            'option1': '継続的インテグレーションと継続的デプロイメント',
            'option2': 'データベース管理システム',
            'option3': 'ネットワークプロトコル',
            'option4': 'プログラミング言語',
            'correct_answer': 1,
            'explanation': 'CI/CDは、継続的インテグレーション（Continuous Integration）と継続的デプロイメント（Continuous Deployment）の略です。コードの自動テストとデプロイを実現します。'
        }
    ]


def create_programming_quizzes():
    """プログラミングカテゴリのクイズデータ"""
    return [
        {
            'question': '変数とは何ですか？',
            'option1': 'データを保存するための名前付きの記憶領域',
            'option2': '関数を定義するためのキーワード',
            'option3': 'クラスを定義するためのキーワード',
            'option4': 'プログラムを実行するためのコマンド',
            'correct_answer': 1,
            'explanation': '変数は、データを保存するための名前付きの記憶領域です。プログラムの実行中に値を変更することができます。'
        },
        {
            'question': '関数とは何ですか？',
            'option1': '特定の処理を実行するコードのブロック',
            'option2': 'データを保存する場所',
            'option3': 'プログラム全体',
            'option4': 'エラーメッセージ',
            'correct_answer': 1,
            'explanation': '関数は、特定の処理を実行するコードのブロックです。引数を受け取り、処理を実行し、結果を返すことができます。コードの再利用性を高めます。'
        },
        {
            'question': 'クラスとは何ですか？',
            'option1': 'オブジェクトの設計図',
            'option2': 'データを保存する場所',
            'option3': 'プログラム全体',
            'option4': 'エラーハンドリングの方法',
            'correct_answer': 1,
            'explanation': 'クラスは、オブジェクト指向プログラミングにおいて、オブジェクトの設計図となるものです。属性（データ）とメソッド（処理）を定義します。'
        },
        {
            'question': 'オブジェクト指向とは何ですか？',
            'option1': 'オブジェクトを中心としたプログラミングのパラダイム',
            'option2': '手続き型プログラミングのパラダイム',
            'option3': '関数型プログラミングのパラダイム',
            'option4': 'データベース設計のパラダイム',
            'correct_answer': 1,
            'explanation': 'オブジェクト指向は、データと処理をオブジェクトとしてまとめ、オブジェクト間の相互作用でプログラムを構築するプログラミングのパラダイムです。'
        },
        {
            'question': '継承とは何ですか？',
            'option1': '既存のクラスの機能を引き継いで新しいクラスを作成すること',
            'option2': 'データをコピーすること',
            'option3': '関数を呼び出すこと',
            'option4': 'エラーを処理すること',
            'correct_answer': 1,
            'explanation': '継承は、既存のクラス（親クラス）の属性とメソッドを引き継いで、新しいクラス（子クラス）を作成する機能です。コードの再利用性を高めます。'
        },
        {
            'question': 'ポリモーフィズムとは何ですか？',
            'option1': '同じインターフェースで異なる実装を提供すること',
            'option2': 'データを変換すること',
            'option3': '関数を定義すること',
            'option4': 'エラーを処理すること',
            'correct_answer': 1,
            'explanation': 'ポリモーフィズムは、同じインターフェースやメソッド名で、異なるクラスが異なる実装を提供する機能です。柔軟性と拡張性を高めます。'
        },
        {
            'question': 'カプセル化とは何ですか？',
            'option1': 'データと処理を一つの単位にまとめ、外部からの直接アクセスを制限すること',
            'option2': 'データを暗号化すること',
            'option3': 'データを圧縮すること',
            'option4': 'データを転送すること',
            'correct_answer': 1,
            'explanation': 'カプセル化は、データと処理を一つの単位（クラス）にまとめ、外部からの直接アクセスを制限することで、データの整合性を保つ機能です。'
        },
        {
            'question': 'アルゴリズムとは何ですか？',
            'option1': '問題を解決するための手順',
            'option2': 'データを保存する方法',
            'option3': 'プログラムを実行する方法',
            'option4': 'エラーを処理する方法',
            'correct_answer': 1,
            'explanation': 'アルゴリズムは、問題を解決するための明確で有限な手順です。効率的なアルゴリズムを選択することで、プログラムのパフォーマンスが向上します。'
        },
        {
            'question': 'データ構造とは何ですか？',
            'option1': 'データを効率的に保存・操作するための構造',
            'option2': 'データベースの構造',
            'option3': 'ネットワークの構造',
            'option4': 'ファイルの構造',
            'correct_answer': 1,
            'explanation': 'データ構造は、データを効率的に保存・操作するための構造です。配列、リスト、スタック、キュー、ツリーなどがあります。'
        },
        {
            'question': '再帰とは何ですか？',
            'option1': '関数が自分自身を呼び出すこと',
            'option2': 'データを繰り返し処理すること',
            'option3': 'エラーを処理すること',
            'option4': 'データを変換すること',
            'correct_answer': 1,
            'explanation': '再帰は、関数が自分自身を呼び出すプログラミング手法です。階乗計算やツリーの走査など、再帰的な問題を解決するのに適しています。'
        },
        {
            'question': '例外処理とは何ですか？',
            'option1': 'エラーが発生した際の処理',
            'option2': 'データを保存する処理',
            'option3': 'データを転送する処理',
            'option4': 'データを変換する処理',
            'correct_answer': 1,
            'explanation': '例外処理は、プログラムの実行中にエラー（例外）が発生した際に、適切に処理する機能です。プログラムの堅牢性を高めます。'
        },
        {
            'question': 'デバッグとは何ですか？',
            'option1': 'プログラムのバグ（エラー）を発見して修正すること',
            'option2': 'データを削除すること',
            'option3': 'プログラムを実行すること',
            'option4': 'データを保存すること',
            'correct_answer': 1,
            'explanation': 'デバッグは、プログラムのバグ（エラー）を発見して修正する作業です。デバッガツールを使用して、プログラムの実行を追跡・分析します。'
        },
        {
            'question': 'バージョン管理とは何ですか？',
            'option1': 'ソースコードの変更履歴を管理すること',
            'option2': 'データベースのバージョンを管理すること',
            'option3': 'プログラムのバージョンを管理すること',
            'option4': 'ファイルのバージョンを管理すること',
            'correct_answer': 1,
            'explanation': 'バージョン管理は、ソースコードの変更履歴を管理するシステムです。Gitが代表的なバージョン管理システムです。変更の追跡、復元、ブランチ管理が可能です。'
        },
        {
            'question': 'Gitとは何ですか？',
            'option1': '分散型バージョン管理システム',
            'option2': 'データベース管理システム',
            'option3': 'Webサーバー',
            'option4': 'プログラミング言語',
            'correct_answer': 1,
            'explanation': 'Gitは、分散型バージョン管理システムです。ソースコードの変更履歴を管理し、複数の開発者が協力して開発する際に使用されます。'
        },
        {
            'question': 'リファクタリングとは何ですか？',
            'option1': 'コードの動作を変えずに構造を改善すること',
            'option2': 'コードを削除すること',
            'option3': 'コードを実行すること',
            'option4': 'コードをコピーすること',
            'correct_answer': 1,
            'explanation': 'リファクタリングは、コードの外部動作を変えずに、内部構造を改善することです。可読性、保守性、パフォーマンスの向上を目的とします。'
        },
        {
            'question': 'デザインパターンとは何ですか？',
            'option1': 'よくある問題に対する再利用可能な解決策',
            'option2': 'データベースの設計方法',
            'option3': 'ネットワークの設計方法',
            'option4': 'UIの設計方法',
            'correct_answer': 1,
            'explanation': 'デザインパターンは、ソフトウェア開発において、よくある問題に対する再利用可能な解決策です。Singleton、Factory、Observerなどがあります。'
        },
        {
            'question': 'テスト駆動開発（TDD）とは何ですか？',
            'option1': 'テストを先に書いてから実装する開発手法',
            'option2': 'テストを書かない開発手法',
            'option3': '実装を先に行う開発手法',
            'option4': 'ドキュメントを先に書く開発手法',
            'correct_answer': 1,
            'explanation': 'テスト駆動開発（TDD）は、テストを先に書き、そのテストが通るように実装する開発手法です。コードの品質と信頼性を向上させます。'
        },
        {
            'question': 'アジャイル開発とは何ですか？',
            'option1': '短いサイクルで反復的に開発する手法',
            'option2': '長期間かけて一度に開発する手法',
            'option3': 'テストをしない開発手法',
            'option4': 'ドキュメントを書かない開発手法',
            'correct_answer': 1,
            'explanation': 'アジャイル開発は、短いサイクル（スプリント）で反復的に開発し、顧客のフィードバックを取り入れながら進める開発手法です。柔軟性と適応性が特徴です。'
        },
        {
            'question': 'コードレビューとは何ですか？',
            'option1': '他の開発者がコードを確認してフィードバックすること',
            'option2': 'コードを実行すること',
            'option3': 'コードを削除すること',
            'option4': 'コードをコピーすること',
            'correct_answer': 1,
            'explanation': 'コードレビューは、他の開発者がコードを確認し、バグ、設計の問題、改善点などを指摘するプロセスです。コードの品質向上に役立ちます。'
        },
        {
            'question': 'ドキュメンテーションとは何ですか？',
            'option1': 'コードやシステムの説明を文書化すること',
            'option2': 'コードを実行すること',
            'option3': 'コードを削除すること',
            'option4': 'コードをコピーすること',
            'correct_answer': 1,
            'explanation': 'ドキュメンテーションは、コードやシステムの説明、使用方法、API仕様などを文書化することです。保守性と使いやすさを向上させます。'
        }
    ]


if __name__ == '__main__':
    create_initial_data()

