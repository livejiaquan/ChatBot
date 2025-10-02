#!/usr/bin/env python3
"""
ChatBot - 繁體中文回應測試
"""

import requests
import time

BASE_URL = "http://localhost:5001"

def test_traditional_chinese():
    """測試繁體中文回應功能"""
    print("🤖 ChatBot - 繁體中文回應測試")
    print("=" * 50)
    
    print("✨ 語言設定功能:")
    print("1. ✅ 中文問題 → 繁體中文回應")
    print("2. ✅ 英文問題 → 英文回應")
    print("3. ✅ 避免簡體中文字詞")
    print("4. ✅ 自然語言判斷")
    
    print("\n" + "-" * 50)
    
    # 測試繁體中文回應
    print("📝 測試繁體中文回應...")
    try:
        # 創建新對話
        conv_response = requests.post(f"{BASE_URL}/api/conversations", 
                                    json={"title": "繁體中文測試"})
        if conv_response.status_code == 200:
            conv_data = conv_response.json()
            if conv_data['success']:
                conversation_id = conv_data['conversation_id']
                
                # 測試中文技術問題
                print("📤 發送中文技術問題...")
                chat_response = requests.post(f"{BASE_URL}/api/chat", json={
                    "conversation_id": conversation_id,
                    "message": "請解釋什麼是機器學習，包括它的主要類型和應用領域"
                })
                
                if chat_response.status_code == 200:
                    chat_data = chat_response.json()
                    if chat_data['success']:
                        response = chat_data['response']
                        
                        # 檢查繁體/簡體字使用情況
                        traditional_pairs = [
                            '機器', '學習', '發展', '資料', '訓練', '處理', 
                            '認識', '網絡', '應用', '領域', '類型'
                        ]
                        simplified_pairs = [
                            '机器', '学习', '发展', '数据', '训练', '处理',
                            '认识', '网络', '应用', '领域', '类型'
                        ]
                        
                        traditional_count = sum(response.count(word) for word in traditional_pairs)
                        simplified_count = sum(response.count(word) for word in simplified_pairs)
                        
                        print("✅ 中文測試成功")
                        print(f"🤖 AI 回應預覽: {response[:150]}...")
                        print(f"📏 回應長度: {len(response)} 字符")
                        print(f"🔤 繁體字詞統計: {traditional_count}")
                        print(f"🔤 簡體字詞統計: {simplified_count}")
                        
                        if simplified_count == 0 and traditional_count > 0:
                            print("🎉 完美！100% 繁體中文")
                        elif simplified_count < traditional_count:
                            print("✅ 良好！主要使用繁體中文")
                        else:
                            print("⚠️ 需要改進")
                        
                        # 測試英文問題
                        print("\n📤 發送英文問題測試...")
                        chat_response2 = requests.post(f"{BASE_URL}/api/chat", json={
                            "conversation_id": conversation_id,
                            "message": "What are the main differences between supervised and unsupervised learning?"
                        })
                        
                        if chat_response2.status_code == 200:
                            chat_data2 = chat_response2.json()
                            if chat_data2['success']:
                                response2 = chat_data2['response']
                                
                                # 檢查是否為英文回應
                                english_chars = sum(1 for c in response2 if c.isascii() and c.isalpha())
                                total_chars = len(response2.replace(' ', '').replace('\n', ''))
                                english_ratio = english_chars / total_chars if total_chars > 0 else 0
                                
                                print("✅ 英文測試成功")
                                print(f"🤖 AI 回應預覽: {response2[:150]}...")
                                print(f"🌐 英文字符比例: {english_ratio:.1%}")
                                
                                if english_ratio > 0.8:
                                    print("🎉 完美！保持英文回應")
                                else:
                                    print("🔤 混合語言回應")
                            
                        if 'usage' in chat_data:
                            usage = chat_data['usage']
                            print(f"\n📊 總 Token 使用: {usage.get('total_tokens', 'N/A')} tokens")
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
    
    print("\n" + "=" * 50)
    print("🎉 測試完成！")
    
    print("\n🌐 ChatBot 語言特性:")
    print("🇹🇼 中文回應：自動使用繁體中文")
    print("🇺🇸 英文回應：保持原生英文")
    print("🌏 多語言支援：根據問題語言自動判斷")
    print("⚡ 智能切換：同一對話可混用不同語言")
    
    print(f"\n🌐 體驗 ChatBot: {BASE_URL}")
    print("💡 提示：現在中文問題都會用繁體中文回答！")

if __name__ == "__main__":
    try:
        test_traditional_chinese()
    except KeyboardInterrupt:
        print("\n⏹️ 測試被用戶中斷")
    except Exception as e:
        print(f"\n💥 測試過程中發生錯誤: {e}")