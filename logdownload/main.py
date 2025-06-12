import util.file_unzip as file_unzip
import util.fileManager as fileManager
import util.file_2json as file_2json
import util.logger as logger
import time
import os
import sys
import threading

# 添加项目根目录到sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
# 导入config模块
from config import BASE_DIR


def get_temp():
    '''
    从服务器上下载“今天的”routing(加密)日志，并返回成功状态，遇到失败时重试3次
    ### 参数：
    - None
    ### 返回值：
    - temp_is_success: 下载是否成功
    - type: bool
'''
    temp_is_success = False
    myfileManager = fileManager.fileManager()
    temp_is_success = myfileManager.down4id()
    # 如果下载失败，重试3次
    if not temp_is_success:
        for i in range(3):
            time.sleep(0.5)
            temp_is_success = myfileManager.down4id()
            if temp_is_success:
                break
    return temp_is_success

def unzip_temp():
    '''
    获取并解压“今天的”缩临时文件，转化为json，并返回成功状态
    ### 参数：
    - None
    ### 返回值：
    - unzip_is_success: 解压缩是否成功
    - type: bool

'''
    unzip_is_success = False
    myfileManager = fileManager.fileManager()
    temp_file_path = os.path.join(BASE_DIR, 'temp', myfileManager.today_routing_filename)
    data_file_path = os.path.join(BASE_DIR, 'data', myfileManager.today_routing_filename)
    try:
        # 读取临时文件的内容
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            temp_file_text = f.read()
        # 解密临时文件内容
        data_file_text = file_unzip.unzip(temp_file_text)
        # 将解密后的内容转换为JSON格式
        data_file_json = file_2json.parse_log_to_json(data_file_text)
        # 将json写入数据文件
        with open(data_file_path, 'w', encoding='utf-8') as f:
            f.write(str(data_file_json))
        unzip_is_success = True
    except Exception as e:
        print(str(e))
    return unzip_is_success


# 全局变量存储定时器对象
active_timer = None

def schedule_tasks():
    """定时执行get_temp和unzip_temp函数"""
    global active_timer
    print("\n--- 开始执行定时任务 ---")
    
    # 执行并记录下载任务
    download_result = get_temp()
    print("下载结果:", download_result)
    logger.log_result("文件下载", download_result)
    
    # 执行并记录解压任务
    unzip_result = unzip_temp()
    print("解压结果:", unzip_result)
    logger.log_result("文件解压", unzip_result)
    
    print("--- 任务执行完成 ---\n")
    
    # 5分钟后再次执行
    active_timer = threading.Timer(300, schedule_tasks)
    active_timer.daemon = True  # 设置为守护线程
    active_timer.start()

if __name__ == '__main__':

    # 首次立即执行
    schedule_tasks()
    
    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止定时任务...")
        if active_timer:
            active_timer.cancel()  # 取消定时器
        print("定时任务已完全停止")
        sys.exit(0)  # 完全退出程序
