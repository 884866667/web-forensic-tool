# 保存为 clean_all_null.py，放在项目根目录
import os

def remove_null_bytes(file_path):
    """移除单个文件中的空字节"""
    try:
        # 二进制模式读取
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # 检查是否包含空字节
        if b'\x00' not in content:
            print(f"✅ {file_path} - 无空字节，无需清理")
            return
        
        # 移除空字节
        cleaned_content = content.replace(b'\x00', b'')
        
        # 写回文件
        with open(file_path, 'wb') as f:
            f.write(cleaned_content)
        
        print(f"✅ {file_path} - 已清理空字节")
    
    except Exception as e:
        print(f"❌ {file_path} - 清理失败: {e}")

# 遍历项目中所有 .py 文件
print("开始批量清理所有 .py 文件中的空字节...\n")
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            remove_null_bytes(file_path)

print("\n📌 批量清理完成！现在重新测试数据库连接")