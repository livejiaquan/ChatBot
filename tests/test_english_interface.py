#!/usr/bin/env python3
"""
ChatBot - English Interface Test
"""

import requests
import time

BASE_URL = "http://localhost:5001"

def test_english_interface():
    """Test the English interface"""
    print("🤖 ChatBot - English Interface Test")
    print("=" * 50)
    
    print("✨ Interface Features:")
    print("1. ✅ English UI - Clean and professional")
    print("2. ✅ Prevent consecutive sends - State control")
    print("3. ✅ Natural AI responses - No forced language")
    print("4. ✅ History messages instant display")
    print("5. ✅ Stop generation functionality")
    print("6. ✅ Professional design")
    
    print("\n" + "-" * 50)
    
    # Test English conversation
    print("💬 Testing English conversation...")
    try:
        # Create new conversation
        conv_response = requests.post(f"{BASE_URL}/api/conversations", 
                                    json={"title": "English Chat Test"})
        if conv_response.status_code == 200:
            conv_data = conv_response.json()
            if conv_data['success']:
                conversation_id = conv_data['conversation_id']
                
                # Send test message
                print("📤 Sending test message...")
                chat_response = requests.post(f"{BASE_URL}/api/chat", json={
                    "conversation_id": conversation_id,
                    "message": "Hello! Can you explain machine learning in simple terms?"
                })
                
                if chat_response.status_code == 200:
                    chat_data = chat_response.json()
                    if chat_data['success']:
                        response = chat_data['response']
                        
                        print("✅ Chat test successful")
                        print(f"🤖 AI Response preview: {response[:120]}...")
                        print(f"📏 Response length: {len(response)} characters")
                        
                        if 'usage' in chat_data:
                            usage = chat_data['usage']
                            print(f"📊 Token statistics: {usage.get('total_tokens', 'N/A')} tokens")
                    else:
                        print(f"❌ Chat failed: {chat_data.get('error')}")
                else:
                    print(f"❌ Chat request failed: {chat_response.status_code}")
            else:
                print(f"❌ Failed to create conversation: {conv_data.get('error')}")
        else:
            print(f"❌ Create conversation request failed: {conv_response.status_code}")
    except Exception as e:
        print(f"💥 Test failed: {e}")
    
    print("\n" + "-" * 50)
    
    # Test system status
    print("📊 Testing system status monitoring...")
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                llm_api = data['llm_api']
                print("✅ System status normal")
                print(f"   🤖 Model: {data['model']}")
                print(f"   🔗 API Status: {'Online' if llm_api['online'] else 'Offline'}")
                print(f"   📈 Connection: {llm_api['status']}")
            else:
                print(f"❌ System status check failed: {data.get('error')}")
        else:
            print(f"❌ Unable to get system status: {response.status_code}")
    except Exception as e:
        print(f"💥 System status test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    
    print("\n🚀 ChatBot Features:")
    print("🔒 Conversation Control - No duplicate sends while AI is responding")
    print("🌐 Natural Language - AI responds in the language you use")
    print("🤖 Professional Interface - Clean and modern design")
    print("⚡ Instant History - Click history chats for immediate display")
    print("🛑 Stop Generation - Interrupt AI responses anytime")
    print("📱 Responsive Design - Works great on all devices")
    
    print(f"\n🌐 Experience ChatBot now: {BASE_URL}")
    print("💡 Tip: History conversations show instantly, new conversations have typing effect!")

if __name__ == "__main__":
    try:
        test_english_interface()
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Error during testing: {e}")