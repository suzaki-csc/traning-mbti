-- 文字コード設定
ALTER DATABASE mbti_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ユーザーが存在する場合は削除
DROP USER IF EXISTS 'mbti_user'@'%';

-- ユーザーを作成
CREATE USER 'mbti_user'@'%' IDENTIFIED BY 'mbti_password';

-- データベースへの権限を付与
GRANT ALL PRIVILEGES ON mbti_db.* TO 'mbti_user'@'%';

-- 権限を反映
FLUSH PRIVILEGES;

-- テーブルが存在する場合は削除
DROP TABLE IF EXISTS diagnosis_answers;
DROP TABLE IF EXISTS diagnosis_sessions;
DROP TABLE IF EXISTS users;

-- usersテーブル作成
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(80) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- diagnosis_sessionsテーブル作成
CREATE TABLE diagnosis_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(36) UNIQUE NOT NULL,
    user_id INT NULL,
    mbti_type VARCHAR(4) NOT NULL,
    scores_json JSON NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_created_at (created_at),
    INDEX idx_mbti_type (mbti_type),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- diagnosis_answersテーブル作成
CREATE TABLE diagnosis_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    question_id INT NOT NULL,
    axis VARCHAR(1) NOT NULL,
    score INT NOT NULL,
    answer_text TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES diagnosis_sessions(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id),
    INDEX idx_question_id (question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- デフォルト管理者ユーザーはアプリケーション起動時に自動作成されます
-- Email: admin@example.com
-- Password: admin123

