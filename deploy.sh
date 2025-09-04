#!/bin/bash
# 部署脚本 - 支持多种云平台

set -e

echo "🚀 邮件处理平台部署脚本"
echo "========================"

# 检查是否存在必要文件
if [ ! -f "requirements.txt" ]; then
    echo "❌ 缺少 requirements.txt 文件"
    exit 1
fi

if [ ! -f "app.py" ]; then
    echo "❌ 缺少 app.py 文件"
    exit 1
fi

# 选择部署平台
echo "请选择部署平台:"
echo "1) Streamlit Cloud (免费)"
echo "2) Railway (推荐)"
echo "3) Google Cloud Run"
echo "4) Heroku"
echo "5) Docker 本地测试"

read -p "输入选择 (1-5): " choice

case $choice in
    1)
        echo "📝 Streamlit Cloud 部署指南:"
        echo "1. 将代码推送到 GitHub"
        echo "2. 访问 https://share.streamlit.io"
        echo "3. 连接 GitHub 仓库"
        echo "4. 配置环境变量"
        echo "5. 点击部署"
        ;;
    2)
        echo "🚂 Railway 部署..."
        if command -v railway &> /dev/null; then
            railway login
            railway init
            echo "📋 请在 Railway 控制台配置环境变量:"
            echo "- GPTBOTS_LLM_API_KEY_1"
            echo "- GPTBOTS_KB_API_KEY_1"
            echo "- GPTBOTS_QA_API_KEY_1"
            railway up
        else
            echo "❌ 请先安装 Railway CLI: npm install -g @railway/cli"
        fi
        ;;
    3)
        echo "☁️ Google Cloud Run 部署..."
        if command -v gcloud &> /dev/null; then
            PROJECT_ID=$(gcloud config get-value project)
            echo "构建 Docker 镜像..."
            docker build -t gcr.io/$PROJECT_ID/eml-processor .
            docker push gcr.io/$PROJECT_ID/eml-processor
            
            echo "部署到 Cloud Run..."
            gcloud run deploy eml-processor \
                --image gcr.io/$PROJECT_ID/eml-processor \
                --region asia-east1 \
                --allow-unauthenticated \
                --port 8501 \
                --memory 1Gi \
                --cpu 1
        else
            echo "❌ 请先安装 Google Cloud CLI"
        fi
        ;;
    4)
        echo "🟣 Heroku 部署..."
        if command -v heroku &> /dev/null; then
            heroku create eml-processor-$(date +%s)
            heroku config:set \
                GPTBOTS_LLM_API_KEY_1=your_llm_key \
                GPTBOTS_KB_API_KEY_1=your_kb_key \
                GPTBOTS_QA_API_KEY_1=your_qa_key
            git push heroku main
        else
            echo "❌ 请先安装 Heroku CLI"
        fi
        ;;
    5)
        echo "🐳 Docker 本地测试..."
        echo "构建镜像..."
        docker build -t eml-processor .
        
        echo "启动容器..."
        docker run -p 8501:8501 \
            -e GPTBOTS_LLM_API_KEY_1=your_llm_key \
            -e GPTBOTS_KB_API_KEY_1=your_kb_key \
            -e GPTBOTS_QA_API_KEY_1=your_qa_key \
            eml-processor
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo "✅ 部署脚本执行完成!"
