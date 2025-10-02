import requests
import json
from typing import List, Dict
from config.config import Config

class LLMClient:
    def __init__(self):
        self.api_url = Config.LLM_API_URL
        self.model = Config.LLM_MODEL
        self.api_key = Config.LLM_API_KEY
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        
    def format_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """格式化訊息為 API 格式"""
        formatted = []
        
        # 添加更強的系統提示，明確要求使用繁體中文
        formatted.append({
            "role": "system",
            "content": "重要：當你用中文回答時，請務必使用繁體中文（Traditional Chinese），不要使用簡體中文。例如：使用「發展」而不是「发展」，使用「學習」而不是「学习」，使用「機器學習」而不是「机器学习」。對於其他語言的問題，請用相應語言回答。請提供準確、有用且友善的回應。"
        })
        
        for msg in messages:
            formatted.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        return formatted
    
    def truncate_conversation(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """截斷對話以適應 token 限制"""
        # 如果對話太長，保留最近的訊息
        max_length = Config.MAX_CONVERSATION_LENGTH
        if len(messages) > max_length:
            # 保留系統訊息（如果有）和最近的對話
            system_messages = [msg for msg in messages if msg.get("role") == "system"]
            recent_messages = messages[-max_length:]
            
            # 如果最近的訊息中沒有系統訊息，則添加系統訊息
            if system_messages and not any(msg.get("role") == "system" for msg in recent_messages):
                return system_messages + recent_messages[-(max_length-len(system_messages)):]
            else:
                return recent_messages
        return messages
    
    def check_api_status(self) -> Dict:
        """檢查 API 服務器狀態"""
        try:
            # 發送簡單的健康檢查請求
            test_payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 1,
                "temperature": 0.1
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.post(
                self.api_url,
                json=test_payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'online': True,
                    'model': self.model,
                    'status': 'connected'
                }
            else:
                return {
                    'online': False,
                    'model': self.model,
                    'status': f'error_{response.status_code}'
                }
                
        except requests.exceptions.Timeout:
            return {
                'online': False,
                'model': self.model,
                'status': 'timeout'
            }
        except requests.exceptions.ConnectionError:
            return {
                'online': False,
                'model': self.model,
                'status': 'connection_error'
            }
        except Exception as e:
            return {
                'online': False,
                'model': self.model,
                'status': f'error: {str(e)}'
            }
    
    def chat_completion_sync(self, messages: List[Dict[str, str]]) -> Dict:
        """同步版本的聊天完成請求"""
        try:
            # 截斷對話
            truncated_messages = self.truncate_conversation(messages)
            formatted_messages = self.format_messages(truncated_messages)
            
            payload = {
                "model": self.model,
                "messages": formatted_messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            print(f"🔗 發送請求到: {self.api_url}")
            print(f"🔑 使用 API 金鑰: {self.api_key}")
            print(f"📝 訊息數量: {len(formatted_messages)}")
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"📊 回應狀態碼: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # 提取回應內容
                if 'choices' in data and len(data['choices']) > 0:
                    content = data['choices'][0]['message']['content']
                    print(f"✅ 成功獲得回應，長度: {len(content)} 字符")
                    return {
                        'success': True,
                        'content': content,
                        'usage': data.get('usage', {})
                    }
                else:
                    print(f"❌ 無效的 API 回應格式: {data}")
                    return {
                        'success': False,
                        'error': '無效的 API 回應格式'
                    }
            else:
                error_text = response.text
                print(f"❌ API 請求失敗: {response.status_code} - {error_text}")
                return {
                    'success': False,
                    'error': f'API 請求失敗: {response.status_code} - {error_text}'
                }
                
        except requests.exceptions.Timeout:
            print("⏱️ API 請求超時")
            return {
                'success': False,
                'error': 'API 請求超時'
            }
        except requests.exceptions.ConnectionError:
            print("🚫 無法連接到 LLM API 服務器")
            return {
                'success': False,
                'error': '無法連接到 LLM API 服務器'
            }
        except Exception as e:
            print(f"💥 發生錯誤: {str(e)}")
            return {
                'success': False,
                'error': f'發生錯誤: {str(e)}'
            }
    
    async def chat_completion(self, messages: List[Dict[str, str]]) -> Dict:
        """非同步版本的聊天完成請求"""
        # 目前直接調用同步版本
        return self.chat_completion_sync(messages)