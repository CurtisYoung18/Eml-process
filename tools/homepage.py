"""
首页概览模块
显示系统概览和处理进度
"""

import streamlit as st
import os
from .utils import count_files


def show_homepage():
    """显示首页概览"""
    from app import CONFIG
    
    st.header("当前进度")
    
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
    st.subheader("系统介绍")
    
    st.info("这是一个邮件知识库管理系统，帮助您管理邮件内容，构建知识库，提供智能问答功能。")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**邮件知识库管理系统** 是一个本地部署的应用，完整的处理流程如下：")
        
        # 系统流程图
        st.subheader("🔄 系统流程")
        mermaid_code = """
        graph TD
            A["📁 上传EML邮件文件"] --> B["📤 批量邮件上传<br/>支持EML格式邮件的<br/>批量上传和管理"]
            B --> C["🔧 智能数据清洗<br/>自动去除重复内容<br/>保留独特信息"]
            C --> D["🤖 LLM二次处理<br/>使用AI技术提取<br/>结构化项目信息"]
            D --> E["📚 知识库构建<br/>将处理后的数据构建为<br/>可查询的知识库"]
            E --> F["💬 智能问答<br/>基于邮件内容提供<br/>项目经验查询"]
            
            B --> G["📊 结果查看<br/>查看处理结果和统计"]
            C --> G
            D --> G
            E --> G
            
            style A fill:#e1f5fe
            style B fill:#f3e5f5
            style C fill:#e8f5e8
            style D fill:#fff3e0
            style E fill:#fce4ec
            style F fill:#e0f2f1
            style G fill:#f1f8e9
        """
        
        st.components.v1.html(
            f"""
            <div class="mermaid">
            {mermaid_code}
            </div>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{startOnLoad:true}});
            </script>
            """,
            height=1000
        )
    
    with col2:
        st.markdown("""
        ### 🚀 快速开始
        1. 点击 **"邮件上传"** 开始上传您的EML邮件文件
        2. 使用 **"数据清洗"** 功能去除重复内容
        3. 通过 **"LLM处理"** 提取结构化信息
        4. 在 **"结果查看"** 中查看处理结果
        """)

        # 导航按钮
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.info("💡 这是起始页面")
        with col3:
            if st.button("➡️ 开始使用", help="前往邮件上传页面", type="primary", key="home_start_btn"):
                st.session_state.current_step = "邮件上传"
                st.rerun()
    
        # 最近活动
        st.subheader("📅 最近活动")
        if os.path.exists("logs/activity.log"):
            with open("logs/activity.log", "r", encoding="utf-8") as f:
                activities = f.readlines()[-5:]  # 显示最近5条活动
                for activity in activities:
                    st.text(activity.strip())
        else:
            st.info("暂无活动记录")
