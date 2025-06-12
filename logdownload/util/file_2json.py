import re
import json
from datetime import datetime

def extract_email_and_name(field_value):
    """从 from 字段提取邮箱地址和名称提示"""
    # 更全面的邮箱地址正则表达式
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    
    # 查找邮箱地址
    email_match = re.search(email_pattern, field_value)
    email_addr = email_match.group(0) if email_match else None
    
    # 提取名称提示
    tips = field_value
    if email_addr:
        # 移除邮箱地址部分
        tips = re.sub(re.escape(email_addr), '', tips)
        # 清理多余字符
        tips = re.sub(r'^[\s"<]+|[\s">]+$', '', tips)
    
    return {
        "from": field_value,  # 保留原始 from 字段
        "from_addr": email_addr,
        "from_tips": tips if tips else None
    }

def extract_to_emails(field_value):
    """从 to 字段提取有效的邮箱地址"""
    # 更全面的邮箱地址正则表达式
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    
    # 查找所有邮箱地址
    emails = re.findall(email_pattern, field_value)
    
    # 去重并返回
    return list(set(emails)) if emails else []

def extract_to_addr(file_path):
    """根据文件路径提取 to_addr 值"""
    # 处理不同格式的路径分隔符
    normalized_path = file_path.replace('\\', '/').lower()
    
    # 查找特定目录
    match = re.search(r'bbb\.com/([^/]+)/', normalized_path)
    if match:
        return match.group(1)  # 返回匹配的目录名
    
    # 对于其他路径，尝试提取倒数第二级目录
    parts = [p for p in normalized_path.split('/') if p]
    if len(parts) >= 2:
        return parts[-2]  # 返回倒数第二级目录
    
    return None

def parse_log_to_json(log_text):
    # 定义正则表达式模式
    event_pattern = re.compile(
        r'^(?P<weekday>\w{3}) (?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2})\.\d{3}: '
        r'\d+: (?P<description>.*)$'
    )
    
    field_pattern = re.compile(
        r'^\w{3} \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}: \d+: \*  '
        r'(?P<key>[^:]+): (?P<value>.*)$'
    )
    
    # 按分隔符分割日志块
    blocks = re.split(r'-{10,}', log_text)
    results = []
    
    for block in blocks:
        if not block.strip():
            continue
            
        event = {}
        lines = block.strip().split('\n')
        
        # 处理第一行（事件行）
        first_line = lines[0].strip()
        first_match = event_pattern.match(first_line)
        
        if first_match:
            event_data = first_match.groupdict()
            # 组合并格式化时间戳
            raw_timestamp = f"{event_data['date']} {event_data['time']}"
            try:
                # 解析时间并重新格式化
                dt = datetime.strptime(raw_timestamp, '%Y-%m-%d %H:%M:%S')
                event["event_timestamp"] = dt.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                event["event_timestamp"] = raw_timestamp
        else:
            # 如果不是标准格式，跳过此块
            continue
            
        # 处理字段行
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
                
            field_match = field_pattern.match(line)
            if field_match:
                key = field_match.group('key').strip().lower().replace(' ', '_')
                value = field_match.group('value').strip()
                
                # 特殊处理 Size 字段
                if key == 'size':
                    # 分离大小和文件路径
                    size_parts = value.split(';')
                    if len(size_parts) > 1:
                        try:
                            event['size'] = int(size_parts[0].strip())
                        except ValueError:
                            event['size'] = size_parts[0].strip()
                        
                        # 提取文件路径（去除尖括号）
                        path_match = re.search(r'<([^>]+)>', size_parts[1])
                        if path_match:
                            file_path = path_match.group(1)
                            event['file_path'] = file_path
                            
                            # 提取 to_addr 字段
                            event['to_addr'] = extract_to_addr(file_path)
                    else:
                        event['size'] = value
                # 处理 From 字段
                elif key == 'from':
                    # 提取邮箱地址和提示信息
                    from_data = extract_email_and_name(value)
                    event.update(from_data)
                # 处理 To 字段
                elif key == 'to':
                    # 提取有效的邮箱地址
                    emails = extract_to_emails(value)
                    if emails:  # 只添加非空列表
                        event[key] = emails
                # 处理其他字段
                else:
                    event[key] = value
        
        # 添加到结果列表
        results.append(event)
    
    # 转换为 JSON 格式（每行一个 JSON 对象）
    json_lines = [json.dumps(item, ensure_ascii=False) for item in results]
    return '\n'.join(json_lines)

# 示例使用
if __name__ == "__main__":
    log_data = r"""


START Event Log / MDaemon PRO v25.0.2, Routing log information

-------------------------------------------------------------------------------

Event Time/Date             Event Description

-------------------------------------------------------------------------------

Sat 2025-06-07 00:00:12.401: 17: INBOUND message: pdd666.msg

Sat 2025-06-07 00:00:12.401: 17: *  From: AAA@BBB.com

Sat 2025-06-07 00:00:12.401: 17: *  To: AAA@BBB.com

Sat 2025-06-07 00:00:12.401: 17: *  Subject: asdasd

Sat 2025-06-07 00:00:12.401: 17: *  Message-ID: <123>

Sat 2025-06-07 00:00:12.401: 17: *  Size: 123123; <z:\mdaemon\queues\local\pd666.msg>

Sat 2025-06-07 00:00:12.401: 17: ----------

Sat 2025-06-07 00:01:31.063: 12: INBOUND message: pdd667.msg

Sat 2025-06-07 00:01:31.063: 12: *  From: nidedie <nidedie@CCC.com>

Sat 2025-06-07 00:01:31.063: 12: *  To: snidedie@CCC.com

Sat 2025-06-07 00:01:31.063: 12: *  Subject: need for help

Sat 2025-06-07 00:01:31.063: 12: *  Size: 123321; <x:\users\bbb.com\nidedie\md666.msg>
"""

    json_output = parse_log_to_json(log_data)
    
    # 打印格式化后的JSON结果
    for line in json_output.splitlines():
        parsed = json.loads(line)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))