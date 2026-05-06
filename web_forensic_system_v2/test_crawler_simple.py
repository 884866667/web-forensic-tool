#!/usr/bin/env python
"""简单测试爬虫"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.crawler.webpage_crawler import WebPageCrawler

def test_crawler():
    """测试爬虫功能"""
    print("测试爬虫功能...")
    
    crawler = WebPageCrawler()
    
    # 测试URL
    test_url = "https://www.baidu.com"
    
    print(f"爬取测试URL: {test_url}")
    web_page = crawler.crawl(test_url)
    
    if web_page:
        print("爬取成功！")
        print(f"标题: {web_page.title}")
        print(f"内容长度: {len(web_page.content)}")
        print(f"哈希: {web_page.content_hash[:20]}...")
        return True
    else:
        print("爬取失败！")
        return False

if __name__ == "__main__":
    test_crawler()