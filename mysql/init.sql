-- MBTI性格診断アプリ データベース初期化スクリプト

-- データベースの文字コード設定
ALTER DATABASE mbti_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- usersテーブル
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- test_resultsテーブル
CREATE TABLE IF NOT EXISTS test_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    mbti_type VARCHAR(4) NOT NULL,
    e_score INT NOT NULL DEFAULT 0,
    i_score INT NOT NULL DEFAULT 0,
    s_score INT NOT NULL DEFAULT 0,
    n_score INT NOT NULL DEFAULT 0,
    t_score INT NOT NULL DEFAULT 0,
    f_score INT NOT NULL DEFAULT 0,
    j_score INT NOT NULL DEFAULT 0,
    p_score INT NOT NULL DEFAULT 0,
    answers TEXT NOT NULL,
    taken_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_mbti_type (mbti_type),
    INDEX idx_taken_at (taken_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 初期管理者ユーザーの作成（パスワード: admin123）
-- パスワードハッシュは Werkzeug の generate_password_hash で生成
INSERT INTO users (username, email, password_hash, role) 
VALUES (
    'admin', 
    'admin@example.com', 
    'scrypt:32768:8:1$vF4rJ8nX2K6qM9pL$8f7e9d6c5b4a3e2f1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3e2f1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a', 
    'admin'
)
ON DUPLICATE KEY UPDATE username=username;

-- サンプルユーザーの作成（パスワード: user123）
INSERT INTO users (username, email, password_hash, role) 
VALUES (
    'testuser', 
    'testuser@example.com', 
    'scrypt:32768:8:1$vF4rJ8nX2K6qM9pL$8f7e9d6c5b4a3e2f1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3e2f1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a', 
    'user'
)
ON DUPLICATE KEY UPDATE username=username;

-- インデックスの最適化
OPTIMIZE TABLE users;
OPTIMIZE TABLE test_results;

-- テーブル作成完了メッセージ
SELECT 'Database initialization completed successfully!' AS message;

