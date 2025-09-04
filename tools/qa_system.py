"""
问答系统模块
支持iframe集成和独立问答功能
"""

import streamlit as st
from config import get_api_key


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
    
    # API配置区域
    st.subheader("🔑 问答API配置")
    
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
            help="选择GPTBots API数据中心节点",
            key="qa_endpoint"
        )
    
    with col2:
        # API Key选择器
        from .api_selector import create_api_selector_with_guide
        
        # 提供多种API Key选择方式
        api_key_mode = st.radio(
            "API Key选择方式",
            ["问答专用API Key", "知识库API Key", "手动输入"],
            help="选择API Key的来源和类型",
            key="qa_api_mode"
        )
        
        if api_key_mode == "问答专用API Key":
            api_key, key_number = create_api_selector_with_guide(
                purpose="qa",
                key_prefix="qa_system",
                show_guide=True
            )
            if not api_key:
                st.warning("⚠️ 请配置问答API Key")
                st.info("💡 请在.env文件中配置GPTBOTS_QA_API_KEY_1等环境变量")
                return
                
        elif api_key_mode == "知识库API Key":
            api_key, key_number = create_api_selector_with_guide(
                purpose="knowledge_base",
                key_prefix="qa_kb",
                show_guide=False
            )
            if not api_key:
                st.warning("⚠️ 请配置知识库API Key")
                st.info("💡 请在.env文件中配置GPTBOTS_KB_API_KEY_1等环境变量")
                return
            st.info("📚 **复用知识库API**: 使用知识库API Key进行问答")
            
        else:  # 手动输入
            api_key = st.text_input(
                "输入问答API Key",
                type="password",
                placeholder="输入您的GPTBots问答API Key",
                help="手动输入问答专用API Key",
                key="qa_manual_api_key"
            )
            key_number = "手动"
            
            if not api_key:
                st.warning("⚠️ 请输入问答API Key")
                return
            else:
                st.success(f"✅ 使用手动API Key: {api_key[:8]}...{api_key[-8:]}")
    
    # 问答模式选择
    st.subheader("🎯 问答模式")
    
    qa_mode = st.radio(
        "选择问答模式",
        ["🤖 直接问答", "💬 交互式问答", "🖼️ iframe嵌入代码", "🔧 API接口测试"],
        horizontal=True,
        help="选择不同的问答交互方式"
    )
    
    if qa_mode == "🤖 直接问答":
        show_direct_qa_iframe(api_key, endpoint)
    elif qa_mode == "💬 交互式问答":
        show_interactive_qa(api_key, endpoint)
    elif qa_mode == "🖼️ iframe嵌入代码":
        show_iframe_integration(api_key, endpoint)
    else:
        show_api_testing(api_key, endpoint)
    
    # 导航按钮
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 上一步", help="返回知识库管理页面", key="qa_prev_btn"):
            st.session_state.current_step = "知识库管理"
            st.rerun()
    with col3:
        st.info("💡 这是最终的问答功能")


def show_direct_qa_iframe(api_key, endpoint):
    """显示直接嵌入的问答iframe"""
    st.subheader("🤖 智能问答助手")
    
    st.markdown("""
    ### 💬 基于知识库的智能问答
    这是基于GPTBots的智能问答系统，可以回答关于已上传知识库的问题。
    
    **功能特点**：
    - 🎯 基于知识库的精准问答
    - 🔄 支持多轮对话
    - 🎤 支持语音输入
    - 📚 上下文理解能力
    
    ---
    """)
    
    # 嵌入GPTBots聊天界面
    import streamlit.components.v1 as components
    
    iframe_html = """
    <iframe 
        width="100%" 
        height="600px" 
        allow="microphone *" 
        src="https://www.gptbots.ai/widget/eesy0snwfrcoqgiib8x0nlm/chat.html"
        style="border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    </iframe>
    """
    
    components.html(iframe_html, height=620)
    
    st.markdown("""
    ---
    ### 📝 使用说明
    1. **直接对话**: 在上方聊天框中输入您的问题
    2. **语音输入**: 点击麦克风图标进行语音输入
    3. **知识库查询**: 系统会自动检索相关知识库内容
    4. **多轮对话**: 支持连续提问和上下文理解
    
    ### ⚙️ 技术说明
    - **API Key**: 当前使用的QA API Key: `{api_key[:8]}...{api_key[-8:]}`
    - **节点**: {endpoint.upper()} 数据中心
    - **知识库**: 基于已上传的邮件处理结果进行问答
    - **响应速度**: 通常在2-5秒内获得回复
    """.format(api_key=api_key, endpoint=endpoint))


def show_interactive_qa(api_key, endpoint):
    """显示交互式问答界面"""
    st.subheader("💬 交互式问答")
    
    # 问答历史
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []
    
    # 问题输入
    question = st.text_input(
        "请输入您的问题",
        placeholder="例如：项目中遇到了什么技术难题？",
        key="qa_question_input"
    )
    
    col_ask, col_clear = st.columns([1, 1])
    
    with col_ask:
        if st.button("🤖 提问", type="primary", disabled=not question):
            if question:
                # 调用问答API
                answer = call_qa_api(api_key, endpoint, question)
                
                # 添加到历史记录
                st.session_state.qa_history.append({
                    "question": question,
                    "answer": answer,
                    "timestamp": st.session_state.get("timestamp", "刚刚")
                })
                
                # 清空输入框
                st.session_state.qa_question_input = ""
                st.rerun()
    
    with col_clear:
        if st.button("🗑️ 清空历史") and st.session_state.qa_history:
            st.session_state.qa_history = []
            st.rerun()
    
    # 显示问答历史
    if st.session_state.qa_history:
        st.subheader("📝 问答历史")
        
        for i, qa in enumerate(reversed(st.session_state.qa_history)):
            with st.expander(f"Q{len(st.session_state.qa_history)-i}: {qa['question'][:50]}..."):
                st.markdown(f"**问题**: {qa['question']}")
                st.markdown(f"**回答**: {qa['answer']}")
                st.caption(f"时间: {qa['timestamp']}")
    else:
        st.info("💡 开始提问吧！基于您的邮件内容，我可以回答项目相关的问题。")


def show_iframe_integration(api_key, endpoint):
    """显示iframe集成代码"""
    st.subheader("🖼️ iframe嵌入集成")
    
    st.info("📋 **iframe集成说明**: 基于GPTBots的智能问答界面，支持语音输入和知识库检索")
    
    # iframe配置选项
    col1, col2 = st.columns(2)
    
    with col1:
        iframe_width = st.selectbox(
            "iframe宽度",
            ["100%", "800px", "600px", "400px"],
            index=0,
            help="设置iframe的宽度"
        )
        
        iframe_height = st.selectbox(
            "iframe高度", 
            ["600px", "500px", "400px", "700px", "800px"],
            index=0,
            help="设置iframe的高度"
        )
    
    with col2:
        enable_microphone = st.checkbox("启用麦克风", value=True, help="允许语音输入功能")
        show_border = st.checkbox("显示边框", value=True, help="为iframe添加边框样式")
    
    # GPTBots iframe URL
    iframe_url = "https://www.gptbots.ai/widget/eesy0snwfrcoqgiib8x0nlm/chat.html"
    
    # 生成iframe代码
    microphone_attr = 'allow="microphone *"' if enable_microphone else ''
    border_style = 'style="border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"' if show_border else 'style="border: none;"'
    
    iframe_code = f'''<iframe 
    width="{iframe_width}" 
    height="{iframe_height}" 
    {microphone_attr}
    src="{iframe_url}"
    {border_style}>
</iframe>'''
    
    st.subheader("📋 iframe嵌入代码")
    st.code(iframe_code, language="html")
    
    st.subheader("🔗 GPTBots聊天链接")
    st.code(iframe_url)
    
    # 实时预览
    st.subheader("👀 效果预览")
    
    # 使用streamlit的components来显示iframe
    import streamlit.components.v1 as components
    
    preview_height = int(iframe_height.replace('px', '')) if 'px' in iframe_height else 600
    
    components.html(f'''
    <iframe 
        width="100%" 
        height="{preview_height}px" 
        {microphone_attr}
        src="{iframe_url}"
        {border_style}>
    </iframe>
    ''', height=preview_height + 20)
    
    # 使用说明
    st.markdown("""
    ---
    ### 📝 使用说明
    
    **功能特点**:
    - 🎯 **智能问答**: 基于上传的知识库内容进行精准回答
    - 🎤 **语音输入**: 支持麦克风语音输入，提升用户体验  
    - 🔄 **多轮对话**: 支持上下文理解和连续对话
    - 📱 **响应式设计**: 自适应不同设备屏幕
    
    **集成步骤**:
    1. 复制上方的iframe代码
    2. 粘贴到您的HTML页面中
    3. 根据需要调整宽度和高度
    4. 确保网站支持iframe嵌入
    
    **注意事项**:
    - 需要网络连接才能正常使用
    - 建议在HTTPS环境下使用以支持麦克风功能
    - 可根据页面布局调整iframe尺寸
    """)


def show_api_testing(api_key, endpoint):
    """显示API接口测试"""
    st.subheader("🔧 API接口测试")
    
    st.info("🧪 **API测试**: 测试问答API的连接和响应")
    
    # 测试问题
    test_question = st.text_area(
        "测试问题",
        value="项目中使用了哪些技术栈？",
        help="输入测试问题来验证API响应"
    )
    
    if st.button("🚀 测试API", type="primary"):
        if test_question:
            with st.spinner("正在调用API..."):
                try:
                    response = call_qa_api(api_key, endpoint, test_question)
                    
                    st.success("✅ API调用成功！")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📤 请求信息")
                        st.json({
                            "question": test_question,
                            "api_key": f"{api_key[:8]}...{api_key[-8:]}",
                            "endpoint": endpoint
                        })
                    
                    with col2:
                        st.subheader("📥 响应结果")
                        st.markdown(response)
                        
                except Exception as e:
                    st.error(f"❌ API调用失败: {str(e)}")
        else:
            st.warning("⚠️ 请输入测试问题")


def call_qa_api(api_key, endpoint, question):
    """调用问答API"""
    try:
        from .api_clients import GPTBotsAPI
        
        client = GPTBotsAPI(api_key, endpoint=endpoint)
        result = client.call_agent(question)
        
        if result and "output" in result:
            # 提取响应内容
            content = ""
            for output_item in result.get("output", []):
                if "content" in output_item:
                    content_obj = output_item["content"]
                    if "text" in content_obj:
                        content += content_obj["text"] + "\n"
            return content.strip() if content else "抱歉，无法获取回答。"
        else:
            return "抱歉，API响应格式异常。"
            
    except Exception as e:
        return f"API调用出错: {str(e)}"


