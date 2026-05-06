"""
配置文件
"""

# 数据库配置
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'lutianxin2005',  # 你的密码
    'database': 'web_forensics_v2',
    'charset': 'utf8mb4'
}

# 爬虫配置
CRAWLER_CONFIG = {
    'request_timeout': 10,
    'delay_between_requests': 1,
    'max_content_length': 5000000,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 系统配置
SYSTEM_CONFIG = {
    'log_level': 'INFO',
    'log_dir': 'logs',
    'data_dir': 'data',
    'backup_enabled': True
}

# 搜索配置
SEARCH_CONFIG = {
    'max_results': 50,
    'enable_fulltext_search': True
}