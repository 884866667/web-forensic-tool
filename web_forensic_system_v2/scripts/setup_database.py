#!/usr/bin/env python
"""
数据库初始化脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.database.db_manager import DatabaseManager
    HAS_DB_MODULE = True
except ImportError:
    HAS_DB_MODULE = False

def main():
    """初始化数据库"""
    print("正在初始化数据库...")
    
    try:
        # 先尝试创建数据库
        import pymysql
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='lutianxin2005'  # 你的密码
        )
        
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS web_forensics_v2")
            print("数据库创建成功")
        
        conn.close()
        
        # 创建数据表（如果db_manager可用）
        if HAS_DB_MODULE:
            with DatabaseManager() as db:
                if db.create_tables():
                    print("数据库初始化完成！")
                    print("数据库名: web_forensics_v2")
                    print("已创建表: web_pages, images, search_log")
                else:
                    print("数据表创建失败！")
        else:
            print("数据库创建成功，但数据表需要手动创建")
            print("请运行: python data/sql/create_tables.sql 在MySQL中")
    
    except ImportError:
        print("错误：请先安装pymysql: pip install pymysql")
    except Exception as e:
        print(f"初始化失败: {e}")

if __name__ == "__main__":
    main()