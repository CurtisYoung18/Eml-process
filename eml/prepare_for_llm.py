import json
from datetime import datetime
import os
from pathlib import Path
import re

def clean_email_content(content):
    """
    清理邮件内容，去除不必要的信息
    """
    # 移除邮件签名和免责声明
    patterns = [
        r"~ ~ ~  Best Regards！~ ~ ~.*?~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~",
        r"This message and any attachment is confidential.*?email\.",
        r"For information about our privacy practices.*?cooperation\.",
        r"Warning: This email originated from outside.*?safe!",
        r"Some people who received this message.*?important",
        r"CAUTION: This email originated.*?safe\."
    ]
    
    text = content
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.DOTALL)
    
    # 移除多余的空行
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def format_email_thread(emails):
    """
    将邮件按时间顺序组织成对话格式
    """
    # 解析日期并排序
    for email in emails:
        try:
            date_str = email['content']['date']
            # 处理不同的日期格式
            try:
                date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
            email['date'] = date
        except Exception as e:
            print(f"Error parsing date for email: {e}")
            email['date'] = datetime.min
    
    # 按时间排序
    sorted_emails = sorted(emails, key=lambda x: x['date'])
    
    # 格式化对话
    conversation = []
    for email in sorted_emails:
        content = email['content']
        clean_body = clean_email_content(content['body'])
        
        # 格式化邮件信息
        email_info = {
            'timestamp': email['date'].strftime("%Y-%m-%d %H:%M:%S"),
            'from': content['from'],
            'to': content['to'],
            'subject': content['subject'],
            'body': clean_body,
            'attachments': content['attachments'] if content['attachments'] else []
        }
        conversation.append(email_info)
    
    return conversation

def prepare_for_llm(json_file):
    """
    读取JSON文件并准备LLM格式
    """
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        emails = json.load(f)
    
    # 组织邮件对话
    conversation = format_email_thread(emails)
    
    # 生成LLM友好的格式
    llm_format = {
        'topic': conversation[0]['subject'],  # 使用第一封邮件的主题作为话题
        'participants': list(set([
            email['from'].split('<')[0].strip()
            for email in conversation
        ])),
        'conversation': conversation,
        'summary': {
            'total_emails': len(conversation),
            'date_range': {
                'start': conversation[0]['timestamp'],
                'end': conversation[-1]['timestamp']
            }
        }
    }
    
    # 保存结果
    output_dir = Path("eml/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"llm_ready_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(llm_format, f, ensure_ascii=False, indent=2)
    
    print(f"Prepared data saved to {output_file}")
    return output_file

if __name__ == "__main__":
    # 查找最新的邮件内容JSON文件
    output_dir = Path("data/output")
    json_files = list(output_dir.glob("email_contents_*.json"))
    if not json_files:
        print("No email content JSON files found!")
        exit(1)
    
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    print(f"Processing {latest_file}...")
    
    # 处理数据
    output_file = prepare_for_llm(latest_file)
    print("Processing completed!")
