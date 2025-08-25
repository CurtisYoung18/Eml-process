#!/usr/bin/env python3
"""
GPTBots API 集成工具
用于批量调用API获取模切材料信息
"""

import requests
import json
import time
import pandas as pd
from typing import List, Dict, Optional
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gptbots_api.log'),
        logging.StreamHandler()
    ]
)

class GPTBotsAPI:
    def __init__(self, app_key: str, endpoint: str = "sg"):
        """
        初始化GPTBots API客户端
        
        Args:
            app_key: API应用密钥
            endpoint: 数据中心端点 (sg, th)
        """
        self.app_key = app_key
        # 根据文档设置正确的API地址
        if endpoint == "sg":
            self.base_url = "https://api-sg.gptbots.ai"
        elif endpoint == "th":
            self.base_url = "https://api-th.gptbots.ai"
        else:
            self.base_url = f"https://api-{endpoint}.gptbots.ai"
        
        # 根据官方文档设置正确的API endpoints
        self.create_conversation_url = f"{self.base_url}/v1/conversation"
        self.send_message_url = f"{self.base_url}/v2/conversation/message"
        self.session = requests.Session()
        
    def create_conversation(self, user_id: str = "api-user", timeout: int = 300) -> Optional[str]:
        """
        创建对话ID
        
        Args:
            user_id: 用户标识
            timeout: 超时时间（秒）
        
        Returns:
            conversation_id或None（如果失败）
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.app_key}"
        }
        
        payload = {
            "user_id": user_id
        }
        
        try:
            response = self.session.post(
                self.create_conversation_url,
                headers=headers,
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                conversation_id = result.get("conversation_id")
                logging.info(f"成功创建对话ID: {conversation_id}")
                return conversation_id
            else:
                logging.error(f"创建对话ID失败 - 状态码: {response.status_code}, 响应: {response.text}")
                return None
                
        except Exception as e:
            logging.error(f"创建对话ID出错: {str(e)}")
            return None

    def send_message(self, conversation_id: str, query: str, timeout: int = 600) -> Optional[Dict]:
        """
        发送消息到指定对话
        
        Args:
            conversation_id: 对话ID
            query: 查询内容
            timeout: 超时时间（秒）
        
        Returns:
            API响应内容或None（如果失败）
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.app_key}"
        }
        
        # 按照官方文档格式构建payload
        payload = {
            "conversation_id": conversation_id,
            "response_mode": "blocking",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": query
                        }
                    ]
                }
            ]
        }
        
        try:
            response = self.session.post(
                self.send_message_url,
                headers=headers,
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                logging.info(f"消息发送成功")
                return result
            else:
                logging.error(f"发送消息失败 - 状态码: {response.status_code}, 响应: {response.text}")
                return None
                
        except Exception as e:
            logging.error(f"发送消息出错: {str(e)}")
            return None

    def call_agent(self, query: str, timeout: int = 600) -> Optional[Dict]:
        """
        调用GPTBots Agent（完整流程：创建对话->发送消息）
        
        Args:
            query: 查询内容
            timeout: 超时时间（秒）
        
        Returns:
            API响应内容或None（如果失败）
        """
        logging.info(f"正在查询: {query}")
        
        # 步骤1: 创建对话ID
        conversation_id = self.create_conversation()
        if not conversation_id:
            logging.error("无法创建对话ID")
            return None
        
        # 步骤2: 发送消息
        result = self.send_message(conversation_id, query, timeout)
        if result:
            logging.info(f"查询成功: {query[:50]}...")
        else:
            logging.error(f"查询失败: {query}")
        
        return result

def generate_search_keywords() -> List[str]:
    """生成搜索关键词列表"""
    
    # 基础关键词
    base_materials = {
        "单面胶": [
            "single sided tape", "单面胶带", "单面粘合胶带",
            "PET单面胶", "PI单面胶", "聚酰亚胺单面胶", 
            "导热单面胶", "绝缘单面胶", "透明单面胶"
        ],
        "双面胶": [
            "double sided tape", "双面胶带", "双面粘合胶带",
            "VHB双面胶", "泡棉双面胶", "PET双面胶",
            "无基材双面胶", "导热双面胶", "结构胶双面胶"
        ],
        "保护膜": [
            "protective film", "保护膜", "防护膜",
            "PET保护膜", "PE保护膜", "PVC保护膜",
            "屏幕保护膜", "金属保护膜", "玻璃保护膜"
        ]
    }
    
    # 知名品牌
    brands = [
        "3M", "tesa", "日东电工", "NITTO", "德莎",
        "SEKISUI", "积水化学", "LINTEC", "琳得科",
        "金利宝", "荣合", "联茂", "深圳鑫佑兴"
    ]
    
    # 应用场景
    applications = [
        "模切加工", "电子制造", "汽车行业", "显示屏",
        "手机制造", "tablet制造", "LED封装"
    ]
    
    keywords = []
    
    # 组合搜索关键词
    for category, materials in base_materials.items():
        # 基础材料 + 品牌
        for material in materials[:3]:  # 限制数量避免过多
            for brand in brands[:8]:  # 每个材料类型配8个主要品牌
                keywords.append(f"{brand} {material}")
        
        # 材料 + 应用场景
        for material in materials[:2]:
            for app in applications[:3]:
                keywords.append(f"{material} {app}")
    
    # 特定型号搜索（基于常见型号模式）
    specific_models = [
        # 3M系列
        "3M 9495MP", "3M 7997MP", "3M 300LSE", "3M 4920", "3M 5112C",
        "3M VHB 4910", "3M 200MP", "3M 468MP", "3M 467MP", "3M 966",
        
        # tesa系列  
        "tesa 4970", "tesa 7920", "tesa 50602", "tesa 75730", "tesa 66514",
        "tesa 4965", "tesa 4972", "tesa 4952", "tesa 4941", "tesa 51970",
        
        # 日东电工系列
        "NITTO 5010P", "NITTO 5000NS", "NITTO 531", "NITTO 5015",
        
        # 其他常见型号
        "金利宝 TLT#2R", "金利宝 TLW50", "荣合 RH050-OPP"
    ]
    
    keywords.extend(specific_models)
    
    logging.info(f"生成了 {len(keywords)} 个搜索关键词")
    return keywords

def batch_query_materials(api_client: GPTBotsAPI, keywords: List[str], 
                         delay: float = 2.0, max_queries: int = 90) -> List[Dict]:
    """
    批量查询材料信息
    
    Args:
        api_client: GPTBots API客户端
        keywords: 搜索关键词列表
        delay: 请求间隔（秒）
        max_queries: 最大查询数量
    
    Returns:
        查询结果列表
    """
    results = []
    total_keywords = min(len(keywords), max_queries)
    
    logging.info(f"开始批量查询，总计 {total_keywords} 个关键词")
    
    for i, keyword in enumerate(keywords[:max_queries]):
        try:
            # 构造查询提示
            query = f"""请搜索 "{keyword}" 相关的模切材料信息，并按以下格式整理成表格：

| 品牌 | 供应商 | 材料型号 | 类型 | 颜色 | 基材 | 总厚度 | 胶水类型 | 对钢板粘性 | 对PC粘性 | 耐温性能 | 产地 | 单价 | 起订量 | 货期Leadtime | 厂商地址 | 厂商联系人 | Notes/备注 |

请重点关注：
1. 准确的技术参数（厚度、粘性、耐温等）
2. 供应商和联系方式信息
3. 价格和起订量信息
4. 如果找不到某些信息，请在对应栏位标注"未找到"或"-"

搜索关键词：{keyword}"""

            result = api_client.call_agent(query)
            
            if result:
                # 保存查询结果
                result_data = {
                    "keyword": keyword,
                    "timestamp": datetime.now().isoformat(),
                    "response": result,
                    "query_index": i + 1
                }
                results.append(result_data)
                
                logging.info(f"进度: {i+1}/{total_keywords} - 成功查询: {keyword}")
                
                # 保存中间结果（每10个查询保存一次）
                if (i + 1) % 10 == 0:
                    save_intermediate_results(results, f"intermediate_results_{i+1}.json")
                
            else:
                logging.warning(f"查询失败: {keyword}")
            
            # 请求间隔
            if i < total_keywords - 1:  # 最后一个请求不需要延迟
                time.sleep(delay)
                
        except KeyboardInterrupt:
            logging.info("用户中断查询")
            break
        except Exception as e:
            logging.error(f"查询出错 {keyword}: {str(e)}")
            continue
    
    logging.info(f"批量查询完成，成功获取 {len(results)} 个结果")
    return results

def save_intermediate_results(results: List[Dict], filename: str):
    """保存中间结果到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        logging.info(f"中间结果已保存到: {filename}")
    except Exception as e:
        logging.error(f"保存中间结果失败: {str(e)}")

def extract_response_content(results: List[Dict]) -> List[Dict]:
    """从API响应中提取内容"""
    extracted = []
    
    for result in results:
        try:
            # 根据GPTBots API官方文档响应格式提取内容
            response = result.get("response", {})
            
            # 从output字段提取内容（根据官方文档格式）
            content = ""
            if "output" in response:
                output_list = response.get("output", [])
                for output_item in output_list:
                    if "content" in output_item:
                        content_obj = output_item["content"]
                        if "text" in content_obj:
                            content += content_obj["text"] + "\n"
                        # 如果有其他类型的内容，也可以处理
            
            # 如果没有找到output，尝试其他可能的字段
            if not content:
                content = (response.get("answer") or 
                          response.get("content") or 
                          response.get("message") or
                          str(response))
            
            extracted_item = {
                "keyword": result["keyword"],
                "timestamp": result["timestamp"],
                "query_index": result["query_index"],
                "content": content.strip()
            }
            
            extracted.append(extracted_item)
            
        except Exception as e:
            logging.error(f"提取内容失败: {str(e)}")
            continue
    
    return extracted

def save_results_to_excel(results: List[Dict], filename: str = None):
    """保存结果到Excel文件"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"material_query_results_{timestamp}.xlsx"
    
    try:
        # 提取内容
        extracted_data = extract_response_content(results)
        
        # 创建DataFrame
        df = pd.DataFrame(extracted_data)
        
        # 保存到Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        
        logging.info(f"查询结果已保存到: {filename}")
        return filename
        
    except Exception as e:
        logging.error(f"保存Excel文件失败: {str(e)}")
        return None

def main():
    """主函数 - 演示用法"""
    # 初始化API客户端
    # api_key = 
    api_key = "app-6XWuLnzhiOgrrPJHZFj9D9Pq"
    client = GPTBotsAPI(api_key, endpoint="sg")
    
    # 生成搜索关键词
    keywords = generate_search_keywords()
    
    print(f"📝 生成了 {len(keywords)} 个搜索关键词")
    print(f"conversation_id: {client.create_conversation()}")
    print("🔍 前10个关键词预览:")
    for i, kw in enumerate(keywords[:10]):
        print(f"  {i+1}. {kw}")
    
    # 询问用户确认
    user_input = input(f"\n是否开始批量查询？(y/n): ")
    if user_input.lower() != 'y':
        print("操作已取消")
        return
    
    # 设置查询参数
    max_queries = int(input("请输入最大查询数量 (建议90个): ") or "90")
    delay = float(input("请输入请求间隔秒数 (建议2.0): ") or "2.0")
    
    print(f"\n🚀 开始批量查询...")
    print(f"📊 查询数量: {max_queries}")
    print(f"⏱️ 请求间隔: {delay}秒")
    print(f"⏳ 预计用时: {(max_queries * delay) / 60:.1f}分钟")
    
    # 执行批量查询
    results = batch_query_materials(client, keywords, delay, max_queries)
    
    if results:
        # 保存完整结果到JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"full_results_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 保存到Excel
        excel_filename = save_results_to_excel(results)
        
        print(f"\n✅ 批量查询完成!")
        print(f"📄 完整结果: {json_filename}")
        print(f"📊 Excel文件: {excel_filename}")
        print(f"📝 日志文件: gptbots_api.log")
        
        print(f"\n💡 下一步:")
        print(f"1. 检查生成的Excel文件")
        print(f"2. 使用 extract_table_data.py 工具提取结构化数据")
        print(f"3. 命令: ./run_extraction.sh {excel_filename}")
    else:
        print("❌ 没有获取到任何结果")

if __name__ == "__main__":
    main()
