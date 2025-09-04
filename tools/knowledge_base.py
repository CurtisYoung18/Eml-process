"""
知识库管理模块
处理知识库上传和管理功能
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from .utils import count_files, log_activity


def show_knowledge_base_page():
    """显示知识库管理页面"""
    from app import CONFIG
    
    st.header("知识库管理")
    
    # 检查是否有LLM处理后的文件
    final_files = count_files(CONFIG["final_dir"], "*.md")
    
    if final_files == 0:
        st.warning("⚠️ 未发现LLM处理后的文件，请先完成前面的处理步骤。")
        st.info("💡 需要先完成：邮件上传 → 数据清洗 → LLM处理，然后才能上传到知识库")
        return
    
    st.success(f"✅ 发现 {final_files} 个LLM处理后的文件可上传到知识库")
    
    # API配置区域
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
            help="选择GPTBots API数据中心节点",
            key="kb_endpoint"
        )
    
    with col2:
        # API Key选择器
        from .api_selector import create_api_selector_with_guide
        api_key, key_number = create_api_selector_with_guide(
            purpose="knowledge_base",
            key_prefix="kb_management",
            show_guide=True
        )
        
        if not api_key:
            st.warning("⚠️ 请配置知识库API Key")
            st.info("💡 请在.env文件中配置GPTBOTS_KB_API_KEY_1等环境变量")
            return
        
        # 显示API Key用途说明
        with st.expander("💡 API Key用途说明"):
            st.markdown("""
            **知识库API Key用途:**
            - 📋 获取知识库列表
            - 📤 批量上传文档到知识库
            - 🔍 查询文档状态
            - 📊 管理知识库内容
            
            **注意**: 此API Key也可以用于后续的问答功能
            """)
    
    # 获取知识库列表
    st.subheader("📋 知识库列表")
    if st.button("🔄 刷新知识库列表", key="get_kb_list_btn"):
        st.session_state.knowledge_bases = get_knowledge_base_list(api_key, endpoint)
    
    st.markdown("---")
    
    # 上传配置区域
    st.subheader("⚙️ 上传配置")
    
    # 知识库选择
    if 'knowledge_bases' not in st.session_state:
        st.session_state.knowledge_bases = []
    
    if st.session_state.knowledge_bases:
        # 构建知识库选项
        kb_options = [{"name": "默认知识库", "id": ""}]  # 默认选项
        kb_options.extend([
            {"name": f"{kb['name']} ({kb['id'][:8]}...)", "id": kb['id']} 
            for kb in st.session_state.knowledge_bases
        ])
        
        selected_kb_index = st.selectbox(
            "选择目标知识库",
            range(len(kb_options)),
            format_func=lambda x: kb_options[x]["name"],
            help="选择要上传文件的目标知识库",
            key="kb_selection"
        )
        knowledge_base_id = kb_options[selected_kb_index]["id"]
    else:
        st.info("💡 请先点击上方的'刷新知识库列表'按钮获取可用的知识库")
        knowledge_base_id = ""
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        # 分块方式选择
        chunk_method = st.radio(
            "分块方式",
            ["按Token数分块", "按分隔符分块"],
            help="选择文档分块方式",
            key="chunk_method"
        )
        
        if chunk_method == "按Token数分块":
            chunk_token = st.number_input(
                "分块Token数",
                min_value=1,
                max_value=1000,
                value=600,
                help="单个知识块的最大Token数",
                key="chunk_token"
            )
            splitter = None
        else:
            splitter = st.text_input(
                "分隔符",
                value="\\n",
                help="使用自定义分隔符进行分块",
                key="splitter"
            )
            # 处理转义字符
            if splitter == "\\n":
                splitter = "\n"
            elif splitter == "\\t":
                splitter = "\t"
            chunk_token = None
    
    with col_config2:
        # 文件选择选项
        st.write("**文件选择**")
        
        upload_all_files = st.checkbox(
            "上传所有文件",
            value=True,
            help="上传final_output目录中的所有Markdown文件",
            key="upload_all"
        )
        
        if not upload_all_files:
            # 文件选择器
            final_dir = Path(CONFIG["final_dir"])
            if final_dir.exists():
                md_files = [f.name for f in final_dir.glob("*.md")]
                selected_files = st.multiselect(
                    "选择要上传的文件",
                    options=md_files,
                    default=md_files[:5] if len(md_files) > 5 else md_files,
                    help="选择特定文件进行上传",
                    key="selected_files"
                )
            else:
                selected_files = []
                st.error("final_output目录不存在")
    
    # 高级选项
    with st.expander("🔧 高级选项", expanded=False):
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            # 错误处理选项
            continue_on_error = st.checkbox(
                "遇到错误时继续",
                value=True,
                help="单个文件失败时继续处理其他文件",
                key="continue_on_error"
            )
            
            # 备份选项
            create_backup = st.checkbox(
                "创建上传记录",
                value=True,
                help="保存上传结果记录到文件",
                key="create_backup"
            )
        
        with col_adv2:
            # 重试选项
            max_retries = st.number_input(
                "最大重试次数",
                min_value=0,
                max_value=5,
                value=3,
                help="API调用失败时的重试次数",
                key="max_retries"
            )
    
    # 开始上传按钮
    st.markdown("---")
    st.subheader("🚀 开始上传")
    
    # 显示上传预览
    if upload_all_files:
        st.info(f"📊 将上传 {final_files} 个文件到知识库")
    else:
        selected_count = len(selected_files) if 'selected_files' in locals() else 0
        st.info(f"📊 将上传 {selected_count} 个选中的文件到知识库")
    
    # 上传按钮
    if st.button("🚀 开始上传到知识库", type="primary", key="start_kb_upload"):
        # 准备上传参数
        upload_params = {
            "api_key": api_key,
            "endpoint": endpoint,
            "knowledge_base_id": knowledge_base_id if knowledge_base_id else None,
            "chunk_token": chunk_token,
            "splitter": splitter,
            "continue_on_error": continue_on_error,
            "max_retries": max_retries,
            "create_backup": create_backup,
            "selected_files": selected_files if not upload_all_files and 'selected_files' in locals() else None
        }
        
        # 开始上传
        start_knowledge_base_upload(CONFIG, **upload_params)
    
    # 导航按钮
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 上一步", help="返回结果查看页面", key="kb_prev_btn"):
            st.session_state.current_step = "结果查看"
            st.rerun()
    with col3:
        if st.button("➡️ 下一步", help="前往问答系统", key="kb_next_btn"):
            st.session_state.current_step = "问答系统"
            st.rerun()


def get_knowledge_base_list(api_key, endpoint):
    """获取并显示知识库列表"""
    st.info("🔄 正在获取知识库列表...")
    
    try:
        from .api_clients import KnowledgeBaseAPI
        
        client = KnowledgeBaseAPI(api_key, endpoint=endpoint)
        result = client.get_knowledge_bases()
        
        if result and "knowledge_base" in result:
            knowledge_bases = result["knowledge_base"]
            
            if knowledge_bases:
                st.success(f"✅ 成功获取 {len(knowledge_bases)} 个知识库")
                
                # 显示知识库列表
                kb_data = []
                for kb in knowledge_bases:
                    kb_data.append({
                        "知识库ID": kb.get("id", "")[:12] + "..." if len(kb.get("id", "")) > 12 else kb.get("id", ""),
                        "名称": kb.get("name", ""),
                        "描述": kb.get("desc", "")[:50] + "..." if len(kb.get("desc", "")) > 50 else kb.get("desc", ""),
                        "文档数": kb.get("doc", 0),
                        "知识块数": kb.get("chunk", 0),
                        "Token数": kb.get("token", 0)
                    })
                
                st.dataframe(pd.DataFrame(kb_data), width='stretch')
                return knowledge_bases
            else:
                st.warning("⚠️ 未发现任何知识库")
                return []
                
        elif result and "error" in result:
            st.error(f"❌ 获取知识库列表失败: {result['message']}")
            return []
        else:
            st.error("❌ 获取知识库列表失败")
            return []
            
    except Exception as e:
        st.error(f"❌ 获取知识库列表出错: {str(e)}")
        return []


def start_knowledge_base_upload(config, **params):
    """开始知识库上传"""
    st.info("🚀 开始上传文件到知识库...")
    log_activity("开始知识库上传")
    
    # 创建进度条和状态显示
    progress_bar = st.progress(0)
    status_text = st.empty()
    result_container = st.empty()
    
    try:
        from .api_clients import KnowledgeBaseAPI
        
        # 初始化API客户端
        status_text.text("🔍 初始化知识库API客户端...")
        client = KnowledgeBaseAPI(params["api_key"], endpoint=params["endpoint"])
        
        # 确定要上传的文件
        final_dir = Path(config["final_dir"])
        if params["selected_files"]:
            # 上传选中的文件
            files_to_upload = [final_dir / filename for filename in params["selected_files"]]
        else:
            # 上传所有文件
            files_to_upload = list(final_dir.glob("*.md"))
        
        if not files_to_upload:
            st.error("❌ 没有找到要上传的文件")
            return
        
        progress_bar.progress(10)
        status_text.text(f"📧 准备上传 {len(files_to_upload)} 个文件...")
        
        # 使用批量上传功能
        upload_result = client.upload_markdown_files_from_directory(
            directory_path=str(final_dir),
            knowledge_base_id=params["knowledge_base_id"],
            chunk_token=params["chunk_token"] or 600,
            splitter=params["splitter"],
            batch_size=10  # 使用固定的批次大小
        )
        
        progress_bar.progress(90)
        status_text.text("📝 处理上传结果...")
        
        if "error" not in upload_result:
            progress_bar.progress(100)
            status_text.empty()
            
            # 显示上传结果
            with result_container.container():
                st.success("🎉 知识库上传完成！")
                
                # 统计信息
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("总文件数", upload_result["total_files"])
                
                with col2:
                    st.metric("上传成功", upload_result["successful_uploads"])
                
                with col3:
                    st.metric("上传失败", upload_result["failed_uploads"])
                
                with col4:
                    st.metric("处理批次", upload_result["batches_processed"])
                
                # 成功上传的文件
                if upload_result["uploaded_files"]:
                    st.subheader("✅ 成功上传的文件")
                    success_data = []
                    for doc in upload_result["uploaded_files"]:
                        success_data.append({
                            "文档ID": doc.get("doc_id", ""),
                            "文档名称": doc.get("doc_name", "")
                        })
                    
                    if success_data:
                        st.dataframe(pd.DataFrame(success_data))
                
                # 失败的文件
                if upload_result["failed_files"]:
                    st.subheader("❌ 上传失败的文件")
                    for failed in upload_result["failed_files"]:
                        st.error(f"{failed['file_name']}: {failed['error']}")
                
                # 保存上传记录
                if params["create_backup"]:
                    backup_filename = f"kb_upload_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    backup_path = Path(config["final_dir"]) / backup_filename
                    
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        json.dump(upload_result, f, indent=2, ensure_ascii=False)
                    
                    st.info(f"📄 上传记录已保存到: {backup_filename}")
                
                log_activity(f"知识库上传完成: {upload_result['successful_uploads']}/{upload_result['total_files']} 成功")
        
        else:
            progress_bar.progress(0)
            status_text.empty()
            result_container.error(f"❌ 上传失败: {upload_result['error']}")
            log_activity(f"知识库上传失败: {upload_result['error']}")
    
    except Exception as e:
        progress_bar.progress(0)
        status_text.empty()
        result_container.error(f"❌ 上传过程中发生错误: {str(e)}")
        log_activity(f"知识库上传错误: {str(e)}")
        st.exception(e)
