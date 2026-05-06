"""
定时任务调度器
"""
import schedule
import time
from typing import List
from .webpage_crawler import WebPageCrawler
from ..database.db_manager import DatabaseManager

class CrawlerScheduler:
    """爬虫调度器"""
    
    def __init__(self, urls: List[str] = None):
        self.urls = urls or [
            "https://www.baidu.com",
            "https://www.qq.com",
            "https://www.sina.com.cn"
        ]
        self.crawler = WebPageCrawler()
        self.running = False
    
    def crawl_job(self):
        """爬虫任务"""
        print(f"\n{'='*60}")
        print(f"开始执行定时爬取任务，时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"目标URL数量: {len(self.urls)}")
        print(f"{'='*60}")
        
        success_count = 0
        total_count = 0
        
        with DatabaseManager() as db:
            for url in self.urls:
                total_count += 1
                print(f"\n[{total_count}/{len(self.urls)}] 爬取: {url}")
                
                web_page = self.crawler.crawl(url)
                if web_page:
                    page_id = db.save_web_page(web_page)
                    if page_id > 0:
                        success_count += 1
                        print(f"✓ 保存成功，ID: {page_id}")
                    else:
                        print(f"✗ 保存失败")
                else:
                    print(f"✗ 爬取失败")
                
                time.sleep(1)  # 礼貌等待
        
        print(f"\n{'='*60}")
        print(f"定时爬取任务完成")
        print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"结果: 成功 {success_count}/{total_count} 个网页")
        print(f"{'='*60}")
    
    def start(self, interval_hours: int = 24):
        """启动定时任务"""
        print(f"启动定时爬取任务...")
        print(f"目标网站: {self.urls}")
        print(f"执行间隔: 每 {interval_hours} 小时")
        
        # 立即执行一次
        self.crawl_job()
        
        # 设置定时任务
        schedule.every(interval_hours).hours.do(self.crawl_job)
        
        print(f"\n定时任务已启动，按 Ctrl+C 停止")
        print(f"下次执行时间: {schedule.next_run()}")
        
        self.running = True
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("\n定时任务已停止")
            self.running = False
    
    def stop(self):
        """停止定时任务"""
        self.running = False
        print("定时任务停止")