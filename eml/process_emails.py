import email
import os
from email import policy
from email.parser import BytesParser
from pathlib import Path
import json
from datetime import datetime

def extract_email_content(eml_file):
    """
    从eml文件中提取邮件内容
    返回一个包含邮件主要信息的字典
    """
    with open(eml_file, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    # 提取基本信息
    content = {
        'subject': msg.get('subject', ''),
        'from': msg.get('from', ''),
        'to': msg.get('to', ''),
        'date': msg.get('date', ''),
        'body': '',
        'attachments': []
    }
    
    # 提取正文内容
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                # 获取文本内容
                try:
                    text = part.get_content()
                    content['body'] += text + "\n"
                except Exception as e:
                    print(f"Error extracting text content: {e}")
            elif part.get_content_type() == "text/html":
                # 如果没有纯文本内容，则使用HTML内容
                if not content['body']:
                    try:
                        text = part.get_content()
                        content['body'] += text + "\n"
                    except Exception as e:
                        print(f"Error extracting HTML content: {e}")
            # 记录附件信息
            if part.get_filename():
                content['attachments'].append(part.get_filename())
    else:
        # 非多部分邮件，直接获取内容
        content['body'] = msg.get_content()
    
    return content

def process_email_directory(directory_path):
    """
    处理指定目录下的所有eml文件
    将结果保存为JSON文件
    """
    directory = Path(directory_path)
    results = []
    
    # 处理所有eml文件
    for eml_file in sorted(directory.glob("*.eml")):
        try:
            print(f"Processing {eml_file.name}...")
            email_content = extract_email_content(eml_file)
            results.append({
                'filename': eml_file.name,
                'content': email_content
            })
        except Exception as e:
            print(f"Error processing {eml_file.name}: {e}")
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"email_contents_{timestamp}.json"
    output_path = Path("eml/output") / output_file

    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Results saved to {output_path}")
    return output_path

if __name__ == "__main__":
    # 设置要处理的邮件目录
    email_dir = Path("eml/防水透气膜")
    
    # 处理邮件并保存结果
    output_path = process_email_directory(email_dir)
    print("Email processing completed!")
