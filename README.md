# 🤖 AI 聊天機器人系統

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)

基於自建 LLM API 的智能聊天機器人，提供類似 ChatGPT 的對話體驗。支援即時通訊、對話管理、主題切換等功能。

## ✨ 功能特色

- 🎯 **即時對話**: 基於 WebSocket 的即時聊天體驗
- 💾 **對話記憶**: 完整的對話歷史儲存和恢復
- 📱 **響應式設計**: 支援桌面和行動裝置
- 🌙 **主題切換**: 深色/淺色主題
- 📝 **Markdown 支援**: 支援程式碼高亮和格式化
- 🗂️ **會話管理**: 創建、重命名、刪除對話
- ⚡ **高效能**: 優化的 API 整合和資料庫設計
- 🔒 **安全性**: 環境變數配置，API 金鑰保護

## 🏗️ 技術架構

- **後端**: Flask + Flask-SocketIO
- **前端**: HTML5 + CSS3 + JavaScript (原生)
- **資料庫**: SQLite + SQLAlchemy ORM
- **即時通訊**: WebSocket
- **LLM 整合**: RESTful API

## 📋 系統需求

- Python 3.9+
- Conda 環境管理器（推薦）或 pip
- 現代瀏覽器 (Chrome, Firefox, Safari, Edge)
- LLM API 服務器（支援 OpenAI API 格式）

## 🚀 快速開始

### 1. 克隆專案

```bash
git clone https://github.com/livejiaquan/ChatBot.git
cd ChatBot
```

### 2. 環境設置

#### 使用 Conda（推薦）

```bash
# 創建並激活 conda 環境
conda create -n chatbot-env python=3.9 -y
conda activate chatbot-env

# 安裝依賴
pip install -r requirements.txt
```

#### 使用 pip

```bash
# 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt
```

### 3. 配置設定

複製環境變數範例檔案並進行配置：

```bash
cp .env.example .env
```

編輯 `.env` 文件：

```env
# LLM API 配置
LLM_API_URL=http://your-llm-server:port/v1/chat/completions
LLM_MODEL=./your-model-name
LLM_API_KEY=your-api-key-here

# Flask 配置
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# 資料庫配置
DATABASE_URL=sqlite:///database/chatbot.db

# 聊天配置
MAX_TOKENS=2000
TEMPERATURE=0.7
MAX_CONVERSATION_LENGTH=20
```

### 4. 啟動應用

#### 方法一：使用啟動腳本（推薦）

```bash
chmod +x start.sh
./start.sh
```

#### 方法二：手動啟動

```bash
# 確保環境已激活
conda activate chatbot-env  # 或 source venv/bin/activate

# 啟動應用
python app.py
```

### 5. 訪問應用

打開瀏覽器訪問：`http://localhost:5001`

## 📂 專案結構

```
chatbot/
├── README.md                 # 專案說明
├── LICENSE                   # 授權協議
├── requirements.txt          # Python 依賴
├── .env.example             # 環境變數範例
├── .gitignore               # Git 忽略檔案
├── start.sh                 # 啟動腳本
├── app.py                   # 主應用程式
├── llm_client.py            # LLM API 客戶端
├── config/
│   └── config.py            # 配置管理
├── database/
│   ├── models.py            # 資料庫模型
│   └── chatbot.db          # SQLite 資料庫（自動創建）
├── static/
│   ├── css/
│   │   └── style.css        # 樣式文件
│   ├── js/
│   │   └── app.js           # 前端邏輯
│   └── images/              # 圖片資源
├── templates/
│   └── index.html           # 主頁面模板
└── tests/                   # 測試檔案
    ├── test_system.py       # 系統測試
    ├── test_llm_api.py      # LLM API 測試
    └── ...                  # 其他測試檔案
```

## 🎮 使用說明

### 基本操作

1. **創建新對話**: 點擊左側邊欄的「新對話」按鈕
2. **發送訊息**: 在輸入框中輸入訊息，按 Enter 發送
3. **查看歷史**: 點擊左側對話列表查看歷史對話
4. **重命名對話**: 點擊對話旁的編輯按鈕或頂部工具欄的重命名按鈕
5. **刪除對話**: 點擊對話旁的刪除按鈕
6. **清空對話**: 點擊頂部工具欄的清空按鈕

### 快捷鍵

- `Enter`: 發送訊息
- `Shift + Enter`: 換行
- `Esc`: 關閉模態框

### 主題切換

點擊左側邊欄底部的主題切換按鈕在深色和淺色主題之間切換。

## 🔧 進階配置

### LLM API 參數調整

在 `.env` 文件中調整以下參數：

- `MAX_TOKENS`: 最大回應長度（默認：2000）
- `TEMPERATURE`: 創造性程度（0.0-1.0，默認：0.7）
- `MAX_CONVERSATION_LENGTH`: 對話長度限制（默認：20）

### 生產環境部署

1. 修改 `.env` 中的配置：
   ```env
   SECRET_KEY=your-random-production-secret-key
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

2. 使用 Gunicorn 部署：
   ```bash
   pip install gunicorn
   gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5001 app:app
   ```

3. 使用 Nginx 反向代理（可選）：
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /socket.io {
           proxy_pass http://127.0.0.1:5001/socket.io;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

## 🔌 API 端點

### REST API

- `GET /api/conversations` - 獲取對話列表
- `POST /api/conversations` - 創建新對話
- `GET /api/conversations/{id}` - 獲取對話訊息
- `DELETE /api/conversations/{id}` - 刪除對話
- `PUT /api/conversations/{id}/title` - 更新對話標題
- `POST /api/conversations/{id}/clear` - 清空對話
- `POST /api/chat` - 發送聊天訊息
- `GET /api/status` - 獲取系統狀態

### WebSocket 事件

- `connect` - 客戶端連接
- `disconnect` - 客戶端斷線
- `join_conversation` - 加入對話房間
- `leave_conversation` - 離開對話房間
- `send_message` - 發送訊息
- `new_message` - 新訊息通知
- `typing` - 正在輸入狀態

## 🧪 測試

運行測試套件：

```bash
# 系統測試
python tests/test_system.py

# LLM API 測試
python tests/test_llm_api.py

# 繁體中文測試
python tests/test_traditional_chinese.py
```

## 🐛 故障排除

### 常見問題

1. **無法連接到 LLM API**
   - 檢查 API 服務器是否運行
   - 確認 `.env` 中的 `LLM_API_URL` 和 `LLM_API_KEY` 設定正確
   - 檢查網路連接和防火牆設定

2. **資料庫錯誤**
   - 確保 `database` 目錄存在且有寫入權限
   - 刪除 `database/chatbot.db` 重新創建
   - 檢查 SQLite 版本

3. **依賴安裝失敗**
   - 確保 Python 版本為 3.9+
   - 嘗試升級 pip：`pip install --upgrade pip`
   - 使用國內鏡像：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/`

4. **WebSocket 連接失敗**
   - 檢查防火牆設定
   - 確認瀏覽器支援 WebSocket
   - 檢查代理服務器配置

5. **環境變數問題**
   - 確保 `.env` 檔案存在且格式正確
   - 檢查檔案權限
   - 重新啟動應用程式

### 調試模式

啟用調試模式查看詳細錯誤訊息：

```bash
export FLASK_DEBUG=True
python app.py
```

### 日誌查看

應用程式會輸出詳細的日誌資訊，包括：
- API 請求狀態
- 資料庫操作
- WebSocket 連接狀態

## 📄 授權協議

本專案採用 MIT 授權協議 - 詳見 [LICENSE](LICENSE) 文件

## 🙏 致謝

- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [Socket.IO](https://socket.io/) - 即時通訊
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
- [Marked.js](https://marked.js.org/) - Markdown 解析
- [Highlight.js](https://highlightjs.org/) - 程式碼高亮
- [Font Awesome](https://fontawesome.com/) - 圖標庫

## 📞 聯絡

- GitHub: https://github.com/livejiaquan/ChatBot
- Email: livejiaquan010313@gmail.com

## 📊 專案狀態

- ✅ 基本聊天功能
- ✅ 對話管理
- ✅ WebSocket 即時通訊
- ✅ 主題切換
- ✅ Markdown 支援
- 🚧 多語言支援（開發中）
- 🚧 語音輸入（計劃中）
- 🚧 檔案上傳（計劃中）

---