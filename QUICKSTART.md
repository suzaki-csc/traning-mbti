# クイックスタートガイド

## 🚀 すぐに始める（最短3ステップ）

### 1. リポジトリに移動
```bash
cd /Users/csc-r063/Documents/github/traning-mbti
```

### 2. Dockerコンテナを起動
```bash
docker-compose up --build
```

### 3. ブラウザでアクセス
```
http://localhost:5000
```

これだけで完了です！

---

## 📱 アクセスURL

| サービス | URL | 認証情報 |
|---------|-----|---------|
| **メインアプリ** | http://localhost:5000 | - |
| **管理画面** | http://localhost:5000/admin | admin / admin123 |
| **pgAdmin** | http://localhost:5050 | admin@example.com / admin |

---

## 🛠️ よく使うコマンド

```bash
# 起動（バックグラウンド）
docker-compose up -d

# 停止
docker-compose down

# ログ確認
docker-compose logs -f web

# 再起動
docker-compose restart

# すべてリセット（データ削除）
docker-compose down -v
docker-compose up --build
```

---

## 🎯 機能一覧

### ユーザー機能
✅ 12問の性格診断  
✅ MBTI 16タイプ判定  
✅ 詳細な結果表示（強み・適職）  
✅ 結果の保存（任意）  

### 管理機能
✅ 統計ダッシュボード  
✅ 診断履歴の閲覧  
✅ タイプ別集計  
✅ データの削除  

---

## 📊 診断フロー

```
トップページ
    ↓
名前・メール入力（任意）
    ↓
質問1/12 → 質問2/12 → ... → 質問12/12
    ↓
結果表示（MBTIタイプ + 詳細）
    ↓
保存（任意）
```

---

## 🔧 トラブルシューティング

### ポート衝突エラー
```bash
# ポート5000が使用中の場合
lsof -i :5000

# docker-compose.ymlを編集
# ports: - "5001:5000"  # 左側を変更
```

### データベース接続エラー
```bash
# コンテナ状態確認
docker-compose ps

# すべてリセット
docker-compose down -v
docker-compose up --build
```

---

## 📂 プロジェクト構造

```
traning-mbti/
├── docker-compose.yml       # Docker設定
├── app/                     # Flaskアプリ
│   ├── app.py              # エントリーポイント
│   ├── models/             # データモデル
│   ├── routes/             # ルーティング
│   ├── services/           # ビジネスロジック
│   ├── templates/          # HTMLテンプレート
│   └── static/             # CSS/JS
└── db/                     # データベース設定
```

---

## 📝 デモデータ作成

```bash
# コンテナに入る
docker-compose exec web python

# Pythonインタラクティブシェルで
>>> from app import app, db
>>> from models import Diagnosis
>>> with app.app_context():
...     # テストデータ作成
...     d = Diagnosis(
...         session_id='test-001',
...         user_name='テストユーザー',
...         mbti_type='INTJ',
...         e_score=2, i_score=4,
...         s_score=2, n_score=4,
...         t_score=6, f_score=0,
...         j_score=4, p_score=2
...     )
...     db.session.add(d)
...     db.session.commit()
>>> exit()
```

---

## 🎨 カスタマイズ

### 質問の変更
`app/services/questions.py` を編集

### スタイルの変更
`app/static/css/custom.css` を編集

### 管理者パスワードの変更
`.env` ファイルを作成して設定:
```
ADMIN_USERNAME=your-admin
ADMIN_PASSWORD=your-password
```

---

## ✅ チェックリスト

- [ ] Docker Desktopが起動している
- [ ] ポート5000, 5432, 5050が空いている
- [ ] `docker-compose up --build` を実行
- [ ] http://localhost:5000 にアクセスできる
- [ ] 診断を1回実行してみる
- [ ] 管理画面で結果が確認できる

---

## 📖 詳細ドキュメント

- [DESIGN.md](DESIGN.md) - 設計書
- [README_SETUP.md](README_SETUP.md) - 詳細セットアップ

---

**問題が発生した場合は、ログを確認してください:**
```bash
docker-compose logs -f
```

