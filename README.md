# 📧 邮件知识库管理系统

本项目是一个基于 Streamlit 的本地邮件处理与知识库管理平台，支持批量上传、清洗、AI结构化处理和结果管理。

---

## 🚀 快速部署指南

### 1. 克隆项目
```bash
git clone https://github.com/CurtisYoung18/Eml_process_platform.git
cd Eml_process_platform
```

### 2. 安装依赖
建议使用虚拟环境：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 配置 API Key
- 在项目根目录下创建 `.env` 文件（已自动生成模板）：
```
GPTBOTS_API_KEY=你的GPTBots_API_Key
```
- 默认会读取 `.env` 文件中的 `GPTBOTS_API_KEY`，如需更换可在界面临时输入。

### 4. 运行平台
推荐使用启动脚本：
```bash
python run_app.py
```
或直接运行：
```bash
streamlit run app.py
```

### 5. 访问界面
浏览器访问 [http://localhost:8501](http://localhost:8501)

---

## 📂 目录结构说明

- `app.py`              主应用入口
- `run_app.py`          启动脚本（自动检查依赖和目录）
- `requirements.txt`    依赖包列表
- `gptbots_api.py`      GPTBots API 封装
- `eml_process/`        邮件处理工作区（数据不上传）
- `Eml/`                示例邮件文件夹（数据不上传）
- `.env`                API Key 配置（不上传）

> **注意：** 邮件原始数据和处理结果均存放于 `Eml/` 和 `eml_process/` 下，这些目录已在 `.gitignore` 中自动忽略，不会上传到 GitHub。

---

## ⚙️ 主要配置项

- **API Key**：在 `.env` 文件中配置 `GPTBOTS_API_KEY`，或在界面手动输入。
- **上传目录**：`eml_process/uploads/`（存放原始 EML 邮件）
- **中间目录**：`eml_process/output/`（中间处理文件）
- **清洗结果**：`eml_process/processed/`（Markdown 格式）
- **最终结果**：`eml_process/final_output/`（LLM结构化结果）

如需修改目录，可在 `app.py` 顶部 `CONFIG` 字典中调整。

---

## 📝 推送到 GitHub

1. 初始化仓库（如未初始化）
```bash
git init
git add .
git commit -m "init project"
git branch -M main
git remote add origin https://github.com/CurtisYoung18/Eml_process_platform.git
git push -u origin main
```
2. 后续开发直接：
```bash
git add .
git commit -m "your message"
git push
```

---

## 🛡️ 隐私与数据安全
- 邮件数据、处理结果均为本地存储，**不会上传到云端或GitHub**。
- `.env`、`Eml/`、`eml_process/` 等敏感目录已自动忽略。

---

## 💡 常见问题
- Python 版本建议 >= 3.8
- 依赖安装失败请检查网络或更换 PyPI 源
- API Key 失效请联系 GPTBots 获取

---

## 📄 LICENSE
本项目仅供内部学习与交流使用。
