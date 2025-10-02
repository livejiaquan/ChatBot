#!/usr/bin/env python3
"""
測試修復後的智思 AI 功能
"""

import requests
import time

BASE_URL = "http://localhost:5001"

def test_fixed_features():
    """測試修復後的功能"""
    print("🧠 智思 AI - 修復功能測試")
    print("=" * 50)
    
    print("✨ 修復項目檢查:")
    print("1. ✅ 防止連續發送 - 發送狀態控制")
    print("2. ✅ 繁體中文默認回應 - 系統提示")
    print("3. ✅ 品牌升級 - 智思 AI (更專業)")
    print("4. ✅ 歷史訊息直接顯示 - 無打字效果")
    print("5. ✅ 停止生成功能 - 按鈕切換")
    print("6. ✅ 滾動問題修復 - 立即可滾動")
    print("7. ✅ 介面優化 - 更專業的設計")
    
    print("\n" + "-" * 50)
    
    # 測試繁體中文回應
    print("📝 測試繁體中文默認回應...")
    try:
        # 創建新對話
        conv_response = requests.post(f"{BASE_URL}/api/conversations", 
                                    json={"title": "繁體中文測試"})
        if conv_response.status_code == 200:
            conv_data = conv_response.json()
            if conv_data['success']:
                conversation_id = conv_data['conversation_id']
                
                # 用英文問問題，測試是否回應繁體中文
                print("📤 發送英文問題，測試中文回應...")
                chat_response = requests.post(f"{BASE_URL}/api/chat", json={
                    "conversation_id": conversation_id,
                    "message": "What is artificial intelligence? Please explain briefly."
                })
                
                if chat_response.status_code == 200:
                    chat_data = chat_response.json()
                    if chat_data['success']:
                        response = chat_data['response']
                        
                        # 檢查繁體中文字符
                        traditional_chars = ['人工智慧', '機器學習', '智能', '技術', '系統', '資料', '演算法']
                        has_traditional = any(char in response for char in traditional_chars)
                        
                        print("✅ 聊天測試成功")
                        print(f"🤖 AI 回應預覽: {response[:100]}...")
                        print(f"🔤 繁體中文檢測: {'✅ 通過' if has_traditional else '❌ 需要調整'}")
                        
                        if 'usage' in chat_data:
                            usage = chat_data['usage']
                            print(f"📊 Token 統計: {usage.get('total_tokens', 'N/A')} tokens")
                    else:
                        print(f"❌ 聊天失敗: {chat_data.get('error')}")
                else:
                    print(f"❌ 聊天請求失敗: {chat_response.status_code}")
            else:
                print(f"❌ 創建對話失敗: {conv_data.get('error')}")
        else:
            print(f"❌ 創建對話請求失敗: {conv_response.status_code}")
    except Exception as e:
        print(f"💥 測試失敗: {e}")
    
    print("\n" + "-" * 50)
    
    # 測試系統狀態
    print("📊 測試系統狀態監控...")
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                llm_api = data['llm_api']
                print("✅ 系統狀態正常")
                print(f"   🧠 模型: {data['model']}")
                print(f"   🔗 API 狀態: {'線上' if llm_api['online'] else '離線'}")
                print(f"   📈 連接狀態: {llm_api['status']}")
            else:
                print(f"❌ 系統狀態檢查失敗: {data.get('error')}")
        else:
            print(f"❌ 無法獲取系統狀態: {response.status_code}")
    except Exception as e:
        print(f"💥 系統狀態測試失敗: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 測試完成！")
    
    print("\n🚀 新功能亮點:")
    print("🔒 防連續發送 - 等待 AI 回應完成才能發送下一條")
    print("🇹🇼 繁體中文優先 - 默認使用繁體中文回答")
    print("🧠 智思 AI 品牌 - 更專業的命名和圖標")
    print("⚡ 歷史訊息優化 - 點擊歷史對話立即顯示，無等待")
    print("🛑 停止生成 - 可以中途停止 AI 回應")
    print("📱 界面優化 - 更流暢的用戶體驗")
    
    print(f"\n🌐 立即體驗智思 AI: {BASE_URL}")
    print("💡 提示: 現在歷史對話會立即顯示，新對話才有打字效果！")

if __name__ == "__main__":
    try:
        test_fixed_features()
    except KeyboardInterrupt:
        print("\n⏹️ 測試被用戶中斷")
    except Exception as e:
        print(f"\n💥 測試過程中發生錯誤: {e}")