"""
初期データ投入スクリプト

カテゴリ、問題、選択肢、用語参考リンクの初期データを作成します。
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db
from app.models import Category, Question, Choice, TermReference, User
from datetime import datetime


def init_categories():
    """カテゴリの初期データ"""
    categories = [
        {
            "name": "セキュリティ",
            "description": "情報セキュリティに関する用語や概念を学習します",
            "display_order": 1
        },
        {
            "name": "IT基礎",
            "description": "ITの基礎知識やネットワーク、ハードウェアについて学習します",
            "display_order": 2
        },
        {
            "name": "プログラミング",
            "description": "プログラミング言語やアルゴリズム、データ構造について学習します",
            "display_order": 3
        },
        {
            "name": "プロジェクトマネージメント",
            "description": "プロジェクト管理手法、リスク管理、チーム運営について学習します",
            "display_order": 4
        }
    ]
    
    created_count = 0
    for cat_data in categories:
        category = Category.query.filter_by(name=cat_data['name']).first()
        if not category:
            category = Category(**cat_data)
            db.session.add(category)
            created_count += 1
    
    db.session.commit()
    if created_count > 0:
        print(f"カテゴリを作成しました（{created_count}件）")
    else:
        print("カテゴリは既に存在します")


def init_security_questions():
    """セキュリティカテゴリの問題"""
    category = Category.query.filter_by(name="セキュリティ").first()
    if not category:
        print("セキュリティカテゴリが見つかりません")
        return
    
    questions_data = [
        {
            "question_text": "XSS (Cross-Site Scripting) 攻撃を防ぐために最も効果的な対策はどれですか？",
            "explanation": "XSS攻撃を防ぐには、ユーザー入力を適切にエスケープ処理することが重要です。HTMLエスケープにより、<script>タグなどの特殊文字が無害な文字列に変換され、ブラウザで実行されることを防ぎます。大学3年生の皆さんは、Webアプリケーション開発時に必ずユーザー入力をエスケープする習慣をつけましょう。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "ユーザー入力を適切にエスケープする", "is_correct": True, "display_order": 1},
                {"choice_text": "HTTPSを使用する", "is_correct": False, "display_order": 2},
                {"choice_text": "データベースを暗号化する", "is_correct": False, "display_order": 3},
                {"choice_text": "Firewallを設置する", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "SQL Injection攻撃のリスクを最小化する最良の方法はどれですか？",
            "explanation": "SQL Injection対策には、Prepared Statement（パラメータ化Query）の使用が最も効果的です。これにより、ユーザー入力がSQL文として解釈されることを防ぎます。例えば、PythonではSQLAlchemyのようなORMを使うことで、自動的にパラメータバインディングが行われます。直接SQL文を組み立てることは避けましょう。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Prepared Statementを使用する", "is_correct": True, "display_order": 1},
                {"choice_text": "データベースのポートを変更する", "is_correct": False, "display_order": 2},
                {"choice_text": "ユーザー入力の文字数を制限する", "is_correct": False, "display_order": 3},
                {"choice_text": "データベースを読み取り専用にする", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "MFA (Multi-Factor Authentication) の「3つの要素」に含まれないものはどれですか？",
            "explanation": "MFAの3要素は、「Knowledge Factor（パスワードなど知っているもの）」「Possession Factor（スマホなど持っているもの）」「Inherence Factor（指紋など自分自身）」です。メールアドレスはKnowledge Factorの一部ですが、それ自体は要素の分類には含まれません。MFAはセキュリティを大幅に向上させる重要な技術なので、可能な限り有効にすることをお勧めします。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Email Address", "is_correct": True, "display_order": 1},
                {"choice_text": "Knowledge Factor (Password)", "is_correct": False, "display_order": 2},
                {"choice_text": "Possession Factor (Smartphone)", "is_correct": False, "display_order": 3},
                {"choice_text": "Inherence Factor (Fingerprint)", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "CSRF (Cross-Site Request Forgery) 攻撃とはどのような攻撃ですか？",
            "explanation": "CSRFは、ログイン中のユーザーに意図しない操作を実行させる攻撃です。対策としては、各Requestに予測不可能なToken（CSRF Token）を付与し、サーバー側で検証することが一般的です。FlaskではFlask-WTFを使うことで簡単にCSRF保護を実装できます。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "ユーザーが意図しない操作を実行させる攻撃", "is_correct": True, "display_order": 1},
                {"choice_text": "データベースに不正なSQL文を挿入する攻撃", "is_correct": False, "display_order": 2},
                {"choice_text": "パスワードを総当たりで試す攻撃", "is_correct": False, "display_order": 3},
                {"choice_text": "ネットワーク通信を盗聴する攻撃", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "パスワードをHash化する際に、Rainbow Table攻撃を防ぐために追加するランダムな文字列を何と呼びますか？",
            "explanation": "Saltは、パスワードをHash化する前に追加するランダムな文字列です。ユーザーごとに異なるSaltを使用することで、同じパスワードでも異なるHash値になり、Rainbow Table攻撃を効果的に防ぐことができます。Pythonではbcryptやargon2などのライブラリを使うと、自動的にSaltが付与されます。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Salt", "is_correct": True, "display_order": 1},
                {"choice_text": "Pepper", "is_correct": False, "display_order": 2},
                {"choice_text": "Key", "is_correct": False, "display_order": 3},
                {"choice_text": "Nonce", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "HTTPSで使用される暗号化Protocolはどれですか？",
            "explanation": "HTTPSは、HTTP通信をSSL/TLS Protocolで暗号化したものです。TLS (Transport Layer Security) が現在の標準で、SSLの後継です。WebサイトとBrowser間の通信を暗号化し、Man-in-the-Middle攻撃から保護します。最新のWebアプリケーションでは必須の技術です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "SSL/TLS", "is_correct": True, "display_order": 1},
                {"choice_text": "AES", "is_correct": False, "display_order": 2},
                {"choice_text": "RSA", "is_correct": False, "display_order": 3},
                {"choice_text": "MD5", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "DoS (Denial of Service) 攻撃の目的は何ですか？",
            "explanation": "DoS攻撃は、サービスを利用不能にすることが目的です。大量のRequestを送信してServerのResourceを枯渇させます。DDoS (Distributed DoS) 攻撃では、複数のコンピュータから同時に攻撃を行います。対策としては、Rate Limiting、CDN、WAFなどが有効です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "サービスを利用不能にする", "is_correct": True, "display_order": 1},
                {"choice_text": "データを盗む", "is_correct": False, "display_order": 2},
                {"choice_text": "パスワードを解読する", "is_correct": False, "display_order": 3},
                {"choice_text": "Malwareを感染させる", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Public Key Cryptography (公開鍵暗号方式) の特徴として正しいものはどれですか？",
            "explanation": "Public Key Cryptographyでは、Public Keyで暗号化したデータは対応するPrivate Keyでのみ復号できます。逆に、Private Keyで署名したデータはPublic Keyで検証できます。RSAやECCなどのAlgorithmが代表的です。HTTPSの鍵交換やDigital Signatureに使用されます。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Public Keyで暗号化し、Private Keyで復号する", "is_correct": True, "display_order": 1},
                {"choice_text": "同じKeyで暗号化と復号を行う", "is_correct": False, "display_order": 2},
                {"choice_text": "Keyを使わずに暗号化する", "is_correct": False, "display_order": 3},
                {"choice_text": "Private Keyを公開して使用する", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Phishing攻撃とはどのような攻撃ですか？",
            "explanation": "Phishing攻撃は、正規のサービスを装った偽SiteやEmailで、ユーザーの認証情報を騙し取る攻撃です。見た目が本物そっくりなLogin Pageを作成し、そこに入力された情報を盗みます。対策として、URLの確認、Two-Factor Authenticationの使用、怪しいLinkをクリックしないことが重要です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "偽Siteで認証情報を騙し取る", "is_correct": True, "display_order": 1},
                {"choice_text": "Network Packetを盗聴する", "is_correct": False, "display_order": 2},
                {"choice_text": "Systemの脆弱性を突く", "is_correct": False, "display_order": 3},
                {"choice_text": "Virusを添付Fileで送る", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Firewallの主な役割は何ですか？",
            "explanation": "Firewallは、Network境界でTrafficを監視・制御するSecurity機器です。事前に定義されたRuleに基づいて、不正なAccessを遮断します。Packet Filtering、Stateful Inspection、Application Level Gatewayなど様々な種類があります。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "不正なNetwork Accessを遮断する", "is_correct": True, "display_order": 1},
                {"choice_text": "データを暗号化する", "is_correct": False, "display_order": 2},
                {"choice_text": "パスワードを管理する", "is_correct": False, "display_order": 3},
                {"choice_text": "Virusを駆除する", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Session Hijacking攻撃を防ぐための対策として適切でないものはどれですか？",
            "explanation": "Session Hijacking対策には、HTTPS通信、Session IDの定期的な再生成、HttpOnly/Secureフラグの設定、IP AddressやUser-Agentの検証などが有効です。パスワードの長さは初回Authenticationには有効ですが、既に確立されたSessionを乗っ取られることを防ぐことはできません。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "パスワードの最小文字数を増やす", "is_correct": True, "display_order": 1},
                {"choice_text": "HTTPS通信を使用する", "is_correct": False, "display_order": 2},
                {"choice_text": "Session IDを定期的に再生成する", "is_correct": False, "display_order": 3},
                {"choice_text": "CookieにHttpOnlyフラグを設定する", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "RansomwareとはどのようなMalwareですか？",
            "explanation": "Ransomwareは、感染したコンピュータのFileを暗号化し、復号と引き換えに身代金を要求するMalwareです。近年、企業や組織を狙った攻撃が増加しています。対策として、定期的なBackup、Security Patchの適用、不審なEmailの添付Fileを開かないことが重要です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Fileを暗号化して身代金を要求する", "is_correct": True, "display_order": 1},
                {"choice_text": "個人情報を盗んで売買する", "is_correct": False, "display_order": 2},
                {"choice_text": "コンピュータを遠隔操作する", "is_correct": False, "display_order": 3},
                {"choice_text": "広告を大量に表示する", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "OAuth 2.0の主な用途は何ですか？",
            "explanation": "OAuth 2.0は、第三者Applicationに対して、ユーザーのパスワードを共有することなく、Resourceへの限定的なAccess権限を付与するためのAuthorization Frameworkです。「Googleでログイン」などのSocial Login機能で広く使われています。Authentication（認証）ではなくAuthorization（認可）のためのProtocolです。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "第三者ApplicationへのAuthorization", "is_correct": True, "display_order": 1},
                {"choice_text": "パスワードの暗号化", "is_correct": False, "display_order": 2},
                {"choice_text": "Emailの送受信", "is_correct": False, "display_order": 3},
                {"choice_text": "Fileの圧縮", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "脆弱性診断において、Penetration Testの目的は何ですか？",
            "explanation": "Penetration Test（侵入Test）は、実際の攻撃者の視点でSystemに侵入を試み、Securityの弱点を発見することが目的です。White Box、Black Box、Gray Boxなどの手法があります。脆弱性診断の一環として、定期的に実施することが推奨されます。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Systemへの侵入可能性を検証する", "is_correct": True, "display_order": 1},
                {"choice_text": "データベースのBackupを取る", "is_correct": False, "display_order": 2},
                {"choice_text": "Systemの処理速度を測定する", "is_correct": False, "display_order": 3},
                {"choice_text": "User Interfaceの使いやすさを評価する", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Brute Force攻撃への対策として最も効果的なものはどれですか？",
            "explanation": "Brute Force攻撃は、すべての組み合わせを試してパスワードを解読する攻撃です。対策として、一定回数のLogin失敗後にAccountをLockすることが効果的です。他にもCAPTCHAの使用、Rate Limiting、Account Lock時の通知なども有効です。強力なPassword Policyと組み合わせることが重要です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Login試行回数を制限する", "is_correct": True, "display_order": 1},
                {"choice_text": "HTTPSを使用する", "is_correct": False, "display_order": 2},
                {"choice_text": "データベースを暗号化する", "is_correct": False, "display_order": 3},
                {"choice_text": "定期的にBackupを取る", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Zero-day攻撃とは何ですか？",
            "explanation": "Zero-day攻撃は、Software Vendorが脆弱性を認識しておらず、Patchが提供されていない状態で行われる攻撃です。防御側が対策を講じる猶予が「ゼロ日」であることから名付けられました。対策として、WAF、IDS/IPS、異常検知Systemなどの多層防御が重要です。",
            "difficulty": 3,
            "choices": [
                {"choice_text": "Patchが存在しない脆弱性を突く攻撃", "is_correct": True, "display_order": 1},
                {"choice_text": "攻撃開始から終了まで0日で完了する攻撃", "is_correct": False, "display_order": 2},
                {"choice_text": "夜間0時に実行される攻撃", "is_correct": False, "display_order": 3},
                {"choice_text": "検知されずに侵入する攻撃", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "JWT (JSON Web Token) の主な用途は何ですか？",
            "explanation": "JWTは、当事者間で安全に情報を伝達するためのCompactで自己完結型のTokenです。主にWeb APIのAuthentication・Authorizationに使用されます。Header、Payload、Signatureの3つの部分で構成され、改ざん検知が可能です。Statelessな認証を実現できるため、Microservices Architectureでよく使われます。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "StatelessなAuthentication・Authorization", "is_correct": True, "display_order": 1},
                {"choice_text": "データベースの暗号化", "is_correct": False, "display_order": 2},
                {"choice_text": "Fileの圧縮", "is_correct": False, "display_order": 3},
                {"choice_text": "Emailの送信", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Secure Codingにおいて、入力値の検証を行うべきタイミングはいつですか？",
            "explanation": "入力値の検証は、Client側とServer側の両方で行うべきです。Client側の検証はUsability向上のため、Server側の検証はSecurityのために必須です。Client側の検証は簡単にBypassできるため、Server側での検証を省略してはいけません。これは「Trust Boundary」の概念に基づいています。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Client側とServer側の両方", "is_correct": True, "display_order": 1},
                {"choice_text": "Client側のみ", "is_correct": False, "display_order": 2},
                {"choice_text": "Server側のみ", "is_correct": False, "display_order": 3},
                {"choice_text": "Database側のみ", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "OWASP Top 10とは何ですか？",
            "explanation": "OWASP Top 10は、Web Application Securityにおける最も重要な10のRiskをまとめたDocumentです。Open Web Application Security Projectが定期的に更新しています。Injection、認証の不備、XSS、Access制御の不備などが含まれます。開発者必読の資料です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Web Applicationの重大な脆弱性Top 10", "is_correct": True, "display_order": 1},
                {"choice_text": "最も人気のあるWeb Framework 10選", "is_correct": False, "display_order": 2},
                {"choice_text": "Security Toolのランキング", "is_correct": False, "display_order": 3},
                {"choice_text": "有名なHacker集団のList", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Directory Traversal攻撃とは何ですか？",
            "explanation": "Directory Traversal攻撃は、「../」などのPath操作文字列を使用して、本来Accessできない DirectoryやFileにAccessする攻撃です。対策として、ユーザー入力からPath操作文字を除去する、Whitelist方式でAccess可能なFileを限定する、適切なFile Permissionを設定するなどが有効です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Path操作で不正なFileにAccessする攻撃", "is_correct": True, "display_order": 1},
                {"choice_text": "Directoryを順番に探索する攻撃", "is_correct": False, "display_order": 2},
                {"choice_text": "Directory構造を解析する攻撃", "is_correct": False, "display_order": 3},
                {"choice_text": "Directoryを削除する攻撃", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "SIEM (Security Information and Event Management) の主な機能は何ですか？",
            "explanation": "SIEMは、Security関連のLogやEvent情報を収集・分析し、RealtimeでSecurity Incidentを検知するSystemです。複数のSystemからLogを集約し、相関分析を行うことで、単独では見逃してしまう攻撃の兆候を発見できます。Compliance対応にも役立ちます。",
            "difficulty": 3,
            "choices": [
                {"choice_text": "Logを収集・分析してIncidentを検知する", "is_correct": True, "display_order": 1},
                {"choice_text": "FirewallのRuleを自動生成する", "is_correct": False, "display_order": 2},
                {"choice_text": "パスワードを一元管理する", "is_correct": False, "display_order": 3},
                {"choice_text": "データベースをBackupする", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Buffer Overflow攻撃の対策として有効なものはどれですか？",
            "explanation": "Buffer Overflow攻撃は、ProgramのBuffer領域を超えるデータを書き込むことで、Memoryを破壊したり任意のCodeを実行させる攻撃です。対策として、入力値の長さCheck、安全な文字列操作関数の使用（strncpy、snprintfなど）、ASLR、DEP/NXなどのOS機能の活用、Memory安全な言語の使用などが有効です。",
            "difficulty": 3,
            "choices": [
                {"choice_text": "入力データの長さを検証する", "is_correct": True, "display_order": 1},
                {"choice_text": "HTTPSを使用する", "is_correct": False, "display_order": 2},
                {"choice_text": "定期的にパスワードを変更する", "is_correct": False, "display_order": 3},
                {"choice_text": "Firewallを設置する", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "GDPR (EU General Data Protection Regulation) に関する説明として正しいものはどれですか？",
            "explanation": "GDPRは、EU域内の個人データ保護とPrivacy権を規定する法律です。EU市民のデータを扱うすべての組織が対象となり、違反時には高額な罰金が科せられます。個人データの処理には法的根拠が必要で、Data主体には忘れられる権利、Access権などが認められています。日本企業も該当する場合があるため注意が必要です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "EU域内の個人データ保護に関する法律", "is_correct": True, "display_order": 1},
                {"choice_text": "国際的なSecurity認証規格", "is_correct": False, "display_order": 2},
                {"choice_text": "暗号化Algorithmの名称", "is_correct": False, "display_order": 3},
                {"choice_text": "Firewallの設定方式", "is_correct": False, "display_order": 4}
            ]
        }
    ]
    
    for q_data in questions_data:
        # 既存チェック
        existing = Question.query.filter_by(
            category_id=category.id,
            question_text=q_data['question_text']
        ).first()
        
        if not existing:
            choices_data = q_data.pop('choices')
            question = Question(category_id=category.id, **q_data)
            db.session.add(question)
            db.session.flush()
            
            for choice_data in choices_data:
                choice = Choice(question_id=question.id, **choice_data)
                db.session.add(choice)
    
    db.session.commit()
    
    total_questions = Question.query.filter_by(category_id=category.id).count()
    print(f"セキュリティカテゴリの問題: {total_questions}問")


def init_security_terms():
    """セキュリティカテゴリの用語参考リンク"""
    category = Category.query.filter_by(name="セキュリティ").first()
    if not category:
        return
    
    terms = [
        {"term_name": "XSS (Cross-Site Scripting)", 
         "description": "Web Applicationの脆弱性の一つで、攻撃者が悪意のあるScriptをWeb Pageに挿入する攻撃。ユーザーの入力値を適切にEscapeすることで防ぐことができます。",
         "url": "#", "display_order": 1},
        {"term_name": "CSRF (Cross-Site Request Forgery)",
         "description": "Login中のユーザーが意図しない操作を実行させられる攻撃。CSRF Tokenを使用することで防御できます。",
         "url": "#", "display_order": 2},
        {"term_name": "SQL Injection",
         "description": "不正なSQL文を挿入してDatabaseを操作する攻撃。Prepared Statementを使用することで防止できます。",
         "url": "#", "display_order": 3},
        {"term_name": "MFA (Multi-Factor Authentication)",
         "description": "パスワードに加えて、SmartphoneやBiometric認証など複数の認証要素を組み合わせる方法。Securityが大幅に向上します。",
         "url": "#", "display_order": 4},
        {"term_name": "Zero Trust",
         "description": "「信頼しない、常に検証する」という考え方に基づくSecurity Model。Networkの内外を問わず、すべてのAccessを検証します。",
         "url": "#", "display_order": 5}
    ]
    
    for term_data in terms:
        existing = TermReference.query.filter_by(
            term_name=term_data['term_name'],
            category_id=category.id
        ).first()
        
        if not existing:
            term = TermReference(category_id=category.id, **term_data)
            db.session.add(term)
    
    db.session.commit()
    
    total_terms = TermReference.query.filter_by(category_id=category.id).count()
    print(f"セキュリティ用語: {total_terms}件")


def init_it_basics_questions():
    """IT基礎カテゴリの問題"""
    category = Category.query.filter_by(name="IT基礎").first()
    if not category:
        print("IT基礎カテゴリが見つかりません")
        return
    
    questions_data = [
        {
            "question_text": "OSの主な役割として正しくないものはどれですか？",
            "explanation": "OS (Operating System) は、Hardware資源の管理、Applicationの実行環境提供、User Interfaceの提供などを担当します。しかし、Web Pageの作成はWeb開発ToolやText Editorの役割であり、OSの主な役割ではありません。OSはあくまでSystemを管理する基盤Softwareです。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Web Pageの作成", "is_correct": True, "display_order": 1},
                {"choice_text": "Hardware資源の管理", "is_correct": False, "display_order": 2},
                {"choice_text": "Applicationの実行環境提供", "is_correct": False, "display_order": 3},
                {"choice_text": "Fileの管理", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "IP AddressのVersion 4 (IPv4) で使用されるBit数は？",
            "explanation": "IPv4 Addressは32 bitで構成され、一般的に「192.168.1.1」のような4つのDecimal数（各0-255）で表現されます。IPv6は128 bitです。IPv4の枯渇問題に対応するため、IPv6への移行が進んでいます。Subnetの概念を理解することも重要です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "32 bit", "is_correct": True, "display_order": 1},
                {"choice_text": "16 bit", "is_correct": False, "display_order": 2},
                {"choice_text": "64 bit", "is_correct": False, "display_order": 3},
                {"choice_text": "128 bit", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "TCP/IP ModelにおけるTransport Layerに属するProtocolはどれですか？",
            "explanation": "TCP (Transmission Control Protocol) とUDPはTransport Layerに属します。TCPは信頼性の高い通信を提供し、UDPは高速だが信頼性は保証されません。HTTPやFTPはApplication Layer、IPはInternet Layerに属します。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "TCP", "is_correct": True, "display_order": 1},
                {"choice_text": "HTTP", "is_correct": False, "display_order": 2},
                {"choice_text": "IP", "is_correct": False, "display_order": 3},
                {"choice_text": "FTP", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "CPUのClockとは何を示していますか？",
            "explanation": "CPU Clockは、CPUが1秒間に実行できる動作の回数を示します。単位はHertz (Hz) で、現代のCPUは数GHz (Giga Hertz = 10億Hz) で動作します。Clock数が高いほど一般的に処理速度が速くなりますが、Core数やArchitectureも性能に影響します。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "CPUの動作周波数", "is_correct": True, "display_order": 1},
                {"choice_text": "CPUの温度", "is_correct": False, "display_order": 2},
                {"choice_text": "CPUの消費電力", "is_correct": False, "display_order": 3},
                {"choice_text": "CPUの物理的なサイズ", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "RAMとROMの違いとして正しいものはどれですか？",
            "explanation": "RAM (Random Access Memory) は揮発性Memoryで、電源を切るとデータが消えます。ROM (Read-Only Memory) は不揮発性Memoryで、電源を切ってもデータが保持されます。RAMは作業用Memory、ROMはFirmwareなどの永続的なデータ保存に使用されます。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "RAMは揮発性、ROMは不揮発性", "is_correct": True, "display_order": 1},
                {"choice_text": "RAMは不揮発性、ROMは揮発性", "is_correct": False, "display_order": 2},
                {"choice_text": "両方とも揮発性", "is_correct": False, "display_order": 3},
                {"choice_text": "両方とも不揮発性", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "DNSの主な役割は何ですか？",
            "explanation": "DNS (Domain Name System) は、人間が読みやすいDomain Name（例: google.com）をIPアドレス（例: 142.250.196.78）に変換します。これにより、数字の羅列を覚えなくても、わかりやすい名前でWebsiteにAccessできます。Internetの電話帳のような役割です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Domain NameをIP Addressに変換", "is_correct": True, "display_order": 1},
                {"choice_text": "Emailの送受信", "is_correct": False, "display_order": 2},
                {"choice_text": "Fileの圧縮", "is_correct": False, "display_order": 3},
                {"choice_text": "Dataの暗号化", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Cloud Computingの主なService Modelに含まれないものはどれですか？",
            "explanation": "Cloud ComputingのService Modelは、IaaS (Infrastructure as a Service)、PaaS (Platform as a Service)、SaaS (Software as a Service) の3つが主要です。DaaS (Data as a Service) という用語もありますが、主要な3つのModelには含まれません。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "DaaS (Data as a Service)", "is_correct": True, "display_order": 1},
                {"choice_text": "IaaS (Infrastructure as a Service)", "is_correct": False, "display_order": 2},
                {"choice_text": "PaaS (Platform as a Service)", "is_correct": False, "display_order": 3},
                {"choice_text": "SaaS (Software as a Service)", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Bit (ビット) とByte (バイト) の関係として正しいものはどれですか？",
            "explanation": "1 Byte = 8 bitです。Bitは最小単位で0または1の値を持ちます。Byteは8 bitをまとめた単位で、ASCII文字1文字を表現できます。Data容量は通常Byte単位（KB、MB、GB）で表されます。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "1 Byte = 8 bit", "is_correct": True, "display_order": 1},
                {"choice_text": "1 Byte = 16 bit", "is_correct": False, "display_order": 2},
                {"choice_text": "1 Byte = 4 bit", "is_correct": False, "display_order": 3},
                {"choice_text": "1 Byte = 1 bit", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "RAID 1 (Mirroring) の主な目的は何ですか？",
            "explanation": "RAID 1 (Mirroring) は、同じDataを複数のDiskに書き込むことで、冗長性を確保しData保護を実現します。1台のDiskが故障してもDataは保持されます。性能向上が目的のRAID 0 (Striping) とは異なります。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Data保護のための冗長性確保", "is_correct": True, "display_order": 1},
                {"choice_text": "Read/Write速度の向上", "is_correct": False, "display_order": 2},
                {"choice_text": "Storage容量の増加", "is_correct": False, "display_order": 3},
                {"choice_text": "消費電力の削減", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "HTTPとHTTPSの主な違いは何ですか？",
            "explanation": "HTTPSは、HTTPに暗号化機能（SSL/TLS）を追加したProtocolです。通信内容が暗号化されるため、第三者による盗聴や改ざんを防ぐことができます。現代のWebでは、個人情報を扱うSiteはHTTPSが必須です。URLは「https://」で始まります。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "通信の暗号化の有無", "is_correct": True, "display_order": 1},
                {"choice_text": "通信速度の違い", "is_correct": False, "display_order": 2},
                {"choice_text": "対応Browserの違い", "is_correct": False, "display_order": 3},
                {"choice_text": "File転送の可否", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Virtual Machineの主なメリットとして適切でないものはどれですか？",
            "explanation": "Virtual Machineは、1台の物理Serverで複数のOSを実行でき、Resource効率が向上します。しかし、仮想化LayerのOverheadにより、物理Machineと比較して若干の性能低下が発生します。Isolation、柔軟性、Cost削減などがメリットです。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "物理Machineより高速な処理", "is_correct": True, "display_order": 1},
                {"choice_text": "Hardware資源の効率的な利用", "is_correct": False, "display_order": 2},
                {"choice_text": "複数のOSを同時実行可能", "is_correct": False, "display_order": 3},
                {"choice_text": "環境の簡単な複製・移行", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "MAC Addressに関する説明として正しいものはどれですか？",
            "explanation": "MAC (Media Access Control) Addressは、Network Interface Cardに割り当てられた物理Address（Hardware Address）です。48 bit（6 Byte）で、世界中で一意です。例: 00:1A:2B:3C:4D:5E。IP AddressがLogical Addressであるのに対し、MAC AddressはPhysical Addressです。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Network機器の物理Address", "is_correct": True, "display_order": 1},
                {"choice_text": "Userの識別番号", "is_correct": False, "display_order": 2},
                {"choice_text": "Softwareの License Key", "is_correct": False, "display_order": 3},
                {"choice_text": "Emailの送信元Address", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "SSDとHDDの主な違いとして正しいものはどれですか？",
            "explanation": "SSD (Solid State Drive) は半導体Memory、HDD (Hard Disk Drive) は磁気Diskを使用します。SSDは可動部品がないため、高速・静音・耐衝撃性に優れますが、容量あたりの価格は高めです。HDDは大容量・低価格ですが、速度と耐久性ではSSDに劣ります。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "SSDは半導体、HDDは磁気Disk", "is_correct": True, "display_order": 1},
                {"choice_text": "SSDは磁気Disk、HDDは半導体", "is_correct": False, "display_order": 2},
                {"choice_text": "両方とも磁気Diskを使用", "is_correct": False, "display_order": 3},
                {"choice_text": "両方とも半導体を使用", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Cookieの主な用途として適切でないものはどれですか？",
            "explanation": "Cookieは、WebsiteがBrowserに保存する小さなText Dataです。Login状態の維持、User設定の保存、広告Trackingなどに使用されます。しかし、Server側のDatabaseへのDataの直接保存はCookieの用途ではありません。Cookieは Client側に保存されます。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Server側のDatabaseへのData保存", "is_correct": True, "display_order": 1},
                {"choice_text": "Login状態の維持", "is_correct": False, "display_order": 2},
                {"choice_text": "User設定の保存", "is_correct": False, "display_order": 3},
                {"choice_text": "Website訪問履歴のTracking", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Load Balancerの主な役割は何ですか？",
            "explanation": "Load Balancerは、複数のServerに対してTrafficを分散させることで、負荷を均等化し、可用性とScalabilityを向上させます。1台のServerに負荷が集中するのを防ぎ、Serverダウン時も他のServerで処理を継続できます。AWS ELBやNginxなどが有名です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "複数のServerへTrafficを分散", "is_correct": True, "display_order": 1},
                {"choice_text": "Dataの暗号化", "is_correct": False, "display_order": 2},
                {"choice_text": "Virusのスキャン", "is_correct": False, "display_order": 3},
                {"choice_text": "User認証の管理", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "API (Application Programming Interface) の主な役割は何ですか？",
            "explanation": "APIは、異なるSoftware間で機能やDataをやり取りするための Interface（仕様）です。REST APIやGraphQL APIなどがあり、Web ServiceやMobile Appの開発に広く使用されます。例えば、天気情報APIを使うことで、自分のAppに天気情報を表示できます。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Software間のData・機能のやり取り", "is_correct": True, "display_order": 1},
                {"choice_text": "User InterfaceのDesign", "is_correct": False, "display_order": 2},
                {"choice_text": "Databaseの管理", "is_correct": False, "display_order": 3},
                {"choice_text": "Networkの監視", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Container技術（例: Docker）の主なメリットとして適切でないものはどれですか？",
            "explanation": "Containerは軽量で高速起動が特徴ですが、Kernelは Host OSと共有します。完全なOS Isolationが必要な場合はVirtual Machineを使用します。Containerは、Application実行環境の一貫性、移植性、Resource効率が主なメリットです。",
            "difficulty": 3,
            "choices": [
                {"choice_text": "完全なOS Isolation", "is_correct": True, "display_order": 1},
                {"choice_text": "高速な起動時間", "is_correct": False, "display_order": 2},
                {"choice_text": "環境の一貫性確保", "is_correct": False, "display_order": 3},
                {"choice_text": "軽量なResource消費", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Latency (レイテンシ) とは何を示す指標ですか？",
            "explanation": "Latencyは、Requestを送信してから Responseが返ってくるまでの遅延時間です。単位はミリ秒（ms）で、Network性能やUser体験に大きく影響します。Latencyが低いほど応答が速く、快適です。Throughput（単位時間あたりの処理量）とは異なる概念です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "通信の遅延時間", "is_correct": True, "display_order": 1},
                {"choice_text": "Data転送速度", "is_correct": False, "display_order": 2},
                {"choice_text": "CPU使用率", "is_correct": False, "display_order": 3},
                {"choice_text": "Memory容量", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "CacheとはどのようなMemory技術ですか？",
            "explanation": "Cacheは、頻繁にAccessされるDataを高速なMemoryに一時保存する技術です。CPU Cache、Browser Cache、CDN Cacheなど様々な階層で使用されます。Cache Hitすると高速にDataを取得でき、全体の性能が向上します。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "頻繁に使うDataの一時保存領域", "is_correct": True, "display_order": 1},
                {"choice_text": "長期的なData保管Storage", "is_correct": False, "display_order": 2},
                {"choice_text": "削除されたFileの復元領域", "is_correct": False, "display_order": 3},
                {"choice_text": "Virusを隔離する領域", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Bandwidthに関する説明として正しいものはどれですか？",
            "explanation": "Bandwidthは、Networkで単位時間あたりに転送できるDataの最大量を示します。単位は bps (bits per second) で、例えば100 Mbpsは1秒間に100メガビットのDataを転送できることを意味します。Bandwidthが大きいほど、大容量Dataの転送が可能です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "単位時間あたりのData転送量", "is_correct": True, "display_order": 1},
                {"choice_text": "Networkの物理的な距離", "is_correct": False, "display_order": 2},
                {"choice_text": "接続可能なDevice数", "is_correct": False, "display_order": 3},
                {"choice_text": "Serverの処理能力", "is_correct": False, "display_order": 4}
            ]
        }
    ]
    
    for q_data in questions_data:
        # 既存チェック
        existing = Question.query.filter_by(
            category_id=category.id,
            question_text=q_data['question_text']
        ).first()
        
        if not existing:
            choices_data = q_data.pop('choices')
            question = Question(category_id=category.id, **q_data)
            db.session.add(question)
            db.session.flush()
            
            for choice_data in choices_data:
                choice = Choice(question_id=question.id, **choice_data)
                db.session.add(choice)
    
    db.session.commit()
    
    total_questions = Question.query.filter_by(category_id=category.id).count()
    print(f"IT基礎カテゴリの問題: {total_questions}問")


def init_it_basics_terms():
    """IT基礎カテゴリの用語参考リンク"""
    category = Category.query.filter_by(name="IT基礎").first()
    if not category:
        return
    
    terms = [
        {"term_name": "TCP/IP", 
         "description": "Internetで使用される通信Protocolの集合。信頼性の高い通信を実現します。",
         "url": "#", "display_order": 1},
        {"term_name": "DNS (Domain Name System)",
         "description": "Domain NameとIP Addressを対応付けるSystem。Internetの電話帳の役割を果たします。",
         "url": "#", "display_order": 2},
        {"term_name": "Cloud Computing",
         "description": "Internetを通じてComputing資源をService として提供する形態。IaaS、PaaS、SaaSなどがあります。",
         "url": "#", "display_order": 3},
        {"term_name": "Virtual Machine",
         "description": "物理的なComputerを Software的に再現したもの。1台の物理Serverで複数のOSを実行できます。",
         "url": "#", "display_order": 4},
        {"term_name": "API (Application Programming Interface)",
         "description": "Software間でData・機能をやり取りするための Interface。Web Serviceの連携に広く使用されます。",
         "url": "#", "display_order": 5}
    ]
    
    for term_data in terms:
        existing = TermReference.query.filter_by(
            term_name=term_data['term_name'],
            category_id=category.id
        ).first()
        
        if not existing:
            term = TermReference(category_id=category.id, **term_data)
            db.session.add(term)
    
    db.session.commit()
    
    total_terms = TermReference.query.filter_by(category_id=category.id).count()
    print(f"IT基礎用語: {total_terms}件")


def init_programming_questions():
    """プログラミングカテゴリの問題"""
    category = Category.query.filter_by(name="プログラミング").first()
    if not category:
        print("プログラミングカテゴリが見つかりません")
        return
    
    questions_data = [
        {
            "question_text": "変数の命名規則として適切でないものはどれですか？",
            "explanation": "変数名は数字で始めることはできません。多くのProgramming言語では、変数名は文字またはUnderscoreで始まる必要があります。camelCase、snake_case、予約語の回避は一般的な良い慣習です。読みやすく意味のある変数名を付けることが重要です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "数字で始まる変数名", "is_correct": True, "display_order": 1},
                {"choice_text": "camelCaseの使用", "is_correct": False, "display_order": 2},
                {"choice_text": "snake_caseの使用", "is_correct": False, "display_order": 3},
                {"choice_text": "予約語を避ける", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Stack (スタック) Data Structureの特徴として正しいものはどれですか？",
            "explanation": "Stackは LIFO (Last In, First Out) の原則に従います。最後に追加された要素が最初に取り出されます。Push（追加）とPop（取り出し）が主な操作です。関数呼び出しの管理、Undo機能、式の評価などに使用されます。Queueは FIFO (First In, First Out) です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "LIFO (Last In, First Out)", "is_correct": True, "display_order": 1},
                {"choice_text": "FIFO (First In, First Out)", "is_correct": False, "display_order": 2},
                {"choice_text": "Random Access可能", "is_correct": False, "display_order": 3},
                {"choice_text": "順序を持たない", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "再帰関数 (Recursive Function) の必須要素として正しいものはどれですか？",
            "explanation": "再帰関数には、再帰を終了させる基底条件（Base Case）が必須です。基底条件がないと無限Loopになり、Stack Overflowが発生します。再帰は自分自身を呼び出す関数で、階乗計算、Tree走査、Fibonacci数列などに使用されます。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "基底条件 (Base Case)", "is_correct": True, "display_order": 1},
                {"choice_text": "Global変数の使用", "is_correct": False, "display_order": 2},
                {"choice_text": "複数のReturn文", "is_correct": False, "display_order": 3},
                {"choice_text": "Loop構文", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Object Oriented Programming (OOP) の4大原則に含まれないものはどれですか？",
            "explanation": "OOPの4大原則は、Encapsulation（カプセル化）、Inheritance（継承）、Polymorphism（多態性）、Abstraction（抽象化）です。Recursion（再帰）はProgramming技法の一つですが、OOPの原則には含まれません。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Recursion（再帰）", "is_correct": True, "display_order": 1},
                {"choice_text": "Encapsulation（カプセル化）", "is_correct": False, "display_order": 2},
                {"choice_text": "Inheritance（継承）", "is_correct": False, "display_order": 3},
                {"choice_text": "Polymorphism（多態性）", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Big O Notationで O(1) が示すものは何ですか？",
            "explanation": "O(1)は定数時間を示し、入力Sizeに関わらず常に同じ時間で処理が完了します。例えば、Arrayのindex accessや、Hash TableのKey検索（平均）などです。O(n)は線形時間、O(n²)は二乗時間、O(log n)は対数時間を示します。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "定数時間", "is_correct": True, "display_order": 1},
                {"choice_text": "線形時間", "is_correct": False, "display_order": 2},
                {"choice_text": "二乗時間", "is_correct": False, "display_order": 3},
                {"choice_text": "対数時間", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Gitにおける 'commit' の役割は何ですか？",
            "explanation": "Git commitは、変更履歴をLocal Repositoryに保存する操作です。Snapshotを作成し、後で変更を追跡・復元できます。commitには意味のあるMessageを付けることが重要です。pushはRemote Repositoryへの送信、pullは取得、cloneは複製です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "変更をLocal Repositoryに保存", "is_correct": True, "display_order": 1},
                {"choice_text": "Remote Repositoryから取得", "is_correct": False, "display_order": 2},
                {"choice_text": "Branchを削除", "is_correct": False, "display_order": 3},
                {"choice_text": "Fileを圧縮", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Binary Search (二分探索) Algorithmの前提条件は何ですか？",
            "explanation": "Binary Searchは、Dataがソート済みであることが前提です。中央の要素と比較し、探索範囲を半分ずつ絞り込みます。時間計算量は O(log n) で、線形探索の O(n) より効率的です。ただし、ソートされていないDataには使用できません。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Dataがソート済み", "is_correct": True, "display_order": 1},
                {"choice_text": "Dataが未ソート", "is_correct": False, "display_order": 2},
                {"choice_text": "Dataが重複なし", "is_correct": False, "display_order": 3},
                {"choice_text": "Dataが数値のみ", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "例外処理 (Exception Handling) の主な目的は何ですか？",
            "explanation": "例外処理は、Programの異常な状態（Error）を適切に処理し、Programのクラッシュを防ぐことが目的です。try-catch（またはtry-except）構文を使用し、Errorが発生してもGracefulに対応できます。適切なError Messageや回復処理を実装することが重要です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Errorを適切に処理しクラッシュを防ぐ", "is_correct": True, "display_order": 1},
                {"choice_text": "Programの実行速度を向上", "is_correct": False, "display_order": 2},
                {"choice_text": "Memoryの使用量を削減", "is_correct": False, "display_order": 3},
                {"choice_text": "Codeの行数を削減", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Hash Table (Hash Map) の平均時間計算量として正しいものはどれですか？",
            "explanation": "Hash Tableは、Key-Value pairを格納するData Structureで、平均的な検索・挿入・削除の時間計算量は O(1) です。Hash関数でKeyをIndexに変換します。衝突（Collision）が多い場合は最悪 O(n) になることもありますが、適切なHash関数を使用すれば平均 O(1) を維持できます。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "O(1)", "is_correct": True, "display_order": 1},
                {"choice_text": "O(n)", "is_correct": False, "display_order": 2},
                {"choice_text": "O(log n)", "is_correct": False, "display_order": 3},
                {"choice_text": "O(n²)", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Mutable (可変) とImmutable (不変) の違いとして正しいものはどれですか？",
            "explanation": "MutableなObjectは作成後に内容を変更できますが、ImmutableなObjectは変更できません。例えば、PythonではListはMutable、TupleやStringはImmutableです。Immutableは Thread-Safeで、Hash Tableの Keyとして使用できるメリットがあります。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Mutableは変更可能、Immutableは変更不可", "is_correct": True, "display_order": 1},
                {"choice_text": "Mutableは変更不可、Immutableは変更可能", "is_correct": False, "display_order": 2},
                {"choice_text": "両方とも変更可能", "is_correct": False, "display_order": 3},
                {"choice_text": "両方とも変更不可", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Unit Test (単体Test) の主な目的は何ですか？",
            "explanation": "Unit Testは、個々の関数やMethodが正しく動作することを確認するTestです。早期にBugを発見し、Refactoring時の安全性を確保します。Test Driven Development (TDD) では、Codeを書く前にTestを書きます。JUnit、pytest、Jestなどの Framework が使用されます。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "個々の関数・Methodの動作確認", "is_correct": True, "display_order": 1},
                {"choice_text": "User Interfaceの確認", "is_correct": False, "display_order": 2},
                {"choice_text": "Network接続の確認", "is_correct": False, "display_order": 3},
                {"choice_text": "Database性能の確認", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Quick Sortの平均時間計算量はどれですか？",
            "explanation": "Quick Sortは分割統治法に基づくSort Algorithmで、平均時間計算量は O(n log n) です。Pivot要素を選び、それより小さい要素と大きい要素に分割して再帰的にSortします。最悪の場合は O(n²) ですが、Random Pivotを使用することで回避できます。",
            "difficulty": 3,
            "choices": [
                {"choice_text": "O(n log n)", "is_correct": True, "display_order": 1},
                {"choice_text": "O(n)", "is_correct": False, "display_order": 2},
                {"choice_text": "O(n²)", "is_correct": False, "display_order": 3},
                {"choice_text": "O(log n)", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "API (Application Programming Interface) のREST原則に含まれないものはどれですか？",
            "explanation": "RESTful APIの原則には、Stateless（状態を持たない）、Client-Server分離、Cacheability、Uniform Interface、Layered Systemなどがあります。Binary Communicationは原則ではなく、RESTは通常HTTPとJSONを使用したText-basedの通信です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Binary Communication", "is_correct": True, "display_order": 1},
                {"choice_text": "Stateless（状態を持たない）", "is_correct": False, "display_order": 2},
                {"choice_text": "Client-Server分離", "is_correct": False, "display_order": 3},
                {"choice_text": "Uniform Interface", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Design Patternの「Singleton Pattern」とは何ですか？",
            "explanation": "Singleton Patternは、Classのインスタンスが1つだけ存在することを保証するDesign Patternです。Global状態の管理、Database接続、Loggerなどに使用されます。ただし、Test困難性やGlobal状態による副作用のため、慎重に使用すべきです。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Classのインスタンスを1つに制限", "is_correct": True, "display_order": 1},
                {"choice_text": "複数のインスタンスを同時生成", "is_correct": False, "display_order": 2},
                {"choice_text": "Objectを複製するPattern", "is_correct": False, "display_order": 3},
                {"choice_text": "Interfaceを統一するPattern", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "関数型Programming (Functional Programming) の特徴として適切でないものはどれですか？",
            "explanation": "関数型Programmingは、Immutable Data、Pure Function（副作用なし）、Higher-Order Function（関数を引数や戻り値として扱う）が特徴です。Global変数の頻繁な使用は、関数型Programmingの原則に反します。Haskell、Lisp、Scalaなどが代表的な言語です。",
            "difficulty": 3,
            "choices": [
                {"choice_text": "Global変数の頻繁な使用", "is_correct": True, "display_order": 1},
                {"choice_text": "Immutable Data", "is_correct": False, "display_order": 2},
                {"choice_text": "Pure Function（副作用なし）", "is_correct": False, "display_order": 3},
                {"choice_text": "Higher-Order Function", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Dynamic Typing (動的型付け) とStatic Typing (静的型付け) の違いとして正しいものはどれですか？",
            "explanation": "Static Typingは Compile時に型Check、Dynamic Typingは実行時に型Checkが行われます。Python、JavaScriptはDynamic、Java、C++、TypeScriptはStaticです。Static Typingは早期Error検出、Dynamic Typingは柔軟性が特徴です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "型Checkのタイミングが異なる", "is_correct": True, "display_order": 1},
                {"choice_text": "Memoryの使用量が異なる", "is_correct": False, "display_order": 2},
                {"choice_text": "実行速度が必ず異なる", "is_correct": False, "display_order": 3},
                {"choice_text": "使用できるData型が異なる", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Linked List (連結List) の主な利点は何ですか？",
            "explanation": "Linked Listは、要素の挿入・削除が O(1)（位置がわかっている場合）で効率的です。ArrayはIndex Accessが O(1) ですが、中間への挿入・削除は O(n) です。Linked ListはNode間のPointer（参照）で繋がっており、動的なSize変更が容易です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "要素の挿入・削除が効率的", "is_correct": True, "display_order": 1},
                {"choice_text": "Random Accessが高速", "is_correct": False, "display_order": 2},
                {"choice_text": "Memory使用量が少ない", "is_correct": False, "display_order": 3},
                {"choice_text": "Sortが高速", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Compile言語とScript言語の主な違いは何ですか？",
            "explanation": "Compile言語（C、C++、Javaなど）はSource CodeをMachine CodeやByte Codeに変換してから実行します。Script言語（Python、JavaScriptなど）はInterpreterで1行ずつ実行されます。Compile言語は一般的に高速ですが、Script言語は柔軟性と開発速度に優れます。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "事前Compileの有無", "is_correct": True, "display_order": 1},
                {"choice_text": "使用できるData構造", "is_correct": False, "display_order": 2},
                {"choice_text": "変数の命名規則", "is_correct": False, "display_order": 3},
                {"choice_text": "Comment記法", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "DRY原則 (Don't Repeat Yourself) が意味することは何ですか？",
            "explanation": "DRY原則は、同じCodeや知識を重複させないという原則です。重複を避けることで、保守性が向上し、Bugの修正が容易になります。関数化、Classの活用、Moduleの分離などで実現します。SOLID原則と並ぶ重要なSoftware開発原則です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Codeの重複を避ける", "is_correct": True, "display_order": 1},
                {"choice_text": "Commentを書かない", "is_correct": False, "display_order": 2},
                {"choice_text": "Global変数を使わない", "is_correct": False, "display_order": 3},
                {"choice_text": "長い関数を避ける", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Garbage Collection (GC) の主な役割は何ですか？",
            "explanation": "Garbage Collectionは、使用されなくなったMemoryを自動的に解放する機能です。Java、Python、JavaScriptなどの言語に実装されており、Memory Leakを防ぎます。C/C++では手動でMemory管理が必要ですが、GCのある言語ではProgrammerの負担が軽減されます。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "不要なMemoryの自動解放", "is_correct": True, "display_order": 1},
                {"choice_text": "Codeの最適化", "is_correct": False, "display_order": 2},
                {"choice_text": "Errorの自動修正", "is_correct": False, "display_order": 3},
                {"choice_text": "Fileの削除", "is_correct": False, "display_order": 4}
            ]
        }
    ]
    
    for q_data in questions_data:
        # 既存チェック
        existing = Question.query.filter_by(
            category_id=category.id,
            question_text=q_data['question_text']
        ).first()
        
        if not existing:
            choices_data = q_data.pop('choices')
            question = Question(category_id=category.id, **q_data)
            db.session.add(question)
            db.session.flush()
            
            for choice_data in choices_data:
                choice = Choice(question_id=question.id, **choice_data)
                db.session.add(choice)
    
    db.session.commit()
    
    total_questions = Question.query.filter_by(category_id=category.id).count()
    print(f"プログラミングカテゴリの問題: {total_questions}問")


def init_programming_terms():
    """プログラミングカテゴリの用語参考リンク"""
    category = Category.query.filter_by(name="プログラミング").first()
    if not category:
        return
    
    terms = [
        {"term_name": "Data Structure (データ構造)", 
         "description": "Dataを効率的に格納・管理するための構造。Array、List、Stack、Queue、Tree、Hash Tableなどがあります。",
         "url": "#", "display_order": 1},
        {"term_name": "Algorithm (アルゴリズム)",
         "description": "問題を解決するための手順。Sort、探索、Graph探索など様々なAlgorithmがあり、効率性が重要です。",
         "url": "#", "display_order": 2},
        {"term_name": "Object Oriented Programming (OOP)",
         "description": "Objectを中心としたProgramming手法。Encapsulation、Inheritance、Polymorphismが特徴です。",
         "url": "#", "display_order": 3},
        {"term_name": "Git",
         "description": "分散型Version管理System。Codeの変更履歴を管理し、共同開発を支援します。",
         "url": "#", "display_order": 4},
        {"term_name": "Design Pattern",
         "description": "繰り返し現れる問題に対する再利用可能な解決策。Singleton、Factory、Observerなど様々なPatternがあります。",
         "url": "#", "display_order": 5}
    ]
    
    for term_data in terms:
        existing = TermReference.query.filter_by(
            term_name=term_data['term_name'],
            category_id=category.id
        ).first()
        
        if not existing:
            term = TermReference(category_id=category.id, **term_data)
            db.session.add(term)
    
    db.session.commit()
    
    total_terms = TermReference.query.filter_by(category_id=category.id).count()
    print(f"プログラミング用語: {total_terms}件")


def init_project_management_questions():
    """プロジェクトマネージメントカテゴリの問題"""
    category = Category.query.filter_by(name="プロジェクトマネージメント").first()
    if not category:
        print("プロジェクトマネージメントカテゴリが見つかりません")
        return
    
    questions_data = [
        {
            "question_text": "Agile開発手法の特徴として適切でないものはどれですか？",
            "explanation": "Agile開発は、短いIterationでの開発、変更への柔軟な対応、顧客との継続的なCollaborationが特徴です。詳細な事前計画と変更の最小化はWaterfall開発の特徴であり、Agileでは変化を歓迎します。Scrum、Kanban、XPなどがAgile手法の代表例です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "詳細な事前計画と変更の最小化", "is_correct": True, "display_order": 1},
                {"choice_text": "短いIterationでの開発", "is_correct": False, "display_order": 2},
                {"choice_text": "顧客との継続的なCollaboration", "is_correct": False, "display_order": 3},
                {"choice_text": "変化への柔軟な対応", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "ScrumにおけるSprint期間として一般的なものはどれですか？",
            "explanation": "Sprintは通常1〜4週間で設定されることが多く、2週間が最も一般的です。短すぎるとOverheadが大きく、長すぎると柔軟性が失われます。Sprint終了時にはReviewとRetrospectiveを実施し、継続的な改善を図ります。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "1〜4週間", "is_correct": True, "display_order": 1},
                {"choice_text": "1〜3日", "is_correct": False, "display_order": 2},
                {"choice_text": "2〜6ヶ月", "is_correct": False, "display_order": 3},
                {"choice_text": "期間の定めなし", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "PMBOKにおけるProject管理の知識エリアに含まれないものはどれですか？",
            "explanation": "PMBOK (Project Management Body of Knowledge) の10の知識エリアは、統合、Scope、Schedule、Cost、品質、Resource、Communication、Risk、調達、Stakeholder管理です。Marketing戦略は知識エリアには含まれません。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Marketing戦略", "is_correct": True, "display_order": 1},
                {"choice_text": "Risk管理", "is_correct": False, "display_order": 2},
                {"choice_text": "Cost管理", "is_correct": False, "display_order": 3},
                {"choice_text": "Stakeholder管理", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Waterfall開発手法の主な特徴は何ですか？",
            "explanation": "Waterfall手法は、要件定義→設計→実装→Test→運用という順序で進み、前工程が完了してから次工程に進みます。変更に弱いですが、計画が明確で、安定した要件のProjectに適しています。対照的にAgileは反復的な開発を行います。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "順序的に工程を進める", "is_correct": True, "display_order": 1},
                {"choice_text": "反復的に開発を進める", "is_correct": False, "display_order": 2},
                {"choice_text": "並行して全工程を実施", "is_correct": False, "display_order": 3},
                {"choice_text": "工程の順序が自由", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Critical Path Method (CPM) の主な目的は何ですか？",
            "explanation": "CPMは、Projectの最短完了期間を求め、遅延が許されないCritical（重要）なTaskの連鎖を特定する手法です。Critical Path上のTaskが遅れると、Project全体が遅延します。Resource配分や進捗管理の優先順位付けに活用されます。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "最短完了期間の算出", "is_correct": True, "display_order": 1},
                {"choice_text": "予算の最適化", "is_correct": False, "display_order": 2},
                {"choice_text": "Team Memberの評価", "is_correct": False, "display_order": 3},
                {"choice_text": "品質の測定", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Stakeholderとは誰を指しますか？",
            "explanation": "Stakeholderは、Projectに影響を与える、またはProjectから影響を受けるすべての個人や組織です。Customer、Sponsor、Team Member、経営陣、End User、Vendorなど多岐にわたります。適切なStakeholder管理がProject成功の鍵となります。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Projectに関わる全ての関係者", "is_correct": True, "display_order": 1},
                {"choice_text": "Project Managerのみ", "is_correct": False, "display_order": 2},
                {"choice_text": "Customerのみ", "is_correct": False, "display_order": 3},
                {"choice_text": "開発Teamのみ", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Risk管理のプロセスに含まれないものはどれですか？",
            "explanation": "Risk管理は、Risk特定、分析、対応計画、監視・管理のプロセスで構成されます。品質Test実施はQuality管理の一部であり、Risk管理の直接的なプロセスではありません。Riskは不確実な事象で、プラス（機会）とマイナス（脅威）の両方があります。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "品質Test実施", "is_correct": True, "display_order": 1},
                {"choice_text": "Risk特定", "is_correct": False, "display_order": 2},
                {"choice_text": "Risk分析", "is_correct": False, "display_order": 3},
                {"choice_text": "Risk対応計画", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Kanbanの主な特徴として正しいものはどれですか？",
            "explanation": "Kanbanは、Work In Progress (WIP) を制限することで、仕掛かり作業を抑え、Flow効率を高めます。Visualizationを重視し、Taskの流れを可視化します。ScrumのようなFixed Iterationはなく、継続的なFlowでTaskを処理します。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "WIP (Work In Progress) の制限", "is_correct": True, "display_order": 1},
                {"choice_text": "固定的なSprint期間", "is_correct": False, "display_order": 2},
                {"choice_text": "毎日のStand-up必須", "is_correct": False, "display_order": 3},
                {"choice_text": "Role定義が厳格", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "EVM (Earned Value Management) で使用されないMetricsはどれですか？",
            "explanation": "EVMは、PV (Planned Value)、EV (Earned Value)、AC (Actual Cost) の3つの基本Metricsを使用します。ROI (Return on Investment) は投資対効果を示す指標で、EVMの直接的なMetricsではありません。EVMはProject進捗とCostを統合的に管理します。",
            "difficulty": 3,
            "choices": [
                {"choice_text": "ROI (Return on Investment)", "is_correct": True, "display_order": 1},
                {"choice_text": "PV (Planned Value)", "is_correct": False, "display_order": 2},
                {"choice_text": "EV (Earned Value)", "is_correct": False, "display_order": 3},
                {"choice_text": "AC (Actual Cost)", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Daily Scrum (Daily Stand-up) の主な目的は何ですか？",
            "explanation": "Daily Scrumは、Team全体で進捗を共有し、障害を早期発見することが目的です。通常15分以内で、「昨日やったこと」「今日やること」「障害」を共有します。詳細な技術議論や意思決定の場ではなく、同期とTransparency確保が目的です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "進捗共有と障害の早期発見", "is_correct": True, "display_order": 1},
                {"choice_text": "詳細な技術的議論", "is_correct": False, "display_order": 2},
                {"choice_text": "Performanceの評価", "is_correct": False, "display_order": 3},
                {"choice_text": "次Sprintの計画", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Product Backlogに関する説明として正しいものはどれですか？",
            "explanation": "Product Backlogは、Productに必要な機能のPriority付きListです。Product Ownerが管理し、優先度の高いものから順に実装されます。動的に変化し、常にRefinementされます。Sprint Backlogとは異なり、Product全体のBacklogです。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Productに必要な機能のPriority付きList", "is_correct": True, "display_order": 1},
                {"choice_text": "完了したTaskのList", "is_correct": False, "display_order": 2},
                {"choice_text": "Bugの一覧", "is_correct": False, "display_order": 3},
                {"choice_text": "Team Memberの割り当て表", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Retrospective (振り返り) の主な目的は何ですか？",
            "explanation": "Retrospectiveは、Teamが自己改善するための重要な機会です。Sprint終了時に実施し、「良かったこと」「改善すべきこと」「次Sprintで試すこと」を議論します。Blame-freeな環境で、プロセス改善にFocusします。継続的改善の核となる活動です。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Processの継続的改善", "is_correct": True, "display_order": 1},
                {"choice_text": "個人のPerformance評価", "is_correct": False, "display_order": 2},
                {"choice_text": "次Projectの計画", "is_correct": False, "display_order": 3},
                {"choice_text": "Budget承認", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Scopeクリープ (Scope Creep) とは何ですか？",
            "explanation": "Scope Creepは、Project範囲が計画なく徐々に拡大していく現象です。小さな追加要求の積み重ねで、Schedule遅延やBudget超過の原因となります。Change管理プロセスの確立、明確なScope定義、Stakeholderとの合意が予防策です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Project範囲の計画外の拡大", "is_correct": True, "display_order": 1},
                {"choice_text": "Budgetの削減", "is_correct": False, "display_order": 3},
                {"choice_text": "Team規模の縮小", "is_correct": False, "display_order": 2},
                {"choice_text": "Scheduleの短縮", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Definition of Done (DoD) の役割は何ですか？",
            "explanation": "DoDは、TaskやUser Storyが「完了」と見なされる基準を明確に定義したものです。Test完了、Code Review済み、Document更新など、Team全体で合意した完了基準です。Qualityを保証し、認識のズレを防ぎます。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "完了の明確な基準定義", "is_correct": True, "display_order": 1},
                {"choice_text": "Projectの最終納品物", "is_correct": False, "display_order": 2},
                {"choice_text": "Team Memberの役割分担", "is_correct": False, "display_order": 3},
                {"choice_text": "Budget上限の設定", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "三点見積もり (Three-Point Estimation) で使用する3つの値は何ですか？",
            "explanation": "三点見積もりは、楽観値 (Optimistic)、最頻値 (Most Likely)、悲観値 (Pessimistic) の3つを使用します。PERT (Program Evaluation and Review Technique) で用いられ、不確実性を考慮した見積もりが可能です。期待値は (O + 4M + P) / 6 で計算されます。",
            "difficulty": 3,
            "choices": [
                {"choice_text": "楽観値、最頻値、悲観値", "is_correct": True, "display_order": 1},
                {"choice_text": "最小値、平均値、最大値", "is_correct": False, "display_order": 2},
                {"choice_text": "過去値、現在値、未来値", "is_correct": False, "display_order": 3},
                {"choice_text": "計画値、実績値、予測値", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Velocity (ベロシティ) とは何を示す指標ですか？",
            "explanation": "Velocityは、TeamがSprint内で完了できる作業量を示す指標です。Story PointやTask数で測定され、将来のSprintの計画に使用されます。Teamのキャパシティを把握し、現実的な計画を立てるために重要です。Team間の比較には使用できません。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "Teamが完了できる作業量", "is_correct": True, "display_order": 1},
                {"choice_text": "Codeの実行速度", "is_correct": False, "display_order": 2},
                {"choice_text": "Bugの発見率", "is_correct": False, "display_order": 3},
                {"choice_text": "Customerの満足度", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Change管理プロセスの主な目的は何ですか？",
            "explanation": "Change管理は、変更要求を体系的に評価・承認・実装するProcessです。影響分析、優先順位付け、Resource配分、Risk評価を行い、Projectへの悪影響を最小化します。Change Boardが承認判断を行うことが一般的です。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "変更の影響を評価し管理", "is_correct": True, "display_order": 1},
                {"choice_text": "変更を一切受け付けない", "is_correct": False, "display_order": 2},
                {"choice_text": "全ての変更を自動承認", "is_correct": False, "display_order": 3},
                {"choice_text": "Teamの組織変更", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Burndown Chartの主な用途は何ですか？",
            "explanation": "Burndown Chartは、残作業量の推移を時系列で可視化するChartです。X軸が時間、Y軸が残作業量で、理想線と実績線を比較します。Sprint進捗の可視化、遅延の早期発見、Velocity調整の判断に活用されます。Transparencyを高める重要なToolです。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "残作業量の推移を可視化", "is_correct": True, "display_order": 1},
                {"choice_text": "Budgetの消費状況", "is_correct": False, "display_order": 2},
                {"choice_text": "Team Memberの稼働率", "is_correct": False, "display_order": 3},
                {"choice_text": "Customerの満足度", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "MVP (Minimum Viable Product) の目的は何ですか？",
            "explanation": "MVPは、最小限の機能でProductをReleaseし、早期にUser Feedbackを得ることが目的です。仮説検証、Market Fit確認、開発Directionの調整を可能にします。Lean StartupやAgile開発で重視される概念で、無駄な機能開発を避けられます。",
            "difficulty": 2,
            "choices": [
                {"choice_text": "早期のUser Feedback取得", "is_correct": True, "display_order": 1},
                {"choice_text": "完璧なProductの完成", "is_correct": False, "display_order": 2},
                {"choice_text": "全機能の実装", "is_correct": False, "display_order": 3},
                {"choice_text": "Costの最大化", "is_correct": False, "display_order": 4}
            ]
        },
        {
            "question_text": "Lessons Learned (教訓) の収集時期として最も適切なのはどれですか？",
            "explanation": "Lessons Learnedは、Project全体を通じて継続的に収集すべきです。各Phase終了時、Major Milestone時、Project完了時だけでなく、日々の活動から学びを得ることが重要です。知識Management Systemに蓄積し、組織の資産とします。",
            "difficulty": 1,
            "choices": [
                {"choice_text": "Project全体を通じて継続的に", "is_correct": True, "display_order": 1},
                {"choice_text": "Project完了時のみ", "is_correct": False, "display_order": 2},
                {"choice_text": "問題発生時のみ", "is_correct": False, "display_order": 3},
                {"choice_text": "収集する必要なし", "is_correct": False, "display_order": 4}
            ]
        }
    ]
    
    for q_data in questions_data:
        # 既存チェック
        existing = Question.query.filter_by(
            category_id=category.id,
            question_text=q_data['question_text']
        ).first()
        
        if not existing:
            choices_data = q_data.pop('choices')
            question = Question(category_id=category.id, **q_data)
            db.session.add(question)
            db.session.flush()
            
            for choice_data in choices_data:
                choice = Choice(question_id=question.id, **choice_data)
                db.session.add(choice)
    
    db.session.commit()
    
    total_questions = Question.query.filter_by(category_id=category.id).count()
    print(f"プロジェクトマネージメントカテゴリの問題: {total_questions}問")


def init_project_management_terms():
    """プロジェクトマネージメントカテゴリの用語参考リンク"""
    category = Category.query.filter_by(name="プロジェクトマネージメント").first()
    if not category:
        return
    
    terms = [
        {"term_name": "Agile", 
         "description": "変化に柔軟に対応する反復的な開発手法。Scrum、Kanban、XPなどが含まれます。",
         "url": "#", "display_order": 1},
        {"term_name": "Scrum",
         "description": "Agile Frameworkの一つ。Sprint、Daily Scrum、Retrospectiveなどの要素で構成されます。",
         "url": "#", "display_order": 2},
        {"term_name": "PMBOK",
         "description": "Project Management Body of Knowledge。PMIが発行するProject管理の知識体系。",
         "url": "#", "display_order": 3},
        {"term_name": "Risk Management",
         "description": "Project上の不確実性を特定・分析・対応するProcess。脅威と機会の両方を扱います。",
         "url": "#", "display_order": 4},
        {"term_name": "Stakeholder Management",
         "description": "Projectに関わる全関係者のExpectationを管理し、適切にEngageするProcess。",
         "url": "#", "display_order": 5}
    ]
    
    for term_data in terms:
        existing = TermReference.query.filter_by(
            term_name=term_data['term_name'],
            category_id=category.id
        ).first()
        
        if not existing:
            term = TermReference(category_id=category.id, **term_data)
            db.session.add(term)
    
    db.session.commit()
    
    total_terms = TermReference.query.filter_by(category_id=category.id).count()
    print(f"プロジェクトマネージメント用語: {total_terms}件")


def init_users():
    """ユーザーの初期データ（デフォルト管理者）"""
    # デフォルト管理者を作成
    admin_email = 'admin@example.com'
    admin_password = 'admin123'
    
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            role='admin',
            is_active=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print(f"デフォルト管理者を作成しました: {admin_email} / {admin_password}")
    else:
        print("デフォルト管理者は既に存在します")


def main():
    """メイン処理"""
    app = create_app('development')
    
    with app.app_context():
        # データベースを作成
        db.create_all()
        print("データベーステーブルを作成しました")
        
        # 初期データを投入
        init_users()
        init_categories()
        init_security_questions()
        init_security_terms()
        init_it_basics_questions()
        init_it_basics_terms()
        init_programming_questions()
        init_programming_terms()
        init_project_management_questions()
        init_project_management_terms()
        
        print("\n初期データの投入が完了しました！")
        print("python run.py でアプリケーションを起動できます")


if __name__ == '__main__':
    main()

