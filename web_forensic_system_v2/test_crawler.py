#!/usr/bin/env python
"""
测试爬虫功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 测试爬取百度
try:
    from src.crawler.webpage_crawler import WebPageCrawler
    from src.database.db_manager import DatabaseManager
    
    print("测试爬虫功能...")
    
    crawler = WebPageCrawler()
    test_url = "https://www.baidu.com"
    
    print(f"爬取测试URL: {test_url}")
    web_page = crawler.crawl(test_url)
    
    if web_page:
        print("爬取成功！正在保存到数据库...")
        with DatabaseManager() as db:
            page_id = db.save_web_page(web_page)
            if page_id:
                print(f"保存成功！网页ID: {page_id}")
            else:
                print("保存失败")
    else:
        print("爬取失败！")
        
except ImportError as e:
    print(f"导入失败: {e}")
    print("请确保已安装依赖: pip install requests beautifulsoup4")
except Exception as e:
    print(f"测试失败: {e}")