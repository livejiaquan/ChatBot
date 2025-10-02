#!/usr/bin/env python3
"""
測試 LLM API 連接的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_client import LLMClient
from config.config import Config

def test_llm_api():
    """測試 LLM API 連接"""
    print("🤖 測試 LLM API 連接...")
    print(f"🔗 API URL: {Config.LLM_API_URL}")
    print(f"🏷️ 模型: {Config.LLM_MODEL}")
    print(f"🔑 API 金鑰: {Config.LLM_API_KEY}")
    print("-" * 50)
    
    # 創建 LLM 客戶端
    client = LLMClient()
    
    # 測試訊息
    test_messages = [
        {"role": "user", "content": "請用繁體中文回答：什麼是人工智慧？用簡單易懂的方式說明。"}
    ]
    
    print("📤 發送測試訊息...")
    result = client.chat_completion_sync(test_messages)
    
    print("-" * 50)
    if result['success']:
        print("✅ LLM API 連接成功！")
        print(f"🤖 AI 回應:\n{result['content']}")
        if 'usage' in result:
            print(f"📊 使用統計: {result['usage']}")
    else:
        print("❌ LLM API 連接失敗！")
        print(f"💥 錯誤: {result['error']}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = test_llm_api()
        if success:
            print("\n🎉 LLM API 測試成功！您可以正常使用聊天機器人了。")
        else:
            print("\n❌ LLM API 測試失敗！請檢查配置和服務器狀態。")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 測試過程中發生錯誤: {e}")
        sys.exit(1)