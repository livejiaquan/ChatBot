#!/usr/bin/env python3
"""
簡單的測試腳本來驗證聊天機器人系統的基本功能
注意：這個測試不會實際調用 LLM API，只測試系統架構
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5001"

def test_api():
    """測試 API 端點"""
    print("🧪 開始測試 API...")
    
    # 測試獲取對話列表
    print("📋 測試獲取對話列表...")
    response = requests.get(f"{BASE_URL}/api/conversations")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✅ 找到 {len(data['conversations'])} 個對話")
        else:
            print("❌ 獲取對話失敗")
            return False
    else:
        print(f"❌ API 請求失敗: {response.status_code}")
        return False
    
    # 測試創建新對話
    print("➕ 測試創建新對話...")
    response = requests.post(f"{BASE_URL}/api/conversations", 
                           json={"title": "API 測試對話"})
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            conversation_id = data['conversation_id']
            print(f"✅ 創建對話成功，ID: {conversation_id}")
        else:
            print("❌ 創建對話失敗")
            return False
    else:
        print(f"❌ 創建對話失敗: {response.status_code}")
        return False
    
    # 測試獲取對話訊息
    print("💬 測試獲取對話訊息...")
    response = requests.get(f"{BASE_URL}/api/conversations/{conversation_id}")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✅ 獲取到 {len(data['messages'])} 則訊息")
        else:
            print("❌ 獲取訊息失敗")
            return False
    else:
        print(f"❌ 獲取訊息失敗: {response.status_code}")
        return False
    
    # 測試重命名對話
    print("✏️ 測試重命名對話...")
    response = requests.put(f"{BASE_URL}/api/conversations/{conversation_id}/title",
                          json={"title": "重命名後的對話"})
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print("✅ 重命名成功")
        else:
            print("❌ 重命名失敗")
            return False
    else:
        print(f"❌ 重命名失敗: {response.status_code}")
        return False
    
    # 測試清空對話
    print("🗑️ 測試清空對話...")
    response = requests.post(f"{BASE_URL}/api/conversations/{conversation_id}/clear")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print("✅ 清空對話成功")
        else:
            print("❌ 清空對話失敗")
            return False
    else:
        print(f"❌ 清空對話失敗: {response.status_code}")
        return False
    
    # 測試刪除對話
    print("🗂️ 測試刪除對話...")
    response = requests.delete(f"{BASE_URL}/api/conversations/{conversation_id}")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print("✅ 刪除對話成功")
        else:
            print("❌ 刪除對話失敗")
            return False
    else:
        print(f"❌ 刪除對話失敗: {response.status_code}")
        return False
    
    print("🎉 所有 API 測試通過！")
    return True

def test_web_interface():
    """測試 Web 介面"""
    print("🌐 測試 Web 介面...")
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        if "AI 聊天機器人" in response.text:
            print("✅ Web 介面載入成功")
            return True
        else:
            print("❌ Web 介面內容不正確")
            return False
    else:
        print(f"❌ Web 介面載入失敗: {response.status_code}")
        return False

def main():
    """主測試函數"""
    print("🤖 聊天機器人系統測試")
    print("=" * 40)
    
    try:
        # 測試 Web 介面
        if not test_web_interface():
            sys.exit(1)
        
        # 測試 API
        if not test_api():
            sys.exit(1)
        
        print("\n🎊 所有測試通過！系統運行正常。")
        print("🌐 請在瀏覽器中訪問 http://localhost:5001 開始使用")
        print("⚠️  請確保您的 LLM API 服務器正在運行以進行實際對話測試")
        
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到服務器。請確保應用程式正在運行。")
        print("💡 運行命令: ./start.sh 或 python app.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()