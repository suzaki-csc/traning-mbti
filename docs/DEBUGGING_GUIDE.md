# デバッグガイド

## データベース関連の問題を調査する際の優先順位

### 1. まずデータベースの状態を直接確認する

問題が発生したら、**最初にデータベースに直接接続して状態を確認**します。

#### MySQLに接続して確認

```bash
# Dockerコンテナ経由でMySQLに接続
docker compose -f docker/docker-compose.yml exec mysql mysql -uquiz_user -pquiz_password quiz_db

# または、ホストから直接接続（ポート3306が公開されている場合）
mysql -uquiz_user -h 127.0.0.1 quiz_db -p
```

#### 確認すべき項目

```sql
-- 1. データベースが存在するか
SHOW DATABASES;

-- 2. テーブルが存在するか
SHOW TABLES;

-- 3. テーブル構造を確認
DESCRIBE category;
DESCRIBE question;
DESCRIBE quiz_session;

-- 4. データが登録されているか
SELECT COUNT(*) FROM category;
SELECT COUNT(*) FROM question;
SELECT * FROM category;

-- 5. テーブルの作成日時を確認（MySQL 8.0以降）
SELECT table_name, create_time 
FROM information_schema.tables 
WHERE table_schema = 'quiz_db';
```

### 2. アプリケーションログを確認する

データベースの状態を確認した後、アプリケーションのログを確認します。

```bash
# Webコンテナのログを確認
docker compose -f docker/docker-compose.yml logs web --tail 100

# エラーや警告をフィルタリング
docker compose -f docker/docker-compose.yml logs web | grep -E "(エラー|Error|Exception|Traceback|データベース|テーブル|初期化)"
```

### 3. コンテナの状態を確認する

```bash
# コンテナが起動しているか
docker compose -f docker/docker-compose.yml ps

# コンテナのヘルスチェック状態
docker compose -f docker/docker-compose.yml ps --format "table {{.Name}}\t{{.Status}}"
```

## 問題の切り分けフローチャート

```
問題: テーブルが作成されていない / データが表示されない
│
├─→ 1. MySQLに直接接続して確認
│   ├─→ テーブルが存在しない
│   │   └─→ アプリケーションの初期化ロジックを確認
│   │       └─→ app.pyのinit_database()を確認
│   │
│   ├─→ テーブルは存在するがデータがない
│   │   └─→ 初期データ登録ロジックを確認
│   │       └─→ init_questions.pyを確認
│   │
│   └─→ テーブルもデータも存在する
│       └─→ アプリケーションの接続設定を確認
│           └─→ DATABASE_URL環境変数を確認
│
├─→ 2. アプリケーションログを確認
│   └─→ エラーメッセージから原因を特定
│
└─→ 3. コンテナの状態を確認
    └─→ コンテナが起動していない場合は起動
```

## よくある問題と確認方法

### 問題1: テーブルが作成されていない

**確認方法:**
```sql
SHOW TABLES;
```

**原因の可能性:**
- `db.create_all()`が実行されていない
- データベース接続エラー
- アプリケーションコンテキストの問題

**確認すべきログ:**
```
データベース接続に成功しました。
データベーステーブルを作成しました。
作成されたテーブル: ['category', 'question', 'quiz_session']
```

### 問題2: テーブルはあるがデータがない

**確認方法:**
```sql
SELECT COUNT(*) FROM category;
SELECT COUNT(*) FROM question;
```

**原因の可能性:**
- 初期データ登録関数が実行されていない
- 初期データ登録関数でエラーが発生している
- アプリケーションコンテキストの問題

**確認すべきログ:**
```
初期データを登録します...
セキュリティカテゴリに20問を登録しました。
初期データの登録が完了しました。
```

### 問題3: アプリケーションコンテキストエラー

**エラーメッセージ:**
```
RuntimeError: The current Flask app is not registered with this 'SQLAlchemy' instance.
```

**確認方法:**
1. エラーログを確認
2. `init_questions.py`で`app`をインポートしていないか確認
3. 関数が`app.app_context()`内で呼び出されているか確認

## デバッグ用スクリプト

### データベース状態確認スクリプト

```bash
#!/bin/bash
# scripts/check-db.sh

echo "=== データベース状態確認 ==="
echo ""

echo "1. テーブル一覧:"
docker compose -f docker/docker-compose.yml exec mysql mysql -uquiz_user -pquiz_password quiz_db -e "SHOW TABLES;"

echo ""
echo "2. カテゴリ数:"
docker compose -f docker/docker-compose.yml exec mysql mysql -uquiz_user -pquiz_password quiz_db -e "SELECT COUNT(*) as count FROM category;"

echo ""
echo "3. 問題数:"
docker compose -f docker/docker-compose.yml exec mysql mysql -uquiz_user -pquiz_password quiz_db -e "SELECT COUNT(*) as count FROM question;"

echo ""
echo "4. カテゴリ一覧:"
docker compose -f docker/docker-compose.yml exec mysql mysql -uquiz_user -pquiz_password quiz_db -e "SELECT id, name FROM category;"
```

## 教訓

1. **データベースの問題は、まずデータベースに直接接続して確認する**
2. **アプリケーションログは、データベースの状態を確認した後に見る**
3. **問題を切り分ける: テーブルがない / データがない / 接続できない**
4. **エラーメッセージを正確に読む（特にFlask-SQLAlchemyのコンテキストエラー）**

