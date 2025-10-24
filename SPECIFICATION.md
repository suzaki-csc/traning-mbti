# MBTI風性格診断Webアプリ 仕様書

## 1. 概要
FlaskとBootstrapを使用したMBTI風の性格診断Webアプリケーション。
10〜12問の質問に答えることで、4軸（E/I, S/N, T/F, J/P）のスコアを合算し、16タイプのうち1つを判定します。

## 2. 技術スタック
- **バックエンド**: Flask (Python 3.12)
- **フロントエンド**: Bootstrap 5
- **データベース**: MySQL
- **ORM**: Flask-SQLAlchemy
- **コンテナ**: Docker + Docker Compose
- **依存管理**: Poetry

## 3. ファイル構成

```
traning-mbti/
├── app/
│   ├── __init__.py          # Flaskアプリケーション初期化
│   ├── models.py            # データベースモデル
│   ├── routes.py            # ルーティング定義
│   ├── questions.py         # 質問データと軸マッピング
│   ├── mbti_logic.py        # MBTI判定ロジック
│   ├── templates/
│   │   ├── base.html        # ベーステンプレート
│   │   ├── index.html       # トップページ
│   │   ├── quiz.html        # 質問ページ
│   │   ├── result.html      # 結果表示ページ
│   │   └── admin/
│   │       ├── dashboard.html  # 管理画面トップ
│   │       └── history.html    # 診断履歴一覧
│   └── static/
│       ├── css/
│       │   └── style.css    # カスタムCSS
│       └── js/
│           └── quiz.js      # クイズ用JavaScript
├── migrations/              # データベースマイグレーション
├── docker/
│   └── mysql/
│       └── init.sql         # DB初期化スクリプト
├── Dockerfile               # アプリコンテナ定義
├── docker-compose.yml       # コンテナオーケストレーション
├── .env                     # 環境変数
├── config.py                # アプリケーション設定
├── run.py                   # アプリケーションエントリポイント
├── pyproject.toml           # Poetry依存関係
└── README.md
```

## 4. ルーティング設計

### 4.1 ユーザー向けルート

| URL | メソッド | 説明 |
|-----|---------|------|
| `/` | GET | トップページ（診断開始） |
| `/quiz` | GET | 質問ページ（セッション管理） |
| `/quiz` | POST | 回答を受け取り次の質問へ |
| `/result` | GET | 診断結果表示 |
| `/result` | POST | 診断結果の保存 |

### 4.2 管理者向けルート

| URL | メソッド | 説明 |
|-----|---------|------|
| `/admin` | GET | 管理画面トップ |
| `/admin/history` | GET | 診断履歴一覧（ページネーション） |
| `/admin/history/<id>` | GET | 特定の診断結果詳細 |
| `/admin/statistics` | GET | 統計情報表示 |

## 5. データ構造

### 5.1 質問データ（questions.py）

```python
QUESTIONS = [
    {
        "id": 1,
        "text": "パーティーや集まりで、あなたは...",
        "options": [
            {"text": "積極的に新しい人と交流する", "axis": "E", "score": 2},
            {"text": "知っている人と話す", "axis": "E", "score": 1},
            {"text": "静かに観察していることが多い", "axis": "I", "score": 1},
            {"text": "一人で過ごす方が好き", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 2,
        "text": "問題に直面したとき、あなたは...",
        "options": [
            {"text": "具体的な事実とデータを重視する", "axis": "S", "score": 2},
            {"text": "過去の経験を参考にする", "axis": "S", "score": 1},
            {"text": "直感的に解決策を探る", "axis": "N", "score": 1},
            {"text": "可能性や全体像を考える", "axis": "N", "score": 2}
        ]
    },
    {
        "id": 3,
        "text": "決断を下すとき、あなたは...",
        "options": [
            {"text": "論理的な分析を優先する", "axis": "T", "score": 2},
            {"text": "客観的に判断する", "axis": "T", "score": 1},
            {"text": "人への影響を考える", "axis": "F", "score": 1},
            {"text": "感情や価値観を重視する", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 4,
        "text": "計画について、あなたは...",
        "options": [
            {"text": "詳細な計画を立てて実行する", "axis": "J", "score": 2},
            {"text": "大まかな予定を決める", "axis": "J", "score": 1},
            {"text": "柔軟に対応したい", "axis": "P", "score": 1},
            {"text": "流れに任せる方が好き", "axis": "P", "score": 2}
        ]
    },
    {
        "id": 5,
        "text": "週末の過ごし方として好きなのは...",
        "options": [
            {"text": "友人と外出して活動的に過ごす", "axis": "E", "score": 2},
            {"text": "少人数で楽しく過ごす", "axis": "E", "score": 1},
            {"text": "一人で趣味に没頭する", "axis": "I", "score": 1},
            {"text": "静かに自宅でリラックスする", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 6,
        "text": "新しいことを学ぶとき、あなたは...",
        "options": [
            {"text": "段階的に実践しながら学ぶ", "axis": "S", "score": 2},
            {"text": "具体例から理解する", "axis": "S", "score": 1},
            {"text": "理論や概念から理解する", "axis": "N", "score": 1},
            {"text": "全体像を把握してから深掘りする", "axis": "N", "score": 2}
        ]
    },
    {
        "id": 7,
        "text": "意見の対立があったとき、あなたは...",
        "options": [
            {"text": "論理的に正しい方を選ぶ", "axis": "T", "score": 2},
            {"text": "効率性を優先する", "axis": "T", "score": 1},
            {"text": "調和を大切にする", "axis": "F", "score": 1},
            {"text": "みんなの気持ちを優先する", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 8,
        "text": "仕事の進め方について、あなたは...",
        "options": [
            {"text": "締切前に余裕を持って完成させる", "axis": "J", "score": 2},
            {"text": "計画的に進める", "axis": "J", "score": 1},
            {"text": "柔軟に調整しながら進める", "axis": "P", "score": 1},
            {"text": "締切ギリギリまで粘る", "axis": "P", "score": 2}
        ]
    },
    {
        "id": 9,
        "text": "エネルギーを充電するには...",
        "options": [
            {"text": "人と話すことでエネルギーを得る", "axis": "E", "score": 2},
            {"text": "グループ活動が好き", "axis": "E", "score": 1},
            {"text": "一人の時間が必要", "axis": "I", "score": 1},
            {"text": "孤独な時間で回復する", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 10,
        "text": "情報を受け取るとき、あなたは...",
        "options": [
            {"text": "詳細や具体的な情報を好む", "axis": "S", "score": 2},
            {"text": "現実的な情報を重視する", "axis": "S", "score": 1},
            {"text": "抽象的なアイデアが好き", "axis": "N", "score": 1},
            {"text": "可能性や意味を探る", "axis": "N", "score": 2}
        ]
    },
    {
        "id": 11,
        "text": "批判を受けたとき、あなたは...",
        "options": [
            {"text": "客観的に分析する", "axis": "T", "score": 2},
            {"text": "改善点を探す", "axis": "T", "score": 1},
            {"text": "個人的に受け止める", "axis": "F", "score": 1},
            {"text": "感情的に反応する", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 12,
        "text": "日常生活において、あなたは...",
        "options": [
            {"text": "ルーティンを守る", "axis": "J", "score": 2},
            {"text": "整理整頓を好む", "axis": "J", "score": 1},
            {"text": "自由に行動する", "axis": "P", "score": 1},
            {"text": "予定を変更することを楽しむ", "axis": "P", "score": 2}
        ]
    }
]

# 軸の説明
AXES_DESCRIPTION = {
    "E": "外向型 (Extraversion) - エネルギーを外部から得る",
    "I": "内向型 (Introversion) - エネルギーを内面から得る",
    "S": "感覚型 (Sensing) - 具体的な事実を重視",
    "N": "直感型 (Intuition) - 可能性やパターンを重視",
    "T": "思考型 (Thinking) - 論理と客観性を重視",
    "F": "感情型 (Feeling) - 価値観と調和を重視",
    "J": "判断型 (Judging) - 計画的で組織的",
    "P": "知覚型 (Perceiving) - 柔軟で適応的"
}
```

### 5.2 データベースモデル（models.py）

#### DiagnosisResult（診断結果）
| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | Integer | 主キー |
| mbti_type | String(4) | 診断結果タイプ（例: INTJ） |
| e_score | Integer | E軸スコア |
| i_score | Integer | I軸スコア |
| s_score | Integer | S軸スコア |
| n_score | Integer | N軸スコア |
| t_score | Integer | T軸スコア |
| f_score | Integer | F軸スコア |
| j_score | Integer | J軸スコア |
| p_score | Integer | P軸スコア |
| created_at | DateTime | 診断日時 |
| session_id | String(100) | セッションID |

#### Answer（回答）
| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | Integer | 主キー |
| diagnosis_id | Integer | 診断結果ID（外部キー） |
| question_id | Integer | 質問番号 |
| selected_option | Integer | 選択した選択肢番号 |
| axis | String(1) | 軸（E/I/S/N/T/F/J/P） |
| score | Integer | スコア（1 or 2） |

## 6. 採点ロジック（mbti_logic.py）

### 6.1 スコア計算アルゴリズム

```python
def calculate_mbti_type(answers):
    """
    回答からMBTIタイプを判定する
    
    Args:
        answers: list of dict [{axis: str, score: int}, ...]
    
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
            'description': str,
            'characteristics': list of str
        }
    """
    # 16タイプの説明データベース
    descriptions = {
        'INTJ': {
            'name': '建築家',
            'description': '戦略的な思考と高い独立性を持つタイプ。長期的なビジョンを持ち、効率的に目標を達成します。論理的で分析的、常に知識を深めることを好みます。',
            'characteristics': [
                '戦略的思考',
                '独立性が高い',
                '論理的分析',
                '長期計画重視'
            ]
        },
        'INTP': {
            'name': '論理学者',
            'description': '知的好奇心が旺盛で、理論や抽象的な概念を探求するタイプ。柔軟な思考で問題を分析し、独創的な解決策を見出します。',
            'characteristics': [
                '論理的思考',
                '知的好奇心',
                '分析力',
                '独創性'
            ]
        },
        # ... 他の14タイプも同様に定義
    }
    return descriptions.get(mbti_type, {})
```

### 6.2 判定ルール
- 各質問の選択肢にはスコア（1 or 2）が設定されている
- 12問×4選択肢で、各軸のスコアは0〜24の範囲
- 各軸ペア（E/I, S/N, T/F, J/P）でスコアが高い方を採用
- 同点の場合は先頭の軸（E, S, T, J）を採用

## 7. セッション管理

- Flaskのセッション機能を使用
- セッションに保存するデータ:
  - `current_question`: 現在の質問番号（1〜12）
  - `answers`: 回答リスト `[{question_id, axis, score}, ...]`
  - `session_id`: ユニークなセッションID（UUID）

## 8. UI設計（Bootstrap 5）

### 8.1 共通要素（base.html）
- レスポンシブデザイン
- ナビゲーションバー（タイトルとロゴ）
- Bootstrapのコンテナ使用

### 8.2 トップページ（index.html）
- アプリの説明
- 「診断を始める」ボタン（中央配置）
- 所要時間の表示（約3分）

### 8.3 質問ページ（quiz.html）
- 進捗バー（現在の質問番号/総質問数）
- 質問文の表示（カード形式）
- 4つの選択肢（ラジオボタン or カード選択）
- 「次へ」ボタン
- JavaScriptで選択肢のハイライト

### 8.4 結果ページ（result.html）
- MBTIタイプの大きな表示（例: INTJ）
- タイプ名（例: 建築家）
- 説明文（100字程度）
- 各軸のスコア表示（プログレスバー）
- 「もう一度診断する」ボタン
- 「結果を保存」ボタン（オプション）

## 9. Docker構成

### 9.1 Dockerfile（Flaskアプリ）

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Poetry のインストール
RUN pip install poetry

# 依存関係のコピーとインストール
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# アプリケーションコードのコピー
COPY . .

# ポート公開
EXPOSE 5000

# アプリケーション起動
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

### 9.2 docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: mbti_app
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=mysql+pymysql://mbti_user:mbti_password@db:3306/mbti_db
    depends_on:
      - db
    volumes:
      - .:/app
    networks:
      - mbti_network

  db:
    image: mysql:8.0
    container_name: mbti_db
    environment:
      - MYSQL_DATABASE=mbti_db
      - MYSQL_USER=mbti_user
      - MYSQL_PASSWORD=mbti_password
      - MYSQL_ROOT_PASSWORD=root_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./docker/mysql/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - mbti_network

networks:
  mbti_network:
    driver: bridge

volumes:
  mysql_data:
```

## 10. 環境変数（.env）

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://mbti_user:mbti_password@localhost:3306/mbti_db
```

## 11. 管理機能

### 11.1 診断履歴一覧
- 診断日時、MBTIタイプ、セッションIDの一覧表示
- ページネーション（1ページ20件）
- フィルタリング機能（タイプ別、日付範囲）
- 詳細表示リンク

### 11.2 統計情報
- 総診断回数
- タイプ別の分布（円グラフ）
- 日別の診断回数（折れ線グラフ）
- 各軸の平均スコア

## 12. 実装の優先順位

### Phase 1: 最小動作アプリ
1. 基本的なルーティング（/, /quiz, /result）
2. 質問データとスコア計算ロジック
3. シンプルなHTMLテンプレート
4. セッション管理

### Phase 2: データベース連携
1. モデル定義
2. 診断結果の保存機能
3. マイグレーション設定

### Phase 3: UI改善
1. Bootstrap適用
2. 進捗バー追加
3. レスポンシブデザイン

### Phase 4: Docker化
1. Dockerfile作成
2. docker-compose.yml作成
3. 環境変数の設定

### Phase 5: 管理機能
1. 管理画面ルート
2. 診断履歴表示
3. 統計情報表示

## 13. テスト項目

### 13.1 機能テスト
- [ ] トップページからクイズ開始
- [ ] 12問すべてに回答可能
- [ ] スコア計算が正確
- [ ] 結果が正しく表示
- [ ] データベースに保存される

### 13.2 UIテスト
- [ ] レスポンシブデザイン（モバイル、タブレット、PC）
- [ ] 進捗バーの表示
- [ ] ボタンの動作

### 13.3 セキュリティテスト
- [ ] セッションハイジャック対策
- [ ] SQLインジェクション対策
- [ ] XSS対策

## 14. 今後の拡張案

- ユーザー登録・ログイン機能
- 診断履歴の個人保存
- SNSシェア機能
- 詳細な性格分析レポート
- 相性診断機能
- 多言語対応

