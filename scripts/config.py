#!/usr/bin/env python3
"""
配置文件 - 用于设置API参数和搜索策略
"""

# GPTBots API 配置
GPTBOTS_CONFIG = {
    "api_key": "app-6XWuLnzhiOgrrPJHZFj9D9Pq",
    "endpoint": "sg",  # Singapore数据中心
    "timeout": 60,     # API请求超时时间（秒）
    "delay": 0.5,      # 请求间隔时间（秒）- 移除限制，加快速度
}

# 搜索策略配置
SEARCH_CONFIG = {
    "max_queries_per_run": 90,    # 每次运行的最大查询数量
    "target_per_category": 30,    # 每个类别目标获取数量
    "save_interval": 10,          # 每N个查询保存一次中间结果
}

# 材料类别和关键词
MATERIAL_CATEGORIES = {
    "单面胶": {
        "keywords": [
            "single sided tape", "单面胶带", "单面粘合胶带",
            "PET单面胶", "PI单面胶", "聚酰亚胺单面胶", 
            "导热单面胶", "绝缘单面胶", "透明单面胶",
            "遮光单面胶", "防静电单面胶"
        ],
        "target_count": 30
    },
    "双面胶": {
        "keywords": [
            "double sided tape", "双面胶带", "双面粘合胶带",
            "VHB双面胶", "泡棉双面胶", "PET双面胶",
            "无基材双面胶", "导热双面胶", "结构胶双面胶",
            "丙烯酸双面胶", "硅胶双面胶"
        ],
        "target_count": 30
    },
    "保护膜": {
        "keywords": [
            "protective film", "保护膜", "防护膜",
            "PET保护膜", "PE保护膜", "PVC保护膜",
            "屏幕保护膜", "金属保护膜", "玻璃保护膜",
            "防刮保护膜", "抗指纹保护膜"
        ],
        "target_count": 30
    }
}

# 知名品牌列表
MAJOR_BRANDS = [
    "3M", "tesa", "日东电工", "NITTO", "德莎",
    "SEKISUI", "积水化学", "LINTEC", "琳得科",
    "金利宝", "荣合", "联茂", "深圳鑫佑兴", "捷顺通"
]

# 常见型号（基于已知的成功案例）
COMMON_MODELS = {
    "3M": [
        "9495MP", "7997MP", "300LSE", "4920", "5112C",
        "VHB 4910", "200MP", "468MP", "467MP", "966"
    ],
    "tesa": [
        "4970", "7920", "50602", "75730", "66514",
        "4965", "4972", "4952", "4941", "51970"
    ],
    "NITTO": [
        "5010P", "5000NS", "531", "5015"
    ],
    "金利宝": [
        "TLT#2R", "TLW50", "SDTS-C12"
    ]
}

# 应用场景
APPLICATIONS = [
    "模切加工", "电子制造", "汽车行业", "显示屏",
    "手机制造", "平板制造", "LED封装", "PCB制造"
]

# 查询模板
QUERY_TEMPLATE = """请搜索 "{keyword}" 相关的模切材料信息，并按以下格式整理成表格：

| 品牌 | 供应商 | 材料型号 | 类型 | 颜色 | 基材 | 总厚度 | 胶水类型 | 对钢板粘性 | 对PC粘性 | 耐温性能 | 产地 | 单价 | 起订量 | 货期Leadtime | 厂商地址 | 厂商联系人 | Notes/备注 |

请重点关注：
1. 准确的技术参数（厚度、粘性、耐温等）
2. 供应商和联系方式信息
3. 价格和起订量信息
4. 如果找不到某些信息，请在对应栏位标注"未找到"或"-"

搜索关键词：{keyword}"""

# 输出文件设置
OUTPUT_SETTINGS = {
    "json_prefix": "material_query_results",
    "excel_prefix": "material_data",
    "log_file": "gptbots_api.log",
    "intermediate_prefix": "intermediate_results"
}
