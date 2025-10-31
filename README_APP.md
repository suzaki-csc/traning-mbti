# MBTI風性格診断Webアプリケーション

## ⚠️ 重要な注意事項

**このアプリケーションは学習目的で作成されており、意図的にセキュリティ脆弱性を含んでいます。**

- **本番環境では使用しないでください**
- XSS（クロスサイトスクリプティング）の脆弱性を含みます
- SQLインジェクションの脆弱性を含みます
- セキュリティ学習・教育目的でのみ使用してください

---

## 📋 概要

Flask、MySQL、Dockerを使用したMBTI（Myers-Briggs Type Indicator）風の性格診断Webアプリケーションです。

### 主な機能

- 12問の質問による性格診断
- 4軸（E/I, S/N, T/F, J/P）のスコアリング
- 16種類のMBTIタイプ判定
- 診断結果の保存と履歴表示
- 管理画面での診断履歴検索
- Bootstrap 5によるレスポンシブデザイン

---

## 🛠️ 技術スタック

- **バックエンド**: Python 3.11、Flask 3.0
- **データベース**: MySQL 8.0
- **フロントエンド**: Bootstrap 5.3、Jinja2
- **インフラ**: Docker、Docker Compose
- **その他**: PyMySQL

---

## 📂 プロジェクト構成

```
traning-mbti/
├── app/
│   ├── app.py              # メインアプリケーション
│   ├── config.py           # 設定ファイル
│   ├── requirements.txt    # Python依存関係
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # カスタムCSS
│   │   └── js/
│   │       └── app.js      # カスタムJavaScript
│   └── templates/
│       ├── base.html       # ベーステンプレート
│       ├── index.html      # トップページ
│       ├── diagnosis.html  # 診断ページ
│       ├── result.html     # 結果ページ
│       └── admin.html      # 管理画面
├── db/
│   └── init.sql            # DB初期化スクリプト
├── Dockerfile              # アプリ用Dockerfile
├── docker-compose.yml      # Docker Compose設定
├── MBTI診断アプリ設計書.md  # 設計書
└── README_APP.md           # このファイル
```

---

## 🚀 セットアップ方法

### 前提条件

- Docker Desktop がインストールされていること
- Docker Compose が利用可能であること

### インストール手順

1. **リポジトリのクローン（または配置）**

```bash
cd /Users/csc-r063/Documents/github/traning-mbti
```

2. **Dockerコンテナの起動**

```bash
docker-compose up -d --build
```

初回起動時は、イメージのビルドとデータベースの初期化に数分かかります。

3. **起動確認**

```bash
docker-compose ps
```

以下の2つのコンテナが起動していることを確認してください：
- `mbti_app` (Flask アプリケーション)
- `mbti_db` (MySQL データベース)

4. **アプリケーションへのアクセス**

ブラウザで以下のURLにアクセス：

```
http://localhost:5000
```

---

## 📖 使用方法

### 1. 診断を受ける

1. トップページの「診断を始める」ボタンをクリック
2. 名前を入力（任意）
3. 12の質問に5段階で回答
4. 「診断結果を見る」ボタンをクリック
5. MBTIタイプと詳細なスコアが表示されます

### 2. 診断履歴を確認

1. ナビゲーションバーの「診断履歴」をクリック
2. 過去の診断結果一覧が表示されます
3. ユーザー名やMBTIタイプで検索可能
4. 「詳細」ボタンで個別の診断結果を再表示

---

## 🔍 脆弱性の説明（学習目的）

### 1. XSS（Cross-Site Scripting）

**場所**: 診断結果ページ、管理画面

**脆弱なコード**:
```python
# app.py
user_name = request.form.get('user_name')
return render_template('result.html', user_name=user_name)
```

```html
<!-- result.html -->
{{ diagnosis.user_name | safe }}
```

**攻撃例**:
ユーザー名に以下を入力：
```html
<script>alert('XSS')</script>
```

**対策**:
- `| safe` フィルターを削除
- Jinja2のデフォルトのエスケープ機能を使用

### 2. SQL Injection

**場所**: 管理画面の検索機能、結果表示

**脆弱なコード**:
```python
# app.py
search_name = request.args.get('name', '')
query = f"SELECT * FROM diagnosis_results WHERE user_name LIKE '%{search_name}%'"
cursor.execute(query)
```

**攻撃例**:
検索欄に以下を入力：
```sql
' OR '1'='1
```

**対策**:
- プレースホルダーを使用
```python
query = "SELECT * FROM diagnosis_results WHERE user_name LIKE %s"
cursor.execute(query, (f'%{search_name}%',))
```

---

## 🛑 コンテナの停止・削除

### コンテナの停止

```bash
docker-compose stop
```

### コンテナの停止と削除

```bash
docker-compose down
```

### データベースを含めて完全に削除

```bash
docker-compose down -v
```

---

## 🔧 トラブルシューティング

### データベース接続エラー

**症状**: `Can't connect to MySQL server`

**解決方法**:
1. MySQLコンテナが起動しているか確認
```bash
docker-compose ps
```

2. MySQLが完全に起動するまで待つ（初回は1-2分かかる場合があります）

3. ログを確認
```bash
docker-compose logs db
```

### ポート競合エラー

**症状**: `port is already allocated`

**解決方法**:
1. 既存のプロセスを確認
```bash
lsof -i :5000
lsof -i :3306
```

2. `docker-compose.yml` のポート番号を変更
```yaml
ports:
  - "5001:5000"  # 5000 → 5001 に変更
```

### アプリケーションが起動しない

**解決方法**:
1. ログを確認
```bash
docker-compose logs app
```

2. コンテナを再起動
```bash
docker-compose restart app
```

3. 完全に再ビルド
```bash
docker-compose down
docker-compose up -d --build
```

---

## 📊 データベース構造

### テーブル一覧

1. **questions**: 診断質問
2. **diagnosis_results**: 診断結果
3. **answers**: 回答データ

### ER図（簡易版）

```
questions (1) ----< (N) answers
                         |
                         |
                        (N)
                         |
diagnosis_results (1) ---<
```

---

## 🎓 学習ポイント

### Flaskの基本

- ルーティング (`@app.route`)
- テンプレートエンジン (Jinja2)
- フォーム処理
- セッション管理

### データベース操作

- MySQL接続
- CRUD操作
- トランザクション
- リレーション

### Docker

- Dockerfileの作成
- Docker Composeによるマルチコンテナ構成
- ボリュームマウント
- 環境変数の管理

### セキュリティ

- XSSの仕組みと対策
- SQLインジェクションの仕組みと対策
- 入力バリデーション
- エスケープ処理

---

## 🔐 セキュリティ修正版の実装方法

### XSS対策

```python
# config.py に追加
class Config:
    # ...
    # Jinja2のautoescapeを有効化（デフォルトで有効）
```

```html
<!-- テンプレートから | safe を削除 -->
<h2>{{ diagnosis.user_name }}さんの診断結果</h2>
```

### SQL Injection対策

```python
# プレースホルダーを使用
@app.route('/admin')
def admin():
    search_name = request.args.get('name', '')
    
    if search_name:
        query = "SELECT * FROM diagnosis_results WHERE user_name LIKE %s"
        cursor.execute(query, (f'%{search_name}%',))
    else:
        query = "SELECT * FROM diagnosis_results"
        cursor.execute(query)
```

---

## 📚 参考資料

- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Bootstrap 5公式ドキュメント](https://getbootstrap.com/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker公式ドキュメント](https://docs.docker.com/)

---

## 📝 ライセンス

このプロジェクトは学習目的で作成されています。

---

## 👨‍💻 開発者向け情報

### 開発モードでの起動

```bash
# アプリケーションのみを再起動（コード変更時）
docker-compose restart app

# ログをリアルタイムで確認
docker-compose logs -f app
```

### データベースに直接接続

```bash
docker exec -it mbti_db mysql -u mbti_user -pmbti_pass mbti_db
```

### 質問データの追加

`db/init.sql` を編集して、データベースを再初期化：

```bash
docker-compose down -v
docker-compose up -d --build
```

---

## 📞 サポート

質問や問題がある場合は、学習教材の担当者にお問い合わせください。

---

**Happy Learning! 🎉**

