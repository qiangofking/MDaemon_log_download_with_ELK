import os
import time
from datetime import datetime
import sys

# 添加项目根目录到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BASE_DIR

def get_log_file_path():
    """获取当天日志文件路径"""
    today = datetime.now().strftime("%Y-%m-%d")
    log_dir = os.path.join(BASE_DIR, 'log')
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, f"task_{today}.log")

def log_result(operation, result):
    """记录任务执行结果"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {operation}: {result}\n"
    
    try:
        with open(get_log_file_path(), 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"日志记录失败: {str(e)}")
