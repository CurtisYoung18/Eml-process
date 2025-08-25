# 材料信息处理工具集

这是一个用于批量查询和处理材料信息的工具集，主要包含两个核心功能：
1. 批量查询材料信息（通过GPTBots API）
2. 从Excel文件中提取结构化的材料信息表格数据

## 项目结构

```
LovePacTest/
├── data/                    # 数据文件目录
│   ├── input/              # 输入文件
│   ├── output/             # 输出文件
│   └── samples/            # 示例文件
├── scripts/                # 主要脚本文件
│   ├── batch_material_query.py    # 批量查询脚本
│   ├── extract_table_data.py      # 数据提取脚本
│   ├── config.py                  # 配置文件
│   ├── gptbots_api.py            # API客户端
│   └── run_extraction.sh         # 快速启动脚本
└── logs/                   # 日志文件目录
```

## 使用流程

### 1. 环境准备

```bash
# 克隆项目后，进入项目目录
cd LovePacTest/scripts

# 运行快速启动脚本，它会自动创建虚拟环境并安装依赖
./run_extraction.sh
```

### 2. 批量查询材料信息

```bash
# 进入scripts目录
cd scripts

# 激活虚拟环境
source venv/bin/activate

# 运行批量查询脚本
python batch_material_query.py
```

批量查询脚本会：
1. 自动生成优化的搜索关键词
2. 通过GPTBots API批量查询材料信息
3. 保存查询结果到JSON和Excel文件
4. 可选择立即进行数据提取

### 3. 提取表格数据

```bash
# 方式1：使用快速启动脚本
./run_extraction.sh 输入文件.xlsx [输出文件.xlsx]

# 方式2：直接运行Python脚本
python extract_table_data.py 输入文件.xlsx [输出文件.xlsx]
```

### 4. 输出文件说明

所有输出文件都会保存在 `data/output/` 目录下：
- `material_query_results_时间戳.json`: 完整的查询结果（JSON格式）
- `material_data_时间戳.xlsx`: 原始查询结果（Excel格式）
- `material_data_时间戳_材料信息表.xlsx`: 提取后的结构化数据（Excel格式）

### 5. 注意事项

1. 确保config.py中配置了正确的API密钥和端点
2. 批量查询时可以选择测试模式（仅查询前5个关键词）
3. 数据提取工具支持两种表格格式：
   - Markdown格式表格
   - 制表符分隔的表格
4. 所有日志文件保存在logs目录下

## 维护说明

1. 虚拟环境和依赖包会保持完整，方便后续类似的表格处理任务
2. 输出文件使用时间戳命名，避免覆盖之前的结果
3. 可以根据需要调整config.py中的配置参数
