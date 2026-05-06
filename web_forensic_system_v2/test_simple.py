#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单测试
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 测试1: 查看状态
print("=== 测试1: 查看状态 ===")
try:
    from src.database.db_manager import DatabaseManager
    with DatabaseManager() as db:
        count = db.get_page_count()
        print(f"数据库中有 {count} 条记录")
except Exception as e:
    print(f"错误: {e}")

# 测试2: 简单搜索
print("\n=== 测试2: 搜索测试 ===")
try:
    from src.database.db_manager import DatabaseManager
    with DatabaseManager() as db:
        results = db.search_by_keyword("Herman")
        print(f"搜索到 {len(results)} 条结果")
        for r in results:
            print(f"ID: {r['id']}, 标题: {r['title'][:20]}")
except Exception as e:
    print(f"错误: {e}")

print("\n=== 测试完成 ===")