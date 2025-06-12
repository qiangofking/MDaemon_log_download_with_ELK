# util/fileManager.py
import base64
import requests
import configparser
import xml.etree.ElementTree as ET
import sys
import os
import time


# 添加项目根目录到sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)  # 使用insert(0)确保优先搜索项目根目录
# 导入config模块
from config import BASE_DIR

class fileManager:
    def __init__(self, config_file_path=os.path.join(BASE_DIR, 'config/config.ini')):
        self.config = configparser.ConfigParser() # 初始化配置解析器
        self.config.read(config_file_path)        # 读取配置文件
        self.filetransfer_list_xml = self.load_file('config/FileTransfer_List.xml') # 加载FileTransfer_List.xml接口文件
        self.today_routing_filename = self.get_today_routing_filename() # 获取今天的routing日志文件名
        self.filetransfer_download_xml = self.load_file('config/FileTransfer_Download.xml')
    
    def load_file(self, file_path):
        with open(file_path, 'r') as f:
            return f.read()
    
    def get_date(self): #获取形如“2025-06-05”的日期
        return time.strftime("%Y-%m-%d", time.localtime())
    
    def get_today_routing_filename(self): #获取今天的routing日志文件名
        date = self.get_date()
        return f"MDaemon-{date}-Routing.log"
    
    def name2id(self, filename=None): # 通过文件名获取文件ID
        if filename is None: # 如果没有指定文件名，则使用默认的routing日志文件名
            filename = self.today_routing_filename
        
        id = 'None ID'
        url = self.config['api_settings']['api_url']
        auth = self.config['api_settings']['auth_token']
        auth = base64.b64encode(auth.encode()).decode()
        data = self.filetransfer_list_xml
        headers = {
            'Content-Type': 'text/xml',
            'User-Agent': 'XmlApi',
            'Authorization': f'Basic {auth}'
        }
        try:
            res = requests.post(url, data=data, headers=headers)
            root = ET.fromstring(res.content)
            target_file = None  # 初始化目标文件为None
            for file in root.findall('.//File'):
                if file.get('name') == filename:
                    target_file = file
                    break
            id = target_file.get('id')
        except Exception as e:
            id = 'Error:getting the File ID,' + str(e)
        return id
    
    def down4id(self, id=None):
        if id is None:
            id = self.name2id() # 如果没有指定文件ID，则使用今天的routing日志文件ID
        
        is_success = False
        url = self.config['api_settings']['api_url']
        auth = self.config['api_settings']['auth_token']
        auth = base64.b64encode(auth.encode()).decode()
        data = self.filetransfer_download_xml.replace('{id}', id)
        headers = {
            'Content-Type': 'text/xml',
            'User-Agent': 'XmlApi',
            'Authorization': f'Basic {auth}'
        }
        try:
            res = requests.post(url, data=data, headers=headers)
            root = ET.fromstring(res.text)
            job_element = root.find('API/Response/Result/Job')

            with open(f'temp/{self.get_today_routing_filename()}', 'w', encoding='utf-8') as f:
                f.write(job_element.text)
            is_success = True
        except Exception as e:
            print(e)
            is_success = False
        return is_success
    
if __name__ == "__main__":
    fm = fileManager()

    myid = fm.name2id()
    
    print(myid)

    print(fm.down4id(myid))
    


    