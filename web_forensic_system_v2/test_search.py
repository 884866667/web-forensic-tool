#!/usr/bin/env python
"""测试搜索功能"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.search.text_search import TextSearch

def test_search():
    """测试搜索功能"""
    print("测试搜索功能...")
    
    searcher = TextSearch()
    
    # 测试搜索百度相关内容
    print("\n1. 搜索'百度':")
    results = searcher.search("百度")
    searcher.display_results(results)
    
    print("\n2. 搜索'腾讯':")
    results = searcher.search("腾讯")
    searcher.display_results(results)
    
    return len(results) > 0

if __name__ == "__main__":
    if test_search():
        print("\n✓ 搜索功能测试通过")
    else:
        print("\n✗ 搜索功能测试失败")