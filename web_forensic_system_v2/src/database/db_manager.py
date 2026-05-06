"""
数据库管理类
"""
import pymysql
import sys
import os
from typing import List, Dict, Any, Optional

# 修复1：添加项目根目录到Python路径
current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
sys.path.insert(0, project_root)

try:
    # 修复2：直接从config模块导入
    import config.settings as settings
    import config.database as database
    
    # 使用配置
    DB_CONFIG = settings.DATABASE_CONFIG
    HAS_CONFIG = True
except ImportError:
    # 如果导入失败，使用硬编码配置
    DB_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'database': 'web_forensics_v2',
        'charset': 'utf8mb4'
    }
    HAS_CONFIG = False
    print("警告：使用默认数据库配置")

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """连接数据库"""
        try:
            if HAS_CONFIG:
                self.connection = database.DatabaseConnection.get_connection()
            else:
                self.connection = pymysql.connect(
                    host=DB_CONFIG['host'],
                    port=DB_CONFIG['port'],
                    user=DB_CONFIG['user'],
                    password=DB_CONFIG['password'],
                    database=DB_CONFIG['database'],
                    charset=DB_CONFIG['charset'],
                    cursorclass=pymysql.cursors.DictCursor
                )
            return self
        except Exception as e:
            print(f"数据库连接失败: {e}")
            raise
    
    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def create_tables(self) -> bool:
        """创建所有数据表"""
        try:
            sql_path = os.path.join(project_root, 'data', 'sql', 'create_tables.sql')
            
            with open(sql_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            with self.connection.cursor() as cursor:
                for statement in sql_script.split(';'):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)
                
                self.connection.commit()
                print("✓ 数据表创建完成")
                return True
                
        except FileNotFoundError:
            print(f"✗ 错误：SQL文件不存在: {sql_path}")
            return False
        except Exception as e:
            print(f"✗ 创建表失败: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def get_page_count(self) -> int:
        """获取网页总数"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as count FROM web_pages")
                result = cursor.fetchone()
                return result['count'] if result else 0
        except Exception as e:
            print(f"获取网页数量失败: {e}")
            return 0
    
    def save_web_page(self, web_page) -> int:
        """保存网页数据到数据库"""
        try:
            with self.connection.cursor() as cursor:
                # 检查是否已存在
                cursor.execute("SELECT id FROM web_pages WHERE content_hash = %s", 
                             (web_page.content_hash,))
                existing = cursor.fetchone()
                
                if existing:
                    print(f"内容已存在 (ID: {existing['id']})")
                    return existing['id']
                
                # 插入网页数据
                cursor.execute("""
                    INSERT INTO web_pages 
                    (url, ip_address, title, content, html_content, timestamp, content_hash)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    web_page.url,
                    web_page.ip_address,
                    web_page.title,
                    web_page.content[:50000],  # 限制长度
                    web_page.html_content[:1000000],  # 限制长度
                    web_page.timestamp,
                    web_page.content_hash
                ))
                
                page_id = cursor.lastrowid
                
                # 保存图像
                for image in web_page.images[:10]:  # 最多保存10张
                    try:
                        cursor.execute("""
                            INSERT INTO images (page_id, image_url, alt_text, image_hash)
                            VALUES (%s, %s, %s, %s)
                        """, (
                            page_id,
                            image.url,
                            image.alt_text,
                            image.image_hash
                        ))
                    except Exception as img_e:
                        print(f"保存图像失败: {img_e}")
                
                self.connection.commit()
                print(f"网页保存成功，ID: {page_id}")
                return page_id
                
        except Exception as e:
            print(f"保存网页失败: {e}")
            self.connection.rollback()
            return 0

def test_database():
    """测试数据库连接"""
    print("测试数据库连接...")
    try:
        with DatabaseManager() as db:
            count = db.get_page_count()
            print(f"当前网页数量: {count}")
            return True
    except Exception as e:
        print(f"数据库测试失败: {e}")
        return False

if __name__ == "__main__":
    test_database()