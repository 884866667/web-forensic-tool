"""
数据模型定义
"""
from datetime import datetime
from typing import Optional, List

class WebPage:
    """网页数据模型"""
    
    def __init__(self, url: str, ip_address: Optional[str] = None, 
                 title: str = "", content: str = "", html_content: str = "",
                 content_hash: str = ""):
        self.url = url
        self.ip_address = ip_address
        self.title = title
        self.content = content
        self.html_content = html_content
        self.timestamp = datetime.now()
        self.content_hash = content_hash
        self.images: List[Image] = []
    
    def to_dict(self):
        """转换为字典"""
        return {
            'url': self.url,
            'ip_address': self.ip_address,
            'title': self.title,
            'content': self.content,
            'html_content': self.html_content,
            'timestamp': self.timestamp,
            'content_hash': self.content_hash
        }

class Image:
    """图像数据模型"""
    
    def __init__(self, url: str, alt_text: str = "", 
                 image_hash: str = "", page_id: Optional[int] = None):
        self.url = url
        self.alt_text = alt_text
        self.image_hash = image_hash
        self.page_id = page_id
    
    def to_dict(self):
        """转换为字典"""
        return {
            'url': self.url,
            'alt_text': self.alt_text,
            'image_hash': self.image_hash,
            'page_id': self.page_id
        }