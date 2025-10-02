#!/usr/bin/env python3
"""
測試優化後的聊天機器人功能
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"

def test_optimized_features():
    """測試優化後的功能"""
    print("🚀 測試優化後的聊天機器人功能")
    print("=" * 50)
    
    # 1. 測試系統狀態 API
    print("📊 測試系統狀態監控...")
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                llm_api = data['llm_api']
                print(f"✅ 系統狀態 API 正常")
                print(f"   🤖 模型: {data['model']}")
                print(f"   🔗 API 狀態: {'線上' if llm_api['online'] else '離線'}")
                print(f"   📈 連接狀態: {llm_api['status']}")
            else:
                print(f"❌ 系統狀態檢查失敗: {data.get('error')}")
        else:
            print(f"❌ 無法獲取系統狀態: {response.status_code}")
    except Exception as e:
        print(f"💥 系統狀態測試失敗: {e}")
    
    print("\n" + "-" * 50)
    
    # 2. 測試完整的對話流程
    print("💬 測試完整對話流程...")
    try:
        # 創建新對話
        conv_response = requests.post(f"{BASE_URL}/api/conversations", 
                                    json={"title": "優化功能測試"})
        if conv_response.status_code == 200:
            conv_data = conv_response.json()
            if conv_data['success']:
                conversation_id = conv_data['conversation_id']
                print(f"✅ 創建對話成功，ID: {conversation_id}")
                
                # 發送測試訊息
                print("📤 發送測試訊息...")
                chat_response = requests.post(f"{BASE_URL}/api/chat", json={
                    "conversation_id": conversation_id,
                    "message": "請簡短介紹什麼是機器學習，並用列表格式說明三個主要特點"
                })
                
                if chat_response.status_code == 200:
                    chat_data = chat_response.json()
                    if chat_data['success']:
                        print("✅ 聊天測試成功")
                        print(f"🤖 AI 回應預覽: {chat_data['response'][:100]}...")
                        if 'usage' in chat_data:
                            usage = chat_data['usage']
                            print(f"📊 Token 使用統計:")
                            print(f"   - 提示 tokens: {usage.get('prompt_tokens', 'N/A')}")
                            print(f"   - 完成 tokens: {usage.get('completion_tokens', 'N/A')}")
                            print(f"   - 總計 tokens: {usage.get('total_tokens', 'N/A')}")
                    else:
                        print(f"❌ 聊天失敗: {chat_data.get('error')}")
                else:
                    print(f"❌ 聊天請求失敗: {chat_response.status_code}")
            else:
                print(f"❌ 創建對話失敗: {conv_data.get('error')}")
        else:
            print(f"❌ 創建對話請求失敗: {conv_response.status_code}")
    except Exception as e:
        print(f"💥 對話測試失敗: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 測試完成！")
    print("\n📱 新功能介紹:")
    print("1. 🎯 系統狀態監控 - 實時顯示模型和連接狀態")
    print("2. ⚡ 打字機效果 - AI 回應逐字顯示，更像真實對話")
    print("3. 🔄 改進的加載狀態 - 更清楚的視覺反饋")
    print("4. 📊 響應式設計優化 - 更好的移動端體驗")
    print("5. 🎨 動畫效果增強 - 更流暢的用戶互動")
    print("\n🌐 立即體驗: http://localhost:5001")

if __name__ == "__main__":
    try:
        test_optimized_features()
    except KeyboardInterrupt:
        print("\n⏹️ 測試被用戶中斷")
    except Exception as e:
        print(f"\n💥 測試過程中發生錯誤: {e}")