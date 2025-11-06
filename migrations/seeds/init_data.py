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
        
        print("\n初期データの投入が完了しました！")
        print("python run.py でアプリケーションを起動できます")


if __name__ == '__main__':
    main()

