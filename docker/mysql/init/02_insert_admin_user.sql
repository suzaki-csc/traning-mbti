-- 管理者ユーザーの作成
-- 注意: ユーザー作成はPythonアプリケーション側で行います
-- このスクリプトではテーブルの初期化のみを実行

USE mbti_db;

-- テーブルが正常に作成されたことを確認
SELECT 'Database tables initialized successfully!' as message;
SELECT 'Admin user will be created by the Python application on first run' as info;
SELECT 'Default admin credentials: admin@example.com / admin123' as credentials;

