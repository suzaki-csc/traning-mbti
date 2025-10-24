# MBTI風性格診断Webアプリケーション 設計書

## 1. システム概要

Flask + PostgreSQL + Docker Composeで構築するMBTI風の性格診断Webアプリケーション。
12問の質問に回答し、4軸（E/I、S/N、T/F、J/P）のスコアを計算して16タイプのいずれかに分類します。

### 1.1 技術スタック

- **バックエンド**: Flask 3.x (Python 3.11+)
- **フロントエンド**: Bootstrap 5.x
- **データベース**: PostgreSQL 15
- **コンテナ化**: Docker + Docker Compose
- **ORM**: SQLAlchemy
- **マイグレーション**: Flask-Migrate

---

## 2. ファイル・ディレクトリ構成

```
traning-mbti/
├── docker-compose.yml          # Docker Compose設定
├── .env.example                # 環境変数サンプル
├── .env                        # 環境変数（gitignore対象）
├── README.md                   # プロジェクト説明
├── DESIGN.md                   # 本設計書
│
├── app/                        # Flaskアプリケーション
│   ├── Dockerfile              # アプリコンテナ定義
│   ├── requirements.txt        # Python依存パッケージ
│   ├── app.py                  # アプリケーションエントリーポイント
│   ├── config.py               # 設定ファイル
│   │
│   ├── models/                 # データモデル
│   │   ├── __init__.py
│   │   ├── diagnosis.py        # 診断結果モデル
│   │   └── question.py         # 質問モデル（初期化用）
│   │
│   ├── routes/                 # ルーティング
│   │   ├── __init__.py
│   │   ├── main.py             # メイン診断フロー
│   │   └── admin.py            # 管理画面
│   │
│   ├── services/               # ビジネスロジック
│   │   ├── __init__.py
│   │   ├── scoring.py          # 採点・判定ロジック
│   │   └── questions.py        # 質問データ管理
│   │
│   ├── static/                 # 静的ファイル
│   │   ├── css/
│   │   │   └── custom.css      # カスタムスタイル
│   │   └── js/
│   │       └── app.js          # フロントエンドロジック
│   │
│   └── templates/              # Jinjaテンプレート
│       ├── base.html           # ベーステンプレート
│       ├── index.html          # トップページ
│       ├── question.html       # 質問ページ
│       ├── result.html         # 結果ページ
│       └── admin/
│           ├── dashboard.html  # 管理ダッシュボード
│           └── history.html    # 診断履歴一覧
│
└── db/                         # データベース関連
    ├── Dockerfile              # DBコンテナ定義（カスタマイズ用）
    └── init.sql                # 初期化SQL（オプション）
```

---

## 3. データ構造

### 3.1 質問データ（questions.py内で定義）

```python
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
```

### 3.2 軸マッピング

| 軸 | 意味 | 説明 |
|---|------|------|
| **E** | Extraversion（外向） | エネルギーを外部から得る |
| **I** | Introversion（内向） | エネルギーを内部から得る |
| **S** | Sensing（感覚） | 具体的な事実を重視 |
| **N** | Intuition（直観） | 抽象的な可能性を重視 |
| **T** | Thinking（思考） | 論理と客観性を重視 |
| **F** | Feeling（感情） | 感情と価値観を重視 |
| **J** | Judging（判断） | 計画的で構造的 |
| **P** | Perceiving（知覚） | 柔軟で適応的 |

### 3.3 MBTIタイプの説明

```python
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
```

---

## 4. データベース設計

### 4.1 テーブル定義

#### diagnoses テーブル（診断結果）

```sql
CREATE TABLE diagnoses (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    user_name VARCHAR(100),
    user_email VARCHAR(255),
    
    -- 各軸のスコア
    e_score INTEGER DEFAULT 0,
    i_score INTEGER DEFAULT 0,
    s_score INTEGER DEFAULT 0,
    n_score INTEGER DEFAULT 0,
    t_score INTEGER DEFAULT 0,
    f_score INTEGER DEFAULT 0,
    j_score INTEGER DEFAULT 0,
    p_score INTEGER DEFAULT 0,
    
    -- 判定結果
    mbti_type VARCHAR(4) NOT NULL,
    
    -- 回答データ（JSON形式）
    answers JSONB,
    
    -- タイムスタンプ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス
    INDEX idx_mbti_type (mbti_type),
    INDEX idx_created_at (created_at),
    INDEX idx_session_id (session_id)
);
```

#### answers JSONBの構造例

```json
{
    "1": {"selected": "A", "axis": "E", "score": 2},
    "2": {"selected": "B", "axis": "S", "score": 2},
    "3": {"selected": "A", "axis": "T", "score": 2},
    ...
}
```

---

## 5. ルーティング設計

### 5.1 メインルーティング（routes/main.py）

| メソッド | パス | 説明 | テンプレート |
|---------|------|------|-------------|
| GET | `/` | トップページ | `index.html` |
| POST | `/start` | 診断開始（セッション作成） | リダイレクト → `/question/1` |
| GET | `/question/<int:q_id>` | 質問ページ表示 | `question.html` |
| POST | `/question/<int:q_id>` | 回答送信・次の質問へ | リダイレクト → 次の質問 or `/result` |
| GET | `/result` | 結果ページ表示 | `result.html` |
| POST | `/result/save` | 結果を永続化（任意） | リダイレクト → `/` |

### 5.2 管理ルーティング（routes/admin.py）

| メソッド | パス | 説明 | テンプレート |
|---------|------|------|-------------|
| GET | `/admin` | 管理ダッシュボード | `admin/dashboard.html` |
| GET | `/admin/history` | 診断履歴一覧 | `admin/history.html` |
| GET | `/admin/history/<int:id>` | 診断詳細 | `admin/detail.html` |
| GET | `/admin/stats` | 統計情報（JSON） | JSON |
| DELETE | `/admin/history/<int:id>` | 診断削除 | JSON |

### 5.3 エンドポイント詳細

#### POST `/start`

**リクエスト:**
```json
{
    "user_name": "山田太郎",  // オプション
    "user_email": "yamada@example.com"  // オプション
}
```

**レスポンス:**
- セッションIDをCookieに保存
- `/question/1` へリダイレクト

#### POST `/question/<int:q_id>`

**リクエスト:**
```json
{
    "question_id": 1,
    "answer": "A"
}
```

**処理:**
1. セッションに回答を保存
2. スコアを累積
3. 次の質問またはresultへリダイレクト

#### GET `/result`

**処理:**
1. セッションからスコアを取得
2. MBTIタイプを判定
3. DBに保存（オプション）
4. 結果を表示

---

## 6. 採点・判定ロジック

### 6.1 採点アルゴリズム（services/scoring.py）

```python
def calculate_mbti_type(scores: dict) -> str:
    """
    4軸のスコアからMBTIタイプを判定
    
    Args:
        scores: {
            'E': 6, 'I': 0,
            'S': 4, 'N': 2,
            'T': 4, 'F': 2,
            'J': 4, 'P': 2
        }
    
    Returns:
        str: 'INTJ', 'ENFP' など
    """
    result = ""
    
    # 1軸目: E vs I
    result += "E" if scores.get('E', 0) >= scores.get('I', 0) else "I"
    
    # 2軸目: S vs N
    result += "S" if scores.get('S', 0) >= scores.get('N', 0) else "N"
    
    # 3軸目: T vs F
    result += "T" if scores.get('T', 0) >= scores.get('F', 0) else "F"
    
    # 4軸目: J vs P
    result += "J" if scores.get('J', 0) >= scores.get('P', 0) else "P"
    
    return result


def calculate_percentage(axis_score: int, total_questions_per_axis: int) -> float:
    """
    各軸の傾向を百分率で計算
    
    Args:
        axis_score: その軸のスコア（例: E=6）
        total_questions_per_axis: その軸の質問数（通常3問）
    
    Returns:
        float: 傾向の強さ（0〜100%）
    """
    max_score = total_questions_per_axis * 2  # 各質問で最大2点
    return (axis_score / max_score) * 100 if max_score > 0 else 50.0
```

### 6.2 判定フロー

```
1. ユーザーが12問に回答
   ↓
2. 各回答のaxisとscoreをセッションに蓄積
   {
       'E': 6, 'I': 0,  // E/I軸: 3問 × 2点
       'S': 2, 'N': 4,  // S/N軸: 3問 × 2点
       'T': 4, 'F': 2,  // T/F軸: 3問 × 2点
       'J': 0, 'P': 6   // J/P軸: 3問 × 2点
   }
   ↓
3. 各軸でスコアの高い方を採用
   E (6) vs I (0) → E
   S (2) vs N (4) → N
   T (4) vs F (2) → T
   J (0) vs P (6) → P
   ↓
4. 結果: ENTP
   ↓
5. MBTI_TYPESから該当する説明を取得
   ↓
6. 結果をDBに保存（オプション）
```

---

## 7. Docker構成

### 7.1 docker-compose.yml

```yaml
version: '3.9'

services:
  # Flaskアプリケーション
  web:
    build: ./app
    container_name: mbti-web
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://mbti_user:mbti_pass@db:5432/mbti_db
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./app:/app
    depends_on:
      - db
    networks:
      - mbti-network
    restart: unless-stopped

  # PostgreSQLデータベース
  db:
    image: postgres:15-alpine
    container_name: mbti-db
    environment:
      - POSTGRES_USER=mbti_user
      - POSTGRES_PASSWORD=mbti_pass
      - POSTGRES_DB=mbti_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - mbti-network
    restart: unless-stopped

  # pgAdmin（オプション: DB管理UI）
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: mbti-pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@example.com
      - PGADMIN_DEFAULT_PASSWORD=admin
    ports:
      - "5050:80"
    depends_on:
      - db
    networks:
      - mbti-network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  mbti-network:
    driver: bridge
```

### 7.2 app/Dockerfile

```dockerfile
FROM python:3.11-slim

# 作業ディレクトリ設定
WORKDIR /app

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# ポート公開
EXPOSE 5000

# アプリケーション起動
CMD ["flask", "run", "--host=0.0.0.0"]
```

### 7.3 app/requirements.txt

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
psycopg2-binary==2.9.9
python-dotenv==1.0.0
gunicorn==21.2.0
```

### 7.4 .env.example

```bash
# Flask設定
SECRET_KEY=your-secret-key-change-in-production
FLASK_ENV=development

# データベース設定
DATABASE_URL=postgresql://mbti_user:mbti_pass@db:5432/mbti_db

# 管理者設定（オプション）
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

---

## 8. UI設計（Bootstrap 5）

### 8.1 共通デザインコンセプト

- **カラースキーム**: プライマリカラー（#4A90E2）、セカンダリカラー（#50C878）
- **レイアウト**: レスポンシブデザイン（モバイルファースト）
- **フォント**: システムフォント + 日本語フォント（Noto Sans JP）
- **コンポーネント**: Bootstrap 5の標準コンポーネントを使用

### 8.2 ページ構成

#### 8.2.1 トップページ（index.html）

```html
<!-- 主要要素 -->
- ヒーローセクション: アプリの説明とCTA
- 診断概要: 12問、所要時間3分
- 開始ボタン（目立つデザイン）
- MBTI簡易説明
```

#### 8.2.2 質問ページ（question.html）

```html
<!-- 主要要素 -->
- プログレスバー: 進捗表示（1/12 → 12/12）
- 質問テキスト（大きく見やすく）
- 選択肢（2択、カード形式）
- 次へボタン
- 戻るボタン（セッション保持）
```

#### 8.2.3 結果ページ（result.html）

```html
<!-- 主要要素 -->
- MBTIタイプ表示（大きなタイトル）
- タイプ名（例: "建築家"）
- 詳細説明
- 各軸のスコア表示（プログレスバー）
  - E/I: E 100% ━━━●━━━ I 0%
  - S/N: S 33% ━●━━━━━ N 67%
  - T/F: T 67% ━━━━●━━ F 33%
  - J/P: J 0% ━━━━━━● P 100%
- 強み・適職
- SNSシェアボタン
- 再診断ボタン
- 結果保存ボタン（オプション）
```

#### 8.2.4 管理ダッシュボード（admin/dashboard.html）

```html
<!-- 主要要素 -->
- 統計サマリー
  - 総診断回数
  - 直近7日間の診断数
  - 最多タイプ
- タイプ別分布グラフ（Chart.js）
- 最新診断一覧（5件）
- 履歴一覧へのリンク
```

#### 8.2.5 診断履歴一覧（admin/history.html）

```html
<!-- 主要要素 -->
- 検索・フィルター機能
  - タイプ別
  - 日付範囲
- ページネーション
- データテーブル
  - ID, 診断日時, タイプ, ユーザー名（あれば）
  - 詳細/削除ボタン
- CSV エクスポート
```

---

## 9. セッション管理

### 9.1 セッション構造

```python
session = {
    'session_id': 'uuid-string',
    'user_name': '山田太郎',  # オプション
    'user_email': 'yamada@example.com',  # オプション
    'started_at': '2025-10-24T10:30:00',
    'current_question': 5,
    'answers': {
        1: {'selected': 'A', 'axis': 'E', 'score': 2},
        2: {'selected': 'B', 'axis': 'S', 'score': 2},
        3: {'selected': 'A', 'axis': 'T', 'score': 2},
        4: {'selected': 'A', 'axis': 'J', 'score': 2}
    },
    'scores': {
        'E': 2, 'I': 0,
        'S': 2, 'N': 0,
        'T': 2, 'F': 0,
        'J': 2, 'P': 0
    }
}
```

### 9.2 セッションライフサイクル

1. **開始**: POST `/start` でセッション作成
2. **進行**: 各質問で回答を蓄積
3. **完了**: 全質問回答後に結果計算
4. **保存**: ユーザー選択でDB永続化
5. **削除**: 結果表示後30分で自動削除（設定可能）

---

## 10. 管理機能詳細

### 10.1 統計情報API（/admin/stats）

```json
{
    "total_diagnoses": 1234,
    "recent_7days": 56,
    "type_distribution": {
        "INTJ": 123,
        "ENTP": 98,
        ...
    },
    "average_completion_time": "3m 24s",
    "completion_rate": 87.5
}
```

### 10.2 履歴データ構造

```python
{
    "id": 1,
    "session_id": "abc-123",
    "user_name": "山田太郎",
    "user_email": "yamada@example.com",
    "mbti_type": "INTJ",
    "scores": {
        "E": 0, "I": 6,
        "S": 2, "N": 4,
        "T": 6, "F": 0,
        "J": 4, "P": 2
    },
    "answers": {...},
    "created_at": "2025-10-24T10:33:24",
    "completion_time": "3m 12s"
}
```

### 10.3 管理画面認証（オプション）

- **方式**: Basic認証またはFlask-Login
- **環境変数**: `ADMIN_USERNAME`, `ADMIN_PASSWORD`
- **保護対象**: `/admin/*` 全エンドポイント

---

## 11. 実装手順

### 11.1 フェーズ1: 環境構築

1. Dockerファイル作成
2. docker-compose.yml作成
3. requirements.txt作成
4. 環境変数設定
5. コンテナ起動確認

### 11.2 フェーズ2: データベース・モデル

1. models/diagnosis.py作成
2. マイグレーション設定
3. 初期テーブル作成
4. 接続確認

### 11.3 フェーズ3: コアロジック

1. services/questions.py（質問データ定義）
2. services/scoring.py（採点ロジック）
3. ユニットテスト作成

### 11.4 フェーズ4: ルーティング・ビュー

1. routes/main.py（診断フロー）
2. セッション管理実装
3. テンプレート作成（base, index, question, result）

### 11.5 フェーズ5: UI実装

1. Bootstrap統合
2. カスタムCSS作成
3. レスポンシブ対応
4. JavaScriptインタラクション

### 11.6 フェーズ6: 管理機能

1. routes/admin.py作成
2. 管理画面テンプレート
3. 統計APIエンドポイント
4. 認証実装

### 11.7 フェーズ7: テスト・デプロイ

1. 統合テスト
2. パフォーマンステスト
3. セキュリティチェック
4. 本番環境設定（Gunicorn、Nginx）

---

## 12. セキュリティ考慮事項

### 12.1 実装すべき対策

- **CSRF対策**: Flask-WTFでトークン生成
- **SQLインジェクション**: SQLAlchemy ORM使用
- **XSS対策**: Jinjaの自動エスケープ
- **セッション管理**: HTTPOnly Cookie、Secure Flag
- **環境変数**: 機密情報を.envに保管（gitignore）
- **管理画面**: 認証必須、IPホワイトリスト（オプション）

### 12.2 本番環境での追加対策

- HTTPS化（Let's Encrypt）
- レート制限（Flask-Limiter）
- ログ監視
- バックアップ自動化

---

## 13. パフォーマンス最適化

### 13.1 データベース

- インデックス設定（mbti_type, created_at）
- コネクションプーリング
- クエリ最適化

### 13.2 アプリケーション

- セッションはRedisに移行（オプション）
- 静的ファイルCDN配信（本番）
- Gunicorn + Nginx構成

### 13.3 フロントエンド

- 画像最適化
- CSS/JSミニファイ
- 遅延ロード

---

## 14. 今後の拡張案

### 14.1 機能拡張

- [ ] ユーザーアカウント機能
- [ ] 診断履歴の再閲覧
- [ ] 友人との相性診断
- [ ] 詳細レポート（PDF出力）
- [ ] 多言語対応

### 14.2 技術的拡張

- [ ] REST API化（JSON応答）
- [ ] React/Vueでのフロントエンド再構築
- [ ] CI/CDパイプライン（GitHub Actions）
- [ ] Kubernetes対応

---

## 15. 参考資料

- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [16Personalities（MBTIインスピレーション）](https://www.16personalities.com/)

---

## 16. まとめ

本設計書では、Flask + PostgreSQL + Docker Composeを使用したMBTI風性格診断Webアプリケーションの全体構成を提案しました。

**主要ポイント:**
- 12問の質問で4軸を評価
- セッションベースの診断フロー
- 管理画面で診断履歴と統計を確認
- Dockerによるコンテナ化で環境構築を簡素化
- Bootstrap 5でモダンなUI

この設計に基づいて実装を進めることで、拡張性とメンテナンス性の高いアプリケーションを構築できます。

---

**作成日**: 2025-10-24  
**バージョン**: 1.0  
**作成者**: AI Assistant

