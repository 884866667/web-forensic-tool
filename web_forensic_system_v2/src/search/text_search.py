"""
文本搜索功能
"""
from typing import List, Dict, Any
from ..database.db_manager import DatabaseManager

class TextSearch:
    """文本搜索类"""
    
    def __init__(self, max_results: int = 50):
        self.max_results = max_results
    
    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索关键词"""
        print(f"搜索关键词: {keyword}")
        
        with DatabaseManager() as db:
            try:
                # 先尝试全文索引搜索
                cursor = db.connection.cursor()
                cursor.execute("""
                    SELECT id, url, title, timestamp, content_hash,
                           MATCH(content) AGAINST(%s) as relevance
                    FROM web_pages 
                    WHERE MATCH(content) AGAINST(%s IN NATURAL LANGUAGE MODE)
                    ORDER BY relevance DESC
                    LIMIT %s
                """, (keyword, keyword, self.max_results))
                results = cursor.fetchall()
                
                if results:
                    print(f"使用全文索引搜索到 {len(results)} 条结果")
                    return results
                
            except:
                # 如果全文索引失败，使用LIKE搜索
                cursor = db.connection.cursor()
                cursor.execute("""
                    SELECT id, url, title, timestamp, content_hash,
                           SUBSTRING(content, 1, 200) as content_preview
                    FROM web_pages 
                    WHERE content LIKE %s OR title LIKE %s
                    LIMIT %s
                """, (f'%{keyword}%', f'%{keyword}%', self.max_results))
                results = cursor.fetchall()
            
            # 记录搜索日志
            try:
                cursor.execute("""
                    INSERT INTO search_log (search_type, search_query, result_count)
                    VALUES (%s, %s, %s)
                """, ('keyword', keyword, len(results)))
                db.connection.commit()
            except:
                pass
            
            return results
    
    def display_results(self, results: List[Dict[str, Any]]):
        """显示搜索结果"""
        if not results:
            print("没有找到相关结果")
            return
        
        print(f"\n找到 {len(results)} 个相关结果:")
        print("=" * 80)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. ID: {result.get('id')}")
            print(f"   标题: {result.get('title', '无标题')}")
            print(f"   URL: {result.get('url')}")
            print(f"   时间: {result.get('timestamp')}")
            
            if 'relevance' in result:
                print(f"   相关度: {result['relevance']:.2f}")
            elif 'content_preview' in result:
                preview = result['content_preview']
                if preview:
                    print(f"   内容预览: {preview[:100]}...")
            
            print(f"   哈希: {result.get('content_hash', 'N/A')[:16]}...")
            print("-" * 80)