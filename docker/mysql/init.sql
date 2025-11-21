-- データベース初期化SQL
-- このファイルはMySQLコンテナの初回起動時に自動実行されます
-- docker-compose.ymlの環境変数でデータベースとユーザーが作成されますが、
-- 念のため明示的に作成と権限設定を行います

-- データベースが存在しない場合は作成（環境変数で作成されるが、念のため）
CREATE DATABASE IF NOT EXISTS quiz_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ユーザーが存在しない場合は作成（環境変数で作成されるが、念のため）
-- すべてのホストから接続可能にするため '%' を使用
CREATE USER IF NOT EXISTS 'quiz_user'@'%' IDENTIFIED BY 'quiz_password';

-- 権限を付与（アプリケーションから接続するために必要）
GRANT ALL PRIVILEGES ON quiz_db.* TO 'quiz_user'@'%';

-- 権限を反映
FLUSH PRIVILEGES;

-- データベースを選択
USE quiz_db;

-- 初期化完了メッセージ
SELECT 'Database quiz_db and user quiz_user have been initialized successfully' AS status;

