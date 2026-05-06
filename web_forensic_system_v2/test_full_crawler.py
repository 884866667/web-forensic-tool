#!/usr/bin/env python
"""完整测试爬虫和数据库保存"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.crawler.webpage_crawler import WebPageCrawler
from src.database.db_manager import DatabaseManager

def test_full_crawler():
    """测试完整爬虫功能（爬取+保存）"""
    print("=" * 60)
    print("测试完整爬虫功能...")
    print("=" * 60)
    
    # 创建爬虫
    crawler = WebPageCrawler()
    
    # 测试URL
    test_url = "https://www.baidu.com"
    
    print(f"爬取测试URL: {test_url}")
    web_page = crawler.crawl(test_url)
    
    if not web_page:
        print("爬取失败！")
        return False
    
    print("✓ 爬取成功")
    print(f"  标题: {web_page.title}")
    print(f"  内容长度: {len(web_page.content)} 字符")
    print(f"  图像数量: {len(web_page.images)}")
    print(f"  哈希值: {web_page.content_hash[:20]}...")
    
    # 保存到数据库
    print("\n保存到数据库...")
    with DatabaseManager() as db:
        page_id = db.save_web_page(web_page)
        if page_id > 0:
            print(f"✓ 保存成功，ID: {page_id}")
            
            # 验证保存
            count = db.get_page_count()
            print(f"✓ 数据库验证：当前共有 {count} 条网页记录")
            return True
        else:
            print("✗ 保存失败")
            return False

if __name__ == "__main__":
    success = test_full_crawler()
    if success:
        print("\n" + "=" * 60)
        print("✓ 完整测试通过！")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✗ 测试失败")
        print("=" * 60)