"""
图像搜索功能
"""
from typing import List, Dict, Any
from ..database.db_manager import DatabaseManager

class ImageSearch:
    """图像搜索类"""
    
    def search_by_hash(self, image_hash: str) -> List[Dict[str, Any]]:
        """根据图像哈希搜索"""
        print(f"搜索图像哈希: {image_hash}")
        
        with DatabaseManager() as db:
            cursor = db.connection.cursor()
            cursor.execute("""
                SELECT p.id, p.url, p.title, p.timestamp, 
                       i.image_url, i.alt_text, i.image_hash
                FROM web_pages p
                JOIN images i ON p.id = i.page_id
                WHERE i.image_hash = %s
            """, (image_hash,))
            
            results = cursor.fetchall()
            
            # 记录搜索日志
            try:
                cursor.execute("""
                    INSERT INTO search_log (search_type, search_query, result_count)
                    VALUES (%s, %s, %s)
                """, ('image_hash', image_hash, len(results)))
                db.connection.commit()
            except:
                pass
            
            return results
    
    def search_by_url(self, image_url: str) -> List[Dict[str, Any]]:
        """根据图像URL搜索"""
        import hashlib
        image_hash = hashlib.sha256(image_url.encode('utf-8')).hexdigest()
        return self.search_by_hash(image_hash)
    
    def display_results(self, results: List[Dict[str, Any]]):
        """显示搜索结果"""
        if not results:
            print("没有找到相关结果")
            return
        
        print(f"\n找到 {len(results)} 个相关结果:")
        print("=" * 80)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. 网页ID: {result.get('id')}")
            print(f"   网页标题: {result.get('title', '无标题')}")
            print(f"   网页URL: {result.get('url')}")
            print(f"   图像URL: {result.get('image_url')}")
            print(f"   图像描述: {result.get('alt_text', '无描述')}")
            print(f"   图像哈希: {result.get('image_hash', 'N/A')[:16]}...")
            print(f"   时间: {result.get('timestamp')}")
            print("-" * 80)