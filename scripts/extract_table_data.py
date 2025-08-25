#!/usr/bin/env python3
"""
材料信息表格数据提取工具
用于从Excel文件的agent_output列中提取结构化表格数据
"""

import pandas as pd
import re
import sys
import os
from typing import Optional, List

def parse_markdown_table(text: str) -> Optional[List[List[str]]]:
    """解析markdown格式的表格"""
    lines = text.strip().split('\n')
    data_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('|') and line.endswith('|') and not '---' in line:
            # 去除首尾的|，然后按|分割
            cells = [cell.strip() for cell in line[1:-1].split('|')]
            # 过滤掉表头行（第一列是"品牌"）和空行
            if len(cells) == 18 and cells[0] != '品牌' and cells[0].strip() != '':
                data_lines.append(cells)
    
    return data_lines if data_lines else None

def parse_tab_separated_table(text: str) -> Optional[List[List[str]]]:
    """解析制表符分隔的表格"""
    lines = text.strip().split('\n')
    data_lines = []
    
    # 寻找数据行（不是表头）
    for line in lines:
        if '\t' in line:
            cells = line.split('\t')
            # 检查是否是数据行（第一个cell不是"品牌"）
            if len(cells) >= 3 and cells[0] != '品牌' and cells[0].strip() != '':
                # 补齐到18列
                while len(cells) < 18:
                    cells.append('')
                data_lines.append(cells[:18])  # 只取前18列
    
    return data_lines if data_lines else None

def extract_table_data(input_file: str, output_file: str = None) -> str:
    """
    从Excel文件提取表格数据
    
    Args:
        input_file: 输入Excel文件路径
        output_file: 输出Excel文件路径，如果为None则自动生成
    
    Returns:
        输出文件路径
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"输入文件不存在: {input_file}")
    
    # 读取原始Excel文件
    print(f"正在读取文件: {input_file}")
    df = pd.read_excel(input_file)
    
    # 检查是否有数据列（支持agent_output或content列）
    if 'agent_output' in df.columns:
        data_column = 'agent_output'
    elif 'content' in df.columns:
        data_column = 'content'
    else:
        raise ValueError("Excel文件中未找到'agent_output'或'content'列")
    
    # 定义列名
    columns = ['品牌', '供应商', '材料型号', '类型', '颜色', '基材', '总厚度', '胶水类型', 
               '对钢板粘性', '对PC粘性', '耐温性能', '产地', '单价', '起订量', 
               '货期Leadtime', '厂商地址', '厂商联系人', 'Notes/备注']
    
    extracted_data = []
    
    print(f"开始处理 {len(df)} 行数据...")
    
    for index, row in df.iterrows():
        data_content = str(row[data_column])
        
        if pd.isna(data_content) or data_content.strip() == '' or data_content == 'nan':
            continue
            
        print(f"处理第 {index + 1} 行...")
        
        # 尝试解析markdown格式表格
        parsed_data = parse_markdown_table(data_content)
        
        # 如果markdown解析失败，尝试制表符分隔格式
        if not parsed_data:
            parsed_data = parse_tab_separated_table(data_content)
        
        if parsed_data:
            # 现在parsed_data是多行数据的列表
            for row_data in parsed_data:
                extracted_data.append(row_data)
                print(f"  ✓ 成功提取: 品牌={row_data[0]}, 材料型号={row_data[2]}")
        else:
            print(f"  ✗ 未能解析数据")
    
    # 创建新的DataFrame
    result_df = pd.DataFrame(extracted_data, columns=columns)
    
    # 生成输出文件名
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_材料信息表.xlsx"
    
    # 保存到新的Excel文件
    result_df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"\n✅ 提取完成!")
    print(f"📊 共提取 {len(extracted_data)} 行有效数据")
    print(f"💾 结果保存到: {output_file}")
    
    # 显示前几行结果预览
    if len(result_df) > 0:
        print(f"\n📝 数据预览 (前3行):")
        print("-" * 80)
        display_df = result_df.head(3)
        for i, row in display_df.iterrows():
            print(f"第{i+1}行: {row['品牌']} | {row['材料型号']} | {row['类型']}")
    
    return output_file

def main():
    """命令行入口函数"""
    if len(sys.argv) < 2:
        print("用法: python extract_table_data.py <输入Excel文件> [输出Excel文件]")
        print("示例: python extract_table_data.py LuoPai_test2_16.xlsx")
        print("示例: python extract_table_data.py LuoPai_test2_16.xlsx 新材料表.xlsx")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        result_file = extract_table_data(input_file, output_file)
        print(f"\n🎉 处理完成! 结果文件: {result_file}")
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
