# パスワード強度チェッカー - 実装仕様書

## 概要

ユーザーが入力したパスワードの強度を即座に評価し、セキュリティ向上のための具体的なアドバイスを提供するWebアプリケーションです。依存ライブラリを使用せず、軽量な自作ロジックで実装します。

**主な機能:**
- リアルタイムパスワード強度評価（5段階）
- エントロピー計算と総当たり攻撃想定時間の表示
- 改善アドバイスの自動生成
- 安全なランダムパスワード生成
- **チェック結果のデータベース保存** 🆕
- **チェック履歴の表示** 🆕
- **ユーザー認証とロール管理** 🆕
- **管理者機能（ユーザー管理）** 🆕

---

## ユーザー認証機能

### 概要

このアプリケーションには、ユーザー認証とロール管理機能が実装されています。

### ユーザーロール

| ロール | 説明 | 権限 |
|--------|------|------|
| **一般ユーザー** | 標準ユーザー | 自分のチェック履歴の閲覧 |
| **管理者** | 管理者ユーザー | すべてのユーザーの管理、全履歴の閲覧 |

### 認証機能

#### 1. ユーザー登録
- `/register` - 新規ユーザー登録
- メールアドレスとパスワードで登録
- パスワードは8文字以上
- 登録時は自動的に「一般ユーザー」として登録

#### 2. ログイン
- `/login` - ログインページ
- メールアドレスとパスワードで認証
- 「ログイン状態を保持する」オプション

#### 3. ログアウト
- `/logout` - ログアウト

### デフォルト管理者

アプリケーション起動時に自動的に作成されます：

- **Email**: admin@example.com
- **Password**: admin123

⚠️ **重要**: 本番環境では必ずパスワードを変更してください！

### ユーザー管理機能（管理者のみ）

管理者は以下の操作が可能です：

#### 管理者ダッシュボード
- `/admin` - 管理者ダッシュボード
- 統計情報の表示（総ユーザー数、総チェック数）
- 最近登録されたユーザーの一覧

#### ユーザー管理
- `/admin/users` - ユーザー一覧
- `/admin/users/<id>` - ユーザー詳細
- `/admin/users/<id>/edit` - ユーザー情報編集
- `/admin/users/<id>/delete` - ユーザー削除

**管理できる項目:**
- メールアドレス
- ユーザー名
- ロール（一般ユーザー / 管理者）
- アカウント状態（有効 / 無効）
- パスワードのリセット

**制限事項:**
- 自分自身のロールは変更不可
- 自分自身のアカウントは削除不可
- 自分自身のアカウントは無効化不可

---

## データベース機能

### パスワード保存形式

パスワードは以下の2つの形式で安全に保存されます：

1. **SHA-256ハッシュ値**
   - 復号不可能な一方向ハッシュ
   - 64文字の16進数文字列
   - 同じパスワードの重複チェックに使用

2. **先頭1文字 + マスク表示**
   - 例: "Password123" → "P***********"
   - ユーザーが履歴で識別しやすくするため
   - 元のパスワードは復元不可能

### 保存される情報

| 項目 | 説明 |
|------|------|
| パスワードハッシュ | SHA-256ハッシュ値 |
| パスワードマスク | 先頭1文字+アスタリスク |
| スコア | 0-100点の評価値 |
| 強度レベル | very-weak, weak, fair, strong, very-strong |
| エントロピー | ビット単位の予測困難性 |
| 総当たり想定時間 | 攻撃にかかる想定時間 |
| 文字種情報 | 小文字/大文字/数字/記号の使用状況 |
| パターン検出結果 | よくある単語/繰り返し/連番/キーボード並び |
| チェック日時 | タイムスタンプ |

### APIエンドポイント

#### 1. チェック結果の保存
```
POST /api/save-check
```

**リクエスト例:**
```json
{
  "password": "MyP@ssw0rd",
  "score": 75,
  "strength_level": "strong",
  "entropy": 52.4,
  "crack_time": "約1,425年",
  "has_lowercase": true,
  "has_uppercase": true,
  "has_digit": true,
  "has_symbol": true,
  "has_common_word": false,
  "has_repeating": false,
  "has_sequential": false,
  "has_keyboard_pattern": false
}
```

#### 2. チェック履歴の取得
```
GET /api/history?limit=10&offset=0
```

#### 3. 統計情報の取得
```
GET /api/stats
```

---

## 起動方法

### 方法1: Docker Compose を使用（推奨）

プロジェクトはDocker Composeで構築されており、簡単に起動できます。

#### macOS / Linux の場合

```bash
# プロジェクトディレクトリに移動
cd /path/to/traning-mbti

# 起動スクリプトを実行
./start_password_checker.sh start
```

#### Windows の場合

```batch
# プロジェクトディレクトリに移動
cd C:\path\to\traning-mbti

# 起動スクリプトを実行
start_password_checker.bat start
```

またはエクスプローラーから `start_password_checker.bat` をダブルクリックして起動

**起動スクリプトが行うこと:**
1. Docker環境のチェック（Docker、Docker Compose）
2. 必要なファイルの存在確認
3. Dockerイメージのビルド
4. コンテナの起動とヘルスチェック

**利用可能なコマンド:**
```bash
./start_password_checker.sh start     # アプリケーションを起動
./start_password_checker.sh stop      # アプリケーションを停止
./start_password_checker.sh restart   # アプリケーションを再起動
./start_password_checker.sh logs      # ログを表示
./start_password_checker.sh status    # コンテナの状態を確認
./start_password_checker.sh build     # イメージを再ビルド
./start_password_checker.sh clean     # コンテナとイメージを削除
./start_password_checker.sh help      # ヘルプを表示
```

### 方法2: Docker Composeを直接使用

起動スクリプトを使わずに、Docker Composeコマンドを直接実行することもできます。

```bash
# イメージをビルド
docker compose build

# コンテナを起動（バックグラウンド）
docker compose up -d

# ログを表示
docker compose logs -f

# コンテナを停止
docker compose down
```

### 方法3: 手動で起動（Poetry環境）

Dockerを使用せず、Poetry環境で直接起動することもできます。

```bash
# プロジェクトディレクトリに移動
cd /path/to/traning-mbti

# Poetry環境をアクティブ化
poetry shell

# アプリケーションを起動
python password_checker_app.py
```

または、Poetry環境をアクティブ化せずに直接実行:

```bash
poetry run python password_checker_app.py
```

### アクセス方法

アプリケーションが起動したら、ブラウザで以下のURLにアクセス:

```
http://localhost:5000
```

### Docker環境の構成

プロジェクトは以下のDocker設定ファイルで構成されています：

#### ファイル一覧

| ファイル | 説明 |
|---------|------|
| `Dockerfile` | アプリケーションコンテナのイメージ定義 |
| `docker-compose.yml` | 開発環境用のコンテナ構成 |
| `docker-compose.prod.yml` | 本番環境用の追加設定 |
| `.dockerignore` | Dockerイメージに含めないファイルを指定 |

#### Dockerイメージの構成

- **ベースイメージ**: Python 3.12-slim
- **パッケージ管理**: Poetry
- **アプリケーションポート**: 5000
- **ヘルスチェック**: `/health` エンドポイント
- **セキュリティ**: 非rootユーザー（appuser）で実行

#### 本番環境での起動

本番環境用の設定を使用する場合:

```bash
# 本番環境用の設定をマージして起動
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

本番環境では以下が変更されます:
- `FLASK_ENV=production`
- ホットリロード用のボリュームマウントを削除
- リソース制限を設定（CPU: 0.5コア、メモリ: 512MB）

### トラブルシューティング

#### Docker関連

**Dockerデーモンが起動していない**
```bash
# macOS: Docker Desktopを起動
# Linux: Dockerサービスを起動
sudo systemctl start docker
```

**ポート5000が既に使用されている場合**
```bash
# 使用中のプロセスを確認
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# 起動スクリプトを使用すると自動で対処
./start_password_checker.sh start
```

**イメージのビルドに失敗する場合**
```bash
# キャッシュをクリアして再ビルド
./start_password_checker.sh build

# または手動で
docker compose build --no-cache
```

**コンテナが起動しない場合**
```bash
# ログを確認
./start_password_checker.sh logs

# コンテナの状態を確認
docker ps -a
docker logs password_checker_app
```

#### Poetry環境（Docker未使用時）

**Poetry環境が見つからない場合**
```bash
# Poetry環境を再作成
poetry install

# 環境の確認
poetry env info
```

---

## 機能要件

### 1. 基本機能

#### 1.1 リアルタイム強度評価
- パスワード入力フィールドに文字を入力するたびに、即座に強度を評価
- 5段階の強度レベルで視覚的に表示

**強度レベル:**
- **Very Weak (非常に弱い)** - スコア: 0-20点
- **Weak (弱い)** - スコア: 21-40点
- **Fair (普通)** - スコア: 41-60点
- **Strong (強い)** - スコア: 61-80点
- **Very Strong (非常に強い)** - スコア: 81-100点

#### 1.2 視覚的フィードバック
- プログレスバー形式の強度メーター
- レベルに応じた色分け:
  - Very Weak: 赤 (#dc3545)
  - Weak: オレンジ (#fd7e14)
  - Fair: 黄色 (#ffc107)
  - Strong: 水色 (#17a2b8)
  - Very Strong: 緑 (#28a745)

#### 1.3 詳細情報の表示
- **推定エントロピー**: パスワードの予測困難性をビット単位で表示
- **オフライン総当たり攻撃の想定時間**: 
  - 仮定: 毎秒10億回の試行速度
  - 時間単位で表示（秒、分、時間、日、年）

#### 1.4 改善アドバイス
パスワードの弱点を分析し、具体的な改善提案をリスト表示:
- 長さが不足している場合: "12文字以上に延ばしてください"
- 文字種が不足している場合: "大文字を含めてください"、"記号を含めてください"など
- よくある単語を含む場合: "一般的な単語（password等）を避けてください"
- 繰り返しパターンがある場合: "繰り返しパターン（aaa、123等）を避けてください"
- キーボード並び検出時: "キーボード配列（qwerty等）を避けてください"
- 文字種置換の警告: "単純な置換（@→a、0→o等）はセキュリティ向上になりません"

#### 1.5 ユーザー補助機能
- **パスワード表示/非表示トグル**: 目のアイコンでワンクリック切替
- **クリップボードコピー**: 入力したパスワードをクリップボードにコピー
- **安全なランダムパスワード生成**:
  - 長さ: 12～16文字（ランダム）
  - 文字種: 小文字、大文字、数字、記号をすべて含む
  - 複数の候補を一度に生成（3個程度）
  - 生成されたパスワードをクリックで入力フィールドに適用

---

## スコアリングロジック（合計100点満点）

### 2.1 長さによる評価（最大30点）
```
0-7文字   : 0点
8-11文字  : 10点
12-15文字 : 20点
16文字以上 : 30点
```

### 2.2 文字種の多様性（最大30点）
各文字種につき7.5点、最大4種類で30点:
- 小文字 (a-z): 7.5点
- 大文字 (A-Z): 7.5点
- 数字 (0-9): 7.5点
- 記号 (!@#$%^&*等): 7.5点

### 2.3 パターン検出による減点（最大-40点）

#### よくある単語（-15点）
簡易辞書に含まれる単語（大文字小文字を区別しない）:
```
password, qwerty, 123456, admin, letmein, welcome, 
iloveyou, monkey, dragon, master, sunshine, princess, 
abc123, 111111, password123, 000000
```

#### 連続した文字の繰り返し（-10点）
- 同じ文字が3回以上連続: "aaa", "111" など

#### 連番パターン（-10点）
- 数字の連続: "1234", "5678", "0123" など（3桁以上）
- アルファベットの連続: "abc", "xyz" など（3文字以上）

#### キーボード並びパターン（-5点）
- よくあるキーボード配列: "qwerty", "asdf", "zxcv" など

### 2.4 ボーナスポイント（最大20点）
- 長さが20文字以上: +10点
- すべての文字種を含み、かつ16文字以上: +10点

---

## エントロピー計算方式

### 3.1 文字セットのサイズ
使用されている文字種に基づいて文字プールサイズを計算:
- 小文字のみ: 26
- 小文字 + 大文字: 52
- 小文字 + 大文字 + 数字: 62
- 小文字 + 大文字 + 数字 + 記号: 95

### 3.2 エントロピー計算式
```
エントロピー (bits) = log2(文字プールサイズ ^ パスワード長)
                    = パスワード長 × log2(文字プールサイズ)
```

### 3.3 総当たり攻撃の想定時間
```
想定試行回数 = 2 ^ エントロピー
攻撃速度 = 10億回/秒 (1,000,000,000 試行/秒)
想定時間 (秒) = 想定試行回数 / (攻撃速度 × 2)
※ 平均して50%の試行で見つかると仮定
```

時間表記の変換:
- 60秒未満: 「○秒」
- 60分未満: 「○分」
- 24時間未満: 「○時間」
- 365日未満: 「○日」
- それ以上: 「○年」、「○千年」、「○百万年」など

---

## UI/UX設計

### 4.1 レイアウト構成
```
┌─────────────────────────────────────────┐
│    パスワード強度チェッカー              │
├─────────────────────────────────────────┤
│ パスワード入力:                          │
│ [_________________] [👁] [📋]            │
│                                         │
│ 強度: [■■■■■□□□□□] Strong (強い)      │
│                                         │
│ 詳細情報:                                │
│ ・スコア: 75/100                         │
│ ・エントロピー: 52.4 bits                │
│ ・総当たり想定時間: 約1,425年            │
│                                         │
│ 改善アドバイス:                          │
│ ✓ 大文字を含めてください                 │
│ ✓ 記号を含めると更に強固になります        │
│                                         │
│ [安全なパスワードを生成]                  │
│                                         │
│ 生成候補:                                │
│ ・Kx9$mP2vQr#5bN (クリックで使用)        │
│ ・Tz7@wL4nHf&8sJ (クリックで使用)        │
│ ・Bp3%rD6kYm*1cG (クリックで使用)        │
└─────────────────────────────────────────┘
```

### 4.2 アクセシビリティ配慮
- すべての入力要素に適切な`label`または`aria-label`を設定
- 色だけでなく、テキストでも強度レベルを表示
- キーボード操作のみで全機能を利用可能 (Tab、Enter、Space)
- コントラスト比はWCAG AA基準を満たす（4.5:1以上）
- スクリーンリーダー対応のaria属性を使用

### 4.3 レスポンシブデザイン
- モバイル、タブレット、デスクトップで最適表示
- Bootstrapグリッドシステムの活用

---

## 技術実装方針

### 5.1 技術スタック
- **バックエンド**: Flask (Python)
- **フロントエンド**: HTML5, CSS3 (Bootstrap 5), JavaScript (Vanilla)
- **データベース**: 不要（すべてクライアント側で処理）

### 5.2 ファイル構成
```
password_checker/
├── app.py                    # Flaskアプリケーションのエントリーポイント
├── templates/
│   └── index.html            # メインページ
├── static/
│   ├── css/
│   │   └── style.css         # カスタムスタイル
│   └── js/
│       └── password_checker.js  # パスワード評価ロジック
└── README.md                 # プロジェクト説明
```

### 5.3 主要な関数設計

#### JavaScript側 (password_checker.js)

**1. `calculatePasswordScore(password)`**
- パスワードを受け取り、スコア（0-100）を返す
- 長さ、文字種、パターン検出を総合評価
- 戻り値: `{ score: number, details: object }`

**2. `checkCharacterTypes(password)`**
- 使用されている文字種を判定
- 戻り値: `{ hasLower, hasUpper, hasDigit, hasSymbol, poolSize }`

**3. `detectCommonWords(password)`**
- 簡易辞書との照合
- 戻り値: `boolean`

**4. `detectRepeatingPatterns(password)`**
- 繰り返しパターンの検出（"aaa", "111"など）
- 戻り値: `boolean`

**5. `detectSequentialPatterns(password)`**
- 連番パターンの検出（"123", "abc"など）
- 戻り値: `boolean`

**6. `detectKeyboardPatterns(password)`**
- キーボード並びの検出（"qwerty", "asdf"など）
- 戻り値: `boolean`

**7. `calculateEntropy(password, poolSize)`**
- エントロピーをビット単位で計算
- 戻り値: `number` (bits)

**8. `estimateCrackTime(entropy)`**
- 総当たり攻撃の想定時間を計算
- 戻り値: `string` (人間が読める形式)

**9. `getStrengthLevel(score)`**
- スコアに基づいて強度レベルを返す
- 戻り値: `{ level: string, color: string, text: string }`

**10. `generateAdvice(password, details)`**
- 改善アドバイスの配列を生成
- 戻り値: `Array<string>`

**11. `generateRandomPassword(length)`**
- 安全なランダムパスワードを生成
- 使用: `crypto.getRandomValues()` (ブラウザの暗号学的に安全な乱数生成)
- 戻り値: `string`

**12. `updateUI(password)`**
- すべての評価結果をUIに反映
- メーター更新、アドバイス表示など

**13. `copyToClipboard(text)`**
- クリップボードにテキストをコピー
- ユーザーへのフィードバック表示

#### Python側 (app.py)

```python
# Flaskアプリケーションの基本設定
# すべての処理はクライアント側で行うため、
# サーバー側はHTMLテンプレートの配信のみ

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """メインページを表示"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### 5.4 セキュリティ考慮事項

**重要: このアプリケーションは教育目的です**

実際のパスワード管理では以下を推奨:
- パスワードをサーバーに送信しない（クライアント側のみで処理）
- HTTPS通信を使用
- パスワードマネージャーの使用を推奨
- 二段階認証の併用

---

## 実装の詳細説明

### 6.1 スコアリング計算の例

**例1: "password123"**
```
長さ評価: 11文字 → 10点
文字種: 小文字+数字 → 15点
よくある単語: "password"を含む → -15点
連番: "123"を含む → -10点
合計: 10 + 15 - 15 - 10 = 0点
→ Very Weak (非常に弱い)
```

**例2: "MyP@ssw0rd2024"**
```
長さ評価: 14文字 → 20点
文字種: 小文字+大文字+数字+記号 → 30点
よくある単語: "password"類似 → -15点
単純置換使用: @→a, 0→o → -5点（アドバイスで指摘）
合計: 20 + 30 - 15 = 35点
→ Weak (弱い)
```

**例3: "Kx9$mP2vQr#5bN"**
```
長さ評価: 14文字 → 20点
文字種: すべての種類 → 30点
パターン検出: なし → 0点
ランダム性高い → ボーナスなし
合計: 20 + 30 = 50点
→ Fair (普通)

※ 16文字以上でボーナス対象になる可能性
```

**例4: "Tr!cky$Passw0rd_2024_Secure!"**
```
長さ評価: 28文字 → 30点
文字種: すべての種類 → 30点
20文字以上ボーナス → +10点
すべての文字種+16文字以上 → +10点
合計: 30 + 30 + 10 + 10 = 80点
→ Strong (強い)
```

### 6.2 エントロピー計算の例

**例: "Kx9$mP2vQr#5bN" (14文字、全文字種)**
```
文字プールサイズ: 95 (26+26+10+33)
エントロピー = 14 × log2(95)
            = 14 × 6.57
            = 91.98 bits

想定試行回数 = 2^91.98 ≈ 5.0 × 10^27
攻撃速度 = 10億回/秒
想定時間 = (5.0 × 10^27) / (10^9 × 2)
         = 2.5 × 10^18 秒
         ≈ 7,900万年
```

### 6.3 簡易辞書の実装

```javascript
// よくあるパスワードの辞書（一部）
const COMMON_PASSWORDS = [
    'password', 'qwerty', '123456', 'admin', 'letmein',
    'welcome', 'iloveyou', 'monkey', 'dragon', 'master',
    'sunshine', 'princess', 'abc123', '111111', 'password123',
    '000000', '12345678', 'qwerty123', 'password1', '123123'
];

// キーボード並びパターン
const KEYBOARD_PATTERNS = [
    'qwerty', 'asdf', 'zxcv', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
    'qwertz', 'azerty', '!@#$%^&*()', '1234567890'
];
```

### 6.4 連番検出ロジック

```javascript
/**
 * 連番パターンを検出する関数
 * @param {string} password - チェックするパスワード
 * @returns {boolean} - 連番が見つかった場合true
 */
function detectSequentialPatterns(password) {
    // 数字の連番チェック (3桁以上)
    for (let i = 0; i < password.length - 2; i++) {
        const char1 = password.charCodeAt(i);
        const char2 = password.charCodeAt(i + 1);
        const char3 = password.charCodeAt(i + 2);
        
        // 昇順または降順の連番
        if ((char2 === char1 + 1 && char3 === char2 + 1) ||
            (char2 === char1 - 1 && char3 === char2 - 1)) {
            return true;
        }
    }
    return false;
}
```

---

## 初心者向けコメント例

すべてのコードには以下のような詳細なコメントを記載:

```javascript
/**
 * パスワードの強度スコアを計算する関数
 * 
 * この関数は以下の要素を評価してスコアを計算します:
 * 1. パスワードの長さ（長いほど高得点）
 * 2. 文字の種類（小文字、大文字、数字、記号）
 * 3. よくある単語が含まれていないか（含まれると減点）
 * 4. 簡単に推測できるパターンがないか（繰り返しや連番など）
 * 
 * @param {string} password - 評価するパスワード文字列
 * @returns {object} スコアと詳細情報を含むオブジェクト
 *   - score: 0-100の数値
 *   - details: 各評価項目の詳細
 */
function calculatePasswordScore(password) {
    // スコアの初期値は0から始める
    let score = 0;
    
    // 評価の詳細を記録するオブジェクト
    const details = {
        length: 0,        // 長さによる得点
        variety: 0,       // 文字種の多様性による得点
        penalties: []     // 減点項目のリスト
    };
    
    // 1. 長さによる評価
    // パスワードが長いほどセキュリティは高くなる
    const length = password.length;
    if (length >= 16) {
        details.length = 30;  // 16文字以上: 満点
    } else if (length >= 12) {
        details.length = 20;  // 12-15文字: 良好
    } else if (length >= 8) {
        details.length = 10;  // 8-11文字: 最低限
    } else {
        details.length = 0;   // 7文字以下: 不十分
    }
    score += details.length;
    
    // ... 続く
}
```

---

## テストケース

実装後、以下のパスワードで動作確認:

1. **"password"** → Very Weak（よくある単語）
2. **"12345678"** → Very Weak（連番）
3. **"qwerty123"** → Very Weak（キーボード並び+連番）
4. **"Password1"** → Weak（よくある単語の変形）
5. **"MySecret2024"** → Fair（まあまあ）
6. **"Tr!cky$P@ss"** → Strong（良好）
7. **"xK9$mP2vQr#5bN"** → Very Strong（優秀）
8. **"aaaaaa"** → Very Weak（繰り返し）
9. **"ThisIsAVeryLongPasswordButNotVerySecure"** → Fair（長いが記号がない）
10. **"Kx9$mP2vQr#5bN8wL4hF!gT"** → Very Strong（最高レベル）

---

## 実装時の注意点

### セキュリティ
- パスワードはクライアント側のみで処理し、サーバーに送信しない
- 入力されたパスワードをログに記録しない
- HTTPSを使用（本番環境）

### パフォーマンス
- 入力のたびに評価を実行するため、処理は軽量に保つ
- 必要に応じてデバウンス処理を実装（連続入力時の負荷軽減）

### ユーザビリティ
- エラーメッセージは具体的かつ建設的に
- パスワード生成機能で複数の選択肢を提供
- モバイルでの使いやすさを考慮

### 教育的価値
- 初心者が読んでコードを理解できるよう、丁寧なコメントを記載
- なぜその評価基準なのかを説明する
- セキュリティのベストプラクティスを学べるようにする

---

## 拡張アイデア（オプション）

将来的に追加できる機能:
1. **パスワードの履歴**: 過去に生成したパスワードの強度を記録
2. **カスタム辞書**: ユーザーが避けたい単語を追加
3. **多言語対応**: 英語UIも追加
4. **パスワードマネージャー連携**: 1Passwordなどへのエクスポート
5. **視覚的なパターン表示**: どの部分が弱いかをハイライト
6. **音声読み上げ**: アクセシビリティ向上
7. **ダークモード**: 目に優しいUI

---

## まとめ

このパスワード強度チェッカーは、以下の特徴を持つ教育的なWebアプリケーションです:

✅ **シンプル**: 外部ライブラリに依存せず、軽量で高速  
✅ **実用的**: 実際のセキュリティ基準に基づいた評価  
✅ **教育的**: 初心者がコードから学べる丁寧なコメント  
✅ **アクセシブル**: すべてのユーザーが使いやすい設計  
✅ **安全**: クライアント側のみで処理、サーバーに送信しない  

この仕様書をもとに実装することで、実践的なWebセキュリティの知識を学びながら、ユーザーにとって有用なツールを作成できます。

