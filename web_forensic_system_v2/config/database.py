"""
数据库连接配置
"""
import pymysql
from pymysql.cursors import DictCursor
from .settings import DATABASE_CONFIG

class DatabaseConnection:
    """数据库连接管理器"""
    
    @staticmethod
    def get_connection():
        """获取数据库连接"""
        try:
            connection = pymysql.connect(
                host=DATABASE_CONFIG['host'],
                port=DATABASE_CONFIG['port'],
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password'],
                database=DATABASE_CONFIG['database'],
                charset=DATABASE_CONFIG['charset'],
                cursorclass=DictCursor
            )
            return connection
        except pymysql.MySQLError as e:
            print(f"数据库连接失败: {e}")
            raise