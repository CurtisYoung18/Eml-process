#!/usr/bin/env python3
"""
邮件知识库处理系统 - 主应用
基于Streamlit构建的本地部署应用
"""

import streamlit as st
import os
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
from email_cleaner import EmailCleaner
from streamlit_option_menu import option_menu
from dotenv import load_dotenv

# 加载.env环境变量
load_dotenv()

# 设置页面配置
st.set_page_config(
    page_title="邮件知识库处理系统",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用配置
CONFIG = {
    "app_title": "📧 邮件知识库处理系统",
    "version": "v1.0.0",
    "upload_dir": "eml_process/uploads",
    "output_dir": "eml_process/output", 
    "processed_dir": "eml_process/processed",
    "final_dir": "eml_process/final_output"
}

def init_directories():
    """初始化必要的目录结构"""
    for dir_name in [CONFIG["upload_dir"], CONFIG["output_dir"], 
                     CONFIG["processed_dir"], CONFIG["final_dir"]]:
        Path(dir_name).mkdir(exist_ok=True)

def main():
    """主应用函数"""
    init_directories()
    
    # 主标题
    st.title(CONFIG["app_title"])
    st.markdown(f"*{CONFIG['version']}*")
    
    # 初始化session state
    if 'current_step' not in st.session_state:
        st.session_state.current_step = "首页概览"
    
    # 侧边栏导航
    with st.sidebar:
        st.header("📋 功能导航")
        
        # 导航选项
        nav_options = [
            "首页概览",
            "邮件上传", 
            "数据清洗",
            "LLM处理",
            "结果查看",
            "知识库管理（预留）",
            "问答系统（预留）"
        ]
        
        selected_step = option_menu(
            None,
            nav_options,
            icons=["house", "cloud-upload", "tools", "robot", "bar-chart", "book", "chat-dots"],
            menu_icon="cast",
            default_index=nav_options.index(st.session_state.current_step) if 'current_step' in st.session_state and st.session_state.current_step in nav_options else 0,
            orientation="vertical",
            styles={
                "container": {"padding": "5px", "background-color": "#fafafa"},
                "icon": {"color": "#fa8800", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#02ab21", "color": "white"},
            }
        )
        
        # 更新session state
        if selected_step != st.session_state.current_step:
            st.session_state.current_step = selected_step
            st.rerun()
        
        current_step = st.session_state.current_step
        
        st.markdown("---")
        st.markdown("### 📈 处理状态")
        
        # 显示各步骤状态
        status_data = get_processing_status()
        for step, status in status_data.items():
            if status == "completed":
                st.success(f"✅ {step}")
            elif status == "processing":
                st.warning(f"⏳ {step}")
            else:
                st.info(f"⏸️ {step}")
    
    # 主内容区域
    if current_step == "首页概览":
        show_homepage()
    elif current_step == "邮件上传":
        show_upload_page()
    elif current_step == "数据清洗":
        show_cleaning_page()
    elif current_step == "LLM处理":
        show_llm_processing_page()
    elif current_step == "结果查看":
        show_results_page()
    elif "预留" in current_step:
        show_future_features_page(current_step)

def get_processing_status():
    """获取各步骤的处理状态"""
    status = {}
    
    # 检查邮件上传状态
    upload_files = count_files(CONFIG["upload_dir"], "*.eml")
    eml_demo_files = count_files("Eml", "*.eml")
    
    if upload_files > 0:
        status["邮件上传"] = "completed"
    elif eml_demo_files > 0:
        status["邮件上传"] = "completed"  # 有示例文件可用
    else:
        status["邮件上传"] = "pending"
    
    # 检查数据清洗状态
    processed_files = count_files(CONFIG["processed_dir"], "*.md")
    if processed_files > 0:
        status["数据清洗"] = "completed"
    else:
        status["数据清洗"] = "pending"
    
    # 检查LLM处理状态
    final_files = count_files(CONFIG["final_dir"], "*.md")
    if final_files > 0:
        status["LLM处理"] = "completed"
    else:
        status["LLM处理"] = "pending"
    
    # 检查知识库构建状态（暂时为pending）
    status["知识库构建"] = "pending"
    
    return status

def show_homepage():
    """显示首页概览"""
    st.header("🏠 系统概览")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📧 已上传邮件",
            value=count_files(CONFIG["upload_dir"], "*.eml"),
            delta="0"
        )
    
    with col2:
        st.metric(
            label="🔧 已清洗邮件", 
            value=count_files(CONFIG["processed_dir"], "*.md"),
            delta="0"
        )
    
    with col3:
        st.metric(
            label="🤖 LLM处理完成",
            value=count_files(CONFIG["final_dir"], "*.md"),
            delta="0"
        )
    
    st.markdown("---")
    
    # 系统介绍
    st.subheader("📖 系统介绍")
    st.markdown("""
    **邮件知识库管理系统** 是一个本地部署的应用，帮助您：
    
    1. **📤 批量上传邮件** - 支持EML格式邮件的批量上传和管理
    2. **🔧 智能数据清洗** - 自动去除重复内容，保留独特信息
    3. **🤖 LLM二次处理** - 使用AI技术提取结构化商务信息
    4. **📚 知识库构建** - 将处理后的数据构建为可查询的知识库
    5. **💬 智能问答** - 基于邮件内容提供项目经验查询
    
    ### 🚀 快速开始
    1. 点击 **"邮件上传"** 开始上传您的EML邮件文件
    2. 使用 **"数据清洗"** 功能去除重复内容
    3. 通过 **"LLM处理"** 提取结构化信息
    4. 在 **"结果查看"** 中查看处理结果
    """)
    
    # 最近活动
    st.subheader("📅 最近活动")
    if os.path.exists("activity.log"):
        with open("activity.log", "r", encoding="utf-8") as f:
            activities = f.readlines()[-5:]  # 显示最近5条活动
            for activity in activities:
                st.text(activity.strip())
    else:
        st.info("暂无活动记录")
    
    # 导航按钮
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.info("💡 这是起始页面")
    with col3:
        if st.button("➡️ 开始使用", help="前往邮件上传页面", type="primary", key="home_start_btn"):
            st.session_state.current_step = "邮件上传"
            st.rerun()

def show_upload_page():
    """显示邮件上传页面"""
    st.header("📤 邮件上传")
    
    upload_method = st.radio(
        "选择上传方式",
        ["📁 本地路径文件扫描", "📄 浏览本地文件上传"]
    )
    
    if upload_method == "📄 浏览本地文件上传":
        uploaded_files = st.file_uploader(
            "选择EML邮件文件",
            type=['eml'],
            accept_multiple_files=True,
            help="支持选择多个EML格式的邮件文件"
        )
        
        if uploaded_files:
            st.success(f"已选择 {len(uploaded_files)} 个文件")
            
            # 显示文件列表
            file_data = []
            for file in uploaded_files:
                file_data.append({
                    "文件名": file.name,
                    "大小": f"{file.size / 1024:.1f} KB",
                    "类型": file.type
                })
            
            st.dataframe(pd.DataFrame(file_data))
            
            if st.button("🚀 开始上传", type="primary"):
                upload_files(uploaded_files)
    
    else:
        upload_method == "📁 本地路径文件扫描"
        st.info("📝 **批量上传说明**")
        st.markdown("""
        1. 将您的EML邮件文件复制到 `eml_process/uploads/` 目录中
        2. 点击下方的"扫描文件夹"按钮
        3. 确认文件列表后开始处理
        """)
        
        if st.button("🔍 扫描uploads文件夹"):
            scan_upload_folder()
    

    
    # 导航按钮
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 上一步", help="返回首页概览", key="upload_prev_btn"):
            st.session_state.current_step = "首页概览"
            st.rerun()
    with col3:
        if st.button("➡️ 下一步", help="前往数据清洗页面", key="upload_next_btn"):
            # 检查是否有邮件文件可处理
            upload_files = count_files(CONFIG["upload_dir"], "*.eml")
            demo_files = count_files("Eml", "*.eml")
            if upload_files > 0 or demo_files > 0:
                st.session_state.current_step = "数据清洗"
                st.rerun()
            else:
                st.warning("⚠️ 请先上传邮件文件再进入下一步")

def show_cleaning_page():
    """显示数据清洗页面"""
    st.header("🔧 数据清洗")
    
    st.info("📋 **清洗功能说明**：自动去除重复邮件内容，保留独特信息，生成Markdown格式文件")
    
    # 检查是否有待处理的邮件
    eml_files = count_files(CONFIG["upload_dir"], "*.eml")
    
    if eml_files == 0:
        st.warning("⚠️ 未发现待处理的EML邮件文件，请先上传邮件。")
        return
    
    st.success(f"✅ 发现 {eml_files} 个EML邮件文件待处理")
    
    # 清洗说明
    st.subheader("⚙️ 清洗规则")
    st.info("📋 **去重规则**: 系统会自动检测100%被包含的邮件内容，将重复邮件合并到包含它们的完整邮件中")
    
    # 开始清洗按钮
    if st.button("🚀 开始数据清洗", type="primary"):
        start_data_cleaning()
    
    # 导航按钮
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 上一步", help="返回邮件上传页面", key="cleaning_prev_btn"):
            st.session_state.current_step = "邮件上传"
            st.rerun()
    with col3:
        if st.button("➡️ 下一步", help="前往LLM处理页面", key="cleaning_next_btn"):
            # 检查是否有处理结果
            processed_files = count_files(CONFIG["processed_dir"], "*.md")
            if processed_files > 0:
                st.session_state.current_step = "LLM处理"
                st.rerun()
            else:
                st.warning("⚠️ 请先完成数据清洗再进入下一步")

def show_llm_processing_page():
    """显示LLM处理页面"""
    st.header("🤖 LLM数据处理")
    
    st.info("🧠 **LLM处理功能**：使用GPTBots AI对清洗后的邮件进行结构化信息提取")
    
    # 检查清洗后的文件
    md_files = count_files(CONFIG["processed_dir"], "*.md")
    
    if md_files == 0:
        st.warning("⚠️ 未发现已清洗的Markdown文件，请先完成数据清洗步骤。")
        return
    
    st.success(f"✅ 发现 {md_files} 个已清洗的Markdown文件待处理")
    
    # API配置
    st.subheader("🔑 API配置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 节点选择
        endpoint = st.selectbox(
            "选择API节点",
            options=["sg", "cn", "th"],
            index=0,  # 默认sg
            format_func=lambda x: {
                "sg": "🌏 新加坡 (sg) - 推荐",
                "cn": "🇨🇳 中国 (cn)",
                "th": "🇹🇭 泰国 (th)"
            }[x],
            help="选择GPTBots API数据中心节点"
        )
    
    with col2:
        # API Key配置
        import os
        default_api_key = os.getenv("GPTBOTS_API_KEY", "")
        
        use_default_key = st.checkbox(
            "使用默认API Key",
            value=True,
            help="使用项目配置的默认API Key"
        )
        
        if use_default_key:
            api_key = default_api_key
            if api_key:
                st.success(f"✅ 使用默认API Key: {api_key[:8]}...{api_key[-8:]}")
            else:
                st.warning("⚠️ .env未配置API Key")
        else:
            api_key = st.text_input(
                "输入临时API Key",
                type="password",
                placeholder="输入您的GPTBots API Key",
                help="临时输入API Key，仅在当前会话中使用"
            )
            
            if not api_key:
                st.warning("⚠️ 请输入API Key")
                return
            else:
                st.success(f"✅ 使用临时API Key: {api_key[:8]}...{api_key[-8:]}")
    
    # 验证API配置
    st.subheader("🔍 API连接测试")
    if st.button("🧪 测试API连接", key="test_api_btn"):
        test_api_connection(api_key, endpoint)
    
    # LLM处理参数
    st.subheader("⚙️ 处理参数")
    
    col1, col2 = st.columns(2)
    
    with col1:
        batch_size = st.number_input(
            "批处理大小",
            min_value=1,
            max_value=10,
            value=3,
            help="每批次处理的文件数量，避免API限流"
        )
    
    with col2:
        delay_seconds = st.number_input(
            "请求间隔(秒)",
            min_value=1,
            max_value=10,
            value=2,
            help="API请求之间的延迟时间"
        )
    
    # 开始LLM处理
    if st.button("🚀 开始LLM处理", type="primary", key="start_llm_btn"):
        start_llm_processing(api_key, endpoint, batch_size, delay_seconds)
    
    # 导航按钮
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 上一步", help="返回数据清洗页面", key="llm_prev_btn"):
            st.session_state.current_step = "数据清洗"
            st.rerun()
    with col3:
        if st.button("➡️ 下一步", help="前往结果查看页面", key="llm_next_btn"):
            st.session_state.current_step = "结果查看"
            st.rerun()

def show_results_page():
    """显示结果查看页面"""
    st.header("📊 处理结果")
    
    # 结果统计
    col1, col2, col3 = st.columns(3)
    
    with col1:
        original_count = count_files(CONFIG["upload_dir"], "*.eml")
        st.metric("原始邮件", original_count)
    
    with col2:
        cleaned_count = count_files(CONFIG["processed_dir"], "*.md")
        st.metric("清洗后邮件", cleaned_count)
    
    with col3:
        final_count = count_files(CONFIG["final_dir"], "*.md")
        st.metric("最终处理完成", final_count)
    
    # 文件浏览器
    st.subheader("📁 文件浏览器")
    
    view_option = st.radio(
        "选择查看内容",
        ["🔧 清洗结果", "🤖 LLM处理结果", "📄 所有文件"],
        horizontal=True
    )
    
    if view_option == "🔧 清洗结果":
        show_file_browser(CONFIG["processed_dir"], "*.md")
    elif view_option == "🤖 LLM处理结果":
        show_file_browser(CONFIG["final_dir"], "*.md")
    else:
        show_all_files()
    
    # 导航按钮
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 上一步", help="返回LLM处理页面", key="results_prev_btn"):
            st.session_state.current_step = "LLM处理"
            st.rerun()
    with col3:
        st.info("💡 这是最后一个处理步骤")

def show_future_features_page(feature_name):
    """显示未来功能预留页面"""
    st.header(f"{feature_name}")
    
    st.info("🔮 **功能预留中**")
    
    if "知识库" in feature_name:
        st.markdown("""
        ### 📚 知识库管理功能（规划中）
        
        **计划功能：**
        - 🔗 集成GPTBots知识库API
        - 📤 批量上传处理后的邮件内容
        - 🏷️ 自动标签和分类管理
        - 🔍 知识库内容搜索和管理
        
        **技术准备：**
        - ✅ API调用框架已就绪
        - ✅ 数据格式标准化完成
        - ⏳ 知识库API接口对接中
        """)
    
    elif "问答" in feature_name:
        st.markdown("""
        ### 💬 智能问答系统（规划中）
        
        **计划功能：**
        - 🤖 基于邮件内容的RAG问答
        - 📊 项目经验智能查询
        - 🎯 上下文相关推荐
        - 📱 iframe嵌入支持
        
        **技术准备：**
        - ✅ LLM处理管道已完成
        - ✅ 结构化数据提取完成
        - ⏳ RAG系统架构设计中
        """)
    
    st.warning("💡 这些功能将在后续版本中实现，当前版本专注于核心邮件处理流程。")

# 辅助函数
def count_files(directory, pattern):
    """计算目录中匹配模式的文件数量"""
    try:
        path = Path(directory)
        if pattern == "*.eml":
            return len(list(path.glob("*.eml")))
        elif pattern == "*.md":
            return len(list(path.glob("*.md")))
        else:
            return len(list(path.glob(pattern)))
    except:
        return 0

def upload_files(uploaded_files):
    """处理文件上传"""
    st.info("🚀 开始上传文件...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, file in enumerate(uploaded_files):
        # 保存文件
        file_path = Path(CONFIG["upload_dir"]) / file.name
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        
        # 更新进度
        progress = (i + 1) / len(uploaded_files)
        progress_bar.progress(progress)
        status_text.text(f"正在上传: {file.name}")
        
        # 记录活动
        log_activity(f"上传文件: {file.name}")
    
    st.success(f"✅ 成功上传 {len(uploaded_files)} 个文件！")

def scan_upload_folder():
    """扫描上传文件夹"""
    upload_path = Path(CONFIG["upload_dir"])
    eml_files = list(upload_path.glob("*.eml"))
    
    if not eml_files:
        st.warning("📂 uploads文件夹中未发现EML文件")
        return
    
    st.success(f"🎉 发现 {len(eml_files)} 个EML文件")
    
    # 显示文件列表
    file_data = []
    for file in eml_files:
        stat = file.stat()
        file_data.append({
            "文件名": file.name,
            "大小": f"{stat.st_size / 1024:.1f} KB",
            "修改时间": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        })
    
    st.dataframe(pd.DataFrame(file_data))

def validate_custom_path(path):
    """验证自定义路径"""
    custom_path = Path(path)
    
    if not custom_path.exists():
        st.error("❌ 路径不存在")
        return
    
    if not custom_path.is_dir():
        st.error("❌ 路径不是文件夹")
        return
    
    eml_files = list(custom_path.glob("*.eml"))
    st.success(f"✅ 路径有效，发现 {len(eml_files)} 个EML文件")

def start_data_cleaning():
    """开始数据清洗"""
    st.info("🚀 开始邮件清洗处理...")
    log_activity("开始数据清洗")
    
    # 创建进度条
    progress_bar = st.progress(0)
    status_text = st.empty()
    result_container = st.empty()
    
    try:
        # 检查输入目录
        eml_dir = CONFIG["upload_dir"]
        eml_files = list(Path(eml_dir).glob("*.eml"))
        
        if not eml_files:
            # 如果uploads目录没有文件，尝试从Eml目录读取示例文件
            eml_dir = "Eml"
            eml_files = list(Path(eml_dir).glob("*.eml"))
            
            if eml_files:
                status_text.info(f"📁 未在uploads目录发现文件，使用示例邮件目录: {eml_dir}")
            else:
                st.error("❌ 未找到任何EML文件进行处理")
                return
        
        progress_bar.progress(10)
        status_text.text("🔍 初始化邮件清洗器...")
        
        # 创建邮件清洗器实例
        cleaner = EmailCleaner(
            input_dir=eml_dir,
            output_dir=CONFIG["processed_dir"]
        )
        
        progress_bar.progress(20)
        status_text.text(f"📧 发现 {len(eml_files)} 个EML文件，开始解析...")
        
        # 执行清洗处理
        result = cleaner.process_all_emails()
        
        progress_bar.progress(90)
        status_text.text("📝 生成处理报告...")
        
        if result["success"]:
            progress_bar.progress(100)
            status_text.empty()
            
            # 显示处理结果
            report = result["report"]
            
            with result_container.container():
                st.success("🎉 邮件清洗完成！")
                
                # 统计信息
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("原始邮件", report["total_input_files"])
                
                with col2:
                    st.metric("解析成功", report["successfully_parsed"])
                
                with col3:
                    st.metric("去重后邮件", report["unique_emails"])
                
                with col4:
                    st.metric("压缩率", report["compression_ratio"])
                
                # 详细信息
                st.subheader("📊 处理详情")
                
                if report["duplicate_emails"] > 0:
                    st.info(f"🗑️ 发现 {report['duplicate_emails']} 封重复邮件已合并")
                    
                    with st.expander("查看重复邮件详情"):
                        duplicate_details = report["duplicate_details"]
                        st.info(f"📊 共发现 {len(duplicate_details)} 封重复邮件")
                        
                        if duplicate_details:
                            # 直接显示所有重复邮件，支持滚动
                            duplicate_data = []
                            for dup in duplicate_details:
                                duplicate_data.append({
                                    "重复文件": dup["duplicate_file"],
                                    "被包含于": dup["contained_by_file"],
                                    "重复主题": dup["duplicate_subject"][:50] + "..." if len(dup["duplicate_subject"]) > 50 else dup["duplicate_subject"]
                                })
                            
                            st.dataframe(pd.DataFrame(duplicate_data), width='stretch', height=400)
                            st.caption(f"共 {len(duplicate_details)} 封重复邮件，可滚动查看全部")
                        else:
                            st.info("没有发现重复邮件")
                
                # 生成的文件列表
                st.subheader("📁 生成的Markdown文件")
                
                generated_files = report["generated_markdown_files"]
                st.info(f"📊 共生成 {len(generated_files)} 个Markdown文件")
                
                if generated_files:
                    # 显示文件网格
                    num_cols = 3
                    for i in range(0, len(generated_files), num_cols):
                        cols = st.columns(num_cols)
                        for j, filename in enumerate(generated_files[i:i+num_cols]):
                            with cols[j]:
                                st.code(filename)
                
                # 路径信息
                st.subheader("📂 文件位置")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.success("📁 Markdown文件保存至:")
                    st.code(CONFIG["processed_dir"])
                
                with col2:
                    st.success("📋 处理报告保存至:")
                    st.code(f"{CONFIG['processed_dir']}/processing_report.json")
                
                # 记录成功日志
                log_activity(f"邮件清洗完成: {report['total_input_files']} -> {report['unique_emails']} 封")
        
        else:
            progress_bar.progress(0)
            status_text.empty()
            result_container.error(f"❌ 处理失败: {result.get('message', '未知错误')}")
            log_activity(f"邮件清洗失败: {result.get('message', '未知错误')}")
    
    except Exception as e:
        progress_bar.progress(0)
        status_text.empty()
        result_container.error(f"❌ 处理过程中发生错误: {str(e)}")
        log_activity(f"邮件清洗错误: {str(e)}")
        st.exception(e)

def test_api_connection(api_key, endpoint):
    """测试API连接"""
    st.info("🔄 正在测试API连接...")
    
    try:
        from gptbots_api import GPTBotsAPI
        
        # 创建API客户端
        client = GPTBotsAPI(api_key, endpoint=endpoint)
        
        # 发送测试消息
        test_query = "你好，这是一个连接测试。"
        result = client.call_agent(test_query)
        
        if result:
            st.success("✅ API连接测试成功！")
            st.info("🎉 GPTBots API工作正常，可以开始LLM处理")
            
            # 显示API响应示例
            with st.expander("查看API响应示例"):
                st.json(result)
                
        else:
            st.error("❌ API连接测试失败")
            st.warning("请检查API Key和网络连接")
            
    except Exception as e:
        st.error(f"❌ API测试出错: {str(e)}")
        st.warning("请确认API配置正确")

def start_llm_processing(api_key, endpoint, batch_size, delay):
    """开始LLM处理"""
    st.info("🚀 开始LLM处理...")
    log_activity("开始LLM处理")
    
    # 创建进度条
    progress_bar = st.progress(0)
    status_text = st.empty()
    result_container = st.empty()
    
    try:
        from gptbots_api import GPTBotsAPI
        
        # 初始化API客户端
        status_text.text("🔍 初始化GPTBots API客户端...")
        client = GPTBotsAPI(api_key, endpoint=endpoint)
        
        # 获取待处理的Markdown文件
        processed_dir = Path(CONFIG["processed_dir"])
        md_files = list(processed_dir.glob("*.md"))
        
        # 过滤掉处理报告文件
        md_files = [f for f in md_files if f.name != "processing_report.json"]
        
        if not md_files:
            st.error("❌ 未找到待处理的Markdown文件")
            return
        
        progress_bar.progress(10)
        status_text.text(f"📧 发现 {len(md_files)} 个Markdown文件待处理...")
        
        # LLM提示词模板（从项目指南中获取）
        llm_prompt_template = """你是一名专业的商务信息提取专家。你的任务是从邮件文本中精准提取关键信息，并生成一份结构化的摘要。请严格遵循以下规则：
1. **忽略无关内容**：忽略所有邮件签名、免责声明、转发标记和寒暄用语。
2. **聚焦核心**：只提取与商务活动相关的事实性内容，如产品、报价、项目状态、日期、数字、决策和行动项。
3. **重要性判断**：优先提取包含数字（如价格、日期、数量）和状态变更（如"提供报价"、"询问进展"、"项目暂停"）的信息。
4. **自适应输出**：如果邮件是讨论报价，就重点输出报价；如果是询问进展，就重点总结状态。不要为不存在的信息创建字段。

请分析邮件内容。如果它是项目沟通中的一部分，请提取其核心信息，并生成一份简洁的Markdown格式摘要。

请使用以下模板，但仅包含邮件中实际提到的部分。如果某个部分没有相关信息，请完全省略该部分。

### 邮件元信息
- **发件人:** [发件人姓名和邮箱]
- **收件人:** [收件人姓名和邮箱]
- **日期:** [邮件发送日期]
- **主题:** [邮件主题]
- **文件名:** [邮件文件名]
- **核心事件:** [用一句话总结这封邮件的核心目的，如"供应商提供最新报价"、"客户询问项目进展"]

### 项目主题
[此处简要总结此封邮件的前因后果，来龙去脉]

### 关键信息摘要
[在此处用列表形式列出邮件中最重要的事实。特别是包含数字、日期、关键决策和状态更新的信息。]
- 例如: `报价更新: VE82029 MOQ 100K 单价为 5.82元 (含13%VAT)`
- 例如: `项目状态: 暂无进展，等待客户确认需求`
- 例如: `下一步行动: 需要我方在7月6日前确认报价`

### 详细内容（如适用）
#### 产品信息
- **型号:** [产品型号]
- **规格:** [产品规格]

#### 报价信息
| MOQ | 单价 | 货币 | 条款 | 付款方式 | 交期 | 有效期 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [例如: 10,000] | [例如: 11.38] | [例如: RMB] | [例如: DDP China] | [例如: 100%预付] | [例如: 4-6周] | [例如: 2023-07-06] |
| ... | ... | ... | ... | ... | ... | ... |

#### 项目状态更新
[如果邮件是关于项目跟进的，在此处描述最新状态、阻塞原因或下一步计划。]

---

以下是需要处理的邮件内容：

{email_content}"""
        
        # 开始处理文件
        processed_files = []
        failed_files = []
        
        for i, md_file in enumerate(md_files):
            try:
                # 更新进度
                progress = 10 + (i / len(md_files)) * 80
                progress_bar.progress(int(progress))
                status_text.text(f"🤖 处理中: {md_file.name} ({i+1}/{len(md_files)})")
                
                # 读取文件内容
                with open(md_file, 'r', encoding='utf-8') as f:
                    email_content = f.read()
                
                # 构建完整的提示词
                full_prompt = llm_prompt_template.format(email_content=email_content)
                
                # 调用LLM API
                result = client.call_agent(full_prompt)
                
                if result and "output" in result:
                    # 提取LLM响应内容
                    llm_response = extract_llm_content(result)
                    
                    if llm_response:
                        # 保存LLM处理结果
                        output_filename = f"llm_{md_file.name}"
                        output_path = Path(CONFIG["final_dir"]) / output_filename
                        
                        # 确保输出目录存在
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # 生成最终的Markdown内容
                        final_content = f"""# LLM处理结果 - {md_file.name}

## 🤖 AI提取的结构化信息

{llm_response}

---

## 📄 原始邮件内容

{email_content}

---
*LLM处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*使用节点: {endpoint}*
*API Key: {api_key[:8]}...{api_key[-8:]}*
"""
                        
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(final_content)
                        
                        processed_files.append(output_filename)
                        
                        # 添加延迟避免API限流
                        if i < len(md_files) - 1:  # 不是最后一个文件
                            import time
                            time.sleep(delay)
                    else:
                        failed_files.append(md_file.name)
                        st.warning(f"⚠️ {md_file.name} - 无法提取LLM响应内容")
                        
                else:
                    failed_files.append(md_file.name)
                    st.warning(f"⚠️ {md_file.name} - LLM处理失败")
                    
            except Exception as e:
                failed_files.append(md_file.name)
                st.error(f"❌ {md_file.name} - 处理出错: {str(e)}")
        
        # 显示处理结果
        progress_bar.progress(100)
        status_text.empty()
        
        with result_container.container():
            st.success("🎉 LLM处理完成！")
            
            # 统计信息
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("输入文件", len(md_files))
            
            with col2:
                st.metric("处理成功", len(processed_files))
            
            with col3:
                st.metric("处理失败", len(failed_files))
            
            # 显示处理结果
            if processed_files:
                st.subheader("✅ 处理成功的文件")
                for filename in processed_files[:5]:  # 显示前5个
                    st.code(filename)
                if len(processed_files) > 5:
                    with st.expander(f"查看剩余 {len(processed_files) - 5} 个文件"):
                        for filename in processed_files[5:]:
                            st.code(filename)
            
            if failed_files:
                st.subheader("❌ 处理失败的文件")
                for filename in failed_files:
                    st.error(filename)
            
            # 输出位置
            st.subheader("📁 输出位置")
            st.success("📁 LLM处理结果保存至:")
            st.code(CONFIG["final_dir"])
            
            log_activity(f"LLM处理完成: {len(processed_files)}/{len(md_files)} 成功")
    
    except Exception as e:
        progress_bar.progress(0)
        status_text.empty()
        result_container.error(f"❌ LLM处理过程中发生错误: {str(e)}")
        log_activity(f"LLM处理错误: {str(e)}")
        st.exception(e)

def extract_llm_content(result):
    """从LLM API响应中提取内容"""
    try:
        if "output" in result:
            output_list = result.get("output", [])
            content = ""
            for output_item in output_list:
                if "content" in output_item:
                    content_obj = output_item["content"]
                    if "text" in content_obj:
                        content += content_obj["text"] + "\n"
            return content.strip()
        
        # 备用提取方法
        return (result.get("answer") or 
                result.get("content") or 
                result.get("message") or
                None)
                
    except Exception as e:
        st.error(f"内容提取失败: {e}")
        return None

def show_file_browser(directory, pattern):
    """显示文件浏览器"""
    path = Path(directory)
    if not path.exists():
        st.warning(f"📂 目录 {directory} 不存在")
        return
    
    files = list(path.glob(pattern))
    if not files:
        st.info(f"📂 {directory} 目录中暂无 {pattern} 文件")
        return
    
    # 文件选择器
    selected_file = st.radio(
        "选择要查看的文件",
        options=[f.name for f in files]
    )
    
    if selected_file:
        file_path = path / selected_file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            st.subheader(f"📄 {selected_file}")
            st.markdown(content)
            
            # 下载按钮
            st.download_button(
                label="💾 下载文件",
                data=content,
                file_name=selected_file,
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"❌ 读取文件失败: {str(e)}")

def show_all_files():
    """显示所有文件概览"""
    st.subheader("📁 全部文件概览")
    
    all_files = []
    
    # 收集所有目录的文件
    directories = [
        (CONFIG["upload_dir"], "原始邮件", "*.eml"),
        (CONFIG["processed_dir"], "清洗结果", "*.md"),
        (CONFIG["final_dir"], "最终结果", "*.md")
    ]
    
    for dir_path, dir_name, pattern in directories:
        path = Path(dir_path)
        if path.exists():
            files = list(path.glob(pattern))
            for file in files:
                stat = file.stat()
                all_files.append({
                    "目录": dir_name,
                    "文件名": file.name,
                    "大小": f"{stat.st_size / 1024:.1f} KB",
                    "修改时间": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "路径": str(file)
                })
    
    if all_files:
        df = pd.DataFrame(all_files)
        st.dataframe(df, width='stretch')
    else:
        st.info("📂 暂无文件")


def log_activity(message):
    """记录活动日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    with open("activity.log", "a", encoding="utf-8") as f:
        f.write(log_entry)

if __name__ == "__main__":
    main()
