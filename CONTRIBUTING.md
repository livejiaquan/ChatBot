# 📝 貢獻指南

感謝您對 AI 聊天機器人專案的貢獻興趣！本文檔將引導您完成貢獻流程。

## 🤝 如何貢獻

### 回報 Bug

1. 搜尋現有的 [Issues](https://github.com/your-username/chatbot/issues) 確認問題尚未被回報
2. 使用 Bug 回報模板創建新的 Issue
3. 提供詳細的問題描述，包括：
   - 系統環境（OS、Python 版本等）
   - 重現步驟
   - 預期行為
   - 實際行為
   - 錯誤訊息和截圖

### 提出功能建議

1. 搜尋現有的 Issues 確認功能尚未被提出
2. 創建新的 Feature Request
3. 詳細描述：
   - 功能的使用場景
   - 預期的實現方式
   - 可能的替代方案

### 提交代碼

1. **Fork 專案**
   ```bash
   # 點擊 GitHub 上的 Fork 按鈕
   git clone https://github.com/your-username/chatbot.git
   cd chatbot
   ```

2. **設置開發環境**
   ```bash
   # 創建開發環境
   conda create -n chatbot-dev python=3.9 -y
   conda activate chatbot-dev
   
   # 安裝依賴（包括開發依賴）
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # 如果存在
   
   # 配置環境變數
   cp .env.example .env
   # 編輯 .env 文件
   ```

3. **創建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

4. **進行開發**
   - 遵循代碼風格指南
   - 添加必要的測試
   - 更新相關文檔

5. **測試您的更改**
   ```bash
   # 運行現有測試
   python -m pytest tests/
   
   # 運行安全檢查
   ./security_check.sh
   
   # 運行代碼格式檢查
   flake8 .
   black . --check
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "類型: 簡短描述
   
   詳細描述更改內容..."
   ```

7. **推送並創建 Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   
   然後在 GitHub 上創建 Pull Request。

## 📝 代碼規範

### Python 代碼風格

我們遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 風格指南：

```python
# 好的例子
def calculate_response_time(start_time, end_time):
    """計算回應時間。
    
    Args:
        start_time (datetime): 開始時間
        end_time (datetime): 結束時間
        
    Returns:
        float: 回應時間（秒）
    """
    return (end_time - start_time).total_seconds()

# 避免
def calc_resp_time(s,e):
    return (e-s).total_seconds()
```

### 提交訊息格式

使用以下格式：

```
類型: 簡短描述（50 個字元以內）

更詳細的解釋（如果需要）。說明為什麼做這個更改，
而不只是做了什麼。

- 項目符號也可以使用
- 通常用連字號或星號，前面有空格

修復 #123
```

**類型：**
- `feat`: 新功能
- `fix`: Bug 修復
- `docs`: 文檔更改
- `style`: 代碼格式（不影響功能）
- `refactor`: 重構代碼
- `test`: 添加或修改測試
- `chore`: 建構過程或輔助工具更改

### 分支命名

- `feature/功能名稱` - 新功能
- `fix/問題描述` - Bug 修復
- `docs/文檔類型` - 文檔更新
- `refactor/重構描述` - 代碼重構

## 🧪 測試指南

### 運行測試

```bash
# 運行所有測試
python -m pytest tests/ -v

# 運行特定測試
python -m pytest tests/test_system.py -v

# 運行測試並生成覆蓋率報告
python -m pytest tests/ --cov=. --cov-report=html
```

### 編寫測試

1. **單元測試**
   ```python
   import unittest
   from your_module import YourClass

   class TestYourClass(unittest.TestCase):
       def setUp(self):
           self.instance = YourClass()

       def test_method_returns_expected_value(self):
           result = self.instance.method()
           self.assertEqual(result, expected_value)
   ```

2. **集成測試**
   ```python
   def test_api_endpoint():
       response = client.get('/api/conversations')
       assert response.status_code == 200
       assert response.json['success'] is True
   ```

## 📚 文檔更新

### README 更新

- 新功能需要在 README 中記錄
- 更新安裝說明（如果需要）
- 添加使用範例

### API 文檔

- 新的 API 端點需要在 README 中記錄
- 包括請求/回應格式
- 提供使用範例

### 代碼註釋

```python
def complex_function(param1, param2):
    """函數的簡短描述。
    
    更詳細的描述（如果需要）。
    
    Args:
        param1 (str): 參數描述
        param2 (int): 參數描述
        
    Returns:
        dict: 回傳值描述
        
    Raises:
        ValueError: 何時會拋出此異常
    """
    pass
```

## 🔍 代碼審查

### Pull Request 檢查清單

提交 PR 前請確認：

- [ ] 代碼遵循專案風格指南
- [ ] 添加了適當的測試
- [ ] 所有測試都通過
- [ ] 更新了相關文檔
- [ ] 通過了安全檢查
- [ ] 提交訊息清晰明確
- [ ] 沒有合併衝突

### 審查標準

我們會檢查：

1. **功能性**: 代碼是否按預期工作？
2. **可讀性**: 代碼是否易於理解？
3. **效能**: 是否有效能問題？
4. **安全性**: 是否有安全漏洞？
5. **測試**: 測試覆蓋是否充分？
6. **文檔**: 是否需要更新文檔？

## 🎯 優先級項目

我們特別歡迎以下方面的貢獻：

### 高優先級
- [ ] 單元測試覆蓋率提升
- [ ] 效能優化
- [ ] 安全性增強
- [ ] 多語言支援

### 中優先級
- [ ] UI/UX 改進
- [ ] 新功能開發
- [ ] 文檔改進
- [ ] 錯誤處理增強

### 低優先級
- [ ] 代碼重構
- [ ] 開發工具改進
- [ ] 範例應用

## 🏷️ Issue 標籤

- `good first issue`: 適合新貢獻者
- `help wanted`: 需要幫助
- `bug`: Bug 回報
- `enhancement`: 功能增強
- `documentation`: 文檔相關
- `question`: 問題討論

## 💬 社群

### 討論

- 使用 [GitHub Discussions](https://github.com/your-username/chatbot/discussions) 進行一般討論
- 技術問題請使用 Issues

### 行為準則

請遵循我們的行為準則：

1. **尊重**: 尊重所有參與者
2. **建設性**: 提供建設性的回饋
3. **包容**: 歡迎不同背景的貢獻者
4. **耐心**: 對新手保持耐心

## 🎉 致謝

感謝所有貢獻者的努力！您的貢獻將會被記錄在：

- CONTRIBUTORS.md 文件中
- GitHub 貢獻者頁面
- 版本發布說明中

## 📞 聯絡

如有任何問題，請：

1. 查看現有的 Issues 和 Discussions
2. 創建新的 Issue
3. 聯絡維護者：your-email@example.com

謝謝您的貢獻！ 🚀