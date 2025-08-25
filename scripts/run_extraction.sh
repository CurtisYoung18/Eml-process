#!/bin/bash

# 材料信息表格数据提取工具 - 快速启动脚本

echo "🔧 材料信息表格数据提取工具"
echo "=================================="

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，正在创建..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 安装依赖包..."
    pip install pandas openpyxl
    echo "✅ 环境设置完成"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
source venv/bin/activate

# 检查参数
if [ $# -eq 0 ]; then
    echo ""
    echo "📖 使用方法:"
    echo "  ./run_extraction.sh <输入Excel文件> [输出Excel文件]"
    echo ""
    echo "📝 示例:"
    echo "  ./run_extraction.sh LuoPai_test2_16.xlsx"
    echo "  ./run_extraction.sh LuoPai_test2_16.xlsx 新材料表.xlsx"
    echo ""
    
    # 显示当前目录的Excel文件
    echo "📁 当前目录的Excel文件:"
    ls -1 *.xlsx 2>/dev/null || echo "  (未找到Excel文件)"
    
    exit 1
fi

# 运行数据提取脚本
echo "🚀 开始处理..."
cd "$(dirname "$0")"
python extract_table_data.py "$@"

echo ""
echo "🎉 处理完成！"
