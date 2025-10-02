# 🚀 快速上手指南

恭喜！您的 AI 聊天機器人系統已經成功部署。以下是使用指南：

## 📍 當前狀態

✅ **系統已啟動**: 應用程式正在 `http://localhost:5001` 運行  
✅ **資料庫已初始化**: SQLite 資料庫已創建並可正常使用  
✅ **API 測試通過**: 所有 REST API 端點工作正常  
✅ **WebSocket 就緒**: 即時通訊功能已準備就緒  

## 🌐 立即使用

1. **打開瀏覽器** 訪問: http://localhost:5001
2. **點擊「新對話」** 開始您的第一次對話
3. **輸入訊息** 並按 Enter 發送

## ⚠️ 重要提醒

**LLM API 連接**: 請確保您的 LLM 服務器正在 `http://203.145.216.159:52843` 運行。如果無法連接，聊天功能將無法正常工作。

## 🎮 功能亮點

### 💬 智能對話
- 支援 Markdown 格式回應
- 程式碼語法高亮
- 自動保存對話歷史

### 📱 響應式介面
- 適配桌面和行動裝置
- 深色/淺色主題切換
- 直觀的操作介面

### 🗂️ 會話管理
- 無限制創建對話
- 重命名和刪除對話
- 清空對話記錄

### ⚡ 即時體驗
- WebSocket 即時通訊
- 打字指示器
- 無刷新頁面操作

## 🔧 系統管理

### 停止應用程式
```bash
# 在運行應用程式的終端按 Ctrl+C
# 或者使用以下命令找到並終止進程
ps aux | grep python
kill -9 <process_id>
```

### 重新啟動
```bash
./start.sh
# 或
conda activate chatbot-env
python app.py
```

### 備份資料
```bash
# 備份對話資料
cp database/chatbot.db database/chatbot_backup_$(date +%Y%m%d).db
```

## 📊 使用統計

執行測試腳本查看系統狀態：
```bash
python test_system.py
```

## 🎯 接下來可以做什麼

1. **測試對話功能**: 確保 LLM API 正常連接後進行實際對話測試
2. **自定義配置**: 修改 `.env` 文件調整 AI 參數
3. **主題定制**: 修改 CSS 文件自定義介面外觀
4. **部署到生產環境**: 使用 Gunicorn 或 uWSGI 部署

## 📞 需要幫助？

- 查看詳細文檔: `README.md`
- 運行系統測試: `python test_system.py`
- 檢查日誌: 查看終端輸出

---

**現在就開始與您的 AI 助手對話吧！** 🤖✨

訪問: http://localhost:5001