"""
问答系统模块
支持iframe集成的智能问答功能
"""

import streamlit as st


def show_qa_system_page():
    """显示问答系统页面"""
    st.header("💬 智能问答系统")
    
    # 检查前置条件
    from .utils import count_files
    from app import CONFIG
    
    final_files = count_files(CONFIG["final_dir"], "*.md")
    
    if final_files == 0:
        st.warning("⚠️ 未发现已处理的文件，请先完成前面的步骤。")
        st.info("💡 需要完成：邮件上传 → 数据清洗 → LLM处理 → 知识库上传")
        return
    
    st.success(f"✅ 发现 {final_files} 个已处理的文件，可以开始问答")
    
    # 直接显示问答界面
    st.markdown("""
    ### 💬 基于知识库的智能问答
    这是基于GPTBots的智能问答系统，可以回答关于已上传知识库的问题。
    
    分享链接：[Agent: NolatoEml](https://gptbots.ai/s/csfmLzGO)
    
    ---
    """)
    
    # 嵌入GPTBots聊天界面
    import streamlit.components.v1 as components
    
    iframe_html = """
    <iframe 
        width="100%" 
        height="1200px" 
        allow="microphone *" 
        src="https://www.gptbots.ai/widget/eesy0snwfrcoqgiib8x0nlm/chat.html"
        style="border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    </iframe>
    """
    
    components.html(iframe_html, height=1300)

    
    # 导航按钮
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 上一步", help="返回知识库管理页面", key="qa_prev_btn"):
            st.session_state.current_step = "知识库管理"
            st.rerun()
    with col3:
        st.info("💡 这是最终的问答功能")