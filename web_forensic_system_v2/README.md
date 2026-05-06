\# 网页综合取证系统 V2

一个功能完善的网页数据采集、存储和检索系统。

\## 功能特性

✅ 爬取指定网页数据

✅ 数据加时间戳和哈希计算

✅ 存储到MySQL数据库

✅ 文本内容检索

✅ 系统状态查看

✅ 批量网页爬取

✅ 图像哈希搜索

✅ 定时爬取任务

✅ 现代化Web界面

✅ 完整系统测试


\## 快速开始



\### 1. 安装依赖

```bash
pip install -r requirements.txt
```
\### 2. 配置数据库
编辑 config/settings.py 文件，修改数据库连接配置：
```
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '你的密码',
    'database': 'web_forensics_v2',
    'charset': 'utf8mb4'
}
```

\### 3. 初始化数据库

# 方法1：使用Web界面
```bash
python web_app.py
```
# 然后在Web界面点击"初始化数据库"

# 方法2：使用命令行
```bash
python setup_database.py
```
# 或
```bash
python main.py --init-db
```


\### 4. 启动Web界面
```bash
python web_app.py
```

\### 5. 使用命令行（可选）
# 爬取单个网页
python main.py --crawl https://www.baidu.com

# 文本搜索
python main.py --search-text "关键词"

# 图像搜索
python main.py --search-image "图像哈希"

# 启动定时任务
python main.py --schedule --interval 24

# 查看系统状态
python main.py --status

# 运行完整测试
python main.py --test





\### Web界面功能
系统管理
初始化数据库

查看系统状态

运行系统测试

网页爬取
单个爬取：爬取指定URL的网页

批量爬取：一次性爬取多个URL（支持文件导入）

定时任务：按设定时间间隔自动爬取

搜索功能
文本搜索：全文检索网页内容

图像搜索：基于图像哈希值搜索

结果展示
实时显示命令执行结果

支持自动滚动

一键复制结果

数据库状态实时更新



\###数据库设计
系统使用MySQL数据库，包含以下表：

web_pages 表
存储网页基本信息：

id: 主键

url: 网页URL

title: 网页标题

content: 文本内容

html_content: HTML源码

timestamp: 爬取时间

content_hash: 内容哈希值（用于去重）

images 表
存储图像信息：

id: 主键

page_id: 关联的网页ID

image_url: 图像URL

alt_text: 图像描述

image_hash: 图像哈希值

search_log 表
记录搜索历史：

id: 主键

search_type: 搜索类型

search_query: 搜索关键词

result_count: 结果数量

search_time: 搜索时间



\### 系统测试
系统提供完整的测试功能：

# 运行完整测试
python test_all.py
# 或
python main.py --test

测试内容包括：

数据库连接测试

爬虫功能测试

搜索功能测试

定时任务模块测试