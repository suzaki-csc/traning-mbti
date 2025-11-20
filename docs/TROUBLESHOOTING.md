# トラブルシューティングガイド

## エラー: `no such table: categories`

### 症状
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: categories
```

### 原因
このエラーは、以下のいずれかが原因で発生します：

1. **Dockerコンテナ内に古いコードが残っている**
   - エラーパスに `/app/app/routes/main.py` が表示される場合
   - 別のアプリケーションコードが混在している可能性

2. **データベースが初期化されていない**
   - テーブルが作成されていない
   - 初期データが登録されていない

3. **ボリュームマウントの問題**
   - 古いコードがマウントされている
   - コードの更新が反映されていない

### 解決方法

#### 方法1: Dockerコンテナを完全に再ビルド（推奨）

```bash
# macOS/Linux
./rebuild.sh

# または手動で
docker compose down -v
docker rmi quiz-app-web 2>/dev/null || true
docker compose build --no-cache
docker compose up
```

#### 方法2: データベースをリセット

```bash
# コンテナを停止
docker compose down

# データベースファイルを削除
rm quiz.db  # macOS/Linux
# del quiz.db  # Windows

# 再起動（自動的に初期化されます）
docker compose up
```

#### 方法3: コンテナ内で手動で初期化

```bash
# コンテナが起動している状態で
docker compose exec web poetry run python data/init_questions.py
```

#### 方法4: コンテナ内のファイル構造を確認

```bash
# コンテナ内のファイル一覧を確認
docker compose exec web ls -la /app/

# 実行されているapp.pyを確認
docker compose exec web cat /app/app.py | head -20

# データベースの状態を確認
docker compose exec web poetry run python -c "from app import app; from models import db, Category; app.app_context().push(); print(f'カテゴリ数: {Category.query.count()}')"
```

### 確認事項

1. **エラーパスが `/app/app/routes/main.py` の場合**
   - これは別のアプリケーションコードです
   - Dockerコンテナを完全に再ビルドしてください

2. **テーブル名が `categories`（複数形）の場合**
   - 正しいテーブル名は `category`（単数形）です
   - モデル定義を確認してください

3. **`display_order` や `is_active` カラムが参照されている場合**
   - これらのカラムは現在のモデルには存在しません
   - 古いコードが実行されている可能性があります

### 予防策

1. **`.dockerignore` を確認**
   - 不要なファイルがコンテナに含まれていないか確認

2. **ボリュームマウントを確認**
   - `docker-compose.yml` の `volumes` セクションを確認
   - 必要なファイルのみをマウント

3. **定期的な再ビルド**
   - 大きな変更後はコンテナを再ビルド

## その他のよくあるエラー

### ポートが既に使用されている

```bash
# docker-compose.yml の ports を変更
ports:
  - "5001:5000"  # ホストの5001ポートを使用
```

### コンテナが起動しない

```bash
# ログを確認
docker compose logs web

# コンテナを再ビルド
docker compose build --no-cache
docker compose up
```

### データベースのロックエラー

```bash
# コンテナを停止
docker compose down

# データベースファイルの権限を確認
ls -la quiz.db

# 再起動
docker compose up
```

