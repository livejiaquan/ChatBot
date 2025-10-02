#!/bin/bash

# 啟動腳本 - 自動激活 conda 環境並運行應用程式

echo "🤖 正在啟動 AI 聊天機器人..."

# 檢查 conda 是否已安裝
if ! command -v conda &> /dev/null; then
    echo "❌ 錯誤: 未找到 conda。請先安裝 Miniconda 或 Anaconda。"
    exit 1
fi

# 激活 conda 環境
echo "📦 激活 conda 環境..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate chatbot-env

if [ $? -ne 0 ]; then
    echo "❌ 錯誤: 無法激活 chatbot-env 環境。請確保環境已正確創建。"
    exit 1
fi

echo "✅ 環境已激活"

# 檢查依賴是否已安裝
echo "🔍 檢查依賴..."
python -c "import flask, requests, sqlalchemy" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "📦 安裝依賴..."
    pip install -r requirements.txt
fi

# 創建資料庫目錄
if [ ! -d "database" ]; then
    echo "📁 創建資料庫目錄..."
    mkdir -p database
fi

echo "🚀 啟動應用程式..."
echo "🌐 應用程式將在 http://localhost:5001 上運行"
echo "⚠️  請確保您的 LLM API 服務器正在運行，並在 .env 檔案中正確配置"
echo ""

# 啟動應用程式
python app.py