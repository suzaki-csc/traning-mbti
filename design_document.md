# MBTI風性格診断Webアプリ 設計書

## 1. 概要

Flask、Bootstrap、Docker、Docker Compose、MySQLを使用したMBTI風の性格診断Webアプリケーション。
利用者と管理者の2つの権限レベルを持ち、診断の実施と履歴管理を行う。

## 2. 技術スタック

- **バックエンド**: Flask (Python)
- **フロントエンド**: Bootstrap 5
- **データベース**: MySQL 8.0
- **コンテナ**: Docker, Docker Compose
- **認証**: Flask-Login
- **ORM**: SQLAlchemy
- **パッケージ管理**: Poetry

## 3. システムアーキテクチャ

```
┌─────────────────┐
│   ユーザー      │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────────────────────┐
│  Flask アプリコンテナ           │
│  - Webサーバー (Flask)          │
│  - 認証処理                     │
│  - ビジネスロジック             │
│  Port: 5000                     │
└────────────┬────────────────────┘
             │ TCP/IP
             ▼
┌─────────────────────────────────┐
│  MySQL DBコンテナ               │
│  - ユーザー情報                 │
│  - 診断結果履歴                 │
│  Port: 3306                     │
└─────────────────────────────────┘
```

## 4. ディレクトリ構成

```
traning-mbti/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── poetry.lock
├── .env.example
├── README.md
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── auth.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── quiz.py
│   │   └── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── index.html
│   │   ├── quiz.html
│   │   ├── result.html
│   │   ├── history.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       └── all_history.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── quiz.js
│   └── utils/
│       ├── __init__.py
│       ├── questions.py
│       └── scoring.py
└── mysql/
    └── init.sql
```

## 5. データベース設計

### 5.1 usersテーブル
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | ユーザーID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | ユーザー名 |
| email | VARCHAR(100) | UNIQUE, NOT NULL | メールアドレス |
| password_hash | VARCHAR(255) | NOT NULL | ハッシュ化されたパスワード |
| role | ENUM('user', 'admin') | NOT NULL, DEFAULT 'user' | 権限 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 作成日時 |

### 5.2 test_resultsテーブル
| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 結果ID |
| user_id | INT | FOREIGN KEY (users.id) | ユーザーID |
| mbti_type | VARCHAR(4) | NOT NULL | MBTIタイプ (例: INTJ) |
| e_score | INT | NOT NULL | 外向性スコア |
| i_score | INT | NOT NULL | 内向性スコア |
| s_score | INT | NOT NULL | 感覚スコア |
| n_score | INT | NOT NULL | 直観スコア |
| t_score | INT | NOT NULL | 思考スコア |
| f_score | INT | NOT NULL | 感情スコア |
| j_score | INT | NOT NULL | 判断スコア |
| p_score | INT | NOT NULL | 知覚スコア |
| answers | JSON | NOT NULL | 回答データ (質問IDと選択肢) |
| taken_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 診断実施日時 |

## 6. 質問データ構造

### 6.1 質問配列の定義
各質問は以下の構造を持つ：

```python
questions = [
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
    # ... 10〜12問
]
```

### 6.2 4軸の説明
- **E/I軸（外向性/内向性）**: エネルギーの方向性
- **S/N軸（感覚/直観）**: 情報の受け取り方
- **T/F軸（思考/感情）**: 意思決定の基準
- **J/P軸（判断/知覚）**: 外界への接し方

### 6.3 質問例（12問構成）

1. **E/I軸 - 質問1**: 初対面の人との会話は楽しいですか？
2. **E/I軸 - 質問2**: 大勢の集まりと少人数の集まり、どちらが好きですか？
3. **E/I軸 - 質問3**: 休日は外出するのと家でゆっくり過ごすのとどちらが好きですか？

4. **S/N軸 - 質問4**: 新しいことを学ぶとき、具体例と理論、どちらから入りたいですか？
5. **S/N軸 - 質問5**: 物事を説明するとき、詳細な事実と全体像、どちらを重視しますか？
6. **S/N軸 - 質問6**: 現実的で実用的なアイデアと、革新的で未来志向のアイデア、どちらに惹かれますか？

7. **T/F軸 - 質問7**: 意思決定をするとき、論理と感情、どちらを重視しますか？
8. **T/F軸 - 質問8**: 友人が悩みを相談してきたとき、解決策と共感、どちらを優先しますか？
9. **T/F軸 - 質問9**: 批判的に分析することと、調和を保つこと、どちらが得意ですか？

10. **J/P軸 - 質問10**: 計画を立てて行動するのと、その場の流れに任せるのと、どちらが好きですか？
11. **J/P軸 - 質問11**: 仕事や勉強は、締め切り前に余裕を持って終わらせますか？
12. **J/P軸 - 質問12**: 決定を下すことと、選択肢を開いておくこと、どちらが好きですか？

## 7. 採点ロジック

### 7.1 スコア計算アルゴリズム

```python
def calculate_mbti_type(answers):
    """
    回答からMBTIタイプを判定する
    
    Parameters:
        answers: list of dict
            [{"question_id": 1, "axis": "E", "score": 3}, ...]
    
    Returns:
        dict: {
            "mbti_type": "INTJ",
            "scores": {
                "E": 2, "I": 7,
                "S": 3, "N": 6,
                "T": 8, "F": 1,
                "J": 7, "P": 2
            }
        }
    """
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    
    # 各回答のスコアを合算
    for answer in answers:
        axis = answer["axis"]
        score = answer["score"]
        scores[axis] += score
    
    # 各軸で優勢な方を判定
    mbti_type = ""
    mbti_type += "E" if scores["E"] > scores["I"] else "I"
    mbti_type += "S" if scores["S"] > scores["N"] else "N"
    mbti_type += "T" if scores["T"] > scores["F"] else "F"
    mbti_type += "J" if scores["J"] > scores["P"] else "P"
    
    return {
        "mbti_type": mbti_type,
        "scores": scores
    }
```

### 7.2 同点の場合の処理
各軸で同点の場合は、デフォルトで以下を採用：
- E/I軸: I（内向性）
- S/N軸: N（直観）
- T/F軸: F（感情）
- J/P軸: P（知覚）

## 8. ルーティング設計

### 8.1 認証関連
| URL | メソッド | 説明 | 権限 |
|-----|---------|------|------|
| `/login` | GET, POST | ログイン | 全員 |
| `/logout` | GET | ログアウト | ログイン済み |
| `/register` | GET, POST | 新規登録 | 全員 |

### 8.2 診断機能
| URL | メソッド | 説明 | 権限 |
|-----|---------|------|------|
| `/` | GET | トップページ | ログイン済み |
| `/quiz` | GET | 診断開始 | ログイン済み |
| `/quiz/submit` | POST | 診断結果送信 | ログイン済み |
| `/result/<int:result_id>` | GET | 診断結果詳細 | ログイン済み |
| `/history` | GET | 自分の診断履歴 | ログイン済み |

### 8.3 管理機能
| URL | メソッド | 説明 | 権限 |
|-----|---------|------|------|
| `/admin/dashboard` | GET | 管理ダッシュボード | 管理者のみ |
| `/admin/history` | GET | 全ユーザーの診断履歴 | 管理者のみ |
| `/admin/result/<int:result_id>/delete` | POST | 診断結果削除 | 管理者のみ |

## 9. UIデザイン（Bootstrap 5）

### 9.1 共通要素
- **ナビゲーションバー**: サイト名、メニュー、ログアウトボタン
- **レスポンシブデザイン**: モバイル、タブレット、デスクトップ対応
- **カラースキーム**: Bootstrapのデフォルトテーマをベースにカスタマイズ

### 9.2 主要画面の構成

#### ログイン画面 (`login.html`)
- 中央配置のログインフォーム
- ユーザー名/メールアドレス入力
- パスワード入力
- ログインボタン
- 新規登録リンク

#### トップページ (`index.html`)
- ウェルカムメッセージ
- 診断開始ボタン（大きく目立つように）
- 過去の診断履歴へのリンク
- MBTIについての簡単な説明

#### 診断画面 (`quiz.html`)
- 進捗バー（現在の質問/総質問数）
- 質問文（大きく読みやすく）
- 4つの選択肢（ラジオボタン or カード形式）
- 次へボタン / 戻るボタン
- 最後の質問では「結果を見る」ボタン

#### 結果画面 (`result.html`)
- 診断結果のMBTIタイプ（大きく表示）
- タイプの説明（100字程度）
- 各軸のスコア（プログレスバーで視覚化）
- 「もう一度診断する」ボタン
- 「履歴を見る」ボタン

#### 履歴画面 (`history.html`)
- 過去の診断結果一覧（テーブル形式）
- 診断日時、MBTIタイプ
- 詳細表示リンク

#### 管理ダッシュボード (`admin/dashboard.html`)
- 統計情報（総診断数、ユーザー数、各タイプの分布）
- 全履歴へのリンク

#### 全履歴画面 (`admin/all_history.html`)
- 全ユーザーの診断履歴（ページネーション付き）
- ユーザー名、診断日時、MBTIタイプ
- 詳細表示リンク
- 削除ボタン（確認ダイアログ付き）

## 10. セキュリティ考慮事項

### 10.1 認証・認可
- パスワードのハッシュ化（bcrypt使用）
- セッション管理（Flask-Login）
- CSRF保護（Flask-WTF）
- 管理者権限のチェック（デコレーター使用）

### 10.2 データ保護
- SQL Injection対策（SQLAlchemyのパラメータ化クエリ）
- XSS対策（Jinjaテンプレートの自動エスケープ）
- 環境変数での機密情報管理（.env）

## 11. Docker構成

### 11.1 docker-compose.yml 概要

```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: mbti-app
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=mysql+pymysql://user:password@db:3306/mbti_db
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    volumes:
      - ./app:/app/app
    networks:
      - mbti-network

  db:
    image: mysql:8.0
    container_name: mbti-db
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=mbti_db
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
      - ./mysql/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - mbti-network

volumes:
  mysql-data:

networks:
  mbti-network:
    driver: bridge
```

### 11.2 Dockerfile 概要

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Poetryのインストール
RUN pip install poetry

# 依存関係のインストール
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# アプリケーションのコピー
COPY . .

# ポート公開
EXPOSE 5000

# アプリケーション起動
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
```

## 12. 必要なPythonパッケージ

```toml
[tool.poetry.dependencies]
python = "^3.11"
flask = "^3.0"
flask-sqlalchemy = "^3.1"
flask-login = "^0.6"
flask-wtf = "^1.2"
pymysql = "^1.1"
cryptography = "^41.0"
python-dotenv = "^1.0"
bcrypt = "^4.1"

[tool.poetry.dev-dependencies]
pytest = "^7.4"
pytest-flask = "^1.3"
```

## 13. 実装の流れ

### Phase 1: 基本セットアップ
1. プロジェクト構造の作成
2. Dockerファイルの作成
3. データベースの初期化スクリプト作成

### Phase 2: 認証機能
1. ユーザーモデルの実装
2. ログイン/ログアウト機能
3. 新規登録機能
4. 権限チェック機能

### Phase 3: 診断機能
1. 質問データの作成
2. 診断画面の実装
3. 採点ロジックの実装
4. 結果表示画面の実装

### Phase 4: 履歴管理
1. 診断履歴の保存
2. ユーザー自身の履歴表示
3. 管理者用の全履歴表示
4. 削除機能

### Phase 5: UIの改善
1. Bootstrap適用
2. レスポンシブデザイン調整
3. 進捗バーの追加
4. スコアの視覚化

### Phase 6: テストとデプロイ
1. ユニットテストの作成
2. 統合テストの実施
3. Docker環境での動作確認

## 14. MBTIタイプ説明文

各タイプの説明（100字程度）を結果画面に表示：

- **INTJ**: 独創的な戦略家。論理的思考と長期計画を重視し、目標達成に向けて効率的に行動します。
- **INTP**: 理論的な革新者。知的好奇心が強く、複雑な問題を分析し解決策を見出すことを楽しみます。
- **ENTJ**: カリスマ的な指導者。大胆で想像力豊かなリーダーで、障害を乗り越える方法を常に見つけます。
- **ENTP**: 賢い討論者。知的挑戦を愛し、新しいアイデアや可能性を追求することに情熱を注ぎます。
- **INFJ**: 理想主義的な助言者。深い洞察力を持ち、他者の成長を支援することに喜びを感じます。
- **INFP**: 献身的な仲介者。理想と価値観を大切にし、調和と真実性を追求します。
- **ENFJ**: 情熱的な主人公。カリスマ性があり、他者を鼓舞し導くことに長けています。
- **ENFP**: 熱狂的な活動家。創造的で社交的。新しい可能性や人間関係を大切にします。
- **ISTJ**: 実務的な管理者。事実と詳細を重視し、信頼性と責任感が強い性格です。
- **ISFJ**: 献身的な擁護者。思いやりがあり、他者のニーズに敏感で支援することを喜びます。
- **ESTJ**: 優秀な管理者。組織力と決断力があり、物事を効率的に進めることが得意です。
- **ESFJ**: 思いやりのある世話役。協調性が高く、他者との調和を重視し支援します。
- **ISTP**: 大胆な職人。実践的で論理的。手を動かして問題を解決することが得意です。
- **ISFP**: 柔軟な芸術家。感受性豊かで、美と調和を大切にする自由な精神の持ち主です。
- **ESTP**: 活発な起業家。エネルギッシュで行動的。リスクを恐れず新しい経験を求めます。
- **ESFP**: 陽気なエンターテイナー。社交的で楽観的。周囲を楽しませることが得意です。

## 15. エラーハンドリング

- 404エラー: カスタムエラーページ
- 500エラー: エラーログの記録とユーザーフレンドリーなメッセージ
- データベース接続エラー: リトライロジックとエラーメッセージ
- フォームバリデーション: 適切なエラーメッセージの表示

## 16. 今後の拡張可能性

- 診断結果のグラフ表示（Chart.js等）
- 診断結果のPDFエクスポート
- メール通知機能
- 多言語対応
- ソーシャルログイン
- 詳細な統計ダッシュボード
- タイプ別の詳細な特徴説明ページ
- 相性診断機能

---

以上がMBTI風性格診断Webアプリの設計書です。この設計に基づいて実装を進めることで、機能的で保守性の高いアプリケーションを構築できます。

