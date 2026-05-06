"""
爬虫工具函数
"""
import hashlib
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from typing import List, Dict

def calculate_hash(content: str) -> str:
    """计算内容的SHA-256哈希值"""
    if isinstance(content, str):
        content = content.encode('utf-8')
    return hashlib.sha256(content).hexdigest()

def extract_domain(url: str) -> str:
    """从URL中提取域名"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return "unknown"

def clean_html_text(html: str) -> str:
    """清理HTML，提取纯文本"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除不需要的标签
        for element in soup(["script", "style", "noscript"]):
            element.decompose()
        
        # 获取文本
        text = soup.get_text()
        
        # 清理空白字符
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text.strip()
    except Exception as e:
        print(f"清理HTML文本失败: {e}")
        return ""

def extract_images(html: str, base_url: str) -> List[Dict[str, str]]:
    """从HTML中提取图像信息"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        images = []
        
        for img in soup.find_all('img'):
            img_url = img.get('src') or img.get('data-src')
            alt_text = img.get('alt', '')
            
            if img_url:
                # 处理相对URL
                if not img_url.startswith(('http://', 'https://')):
                    img_url = urljoin(base_url, img_url)
                
                # 计算图像哈希
                img_hash = calculate_hash(img_url)
                
                images.append({
                    'url': img_url,
                    'alt_text': alt_text,
                    'image_hash': img_hash
                })
        
        return images[:10]  # 最多返回10张图片
    except Exception as e:
        print(f"提取图像失败: {e}")
        return []

def is_valid_url(url: str) -> bool:
    """验证URL是否有效"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False