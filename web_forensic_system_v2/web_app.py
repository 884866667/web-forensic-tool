#!/usr/bin/env python
"""
网页综合取证系统 Web界面 - 修复版
"""
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import subprocess
import sys
import os
import threading
import json
import traceback

app = Flask(__name__)
app.secret_key = 'web_forensics_secret_key_2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class CommandExecutor:
    """执行命令行命令的辅助类"""

    @staticmethod
    def run_command(args):
        """运行命令行命令并返回结果"""
        try:
            print(f"执行命令: python main.py {' '.join(args)}")

            # 获取当前工作目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            main_py_path = os.path.join(current_dir, 'main.py')

            # 检查main.py是否存在
            if not os.path.exists(main_py_path):
                return {
                    'success': False,
                    'output': f"错误：找不到 main.py 文件\n路径：{main_py_path}",
                    'returncode': -1
                }

            # 构建完整命令
            cmd = [sys.executable, main_py_path] + args

            # 设置环境变量确保编码正确
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONUTF8'] = '1'

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=300,  # 5分钟超时
                cwd=current_dir,  # 设置工作目录
                env=env
            )

            # 合并输出
            output = ""
            if result.stdout:
                output += "标准输出:\n" + result.stdout + "\n"
            if result.stderr:
                output += "\n错误输出:\n" + result.stderr

            print(f"命令执行完成，返回码: {result.returncode}")
            print(f"输出长度: {len(output)} 字符")

            return {
                'success': result.returncode == 0,
                'output': output.strip() or "命令执行完成，但没有输出",
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            error_msg = "命令执行超时（超过5分钟）"
            print(error_msg)
            return {
                'success': False,
                'output': error_msg,
                'returncode': -1
            }
        except Exception as e:
            error_msg = f"执行命令时发生错误: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return {
                'success': False,
                'output': error_msg,
                'returncode': -1
            }


@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')


@app.route('/api/init_db', methods=['POST'])
def init_database():
    """初始化数据库"""
    print("API调用: /api/init_db")
    result = CommandExecutor.run_command(['--init-db'])
    return jsonify(result)


@app.route('/api/status', methods=['GET', 'POST'])
def get_status():
    """查看系统状态"""
    print("API调用: /api/status")
    result = CommandExecutor.run_command(['--status'])
    return jsonify(result)


@app.route('/api/test', methods=['POST'])
def test_system():
    """测试系统"""
    print("API调用: /api/test")
    result = CommandExecutor.run_command(['--test'])
    return jsonify(result)


@app.route('/api/crawl', methods=['POST'])
def crawl_page():
    """爬取单个网页"""
    data = request.json
    url = data.get('url', '').strip()

    if not url:
        return jsonify({
            'success': False,
            'output': '请提供URL地址',
            'returncode': -1
        })

    print(f"API调用: /api/crawl, URL: {url}")
    result = CommandExecutor.run_command(['--crawl', url])
    return jsonify(result)


@app.route('/api/search_text', methods=['POST'])
def search_text():
    """文本搜索"""
    data = request.json
    keyword = data.get('keyword', '').strip()

    if not keyword:
        return jsonify({
            'success': False,
            'output': '请提供搜索关键词',
            'returncode': -1
        })

    print(f"API调用: /api/search_text, 关键词: {keyword}")
    result = CommandExecutor.run_command(['--search-text', keyword])
    return jsonify(result)


@app.route('/api/search_image', methods=['POST'])
def search_image():
    """图像哈希搜索"""
    data = request.json
    image_hash = data.get('image_hash', '').strip()

    if not image_hash:
        return jsonify({
            'success': False,
            'output': '请提供图像哈希值',
            'returncode': -1
        })

    print(f"API调用: /api/search_image, 哈希: {image_hash}")
    result = CommandExecutor.run_command(['--search-image', image_hash])
    return jsonify(result)


@app.route('/api/schedule', methods=['POST'])
def start_schedule():
    """启动定时爬取任务"""
    data = request.json
    interval = data.get('interval', 24)

    try:
        interval = int(interval)
        if interval < 1:
            interval = 24
    except:
        interval = 24

    print(f"API调用: /api/schedule, 间隔: {interval}小时")

    # 直接返回，不在后台运行定时任务
    result = CommandExecutor.run_command(['--schedule', '--interval', str(interval)])
    return jsonify(result)


@app.route('/api/get_db_stats', methods=['GET'])
def get_db_stats():
    """获取数据库统计信息"""
    print("API调用: /api/get_db_stats")
    try:
        from src.database.db_manager import DatabaseManager
        with DatabaseManager() as db:
            count = db.get_page_count()
            return jsonify({
                'success': True,
                'page_count': count,
                'output': f'数据库中有 {count} 条网页记录',
                'returncode': 0
            })
    except Exception as e:
        error_msg = f'获取数据库统计失败: {str(e)}\n{traceback.format_exc()}'
        print(error_msg)
        return jsonify({
            'success': False,
            'output': error_msg,
            'returncode': -1
        })


@app.route('/api/quick_test', methods=['POST'])
def quick_test():
    """快速测试所有功能"""
    print("API调用: /api/quick_test")
    tests = []

    # 1. 测试main.py是否存在
    main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
    if os.path.exists(main_py_path):
        tests.append(f"✓ main.py 文件存在: {main_py_path}")
    else:
        tests.append(f"✗ main.py 文件不存在: {main_py_path}")

    # 2. 测试数据库连接
    try:
        from src.database.db_manager import DatabaseManager
        with DatabaseManager() as db:
            count = db.get_page_count()
            tests.append(f"✓ 数据库连接成功，有 {count} 条记录")
    except Exception as e:
        tests.append(f"✗ 数据库连接失败: {str(e)}")

    # 3. 测试爬虫
    try:
        from src.crawler.webpage_crawler import WebPageCrawler
        crawler = WebPageCrawler()
        tests.append("✓ 爬虫模块加载成功")
    except Exception as e:
        tests.append(f"✗ 爬虫模块加载失败: {str(e)}")

    # 4. 测试搜索
    try:
        from src.search.text_search import TextSearch
        searcher = TextSearch()
        tests.append("✓ 搜索模块加载成功")
    except Exception as e:
        tests.append(f"✗ 搜索模块加载失败: {str(e)}")

    # 5. 测试配置文件
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
    if os.path.exists(config_path):
        tests.append(f"✓ 配置目录存在: {config_path}")
    else:
        tests.append(f"✗ 配置目录不存在: {config_path}")

    return jsonify({
        'success': True,
        'output': "快速测试结果:\n" + "\n".join(tests),
        'returncode': 0
    })


@app.route('/api/debug_info', methods=['GET'])
def debug_info():
    """调试信息"""
    info = []

    # 当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    info.append(f"当前目录: {current_dir}")

    # main.py路径
    main_py_path = os.path.join(current_dir, 'main.py')
    info.append(f"main.py路径: {main_py_path}")
    info.append(f"main.py是否存在: {os.path.exists(main_py_path)}")

    # 列出目录内容
    info.append("\n目录内容:")
    for item in os.listdir(current_dir):
        full_path = os.path.join(current_dir, item)
        if os.path.isdir(full_path):
            info.append(f"  目录: {item}/")
        else:
            info.append(f"  文件: {item}")

    return jsonify({
        'success': True,
        'output': '\n'.join(info),
        'returncode': 0
    })


@app.route('/api/execute_raw', methods=['POST'])
def execute_raw():
    """执行原始命令（调试用）"""
    data = request.json
    command = data.get('command', '')

    if not command:
        return jsonify({
            'success': False,
            'output': '请提供命令',
            'returncode': -1
        })

    print(f"执行原始命令: {command}")
    args = command.split()
    result = CommandExecutor.run_command(args)
    return jsonify(result)

@app.route('/api/batch_crawl', methods=['POST'])
def batch_crawl_pages():
    """批量爬取网页"""
    data = request.json
    urls_text = data.get('urls', '').strip()

    if not urls_text:
        return jsonify({
            'success': False,
            'output': '请提供URL列表',
            'returncode': -1
        })

    print("API调用: /api/batch_crawl")

    # 解析URL列表（支持逗号、换行、空格分隔）
    urls = []
    for line in urls_text.split('\n'):
        line = line.strip()
        if ',' in line:
            urls.extend([url.strip() for url in line.split(',') if url.strip()])
        else:
            if line:
                urls.append(line)

    # 去重
    urls = list(dict.fromkeys(urls))

    print(f"解析到 {len(urls)} 个URL: {urls}")

    results = []
    success_count = 0
    fail_count = 0

    for i, url in enumerate(urls, 1):
        try:
            if not url.startswith(('http://', 'https://')):
                results.append(f"[{i}/{len(urls)}] ✗ {url} - 无效URL（需要http://或https://开头）")
                fail_count += 1
                continue

            print(f"[{i}/{len(urls)}] 爬取: {url}")

            # 调用单个爬取命令
            cmd_result = CommandExecutor.run_command(['--crawl', url])

            if cmd_result['success']:
                results.append(f"[{i}/{len(urls)}] ✓ {url} - 爬取成功")
                success_count += 1
            else:
                results.append(f"[{i}/{len(urls)}] ✗ {url} - 爬取失败: {cmd_result['output'][:100]}...")
                fail_count += 1

            # 礼貌延迟
            import time
            time.sleep(1)

        except Exception as e:
            results.append(f"[{i}/{len(urls)}] ✗ {url} - 异常: {str(e)}")
            fail_count += 1

    summary = f"\n批量爬取完成！\n"
    summary += f"总URL数: {len(urls)}\n"
    summary += f"成功: {success_count}\n"
    summary += f"失败: {fail_count}\n"
    summary += f"成功率: {success_count / len(urls) * 100:.1f}%\n"

    return jsonify({
        'success': success_count > 0,
        'output': summary + '\n' + '\n'.join(results),
        'returncode': 0 if success_count > 0 else -1,
        'stats': {
            'total': len(urls),
            'success': success_count,
            'fail': fail_count
        }
    })

# 还可以添加一个从文件导入的API
@app.route('/api/import_urls', methods=['POST'])
def import_urls_from_file():
    """从上传的文件中导入URL"""
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'output': '没有上传文件',
            'returncode': -1
        })

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'success': False,
            'output': '没有选择文件',
            'returncode': -1
        })

    if file and file.filename.endswith('.txt'):
        try:
            content = file.read().decode('utf-8')
            urls = []
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)

            return jsonify({
                'success': True,
                'output': f"从文件导入 {len(urls)} 个URL",
                'urls': urls,
                'returncode': 0
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'output': f"读取文件失败: {str(e)}",
                'returncode': -1
            })
    else:
        return jsonify({
            'success': False,
            'output': '只支持.txt文件',
            'returncode': -1
        })


# 在 web_app.py 中添加以下路由

@app.route('/api/full_test', methods=['POST'])
def full_system_test():
    """运行完整的系统测试"""
    print("API调用: /api/full_test - 运行完整系统测试")

    try:
        # 直接运行 test_all.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_all_path = os.path.join(current_dir, 'test_all.py')

        if not os.path.exists(test_all_path):
            return jsonify({
                'success': False,
                'output': f"错误：找不到测试文件 {test_all_path}",
                'returncode': -1
            })

        # 导入 test_all 模块
        import importlib.util
        import sys

        spec = importlib.util.spec_from_file_location("test_all", test_all_path)
        test_all_module = importlib.util.module_from_spec(spec)
        sys.modules["test_all"] = test_all_module
        spec.loader.exec_module(test_all_module)

        # 捕获测试输出
        import io
        from contextlib import redirect_stdout, redirect_stderr

        output_buffer = io.StringIO()

        with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
            try:
                success = test_all_module.test_all()
            except Exception as e:
                output_buffer.write(f"\n测试执行异常: {str(e)}\n{traceback.format_exc()}")
                success = False

        output = output_buffer.getvalue()

        return jsonify({
            'success': success,
            'output': output,
            'returncode': 0 if success else 1
        })

    except Exception as e:
        error_msg = f"运行完整测试失败: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return jsonify({
            'success': False,
            'output': error_msg,
            'returncode': -1
        })

if __name__ == '__main__':
    print("=" * 60)
    print("网页综合取证系统 Web界面 - 修复版")
    print("=" * 60)
    print(f"当前工作目录: {os.getcwd()}")
    print(f"脚本所在目录: {os.path.dirname(os.path.abspath(__file__))}")

    # 检查main.py
    main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
    if os.path.exists(main_py_path):
        print(f"✓ 找到 main.py: {main_py_path}")
    else:
        print(f"✗ 未找到 main.py: {main_py_path}")
        print("请确保 web_app.py 和 main.py 在同一目录下")

    print("访问地址: http://127.0.0.1:5000")
    print("调试地址: http://127.0.0.1:5000/api/debug_info")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5000)