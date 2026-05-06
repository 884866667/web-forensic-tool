"""
网页爬虫
"""
import requests
from typing import Optional
from bs4 import BeautifulSoup
from ..database.models import WebPage, Image
from .utils import calculate_hash, clean_html_text, extract_images, extract_domain

class WebPageCrawler:
    """网页爬虫类"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = 10
    
    def crawl(self, url: str) -> Optional[WebPage]:
        """爬取单个网页"""
        try:
            print(f"开始爬取: {url}")
            
            # 发送请求
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # 修复编码检测 - 处理中文网站
            if response.encoding is None or response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'
            elif response.encoding.lower() in ['gb2312', 'gbk']:
                response.encoding = 'gb18030'  # 中文编码兼容
            
            html_content = response.text
            
            # 提取标题
            soup = BeautifulSoup(html_content, 'html.parser')
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "无标题"
            
            # 修复标题编码问题
            try:
                # 尝试多种编码方式
                if '�' in title or 'æ' in title:  # 常见的编码错误字符
                    # 尝试重新编码
                    title_bytes = title.encode('latin-1')
                    title = title_bytes.decode('utf-8')
            except:
                pass  # 如果转换失败，保持原样
            
            # 提取纯文本内容
            text_content = clean_html_text(html_content)
            
            # 计算哈希
            content_hash = calculate_hash(html_content)
            
            # 提取域名
            ip_address = extract_domain(url)
            
            # 提取图像
            image_data = extract_images(html_content, url)
            
            # 创建网页对象
            web_page = WebPage(
                url=url,
                ip_address=ip_address,
                title=title,
                content=text_content,
                html_content=html_content,
                content_hash=content_hash
            )
            
            # 添加图像对象
            for img_data in image_data:
                image = Image(
                    url=img_data['url'],
                    alt_text=img_data['alt_text'],
                    image_hash=img_data['image_hash']
                )
                web_page.images.append(image)
            
            print(f"成功爬取: {url}")
            print(f"标题: {title}")
            print(f"内容长度: {len(text_content)} 字符")
            print(f"图像数量: {len(image_data)}")
            
            return web_page
            
        except requests.exceptions.Timeout:
            print(f"请求超时 {url}: 连接超时")
            return None
        except requests.exceptions.ConnectionError:
            print(f"连接错误 {url}: 无法连接到服务器")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP错误 {url}: {e.response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"请求失败 {url}: {e}")
            return None
        except UnicodeDecodeError as e:
            print(f"编码错误 {url}: {e}")
            return None
        except Exception as e:
            print(f"爬取失败 {url}: {e}")
            return None
    
    def crawl_multiple(self, urls: list) -> list:
        """批量爬取网页"""
        results = []
        import time
        
        for url in urls:
            web_page = self.crawl(url)
            if web_page:
                results.append(web_page)
            time.sleep(1)  # 礼貌等待，防止被封IP
        
        return results

def test_crawler():
    """测试函数"""
    print("测试爬虫功能...")
    
    crawler = WebPageCrawler()
    
    # 测试多个网站
    test_urls = [
        "https://www.baidu.com",
        "https://www.qq.com",
        "https://www.sina.com.cn"
    ]
    
    for url in test_urls:
        print(f"\n测试爬取: {url}")
        web_page = crawler.crawl(url)
        if web_page:
            print(f"✓ 成功爬取: {web_page.title}")
        else:
            print(f"✗ 爬取失败")

if __name__ == "__main__":
    test_crawler()