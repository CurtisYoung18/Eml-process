# 📧 邮件知识库管理系统

本项目是基于 Streamlit 的本地邮件处理与知识库管理平台，支持邮件上传、去重清洗、AI结构化处理与结果浏览。

---

## 🚀 快速部署指南

### 1. 环境准备
**如果没有安装 Python：**
- 访问 [Python官网](https://www.python.org/downloads/) 下载并安装 Python 3.8+
- 安装时勾选 "Add Python to PATH" 选项
- 验证安装：在命令行运行 `python --version`

### 2. 克隆代码
```bash
git clone https://github.com/CurtisYoung18/Eml_process_platform.git
cd Eml_process_platform
```

### 3. 创建虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 4. 安装依赖
```bash
pip install -r requirements.txt
```

### 5. 配置环境变量（API Key）
在项目根目录下创建 `.env` 文件（已自动生成，可直接修改）：
```
GPTBOTS_API_KEY=你的GPTBots_API_Key
```
> **注意**：API Key 仅存放于 .env 文件，切勿提交到 GitHub。

### 6. 启动应用
推荐使用启动脚本：
```bash
python run_app.py
```
或手动启动：
```bash
streamlit run app.py
```

### 7. 访问平台
浏览器打开 http://localhost:8501

---

## ⚙️ 主要配置项说明

所有主要配置均在 `app.py` 顶部的 `CONFIG` 字典中：
```python
CONFIG = {
    "app_title": "📧 邮件知识库管理系统",
    "version": "v1.0.0",
    "upload_dir": "eml_process/uploads",      # 上传目录
    "output_dir": "eml_process/output",       # 中间输出目录
    "processed_dir": "eml_process/processed", # 清洗结果目录
    "final_dir": "eml_process/final_output"   # LLM处理结果目录
}
```
如需更改邮件存放、输出等目录，直接修改此处路径。

### API Key 配置
- 默认从 `.env` 文件读取 `GPTBOTS_API_KEY`。
- 也可在界面手动输入临时 Key（仅本次会话有效）。

---

## 📁 目录结构简述

```
Eml_process_platform/
├── app.py                # 主应用入口
├── run_app.py            # 启动脚本
├── requirements.txt      # 依赖列表
├── .env                  # API Key（需手动配置）
├── eml_process/          # 邮件数据与处理结果（已被 .gitignore 忽略）
│   ├── uploads/          # 上传邮件
│   ├── output/           # 中间文件
│   ├── processed/        # 清洗后Markdown
│   └── final_output/     # LLM处理结果
├── Eml/                  # 示例邮件（不上传）
├── venv_new/             # 虚拟环境（不上传）
└── ...
```

---

## 🛠️ 常见问题

- **如何更换API Key？**
  - 修改 `.env` 文件中的 `GPTBOTS_API_KEY`，重启应用即可。
- **如何更改邮件/结果存放目录？**
  - 修改 `app.py` 顶部 `CONFIG` 字典中的路径。
---

## 📄 许可证

本项目仅供内部学习与交流，禁止商业用途。