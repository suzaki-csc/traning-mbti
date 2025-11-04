# MBTI風性格診断Webアプリケーション - 要件定義・設計書

## 1. アプリケーション概要

### 1.1 目的
MBTI（Myers-Briggs Type Indicator）風の性格診断をWebで提供し、ユーザーの性格タイプを判定するアプリケーション。

### 1.2 概要
- 簡潔な質問（10〜12問）に回答することで、4つの軸に基づいた16種類の性格タイプを判定
- シンプルで使いやすいUIで誰でも簡単に診断可能

---

## 2. 要件定義

### 2.1 機能要件

#### 2.1.1 必須機能
1. **トップページ**: 診断開始画面
2. **質問ページ**: 10〜12問の質問を表示し、選択肢で回答
3. **結果ページ**: 判定された性格タイプと説明を表示

#### 2.1.2 診断仕様
- **質問数**: 10〜12問
- **回答形式**: 各質問に対して選択肢（例: 強くそう思う、そう思う、どちらでもない、そう思わない、全くそう思わない）
- **判定軸**: 4軸
  - **E/I軸**: 外向型（Extraversion）/ 内向型（Introversion）
  - **S/N軸**: 感覚型（Sensing）/ 直感型（Intuition）
  - **T/F軸**: 思考型（Thinking）/ 感情型（Feeling）
  - **J/P軸**: 判断型（Judging）/ 知覚型（Perceiving）
- **性格タイプ**: 16種類（ISTJ, ISFJ, INFJ, INTJ, ISTP, ISFP, INFP, INTP, ESTP, ESFP, ENFP, ENTP, ESTJ, ESFJ, ENFJ, ENTJ）

### 2.2 非機能要件

#### 2.2.1 技術要件
- **バックエンド**: Flask（Python）
- **フロントエンド**: Bootstrap 5を利用したレスポンシブデザイン
- **データ管理**: セッションベース（将来的にはDB連携可能な設計）

#### 2.2.2 UI/UX要件
- シンプルで直感的な操作
- モバイル対応（レスポンシブデザイン）
- 1問ずつ表示する形式
- 進捗が分かるUI

---

## 3. アーキテクチャ設計

### 3.1 システム構成

```
┌─────────────┐
│   ブラウザ   │
└──────┬──────┘
       │ HTTP
       ↓
┌─────────────┐
│    Flask    │
│  (Python)   │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Session   │
│   Storage   │
└─────────────┘
```

### 3.2 処理フロー

```
[トップページ] → [質問ページ（問1〜12）] → [結果ページ]
     ↓                  ↓                      ↓
  診断開始          回答を保存            タイプ判定・表示
```

---

## 4. ファイル構成

```
traning-mbti/
├── app.py                    # Flaskアプリケーションのメインファイル
├── questions.py              # 質問データと軸マッピング
├── mbti_logic.py             # 採点ロジック・判定処理
├── mbti_descriptions.py      # 各性格タイプの説明文
├── templates/
│   ├── base.html            # ベーステンプレート
│   ├── index.html           # トップページ
│   ├── question.html        # 質問ページ
│   └── result.html          # 結果ページ
├── static/
│   ├── css/
│   │   └── style.css        # カスタムスタイル
│   └── js/
│       └── script.js        # フロントエンドスクリプト（必要に応じて）
├── pyproject.toml           # Poetry設定ファイル
└── README_APP.md            # 本ドキュメント
```

---

## 5. ルーティング設計

| エンドポイント | メソッド | 説明 | 処理内容 |
|--------------|---------|------|---------|
| `/` | GET | トップページ | 診断開始画面を表示 |
| `/start` | POST | 診断開始 | セッション初期化して質問ページへリダイレクト |
| `/question/<int:q_num>` | GET | 質問ページ | 指定された問題番号の質問を表示 |
| `/answer/<int:q_num>` | POST | 回答受付 | 回答をセッションに保存し、次の質問へ |
| `/result` | GET | 結果ページ | 回答を採点してMBTIタイプを判定・表示 |
| `/restart` | GET | 再診断 | セッションをクリアしてトップページへ |

---

## 6. データ構造設計

### 6.1 質問データ構造

```python
# questions.py
QUESTIONS = [
    {
        "id": 1,
        "text": "パーティーや集まりでは、積極的に多くの人と話すほうだ",
        "axis": "EI",  # E/I軸
        "direction": "E"  # Eに寄せる質問（肯定的回答でEスコア増加）
    },
    {
        "id": 2,
        "text": "一人で静かに過ごす時間が大切だ",
        "axis": "EI",
        "direction": "I"  # Iに寄せる質問
    },
    {
        "id": 3,
        "text": "具体的な事実やデータを重視する",
        "axis": "SN",
        "direction": "S"
    },
    {
        "id": 4,
        "text": "将来の可能性や全体像を考えることが好きだ",
        "axis": "SN",
        "direction": "N"
    },
    {
        "id": 5,
        "text": "論理的で客観的な判断を重視する",
        "axis": "TF",
        "direction": "T"
    },
    {
        "id": 6,
        "text": "人の感情や気持ちを考慮して決断する",
        "axis": "TF",
        "direction": "F"
    },
    {
        "id": 7,
        "text": "計画を立てて、順序立てて物事を進めたい",
        "axis": "JP",
        "direction": "J"
    },
    {
        "id": 8,
        "text": "柔軟に対応し、臨機応変に行動したい",
        "axis": "JP",
        "direction": "P"
    },
    {
        "id": 9,
        "text": "グループで活動することでエネルギーが湧く",
        "axis": "EI",
        "direction": "E"
    },
    {
        "id": 10,
        "text": "抽象的な概念や理論を考えることが楽しい",
        "axis": "SN",
        "direction": "N"
    },
    {
        "id": 11,
        "text": "決定する前に、じっくり考える時間が必要だ",
        "axis": "EI",
        "direction": "I"
    },
    {
        "id": 12,
        "text": "スケジュールよりも、その場の流れを大事にする",
        "axis": "JP",
        "direction": "P"
    }
]
```

### 6.2 回答選択肢とスコア

```python
# 5段階評価
ANSWER_OPTIONS = [
    {"value": 5, "label": "強くそう思う"},
    {"value": 4, "label": "そう思う"},
    {"value": 3, "label": "どちらでもない"},
    {"value": 2, "label": "そう思わない"},
    {"value": 1, "label": "全くそう思わない"}
]
```

### 6.3 セッションデータ構造

```python
session = {
    "answers": {
        1: 5,  # 質問IDと回答値
        2: 3,
        # ...
    },
    "scores": {
        "EI": 0,  # E寄りなら正、I寄りなら負
        "SN": 0,  # S寄りなら正、N寄りなら負
        "TF": 0,  # T寄りなら正、F寄りなら負
        "JP": 0   # J寄りなら正、P寄りなら負
    }
}
```

---

## 7. 採点ロジック設計

### 7.1 スコアリング方式

各質問の回答（1〜5）を、質問の方向性（direction）に基づいてスコア化します。

```python
# 疑似コード
def calculate_score(answer_value, direction):
    """
    answer_value: 1〜5（1:全くそう思わない、5:強くそう思う）
    direction: 質問の方向性（例: "E", "I", "S", "N", "T", "F", "J", "P"）
    """
    # 中央値を3とし、-2〜+2のスコアに変換
    base_score = answer_value - 3  # -2, -1, 0, 1, 2
    
    return base_score
```

### 7.2 軸別スコア集計

```python
def aggregate_scores(answers, questions):
    """
    各軸のスコアを集計
    """
    scores = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}
    
    for q in questions:
        q_id = q["id"]
        if q_id in answers:
            answer_value = answers[q_id]
            base_score = answer_value - 3
            
            axis = q["axis"]
            direction = q["direction"]
            
            # 方向性に基づいてスコアを加算
            # 例: direction="E"の場合、正のスコアでE寄り
            #     direction="I"の場合、正のスコアでI寄りなので符号反転
            if direction in ["E", "S", "T", "J"]:
                scores[axis] += base_score
            else:  # direction in ["I", "N", "F", "P"]
                scores[axis] -= base_score
    
    return scores
```

### 7.3 タイプ判定

```python
def determine_type(scores):
    """
    各軸のスコアから性格タイプを判定
    """
    mbti_type = ""
    
    # E/I軸: 正ならE、負ならI
    mbti_type += "E" if scores["EI"] >= 0 else "I"
    
    # S/N軸: 正ならS、負ならN
    mbti_type += "S" if scores["SN"] >= 0 else "N"
    
    # T/F軸: 正ならT、負ならF
    mbti_type += "T" if scores["TF"] >= 0 else "F"
    
    # J/P軸: 正ならJ、負ならP
    mbti_type += "J" if scores["JP"] >= 0 else "P"
    
    return mbti_type  # 例: "INTJ", "ESFP"など
```

### 7.4 採点フロー

```
[回答データ取得]
       ↓
[各質問の回答をスコア化]
       ↓
[軸別にスコア集計]
       ↓
[各軸の正負でタイプ判定]
       ↓
[MBTIタイプ（4文字）を返す]
```

---

## 8. UI/UX設計

### 8.1 画面構成

#### 8.1.1 トップページ（index.html）
- アプリタイトル
- 簡単な説明（「12の質問であなたの性格タイプを診断します」）
- 「診断を始める」ボタン

#### 8.1.2 質問ページ（question.html）
- 進捗インジケーター（「質問 X / 12」）
- 質問文
- 5つの選択肢ボタン（強くそう思う〜全くそう思わない）
- 「前の質問に戻る」ボタン（2問目以降）

#### 8.1.3 結果ページ（result.html）
- 判定結果（例: 「あなたのタイプは INTJ です」）
- タイプの説明文
- 各軸のスコア表示（バー表示など）
- 「もう一度診断する」ボタン
- 「結果をシェアする」機能（将来的な拡張）

### 8.2 デザイン指針

- **カラースキーム**: 落ち着いた色合い（Bootstrap標準色を活用）
- **レスポンシブ対応**: スマートフォン、タブレット、PC全てで快適に操作可能
- **ボタンの視認性**: 大きめのボタンで押しやすく
- **フォント**: 読みやすいゴシック体（システムフォント）

---

## 9. 性格タイプ説明

各MBTIタイプには簡潔な説明を用意します。

```python
# mbti_descriptions.py
MBTI_DESCRIPTIONS = {
    "INTJ": {
        "name": "建築家",
        "description": "戦略的で論理的な思考を持ち、独立心が強く、目標達成に向けて計画的に行動します。"
    },
    "INTP": {
        "name": "論理学者",
        "description": "知的好奇心が旺盛で、理論的な分析を得意とし、新しいアイデアを追求します。"
    },
    "ENTJ": {
        "name": "指揮官",
        "description": "リーダーシップが強く、効率的で決断力があり、組織をまとめる力があります。"
    },
    # ... 残り13タイプ
}
```

---

## 10. 今後の拡張可能性

### 10.1 データベース連携（将来実装）
- ユーザー登録・ログイン機能
- 診断履歴の保存
- 統計情報の表示（各タイプの割合など）

### 10.2 管理機能（将来実装）
- 質問の追加・編集・削除
- ユーザー管理
- アクセス統計

### 10.3 追加機能（将来実装）
- 詳細な診断結果レポート
- 相性診断
- SNSシェア機能
- 多言語対応

---

## 11. 開発ステップ

1. **Phase 1: 基本機能実装** ← 今回のスコープ
   - Flaskアプリケーション構築
   - 質問・回答・結果の画面実装
   - 採点ロジック実装

2. **Phase 2: データベース連携**
   - MySQL連携
   - Docker化

3. **Phase 3: ログイン・管理機能**
   - ユーザー認証
   - 管理画面

4. **Phase 4: 機能拡張**
   - 履歴管理
   - 統計機能

---

## 12. まとめ

本設計書では、MBTI風性格診断Webアプリケーションの基本機能に焦点を当て、以下を定義しました:

- ✅ 明確な機能要件（トップ、質問、結果の3画面）
- ✅ 12問の質問と4軸のスコアリング方式
- ✅ シンプルなファイル構成とルーティング
- ✅ 論理的な採点アルゴリズム
- ✅ Bootstrap活用のシンプルUI

この設計に基づき、実装フェーズに進むことが可能です。

---

## 13. 起動方法

### 13.1 必要な環境

- Python 3.8以上
- Poetry（パッケージ管理）

### 13.2 依存パッケージのインストール

```bash
# Poetryを使用している場合
poetry install

# または、pipを使用する場合
pip install flask
```

### 13.3 アプリケーションの起動

#### 方法1: 管理スクリプトを使用（推奨）

```bash
# 起動スクリプトに実行権限を付与（初回のみ）
chmod +x run_app.sh

# アプリケーションを起動（自動検出）
./run_app.sh start

# Docker環境で起動
./run_app.sh --docker start

# ネイティブ環境で起動
./run_app.sh --native start

# アプリケーションの状態を確認
./run_app.sh status

# アプリケーションを停止
./run_app.sh stop

# アプリケーションを再起動
./run_app.sh restart
```

**利用可能なコマンド:**
- `start` - アプリケーションを起動
- `stop` - アプリケーションを停止
- `restart` - アプリケーションを再起動
- `status` - アプリケーションの実行状態を確認

**環境指定オプション:**
- `--docker` - Docker環境で実行
- `--native` - ネイティブPython環境で実行
- （指定なし） - 自動検出

#### 方法2: 直接起動（フォアグラウンド）

```bash
# Poetryを使用している場合
poetry run python app.py

# または、pipを使用した場合
python app.py
```

### 13.4 アクセス方法

アプリケーションが起動したら、ブラウザで以下のURLにアクセスします：

```
http://localhost:5000
```

### 13.5 ログの確認

管理スクリプトで起動した場合、ログは `app.log` ファイルに出力されます：

```bash
# ログをリアルタイムで確認
tail -f app.log

# ログの最後の50行を表示
tail -n 50 app.log
```

---

## 14. Docker環境での運用

### 14.1 Docker構成

アプリケーションはDockerコンテナで運用できるように構成されています。

#### サービス構成
- **app**: Flaskアプリケーション（Python 3.12）
- **db**: MySQL 8.0データベース
- **phpmyadmin**: データベース管理ツール（開発用・オプション）

### 14.2 Dockerでの起動方法

#### 初回セットアップ

```bash
# 1. 環境変数ファイルを作成
cp .env.example .env

# 2. .envファイルを編集（SECRET_KEYとパスワードを変更）
vim .env

# 3. Dockerイメージをビルド
docker-compose build

# 4. コンテナを起動
docker-compose up -d
```

#### アクセス

- **アプリケーション**: http://localhost:5000
- **phpMyAdmin**（開発モード）: http://localhost:8080

#### 基本コマンド

```bash
# 起動
docker-compose up -d

# 停止
docker-compose down

# ログ確認
docker-compose logs -f app

# コンテナの状態確認
docker-compose ps

# 開発モード（phpMyAdmin含む）で起動
docker-compose --profile dev up -d
```

### 14.3 データベース管理

#### バックアップ

```bash
docker-compose exec db mysqldump -u root -p mbti_db > backup.sql
```

#### リストア

```bash
docker-compose exec -T db mysql -u root -p mbti_db < backup.sql
```

#### データベース初期化

```bash
docker-compose down -v
docker-compose up -d
```

### 14.4 デフォルト認証情報

#### 管理者アカウント
- Email: admin@example.com
- Password: admin123

⚠️ **本番環境では必ずパスワードを変更してください！**

### 14.5 詳細情報

Docker環境の詳細な運用方法は `DOCKER_README.md` を参照してください。

---

## 15. 実装完了

### 15.1 作成ファイル一覧

✅ **Pythonファイル**
- `app.py` - Flaskメインアプリケーション
- `questions.py` - 質問データと軸マッピング
- `mbti_logic.py` - 採点ロジック・判定処理
- `mbti_descriptions.py` - 各性格タイプの説明文

✅ **テンプレートファイル**
- `templates/base.html` - ベーステンプレート
- `templates/index.html` - トップページ
- `templates/question.html` - 質問ページ
- `templates/result.html` - 結果ページ

✅ **静的ファイル**
- `static/css/style.css` - カスタムスタイル

✅ **補助ファイル**
- `run_app.sh` - アプリケーション管理スクリプト（start/stop/restart/status）

✅ **Docker関連ファイル**
- `Dockerfile` - アプリケーションコンテナの定義
- `docker-compose.yml` - サービス構成定義
- `.dockerignore` - Dockerビルド時の除外ファイル
- `.env.example` - 環境変数テンプレート
- `docker/mysql/init/01_create_tables.sql` - データベーススキーマ定義
- `docker/mysql/init/02_insert_admin_user.sql` - 初期データ投入
- `docker/mysql/conf.d/my.cnf` - MySQL設定ファイル
- `DOCKER_README.md` - Docker運用ガイド

### 15.2 機能確認

以下の機能が実装されています：

### 診断機能
1. ✅ トップページ（診断開始）
2. ✅ 12問の質問表示
3. ✅ 5段階評価での回答
4. ✅ 進捗バー表示
5. ✅ 前の質問に戻る機能
6. ✅ 4軸スコア計算
7. ✅ MBTIタイプ判定（16タイプ）
8. ✅ 結果ページ（タイプ名・説明・スコア表示）
9. ✅ 再診断機能
10. ✅ レスポンシブデザイン（モバイル対応）

### ログイン・認証機能
11. ✅ ログイン・ログアウト機能
12. ✅ 新規ユーザー登録
13. ✅ ユーザーロール管理（一般ユーザー/管理者）
14. ✅ デフォルト管理者アカウント（admin@example.com / admin123）

### ユーザー機能
15. ✅ 診断履歴の保存と表示
16. ✅ ログイン済みユーザーの診断結果自動保存

### 管理機能
17. ✅ 管理ダッシュボード（統計情報表示）
18. ✅ ユーザー管理（一覧表示）
19. ✅ ユーザー詳細表示（診断履歴付き）
20. ✅ ユーザー情報編集（名前、メール、ロール、状態）
21. ✅ ユーザーパスワードリセット
22. ✅ ユーザー削除（自己削除防止機能付き）
23. ✅ 診断履歴の閲覧

### インフラ
24. ✅ Docker / Docker Compose対応
25. ✅ MySQL データベース対応
26. ✅ SQLite データベース対応（開発環境）

