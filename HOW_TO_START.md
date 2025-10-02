# 🚀 專案啟動指南

## 快速啟動（推薦）

在專案目錄中執行以下命令：

```bash
./start.sh
```

## 手動啟動步驟

### 1. 打開終端並進入專案目錄

```bash
cd /Users/jiaquan/Development/vllm/chatbot
```

### 2. 激活 conda 環境

```bash
# macOS/Linux
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
conda activate chatbot-env

# 或者如果已經初始化過 conda
conda activate chatbot-env
```

### 3. 確認環境正確

```bash
# 檢查 Python 版本
python --version  # 應該顯示 Python 3.9.x

# 檢查依賴
python -c "import flask, requests, sqlalchemy; print('✅ 依賴正常')"
```

### 4. 啟動應用程式

```bash
python app.py
```

## 📋 啟動檢查清單

- [ ] 終端已打開並在專案目錄中
- [ ] conda 環境已激活 (chatbot-env)
- [ ] Python 版本為 3.9.x
- [ ] 依賴套件已安裝
- [ ] LLM API 服務器在 http://203.145.216.159:52843 運行

## 🌐 訪問應用程式

啟動成功後，您會看到類似以下輸出：

```
* Serving Flask app 'app'
* Debug mode: on
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5001
* Running on http://192.168.125.109:5001
```

然後在瀏覽器中訪問：**http://localhost:5001**

## 🛠️ 故障排除

### 問題 1: conda 命令找不到
```bash
# 解決方案：添加 conda 到 PATH 或使用完整路徑
export PATH="/opt/homebrew/Caskroom/miniconda/base/bin:$PATH"
```

### 問題 2: 環境激活失敗
```bash
# 解決方案：初始化 conda
conda init bash  # 或 conda init zsh
# 然後重新打開終端
```

### 問題 3: 端口被佔用
```bash
# 檢查端口使用情況
lsof -i :5001
# 如果需要，修改 app.py 中的端口號
```

### 問題 4: 依賴缺失
```bash
# 重新安裝依賴
pip install -r requirements.txt
```

## 🧪 測試系統

啟動後，運行測試腳本驗證系統：

```bash
python test_system.py
```

## 🔄 重啟應用程式

要停止應用程式：
- 在運行應用程式的終端按 `Ctrl + C`

要重新啟動：
```bash
./start.sh
```

## 📞 獲取幫助

如果遇到問題：
1. 檢查終端錯誤訊息
2. 確認 LLM API 服務器狀態
3. 運行 `python test_system.py` 診斷問題
4. 查看 `README.md` 獲取更多資訊