#!/usr/bin/env python
"""
网页综合取证系统 V2 - 主程序
"""
import argparse
import sys
import os

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='网页综合取证系统 V2',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s --crawl https://www.example.com
  %(prog)s --search-text "关键词"
  %(prog)s --search-image "图像哈希"
  %(prog)s --schedule --interval 24
  %(prog)s --status
        '''
    )
    
    parser.add_argument('--init-db', action='store_true', help='初始化数据库')
    parser.add_argument('--status', action='store_true', help='查看系统状态')
    parser.add_argument('--test', action='store_true', help='测试系统')
    parser.add_argument('--crawl', type=str, help='爬取单个网页')
    parser.add_argument('--search-text', type=str, help='文本搜索')
    parser.add_argument('--search-image', type=str, help='图像哈希搜索')
    parser.add_argument('--schedule', action='store_true', help='启动定时爬取任务')
    parser.add_argument('--interval', type=int, default=24, help='定时任务间隔时间（小时）')
    
    args = parser.parse_args()
    
    try:
        if args.init_db:
            print("正在初始化数据库...")
            from scripts.setup_database import main as setup_db
            setup_db()
        
        elif args.crawl:
            print(f"爬取网页: {args.crawl}")
            from src.crawler.webpage_crawler import WebPageCrawler
            from src.database.db_manager import DatabaseManager
            
            crawler = WebPageCrawler()
            web_page = crawler.crawl(args.crawl)
            
            if web_page:
                with DatabaseManager() as db:
                    page_id = db.save_web_page(web_page)
                    if page_id > 0:
                        print(f"✓ 爬取并保存成功，ID: {page_id}")
                    else:
                        print("✗ 保存失败")
            else:
                print("✗ 爬取失败")
        
        elif args.search_text:
            print(f"文本搜索: {args.search_text}")
            from src.search.text_search import TextSearch
            
            searcher = TextSearch()
            results = searcher.search(args.search_text)
            searcher.display_results(results)
        
        elif args.search_image:
            print(f"图像搜索: {args.search_image}")
            from src.search.image_search import ImageSearch
            
            searcher = ImageSearch()
            results = searcher.search_by_hash(args.search_image)
            searcher.display_results(results)
        
        elif args.schedule:
            print("启动定时爬取任务...")
            from src.crawler.scheduler import CrawlerScheduler
            
            scheduler = CrawlerScheduler()
            scheduler.start(args.interval)
        
        elif args.status:
            print("查看系统状态...")
            from src.database.db_manager import test_database
            test_database()
        
        elif args.test:
            print("测试系统...")
            from src.database.db_manager import test_database
            db_ok = test_database()
            
            if db_ok:
                print("✓ 系统测试通过")
            else:
                print("✗ 系统测试失败")
        
        else:
            parser.print_help()
            print("\n请使用: python main.py --test 测试系统")
    
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    main()