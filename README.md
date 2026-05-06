# 网页综合取证系统 V2

一个功能完善的网页数据采集、存储和检索系统，用于网页数据的取证和分析。

## 🚀 功能特性

### 核心功能
1. **定时网页爬取** - 支持定时自动爬取指定网页
2. **数据完整性验证** - 自动计算SHA-256哈希值并添加时间戳
3. **数据存储** - 将网页内容、IP地址、哈希值等存储到MySQL数据库
4. **内容检索** - 支持文本关键字搜索和图像哈希搜索

### 技术特点
- 模块化设计，代码结构清晰
- 支持中文网页编码自动检测
- 完善的异常处理和日志记录
- 可配置的定时任务系统
- 数据库备份功能

## 📁 项目结构
web_forensic_system_v2/
├── main.py # 主程序入口
├── requirements.txt # Python依赖包
├── README.md # 项目说明文档
├── config/ # 配置文件目录
│ ├── settings.py # 系统配置文件
│ └── database.py # 数据库连接配置
├── src/ # 源代码目录
│ ├── crawler/ # 爬虫模块
│ │ ├── webpage_crawler.py # 网页爬虫
│ │ ├── scheduler.py # 定时任务调度
│ │ └── utils.py # 爬虫工具函数
│ ├── database/ # 数据库模块
│ │ ├── db_manager.py # 数据库管理器
│ │ ├── models.py # 数据模型定义
│ │ └── queries.py # SQL查询语句
│ ├── search/ # 搜索模块
│ │ ├── text_search.py # 文本搜索功能
│ │ └── image_search.py # 图像搜索功能
│ └── utils/ # 通用工具模块
├── data/ # 数据目录
│ ├── sql/ # SQL脚本
│ │ └── create_tables.sql # 数据库建表脚本
│ └── images/ # 图像存储目录
├── logs/ # 日志文件目录
├── tests/ # 测试目录
│ ├── test_all.py # 完整系统测试
│ ├── test_crawler.py # 爬虫功能测试
│ └── test_search.py # 搜索功能测试
└── scripts/ # 脚本目录
├── setup_database.py # 数据库初始化脚本
└── backup_database.py # 数据库备份脚本

## ⚙️ 安装部署

### 1. 环境要求
- Python 3.8+
- MySQL 5.7+
- Windows/Linux/macOS

### 2. 安装依赖
```bash
pip install -r requirements.txt
3. 数据库配置
修改 config/settings.py 中的数据库配置：
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '你的密码',  # 修改这里
    'database': 'web_forensics_v2',
    'charset': 'utf8mb4'
}
4. 初始化数据库
python scripts/setup_database.py
🎯 使用方法
基本命令
# 查看帮助
python main.py --help
# 初始化数据库
python main.py --init-db
# 查看系统状态
python main.py --status
# 系统测试
python main.py --test

爬取功能
# 爬取单个网页
python main.py --crawl https://www.example.com
# 爬取多个网页（用空格分隔）
python main.py --crawl https://www.baidu.com https://www.qq.com

搜索功能
# 文本关键字搜索
python main.py --search-text "关键词"
# 图像哈希搜索
python main.py --search-image "图像哈希值"

定时任务
# 启动定时爬取任务（默认24小时）
python main.py --schedule
# 自定义执行间隔（小时）
python main.py --schedule --interval 12

🔍 数据库结构
web_pages 表
存储网页基本信息：
id: 主键，自增
url: 网页URL
ip_address: 网站IP/域名
title: 网页标题
content: 纯文本内容
html_content: 完整HTML内容
timestamp: 爬取时间戳
content_hash: 内容SHA-256哈希值
created_at: 创建时间

images 表
存储网页图像信息：
id: 主键，自增
page_id: 关联的网页ID
image_url: 图像URL
alt_text: 图像描述文本
image_hash: 图像SHA-256哈希值
created_at: 创建时间

search_log 表
存储搜索记录：
id: 主键，自增
search_type: 搜索类型（keyword/image_hash）
search_query: 搜索关键词
result_count: 搜索结果数量
search_time: 搜索时间

🧪 测试验证
运行完整测试：
python tests/test_all.py
测试爬虫功能：
python tests/test_crawler.py
测试搜索功能：
python tests/test_search.py

🔧 维护脚本
数据库备份
python scripts/backup_database.py
备份文件保存在 backups/ 目录，格式为 .sql.gz

查看数据库内容
# 创建检查脚本
python -c "
import sys
sys.path.append('.')
from src.database.db_manager import DatabaseManager
with DatabaseManager() as db:
    count = db.get_page_count()
    print(f'当前网页数量: {count}')
"

📊 数据验证
系统自动为每条记录生成：
1.时间戳：精确到秒的爬取时间
2.哈希值：SHA-256哈希，确保数据完整性
3.IP地址：网页来源域名/IP
可通过以下方式验证：
-- 在MySQL中验证数据完整性
SELECT 
    id,
    url,
    timestamp,
    LEFT(content_hash, 16) as hash_prefix,
    LENGTH(content) as content_length
FROM web_pages;

⚠️ 注意事项
1.遵守robots.txt：请确保爬取的网站允许爬取
2.控制爬取频率：避免对目标网站造成过大压力
3.数据安全：数据库密码等敏感信息请妥善保管
4.法律法规：遵守相关法律法规，仅用于合法用途

📈 性能指标
单页爬取时间：1-5秒
数据库查询响应：< 100ms
支持并发爬取：可配置
数据存储容量：支持百万级记录

🆘 故障排除
常见问题
1.数据库连接失败
检查MySQL服务是否启动
验证config/settings.py中的密码
确认防火墙设置

2.爬取失败
检查网络连接
验证URL是否正确
检查目标网站是否可访问

3.编码问题
系统已自动处理常见编码
如遇乱码可手动指定编码

日志查看
日志文件保存在 logs/ 目录：
system.log: 系统运行日志
crawler.log: 爬虫操作日志
error.log: 错误日志

🤝 贡献指南
1.Fork 本仓库
2.创建功能分支
3.提交更改
4.创建 Pull Request

📄 许可证
本项目仅供学习和研究使用。

📞 联系支持
如有问题或建议，请提交Issue或联系维护者。

版本: V2.0
最后更新: 2026年1月
状态: ✅ 生产就绪