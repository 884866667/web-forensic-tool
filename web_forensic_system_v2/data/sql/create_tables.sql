-- 网页数据表
CREATE TABLE IF NOT EXISTS web_pages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(500) NOT NULL,
    ip_address VARCHAR(45),
    title VARCHAR(500),
    content LONGTEXT,
    html_content LONGTEXT,
    timestamp DATETIME NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_url (url(100)),
    INDEX idx_timestamp (timestamp),
    INDEX idx_hash (content_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 图像数据表
CREATE TABLE IF NOT EXISTS images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    page_id INT,
    image_url VARCHAR(500),
    alt_text VARCHAR(500),
    filename VARCHAR(255),
    image_hash VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (page_id) REFERENCES web_pages(id) ON DELETE CASCADE,
    INDEX idx_image_hash (image_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 检索日志表
CREATE TABLE IF NOT EXISTS search_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    search_type VARCHAR(50),
    search_query TEXT,
    result_count INT,
    search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;