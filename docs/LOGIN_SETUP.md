# ログイン機能・管理機能のセットアップと使い方

## 概要

MBTI風性格診断アプリケーションに、以下の機能が追加されました：

- **ログイン・ログアウト機能**
- **新規ユーザー登録**
- **ユーザーロール管理**（一般ユーザー / 管理者）
- **診断履歴の保存と表示**
- **管理画面**（ユーザー管理、統計情報）

## 主要ファイル

- `app.py` - メインアプリケーション（ログイン機能統合済み）
- `database.py` - データベースモデル定義（User, DiagnosisResult）
- `templates/auth/` - 認証画面テンプレート
- `templates/diagnosis/history.html` - 診断履歴
- `templates/admin/` - 管理画面テンプレート

## デフォルト管理者アカウント

アプリケーション初回起動時に、以下の管理者アカウントが自動作成されます：

- **メールアドレス**: admin@example.com
- **パスワード**: admin123
- **ロール**: 管理者

## 機能説明

### 1. ログイン機能

- URL: `/login`
- メールアドレスとパスワードで認証
- ログイン状態はセッションで管理
- ナビゲーションバーにユーザー名とログアウトボタンが表示

### 2. 新規登録機能

- URL: `/register`
- ユーザー名、メールアドレス、パスワードで新規アカウント作成
- 新規ユーザーは「一般ユーザー」ロールで登録

### 3. 診断履歴機能

- URL: `/history`
- ログイン済みユーザーのみアクセス可能
- 過去の診断結果を一覧表示
- 診断日時、MBTIタイプ、各軸のスコアを表示

### 4. 診断結果の自動保存

- ログイン済みユーザーが診断を完了すると、自動的にデータベースに保存
- 保存内容：
  - MBTIタイプ
  - 各軸のスコア（E/I, S/N, T/F, J/P）
  - 回答データ
  - 診断日時

### 5. 管理画面

#### ダッシュボード
- URL: `/admin`
- 管理者のみアクセス可能
- 総ユーザー数と総診断数を表示

#### ユーザー管理
- URL: `/admin/users`
- 管理者のみアクセス可能
- 全ユーザーの一覧表示
- 表示情報：
  - ID、ユーザー名、メールアドレス
  - ロール（一般 / 管理者）
  - 登録日、最終ログイン日
  - 診断実施回数

## 起動方法

### Docker環境（推奨）

```bash
# 起動
./run_app.sh start

# 停止
./run_app.sh stop

# 再起動
./run_app.sh restart

# 状態確認
./run_app.sh status
```

アクセス:
- アプリケーション: http://localhost:5000
- phpMyAdmin: http://localhost:8080

### ネイティブ環境

```bash
# 依存関係インストール
poetry install

# 起動
poetry run python app.py
```

アクセス: http://localhost:5000

## データベース構造

### users テーブル

| カラム | 型 | 説明 |
|--------|-----|------|
| id | Integer | 主キー |
| email | String(255) | メールアドレス（ユニーク） |
| password_hash | String(255) | ハッシュ化されたパスワード |
| username | String(100) | ユーザー名 |
| role | String(10) | ロール（'user' または 'admin'） |
| created_at | DateTime | 登録日時 |
| last_login | DateTime | 最終ログイン日時 |
| is_active | Boolean | アカウント有効状態 |

### diagnosis_results テーブル

| カラム | 型 | 説明 |
|--------|-----|------|
| id | Integer | 主キー |
| user_id | Integer | ユーザーID（外部キー） |
| mbti_type | String(4) | MBTIタイプ（例: INTJ） |
| score_ei | Integer | E/I軸スコア |
| score_sn | Integer | S/N軸スコア |
| score_tf | Integer | T/F軸スコア |
| score_jp | Integer | J/P軸スコア |
| answers | JSON | 回答データ |
| created_at | DateTime | 診断日時 |

## セキュリティ

- パスワードは`werkzeug.security`の`generate_password_hash`でハッシュ化
- ログイン状態は`flask-login`で管理
- 管理画面は`@admin_required`デコレータで保護
- 診断履歴は`@login_required`デコレータで保護

## トラブルシューティング

### 管理者でログインできない

初回起動時にデフォルト管理者が作成されているか確認：

```bash
# Docker環境
docker exec -it mbti-app python -c "from app import app, db, User; \
  with app.app_context(): \
    admin = User.query.filter_by(email='admin@example.com').first(); \
    print('Admin:', admin.email if admin else 'Not found')"

# ネイティブ環境
poetry run python -c "from app import app, db, User; \
  with app.app_context(): \
    admin = User.query.filter_by(email='admin@example.com').first(); \
    print('Admin:', admin.email if admin else 'Not found')"
```

### データベースをリセットしたい

```bash
# Docker環境
docker exec -it mbti-app rm -f /app/mbti.db
./run_app.sh restart

# ネイティブ環境
rm -f mbti.db
poetry run python app.py
```

## 今後の拡張案

- パスワードリセット機能
- メール認証
- ユーザープロフィール編集
- 管理画面でのユーザー編集・削除機能
- 診断結果の詳細ページ
- 診断結果のエクスポート機能
- 複数回診断時の傾向分析

---

**注意**: このアプリケーションは教育目的で開発されており、本番環境での使用は推奨されません。

