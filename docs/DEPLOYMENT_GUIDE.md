# 🚀 邮件处理平台部署指南

本指南提供多种云端部署方案，适合不同需求和预算。

## 📋 部署前准备

### 1. 环境变量配置
```bash
# 必需的 API Keys
GPTBOTS_LLM_API_KEY_1=your_llm_api_key
GPTBOTS_KB_API_KEY_1=your_knowledge_base_api_key
GPTBOTS_QA_API_KEY_1=your_qa_api_key

# 可选配置
GPTBOTS_DEFAULT_ENDPOINT=sg
DEBUG=false
LOG_LEVEL=INFO
MAX_FILE_SIZE=50
BATCH_SIZE_LIMIT=200
```

### 2. 代码准备
```bash
# 确保所有依赖都在 requirements.txt 中
pip freeze > requirements.txt

# 提交最新代码
git add .
git commit -m "Ready for deployment"
git push origin main
```

## 🌟 推荐部署方案

### 方案一：Streamlit Cloud (免费，适合演示)

**优势：**
- ✅ 完全免费
- ✅ 零配置部署
- ✅ 与 GitHub 直接集成
- ✅ 自动 HTTPS
- ✅ 适合快速原型和演示

**限制：**
- ❌ 资源限制较严格
- ❌ 不适合高并发生产环境
- ❌ 文件存储不持久

**部署步骤：**
1. 推送代码到 GitHub 公开仓库
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 使用 GitHub 账号登录
4. 选择仓库和分支
5. 配置环境变量
6. 点击 "Deploy" 按钮

**环境变量配置：**
```
GPTBOTS_LLM_API_KEY_1 = your_llm_api_key
GPTBOTS_KB_API_KEY_1 = your_kb_api_key
GPTBOTS_QA_API_KEY_1 = your_qa_api_key
```

---

### 方案二：Railway (推荐，生产就绪)

**优势：**
- ✅ 简单易用
- ✅ 自动扩容
- ✅ 合理定价 ($5/月起)
- ✅ 支持持久存储
- ✅ 内置监控和日志

**部署步骤：**
```bash
# 1. 安装 Railway CLI
npm install -g @railway/cli

# 2. 登录
railway login

# 3. 初始化项目
railway init

# 4. 配置环境变量
railway variables set GPTBOTS_LLM_API_KEY_1=your_key
railway variables set GPTBOTS_KB_API_KEY_1=your_key
railway variables set GPTBOTS_QA_API_KEY_1=your_key

# 5. 部署
railway up
```

**定价：**
- 免费额度：每月 $5 额度
- 付费计划：$5/月起，按使用量计费

---

### 方案三：Google Cloud Run (企业级)

**优势：**
- ✅ 企业级稳定性
- ✅ 按需付费
- ✅ 自动扩容到零
- ✅ 全球 CDN
- ✅ 高级监控

**部署步骤：**
```bash
# 1. 设置项目
gcloud config set project YOUR_PROJECT_ID

# 2. 构建并推送镜像
docker build -t gcr.io/YOUR_PROJECT_ID/eml-processor .
docker push gcr.io/YOUR_PROJECT_ID/eml-processor

# 3. 部署到 Cloud Run
gcloud run deploy eml-processor \
    --image gcr.io/YOUR_PROJECT_ID/eml-processor \
    --region asia-east1 \
    --allow-unauthenticated \
    --port 8501 \
    --memory 2Gi \
    --cpu 2 \
    --set-env-vars GPTBOTS_LLM_API_KEY_1=your_key,GPTBOTS_KB_API_KEY_1=your_key
```

**定价：**
- 前 200 万请求免费
- 之后 $0.40/百万请求
- CPU: $0.00002400/vCPU-秒
- 内存: $0.00000250/GiB-秒

---

### 方案四：DigitalOcean App Platform

**优势：**
- ✅ 简单部署
- ✅ 预测性定价
- ✅ 集成数据库
- ✅ 自动 SSL

**部署步骤：**
1. 在 DigitalOcean 控制台创建新应用
2. 连接 GitHub 仓库
3. 选择 Python 构建包
4. 配置环境变量
5. 设置运行命令：`streamlit run app.py --server.headless true --server.address 0.0.0.0 --server.port 8080`

**定价：**
- 基础版：$5/月
- 专业版：$12/月

---

## 🐳 Docker 部署

### 本地测试
```bash
# 构建镜像
docker build -t eml-processor .

# 运行容器
docker run -p 8501:8501 \
    -e GPTBOTS_LLM_API_KEY_1=your_key \
    -e GPTBOTS_KB_API_KEY_1=your_key \
    -e GPTBOTS_QA_API_KEY_1=your_key \
    eml-processor
```

### 使用 Docker Compose
```bash
# 创建 .env 文件
cp env_example.txt .env
# 编辑 .env 文件配置 API Keys

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 🔧 生产环境优化

### 1. 性能优化
```python
# config/production.py
STREAMLIT_CONFIG = {
    "server.maxUploadSize": 200,  # MB
    "server.maxMessageSize": 200,  # MB
    "server.enableCORS": False,
    "server.enableXsrfProtection": True,
}
```

### 2. 安全配置
```bash
# 环境变量
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### 3. 监控和日志
```python
# 添加到 app.py
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

# 配置 Sentry (可选)
sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[LoggingIntegration()],
    traces_sample_rate=1.0,
)
```

## 📊 部署方案对比

| 方案 | 成本 | 难度 | 性能 | 扩展性 | 适用场景 |
|------|------|------|------|--------|----------|
| Streamlit Cloud | 免费 | ⭐ | ⭐⭐ | ⭐ | 演示、原型 |
| Railway | $5/月起 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 小到中型项目 |
| Google Cloud Run | 按需付费 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 企业级应用 |
| DigitalOcean | $5/月起 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 中小型企业 |

## 🚨 注意事项

### 1. API Key 安全
- ❌ 不要将 API Key 硬编码在代码中
- ✅ 使用环境变量
- ✅ 定期轮换 API Key
- ✅ 限制 API Key 权限

### 2. 文件存储
- 生产环境建议使用对象存储（如 AWS S3、Google Cloud Storage）
- 配置文件清理策略，避免磁盘空间不足

### 3. 监控和告警
```python
# 建议添加的监控指标
- API 调用成功率
- 文件处理时间
- 内存和 CPU 使用率
- 错误日志统计
```

## 🆘 故障排除

### 常见问题

**1. 内存不足**
```bash
# 解决方案：增加内存限制
docker run -m 2g eml-processor
```

**2. API 超时**
```python
# 增加超时时间
requests.post(url, timeout=300)
```

**3. 文件上传失败**
```python
# 检查文件大小限制
st.set_page_config(
    page_title="邮件处理平台",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

## 📞 技术支持

如需部署支持，请：
1. 查看应用日志
2. 检查环境变量配置
3. 验证 API Key 有效性
4. 联系技术支持团队

---

**推荐使用 Railway 进行生产部署，它提供了最佳的易用性和性能平衡。**
