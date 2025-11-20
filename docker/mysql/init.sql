-- MySQL初期化スクリプト
-- データベースとユーザーの作成

-- データベースが存在しない場合は作成
CREATE DATABASE IF NOT EXISTS quiz_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ユーザーが存在しない場合は作成
CREATE USER IF NOT EXISTS 'quiz_user'@'%' IDENTIFIED BY 'quiz_password';

-- ユーザーに権限を付与
GRANT ALL PRIVILEGES ON quiz_db.* TO 'quiz_user'@'%';

-- 権限を反映
FLUSH PRIVILEGES;

-- 使用するデータベースを選択
USE quiz_db;

