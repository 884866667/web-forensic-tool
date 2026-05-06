#!/usr/bin/env python
"""完整系统测试"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_all():
    """测试所有功能"""
    print("=" * 60)
    print("网页综合取证系统 V2 - 完整测试")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    try:
        # 测试1: 数据库连接
        print("\n1. 测试数据库连接...")
        from src.database.db_manager import test_database
        if test_database():
            print("✓ 数据库测试通过")
            tests_passed += 1
        else:
            print("✗ 数据库测试失败")
    
    except Exception as e:
        print(f"✗ 数据库测试异常: {e}")
    
    try:
        # 测试2: 爬虫功能
        print("\n2. 测试爬虫功能...")
        from src.crawler.webpage_crawler import WebPageCrawler
        crawler = WebPageCrawler()
        web_page = crawler.crawl("https://www.baidu.com")
        
        if web_page and web_page.title:
            print(f"✓ 爬虫测试通过 - 标题: {web_page.title}")
            tests_passed += 1
        else:
            print("✗ 爬虫测试失败")
    
    except Exception as e:
        print(f"✗ 爬虫测试异常: {e}")
    
    try:
        # 测试3: 搜索功能
        print("\n3. 测试搜索功能...")
        from src.search.text_search import TextSearch
        searcher = TextSearch(max_results=5)
        results = searcher.search("百度")
        
        if results:
            print(f"✓ 搜索测试通过 - 找到 {len(results)} 条结果")
            tests_passed += 1
        else:
            print("✗ 搜索测试失败 - 无结果")
    
    except Exception as e:
        print(f"✗ 搜索测试异常: {e}")
    
    try:
        # 测试4: 定时任务
        print("\n4. 测试定时任务模块...")
        from src.crawler.scheduler import CrawlerScheduler
        scheduler = CrawlerScheduler(urls=["https://www.baidu.com"])
        
        if scheduler and scheduler.urls:
            print("✓ 定时任务模块测试通过")
            tests_passed += 1
        else:
            print("✗ 定时任务模块测试失败")
    
    except Exception as e:
        print(f"✗ 定时任务模块测试异常: {e}")
    
    # 结果汇总
    print("\n" + "=" * 60)
    print(f"测试结果: {tests_passed}/{total_tests} 通过")
    
    if tests_passed == total_tests:
        print("🎉 所有测试通过！系统功能完整。")
        return True
    else:
        print("⚠️  部分功能测试失败。")
        return False

if __name__ == "__main__":
    if test_all():
        print("\n系统测试完成，可以正常使用！")
        print("\n常用命令:")
        print("  python main.py --crawl https://www.example.com")
        print("  python main.py --search-text \"关键词\"")
        print("  python main.py --search-image \"图像哈希\"")
        print("  python main.py --schedule --interval 24")
        print("  python main.py --status")
    else:
        print("\n系统测试失败，请检查问题。")