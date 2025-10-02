from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid
import json
from datetime import datetime

# 導入自定義模組
from config.config import Config
from database.models import db_manager
from llm_client import LLMClient

# 創建 Flask 應用
app = Flask(__name__)
app.config.from_object(Config)

# 啟用 CORS
CORS(app)

# 初始化 SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# 初始化 LLM 客戶端
llm_client = LLMClient()

# 儲存活躍的會話
active_sessions = {}

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    """獲取所有對話列表"""
    try:
        conversations = db_manager.get_conversations()
        return jsonify({
            'success': True,
            'conversations': conversations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/conversations', methods=['POST'])
def create_conversation():
    """創建新對話"""
    try:
        data = request.get_json()
        title = data.get('title', '新對話')
        
        conversation_id = db_manager.create_conversation(title)
        return jsonify({
            'success': True,
            'conversation_id': conversation_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation_messages(conversation_id):
    """獲取對話的所有訊息"""
    try:
        messages = db_manager.get_conversation_messages(conversation_id)
        return jsonify({
            'success': True,
            'messages': messages
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """刪除對話"""
    try:
        success = db_manager.delete_conversation(conversation_id)
        return jsonify({
            'success': success
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/conversations/<int:conversation_id>/title', methods=['PUT'])
def update_conversation_title(conversation_id):
    """更新對話標題"""
    try:
        data = request.get_json()
        new_title = data.get('title', '')
        
        success = db_manager.update_conversation_title(conversation_id, new_title)
        return jsonify({
            'success': success
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/conversations/<int:conversation_id>/clear', methods=['POST'])
def clear_conversation(conversation_id):
    """清空對話訊息"""
    try:
        success = db_manager.clear_conversation(conversation_id)
        return jsonify({
            'success': success
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def get_system_status():
    """獲取系統狀態"""
    try:
        # 檢查 LLM API 狀態
        api_status = llm_client.check_api_status()
        
        return jsonify({
            'success': True,
            'llm_api': api_status,
            'model': Config.LLM_MODEL,
            'server_time': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'llm_api': {
                'online': False,
                'model': Config.LLM_MODEL,
                'status': 'error'
            }
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """處理聊天請求"""
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        message = data.get('message', '').strip()
        
        if not conversation_id or not message:
            return jsonify({
                'success': False,
                'error': '缺少對話 ID 或訊息內容'
            }), 400
        
        # 保存用戶訊息
        db_manager.add_message(conversation_id, 'user', message)
        
        # 獲取對話歷史
        messages = db_manager.get_conversation_messages(conversation_id)
        
        # 準備發送給 LLM 的訊息格式
        llm_messages = []
        for msg in messages:
            llm_messages.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        # 發送請求到 LLM
        response = llm_client.chat_completion_sync(llm_messages)
        
        if response['success']:
            # 保存 AI 回應
            db_manager.add_message(conversation_id, 'assistant', response['content'])
            
            return jsonify({
                'success': True,
                'response': response['content'],
                'usage': response.get('usage', {})
            })
        else:
            return jsonify({
                'success': False,
                'error': response['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# WebSocket 事件處理
@socketio.on('connect')
def handle_connect():
    """處理客戶端連接"""
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    active_sessions[session_id] = {
        'connected_at': datetime.utcnow(),
        'socket_id': request.sid
    }
    print(f"客戶端已連接: {session_id}")
    emit('connected', {'session_id': session_id})

@socketio.on('disconnect')
def handle_disconnect():
    """處理客戶端斷線"""
    session_id = session.get('session_id')
    if session_id and session_id in active_sessions:
        del active_sessions[session_id]
        print(f"客戶端已斷線: {session_id}")

@socketio.on('join_conversation')
def handle_join_conversation(data):
    """加入對話房間"""
    conversation_id = data.get('conversation_id')
    if conversation_id:
        join_room(f"conversation_{conversation_id}")
        emit('joined_conversation', {'conversation_id': conversation_id})

@socketio.on('leave_conversation')
def handle_leave_conversation(data):
    """離開對話房間"""
    conversation_id = data.get('conversation_id')
    if conversation_id:
        leave_room(f"conversation_{conversation_id}")
        emit('left_conversation', {'conversation_id': conversation_id})

@socketio.on('send_message')
def handle_send_message(data):
    """處理即時聊天訊息"""
    try:
        conversation_id = data.get('conversation_id')
        message = data.get('message', '').strip()
        
        if not conversation_id or not message:
            emit('error', {'error': '缺少對話 ID 或訊息內容'})
            return
        
        # 保存用戶訊息（不向房間廣播用戶訊息，因為前端已經顯示了）
        db_manager.add_message(conversation_id, 'user', message)
        
        # 獲取對話歷史
        messages = db_manager.get_conversation_messages(conversation_id)
        
        # 準備發送給 LLM 的訊息格式
        llm_messages = []
        for msg in messages:
            llm_messages.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        # 發送正在輸入的狀態
        socketio.emit('typing', {
            'conversation_id': conversation_id,
            'is_typing': True
        }, room=f"conversation_{conversation_id}")
        
        # 發送請求到 LLM
        response = llm_client.chat_completion_sync(llm_messages)
        
        # 停止正在輸入的狀態
        socketio.emit('typing', {
            'conversation_id': conversation_id,
            'is_typing': False
        }, room=f"conversation_{conversation_id}")
        
        if response['success']:
            # 保存 AI 回應
            db_manager.add_message(conversation_id, 'assistant', response['content'])
            
            # 向房間內的所有客戶端廣播 AI 回應
            socketio.emit('new_message', {
                'conversation_id': conversation_id,
                'role': 'assistant',
                'content': response['content'],
                'timestamp': datetime.utcnow().isoformat()
            }, room=f"conversation_{conversation_id}")
            
        else:
            # 發送錯誤訊息
            emit('error', {'error': response['error']})
            
    except Exception as e:
        emit('error', {'error': str(e)})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '頁面未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '內部服務器錯誤'}), 500

if __name__ == '__main__':
    # 確保資料庫目錄存在
    import os
    if not os.path.exists('database'):
        os.makedirs('database')
    
    # 啟動應用
    socketio.run(app, host='0.0.0.0', port=5001, debug=Config.DEBUG)