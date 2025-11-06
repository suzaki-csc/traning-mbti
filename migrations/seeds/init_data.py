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
        
        print("\n初期データの投入が完了しました！")
        print("python run.py でアプリケーションを起動できます")


if __name__ == '__main__':
    main()

