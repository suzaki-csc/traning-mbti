# クイズデータ管理

このディレクトリには、ITクイズアプリケーションで使用する全ての問題データ、カテゴリ定義、用語参考がJSON形式で保存されています。

## ディレクトリ構造

```
data/
├── categories.json           # カテゴリ定義
├── questions/               # 問題データ
│   ├── security.json        # セキュリティ問題
│   ├── it_basics.json       # IT基礎問題
│   ├── programming.json     # プログラミング問題
│   └── project_management.json  # プロジェクトマネージメント問題
└── terms/                   # 用語参考データ
    ├── security.json        # セキュリティ用語
    ├── it_basics.json       # IT基礎用語
    ├── programming.json     # プログラミング用語
    └── project_management.json  # プロジェクトマネージメント用語
```

## データフォーマット

### categories.json

カテゴリ定義を含むJSON配列です。

```json
[
  {
    "name": "カテゴリ名",
    "description": "カテゴリの説明",
    "display_order": 1
  }
]
```

**フィールド説明:**
- `name` (string, 必須): カテゴリの表示名
- `description` (string, 必須): カテゴリの説明文
- `display_order` (integer, 必須): 表示順序（小さい順に表示）

### questions/*.json

各カテゴリの問題データを含むJSON配列です。

```json
[
  {
    "question_text": "問題文",
    "explanation": "解説文",
    "difficulty": 2,
    "choices": [
      {
        "choice_text": "選択肢1",
        "is_correct": true,
        "display_order": 1
      },
      {
        "choice_text": "選択肢2",
        "is_correct": false,
        "display_order": 2
      }
    ]
  }
]
```

**フィールド説明:**
- `question_text` (string, 必須): 問題文
- `explanation` (string, 必須): 正解後に表示される解説
- `difficulty` (integer, 必須): 難易度 (1: 易しい, 2: 普通, 3: 難しい)
- `choices` (array, 必須): 選択肢の配列（4つ必須）
  - `choice_text` (string, 必須): 選択肢の文言
  - `is_correct` (boolean, 必須): 正解かどうか
  - `display_order` (integer, 必須): 表示順序

### terms/*.json

各カテゴリの用語参考データを含むJSON配列です。

```json
[
  {
    "term_name": "用語名",
    "description": "用語の説明",
    "url": "#",
    "display_order": 1
  }
]
```

**フィールド説明:**
- `term_name` (string, 必須): 用語名
- `description` (string, 必須): 用語の説明文
- `url` (string, 必須): 参考リンク（現在は"#"でプレースホルダー）
- `display_order` (integer, 必須): 表示順序

## データの編集方法

### 1. 問題の追加

1. 該当カテゴリの `questions/*.json` ファイルを開く
2. 配列の最後に新しい問題オブジェクトを追加
3. 必ず4つの選択肢を含め、1つだけ `is_correct: true` に設定
4. ファイルを保存

### 2. 問題の修正

1. 該当カテゴリの `questions/*.json` ファイルを開く
2. 修正したい問題を `question_text` で検索
3. 必要な箇所を修正
4. ファイルを保存

### 3. 用語の追加

1. 該当カテゴリの `terms/*.json` ファイルを開く
2. 配列の最後に新しい用語オブジェクトを追加
3. `display_order` を適切に設定
4. ファイルを保存

### 4. カテゴリの追加

1. `categories.json` に新しいカテゴリを追加
2. `questions/` と `terms/` に対応するJSONファイルを作成
3. `migrations/seeds/init_data.py` の `main()` 関数を修正し、新しいカテゴリのロード処理を追加

## データベースへの反映

編集したJSONファイルをデータベースに反映するには、以下のコマンドを実行します：

### 問題データのみ更新（クイズ履歴保持）

```bash
./update_questions.sh
```

このコマンドは：
- ✅ ユーザーアカウントを保持
- ✅ クイズ履歴を保持
- 🔄 問題・選択肢・用語のみ更新

### データベース全体を初期化（全データ削除）

```bash
./init_db.sh
```

このコマンドは：
- ❌ 全データを削除
- 🆕 JSONファイルから全データを再投入
- 🔐 デフォルト管理者アカウントを作成

## 注意事項

### JSONファイルの編集時の注意

1. **UTF-8エンコーディング**: 必ずUTF-8でファイルを保存してください
2. **JSON構文**: カンマ、括弧、引用符などの構文エラーに注意
3. **必須フィールド**: 全ての必須フィールドを含めてください
4. **選択肢の数**: 問題には必ず4つの選択肢が必要です
5. **正解の数**: 1つの問題につき正解は1つだけです

### JSON構文チェック

編集後、以下のツールでJSON構文をチェックできます：

```bash
# Python標準ライブラリでチェック
python -m json.tool data/questions/security.json > /dev/null
```

エラーがなければ何も表示されません。

### バックアップ

重要な編集を行う前に、`data/` ディレクトリ全体をバックアップすることをお勧めします：

```bash
cp -r data/ data_backup_$(date +%Y%m%d_%H%M%S)/
```

## 現在のデータ統計

| カテゴリ | 問題数 | 用語数 |
|---------|--------|--------|
| セキュリティ | 23問 | 5件 |
| IT基礎 | 20問 | 5件 |
| プログラミング | 20問 | 5件 |
| プロジェクトマネージメント | 20問 | 5件 |
| **合計** | **83問** | **20件** |

## トラブルシューティング

### JSON構文エラー

**症状**: `update_questions.sh` 実行時にエラーが出る

**解決方法**:
1. エラーメッセージを確認
2. 該当JSONファイルをJSON Validatorでチェック
3. 構文エラーを修正

### データが反映されない

**症状**: JSONを編集したがアプリに反映されない

**解決方法**:
1. `./update_questions.sh` を実行してデータベースに反映
2. ブラウザのキャッシュをクリア（Cmd/Ctrl + Shift + R）
3. アプリケーションを再起動: `./restart.sh`

### 問題の重複

**症状**: 同じ問題が複数回表示される

**解決方法**:
1. JSONファイル内で `question_text` が重複していないか確認
2. 重複を削除して `./update_questions.sh` を実行

## 関連ファイル

- `migrations/seeds/init_data.py`: データロードスクリプト
- `extract_data_to_json.py`: データベースからJSON抽出スクリプト
- `update_questions.sh`: 問題データ更新スクリプト
- `init_db.sh`: データベース初期化スクリプト


