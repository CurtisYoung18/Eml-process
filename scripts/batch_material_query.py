#!/usr/bin/env python3
"""
批量材料信息查询工具
整合GPTBots API和数据提取工具的完整工作流程
"""

import sys
import os
from datetime import datetime
import json
# 添加当前目录到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import *
from gptbots_api import GPTBotsAPI, batch_query_materials, save_results_to_excel
import subprocess

def generate_optimized_keywords(max_total: int = 90) -> list:
    """
    生成优化的搜索关键词列表
    确保三个类别均匀分布
    """
    keywords = []
    per_category = max_total // 3  # 每个类别的关键词数量
    
    for category, config in MATERIAL_CATEGORIES.items():
        category_keywords = []
        
        # 1. 基础关键词 + 主要品牌组合
        base_keywords = config["keywords"][:6]  # 取前6个基础关键词
        top_brands = MAJOR_BRANDS[:5]  # 取前5个主要品牌
        
        for keyword in base_keywords:
            for brand in top_brands:
                category_keywords.append(f"{brand} {keyword}")
                if len(category_keywords) >= per_category // 2:
                    break
            if len(category_keywords) >= per_category // 2:
                break
        
        # 2. 具体型号搜索
        if category == "单面胶":
            specific_models = [
                "3M 7997MP", "tesa 7920", "NITTO 5010P",
                "金利宝 TLT#2R", "荣合 RH-PET-01"
            ]
        elif category == "双面胶":
            specific_models = [
                "3M 9495MP", "3M 300LSE", "tesa 4970", "tesa 50602",
                "金利宝 TLW50", "深圳鑫佑兴 TLT#3R"
            ]
        else:  # 保护膜
            specific_models = [
                "3M 5112C", "tesa 75730", "荣合 RH050-OPP",
                "NITTO 5000NS", "联茂 ls...pet_1"
            ]
        
        category_keywords.extend(specific_models[:per_category//2])
        
        # 确保每个类别的关键词数量
        category_keywords = category_keywords[:per_category]
        keywords.extend(category_keywords)
        
        print(f"📋 {category}: 生成 {len(category_keywords)} 个关键词")
    
    return keywords

def main():
    """主执行函数"""
    print("🔧 批量材料信息查询工具")
    print("=" * 50)
    
    # 显示配置信息
    print(f"🔑 API Key: {GPTBOTS_CONFIG['api_key']}")
    print(f"🌏 数据中心: {GPTBOTS_CONFIG['endpoint']}")
    print(f"🎯 目标: 每个类别获取 {SEARCH_CONFIG['target_per_category']} 个材料信息")
    print(f"⏱️ 请求间隔: {GPTBOTS_CONFIG['delay']} 秒")
    
    # 生成关键词
    keywords = generate_optimized_keywords(SEARCH_CONFIG['max_queries_per_run'])
    print(f"\n📝 总共生成 {len(keywords)} 个搜索关键词")
    
    # 显示关键词预览
    print("\n🔍 关键词预览 (前15个):")
    for i, kw in enumerate(keywords[:15]):
        print(f"  {i+1:2d}. {kw}")
    if len(keywords) > 15:
        print(f"  ... 还有 {len(keywords)-15} 个关键词")
    
    # 用户确认
    print(f"\n预计查询时间: {(len(keywords) * GPTBOTS_CONFIG['delay']) / 60:.1f} 分钟")
    
    while True:
        choice = input(f"\n请选择操作:\n1. 开始完整批量查询 ({len(keywords)}个)\n2. 测试模式 (仅前5个)\n3. 自定义数量\n4. 退出\n请选择 (1-4): ").strip()
        
        if choice == '1':
            max_queries = len(keywords)
            break
        elif choice == '2':
            max_queries = 5
            keywords = keywords[:5]
            print("🧪 测试模式：仅查询前5个关键词")
            break
        elif choice == '3':
            try:
                max_queries = int(input("请输入查询数量: "))
                keywords = keywords[:max_queries]
                break
            except ValueError:
                print("❌ 请输入有效数字")
                continue
        elif choice == '4':
            print("👋 操作已取消")
            return
        else:
            print("❌ 无效选择，请重新输入")
    
    # 创建API客户端
    print(f"\n🚀 初始化API客户端...")
    api_client = GPTBotsAPI(
        app_key=GPTBOTS_CONFIG['api_key'],
        endpoint=GPTBOTS_CONFIG['endpoint']
    )
    
    # 开始批量查询
    print(f"🔄 开始批量查询 {max_queries} 个关键词...")
    results = batch_query_materials(
        api_client=api_client,
        keywords=keywords,
        delay=GPTBOTS_CONFIG['delay'],
        max_queries=max_queries
    )
    
    if not results:
        print("❌ 没有获取到任何结果")
        return
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存JSON格式（完整数据）
    json_filename = f"{OUTPUT_SETTINGS['json_prefix']}_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 保存Excel格式（用于数据提取）
    excel_filename = save_results_to_excel(results, f"{OUTPUT_SETTINGS['excel_prefix']}_{timestamp}.xlsx")
    
    print(f"\n✅ 批量查询完成!")
    print(f"📊 成功获取: {len(results)} 个查询结果")
    print(f"📄 JSON文件: {json_filename}")
    print(f"📊 Excel文件: {excel_filename}")
    
    # 询问是否立即进行数据提取
    if excel_filename:
        extract_choice = input(f"\n🔧 是否立即使用数据提取工具处理结果? (y/n): ").strip().lower()
        if extract_choice == 'y':
            print(f"🔄 正在运行数据提取工具...")
            try:
                # 激活虚拟环境并运行提取脚本
                result = subprocess.run([
                    'bash', '-c', 
                    f'source venv/bin/activate && python extract_table_data.py "{excel_filename}"'
                ], capture_output=True, text=True, cwd=os.getcwd())
                
                if result.returncode == 0:
                    print("✅ 数据提取完成!")
                    print(result.stdout)
                else:
                    print("❌ 数据提取失败:")
                    print(result.stderr)
                    
            except Exception as e:
                print(f"❌ 运行数据提取工具失败: {str(e)}")
                print(f"💡 请手动运行: ./run_extraction.sh \"{excel_filename}\"")
    
    # 显示总结
    print(f"\n📋 处理总结:")
    print(f"   🔍 查询关键词: {max_queries} 个")
    print(f"   ✅ 成功获取: {len(results)} 个结果")
    print(f"   💾 保存文件: {json_filename}")
    print(f"   📊 Excel文件: {excel_filename}")
    print(f"   📝 日志文件: {OUTPUT_SETTINGS['log_file']}")
    
    print(f"\n💡 后续步骤:")
    print(f"   1. 检查Excel文件内容质量")
    print(f"   2. 如需要，运行数据提取: ./run_extraction.sh \"{excel_filename}\"")
    print(f"   3. 合并多次查询结果")
    print(f"   4. 进行数据清洗和去重")

if __name__ == "__main__":
    main()
