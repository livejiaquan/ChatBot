// 應用程式主類
class ChatbotApp {
    constructor() {
        this.socket = null;
        this.currentConversationId = null;
        this.isConnected = false;
        this.isTyping = false;
        this.isSending = false; // 添加發送狀態控制
        this.isGenerating = false; // 添加生成狀態控制
        
        this.initializeElements();
        this.initializeSocket();
        this.bindEvents();
        this.loadConversations();
        this.initializeTheme();
        this.initializeSystemStatus();
        
        // 配置 marked.js
        marked.setOptions({
            breaks: true,
            gfm: true,
            highlight: function(code, lang) {
                if (lang && hljs.getLanguage(lang)) {
                    try {
                        return hljs.highlight(code, { language: lang }).value;
                    } catch (err) {}
                }
                try {
                    return hljs.highlightAuto(code).value;
                } catch (err) {}
                return code;
            }
        });
    }
    
    initializeSystemStatus() {
        // 初始化系統狀態檢查
        this.updateSystemStatus();
        
        // 每30秒檢查一次系統狀態
        setInterval(() => {
            this.updateSystemStatus();
        }, 30000);
    }
    
    async updateSystemStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (data.success) {
                const llmApi = data.llm_api;
                
                // 更新模型名稱
                this.modelName.textContent = this.getModelDisplayName(data.model);
                
                // 更新連接狀態
                if (llmApi.online) {
                    this.statusDot.className = 'fas fa-circle status-dot online';
                    this.connectionText.textContent = 'Online';
                    this.connectionText.style.color = 'var(--success-color)';
                } else {
                    this.statusDot.className = 'fas fa-circle status-dot offline';
                    this.connectionText.textContent = 'Offline';
                    this.connectionText.style.color = 'var(--danger-color)';
                }
            } else {
                this.statusDot.className = 'fas fa-circle status-dot offline';
                this.connectionText.textContent = 'Error';
                this.connectionText.style.color = 'var(--danger-color)';
            }
        } catch (error) {
            console.error('檢查系統狀態失敗:', error);
            this.statusDot.className = 'fas fa-circle status-dot checking';
            this.connectionText.textContent = 'Checking...';
            this.connectionText.style.color = 'var(--warning-color)';
        }
    }
    
    getModelDisplayName(modelPath) {
        // 從模型路徑提取顯示名稱
        if (modelPath.includes('Qwen2.5-14B-Instruct')) {
            return 'Qwen2.5-14B';
        } else if (modelPath.includes('Qwen')) {
            return 'Qwen';
        } else {
            return modelPath.split('/').pop() || '未知模型';
        }
    }
    
    initializeElements() {
        // 側邊欄相關
        this.sidebar = document.getElementById('sidebar');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.conversationsList = document.getElementById('conversationsList');
        this.newChatBtn = document.getElementById('newChatBtn');
        
        // 聊天相關
        this.chatContainer = document.getElementById('chatContainer');
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.chatInputContainer = document.getElementById('chatInputContainer');
        this.currentChatTitle = document.getElementById('currentChatTitle');
        
        // 頂部工具欄
        this.clearChatBtn = document.getElementById('clearChatBtn');
        this.renameChatBtn = document.getElementById('renameChatBtn');
        
        // 系統狀態
        this.systemStatus = document.getElementById('systemStatus');
        this.modelStatus = document.getElementById('modelStatus');
        this.connectionStatus = document.getElementById('connectionStatus');
        this.modelName = document.getElementById('modelName');
        this.connectionText = document.getElementById('connectionText');
        this.statusDot = document.getElementById('statusDot');
        
        // 指示器
        this.typingIndicator = document.getElementById('typingIndicator');
        this.generatingMessage = document.getElementById('generatingMessage');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        
        // 主題切換
        this.themeToggle = document.getElementById('themeToggle');
        
        // 模態框
        this.modalOverlay = document.getElementById('modalOverlay');
        this.modalTitle = document.getElementById('modalTitle');
        this.modalMessage = document.getElementById('modalMessage');
        this.modalConfirm = document.getElementById('modalConfirm');
        this.modalCancel = document.getElementById('modalCancel');
        this.modalClose = document.getElementById('modalClose');
        
        // 重命名模態框
        this.renameModalOverlay = document.getElementById('renameModalOverlay');
        this.newTitleInput = document.getElementById('newTitleInput');
        this.renameModalConfirm = document.getElementById('renameModalConfirm');
        this.renameModalCancel = document.getElementById('renameModalCancel');
        this.renameModalClose = document.getElementById('renameModalClose');
        
        // Toast 容器
        this.toastContainer = document.getElementById('toastContainer');
    }
    
    initializeSocket() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            this.isConnected = true;
            console.log('已連接到服務器');
        });
        
        this.socket.on('disconnect', () => {
            this.isConnected = false;
            console.log('已斷開與服務器的連接');
        });
        
        this.socket.on('connected', (data) => {
            console.log('會話 ID:', data.session_id);
        });
        
        this.socket.on('new_message', (data) => {
            if (data.conversation_id === this.currentConversationId) {
                this.hideTypingIndicator();
                // 新訊息使用打字效果，設置 isHistoryMessage = false
                this.appendMessage(data.role, data.content, data.timestamp, true, false);
            }
        });
        
        this.socket.on('typing', (data) => {
            if (data.conversation_id === this.currentConversationId) {
                if (data.is_typing) {
                    this.showTypingIndicator();
                } else {
                    this.hideTypingIndicator();
                }
            }
        });
        
        this.socket.on('error', (data) => {
            this.showToast('錯誤: ' + data.error, 'error');
        });
    }
    
    bindEvents() {
        // 新對話按鈕
        this.newChatBtn.addEventListener('click', () => this.createNewConversation());
        
        // 發送按鈕
        this.sendBtn.addEventListener('click', () => {
            if (this.isGenerating) {
                this.stopGeneration();
            } else {
                this.sendMessage();
            }
        });
        
        // 輸入框事件
        this.messageInput.addEventListener('input', () => this.handleInputChange());
        this.messageInput.addEventListener('keydown', (e) => this.handleKeyDown(e));
        
        // 清空對話
        this.clearChatBtn.addEventListener('click', () => this.confirmClearChat());
        
        // 重命名對話
        this.renameChatBtn.addEventListener('click', () => this.showRenameModal());
        
        // 側邊欄切換
        this.sidebarToggle.addEventListener('click', () => this.toggleSidebar());
        
        // 主題切換
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // 模態框事件
        this.modalCancel.addEventListener('click', () => this.hideModal());
        this.modalClose.addEventListener('click', () => this.hideModal());
        this.modalOverlay.addEventListener('click', (e) => {
            if (e.target === this.modalOverlay) this.hideModal();
        });
        
        // 重命名模態框事件
        this.renameModalCancel.addEventListener('click', () => this.hideRenameModal());
        this.renameModalClose.addEventListener('click', () => this.hideRenameModal());
        this.renameModalConfirm.addEventListener('click', () => this.confirmRename());
        this.renameModalOverlay.addEventListener('click', (e) => {
            if (e.target === this.renameModalOverlay) this.hideRenameModal();
        });
        
        this.newTitleInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') this.confirmRename();
            if (e.key === 'Escape') this.hideRenameModal();
        });
        
        // 點擊外部關閉側邊欄（移動端）
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768 && this.sidebar.classList.contains('open')) {
                if (!this.sidebar.contains(e.target) && !this.sidebarToggle.contains(e.target)) {
                    this.sidebar.classList.remove('open');
                }
            }
        });
        
        // 窗口大小變化
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                this.sidebar.classList.remove('open');
            }
        });
    }
    
    async loadConversations() {
        try {
            this.showLoading(true);
            const response = await fetch('/api/conversations');
            const data = await response.json();
            
            if (data.success) {
                this.renderConversations(data.conversations);
            } else {
                this.showToast('載入對話失敗: ' + data.error, 'error');
            }
        } catch (error) {
            this.showToast('載入對話失敗: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    renderConversations(conversations) {
        this.conversationsList.innerHTML = '';
        
        if (conversations.length === 0) {
            this.conversationsList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-comments"></i>
                    <p>No conversations yet</p>
                    <p>Click "New Chat" to start</p>
                </div>
            `;
            return;
        }
        
        conversations.forEach(conv => {
            const item = document.createElement('div');
            item.className = 'conversation-item';
            item.dataset.conversationId = conv.id;
            
            const date = new Date(conv.updated_at).toLocaleDateString('zh-TW', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            
            item.innerHTML = `
                <div class="conversation-content">
                    <div class="conversation-title">${this.escapeHtml(conv.title)}</div>
                    <div class="conversation-meta">${conv.message_count} messages · ${date}</div>
                </div>
                <div class="conversation-actions">
                    <button class="btn btn-icon btn-sm" onclick="app.showRenameModal(${conv.id})" title="Rename">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-icon btn-sm" onclick="app.confirmDeleteConversation(${conv.id})" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
            
            item.addEventListener('click', (e) => {
                if (!e.target.closest('.conversation-actions')) {
                    this.selectConversation(conv.id, conv.title);
                }
            });
            
            this.conversationsList.appendChild(item);
        });
    }
    
    async createNewConversation() {
        try {
            this.showLoading(true);
            const response = await fetch('/api/conversations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: 'New Chat' })
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.loadConversations();
                this.selectConversation(data.conversation_id, '新對話');
                this.showToast('已創建新對話', 'success');
            } else {
                this.showToast('創建對話失敗: ' + data.error, 'error');
            }
        } catch (error) {
            this.showToast('創建對話失敗: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    async selectConversation(conversationId, title) {
        if (this.currentConversationId) {
            this.socket.emit('leave_conversation', {
                conversation_id: this.currentConversationId
            });
        }
        
        this.currentConversationId = conversationId;
        this.currentChatTitle.textContent = title;
        
        // 更新側邊欄選中狀態
        document.querySelectorAll('.conversation-item').forEach(item => {
            item.classList.remove('active');
        });
        
        const selectedItem = document.querySelector(`[data-conversation-id="${conversationId}"]`);
        if (selectedItem) {
            selectedItem.classList.add('active');
        }
        
        // 顯示聊天輸入區域和工具按鈕
        this.chatInputContainer.style.display = 'block';
        this.clearChatBtn.style.display = 'inline-flex';
        this.renameChatBtn.style.display = 'inline-flex';
        
        // 加入對話房間
        this.socket.emit('join_conversation', {
            conversation_id: conversationId
        });
        
        // 載入對話訊息
        await this.loadConversationMessages(conversationId);
        
        // 關閉移動端側邊欄
        if (window.innerWidth <= 768) {
            this.sidebar.classList.remove('open');
        }
        
        // 聚焦輸入框
        this.messageInput.focus();
    }
    
    async loadConversationMessages(conversationId) {
        try {
            const response = await fetch(`/api/conversations/${conversationId}`);
            const data = await response.json();
            
            if (data.success) {
                this.renderMessages(data.messages);
            } else {
                this.showToast('載入訊息失敗: ' + data.error, 'error');
            }
        } catch (error) {
            this.showToast('載入訊息失敗: ' + error.message, 'error');
        }
    }
    
    renderMessages(messages) {
        this.chatMessages.innerHTML = '';
        
        if (messages.length === 0) {
            this.chatMessages.innerHTML = `
                <div class="welcome-message">
                    <div class="welcome-icon">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h2>Start a new conversation</h2>
                    <p>Type your message to start chatting with the AI</p>
                </div>
            `;
        } else {
            messages.forEach(msg => {
                // 歷史訊息不使用打字效果，直接顯示
                this.appendMessage(msg.role, msg.content, msg.timestamp, false, true);
            });
        }
        
        this.scrollToBottom();
    }
    
    appendMessage(role, content, timestamp, animate = true, isHistoryMessage = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const avatarIcon = role === 'user' ? 'fa-user' : 'fa-robot';
        const time = new Date(timestamp).toLocaleTimeString('zh-TW', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas ${avatarIcon}"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="message-text"></div>
                </div>
                <div class="message-time">${time}</div>
            </div>
        `;
        
        if (!animate) {
            messageDiv.style.animation = 'none';
        }
        
        this.chatMessages.appendChild(messageDiv);
        
        const messageTextElement = messageDiv.querySelector('.message-text');
        
        if (role === 'user' || isHistoryMessage) {
            // 用戶訊息或歷史訊息直接顯示
            if (role === 'user') {
                messageTextElement.innerHTML = this.escapeHtml(content).replace(/\n/g, '<br>');
            } else {
                // AI 歷史訊息直接顯示 Markdown 渲染結果
                messageTextElement.innerHTML = marked.parse(content);
                // 立即高亮程式碼
                messageDiv.querySelectorAll('pre code').forEach(block => {
                    hljs.highlightElement(block);
                });
            }
        } else {
            // 只有新的 AI 訊息使用打字機效果
            this.typeWriterEffect(messageTextElement, content, () => {
                // 完成後高亮程式碼
                messageDiv.querySelectorAll('pre code').forEach(block => {
                    hljs.highlightElement(block);
                });
                // 打字完成，允許新的訊息
                this.isGenerating = false;
                this.updateSendButton();
            });
        }
        
        this.scrollToBottom();
        return messageDiv;
    }
    
    typeWriterEffect(element, text, callback) {
        // 處理 Markdown
        const processedContent = marked.parse(text);
        
        // 創建一個暫時的 div 來解析 HTML
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = processedContent;
        
        // 提取純文字內容用於打字效果
        const textContent = tempDiv.textContent || tempDiv.innerText || '';
        
        let currentIndex = 0;
        const typingSpeed = 30; // 毫秒
        
        // 清空元素並開始打字效果
        element.innerHTML = '';
        
        const typeInterval = setInterval(() => {
            if (currentIndex < textContent.length) {
                // 逐字添加
                const char = textContent[currentIndex];
                const currentText = textContent.substring(0, currentIndex + 1);
                
                // 對於簡單文字，直接添加字符
                element.textContent = currentText;
                currentIndex++;
                
                // 自動滾動
                this.scrollToBottom();
            } else {
                // 打字完成，顯示完整的 Markdown 渲染內容
                clearInterval(typeInterval);
                element.innerHTML = processedContent;
                
                if (callback) callback();
            }
        }, typingSpeed);
        
        // 保存間隔 ID 以便可能的取消
        element.dataset.typingInterval = typeInterval;
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'block';
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || !this.currentConversationId || this.isSending || this.isGenerating) {
            return; // 如果正在發送或生成中，不允許發送新訊息
        }
        
        // 設置發送狀態
        this.isSending = true;
        this.isGenerating = true;
        
        // 立即顯示用戶訊息
        const userMessageDiv = this.appendMessage('user', message, new Date().toISOString());
        
        // 清空輸入框
        this.messageInput.value = '';
        this.updateSendButton();
        this.autoResizeTextarea();
        
        // 顯示打字指示器
        this.showTypingIndicator();
        
        // 通過 WebSocket 發送訊息
        this.socket.emit('send_message', {
            conversation_id: this.currentConversationId,
            message: message
        });
        
        // 重置發送狀態（但保持生成狀態直到收到回應）
        this.isSending = false;
    }
    
    handleInputChange() {
        this.updateSendButton();
        this.autoResizeTextarea();
        this.updateCharCount();
    }
    
    stopGeneration() {
        // 停止當前的打字效果
        const generatingElements = document.querySelectorAll('[data-typing-interval]');
        generatingElements.forEach(element => {
            const intervalId = element.dataset.typingInterval;
            if (intervalId) {
                clearInterval(parseInt(intervalId));
                delete element.dataset.typingInterval;
            }
        });
        
        // 重置狀態
        this.isGenerating = false;
        this.hideTypingIndicator();
        this.updateSendButton();
        
        // 通知服務器停止生成（如果支持的話）
        this.socket.emit('stop_generation', {
            conversation_id: this.currentConversationId
        });
    }
    
    handleKeyDown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!this.isGenerating) {
                this.sendMessage();
            }
        }
    }
    
    updateSendButton() {
        const hasContent = this.messageInput.value.trim().length > 0;
        const canSend = hasContent && this.currentConversationId && !this.isSending && !this.isGenerating;
        this.sendBtn.disabled = !canSend;
        
        // 更新按鈕文字和圖標
        if (this.isGenerating) {
            this.sendBtn.innerHTML = '<i class="fas fa-stop"></i>';
            this.sendBtn.title = '點擊停止生成';
        } else {
            this.sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
            this.sendBtn.title = '發送訊息';
        }
    }
    
    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    updateCharCount() {
        const charCount = this.messageInput.value.length;
        const charCountEl = document.querySelector('.char-count');
        if (charCountEl) {
            charCountEl.textContent = `${charCount}/2000`;
        }
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    confirmClearChat() {
        this.showModal(
            '清空對話',
            '您確定要清空當前對話的所有訊息嗎？此操作無法撤銷。',
            async () => {
                await this.clearChat();
            }
        );
    }
    
    async clearChat() {
        if (!this.currentConversationId) return;
        
        try {
            this.showLoading(true);
            const response = await fetch(`/api/conversations/${this.currentConversationId}/clear`, {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.renderMessages([]);
                this.showToast('對話已清空', 'success');
            } else {
                this.showToast('清空對話失敗: ' + data.error, 'error');
            }
        } catch (error) {
            this.showToast('清空對話失敗: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    showRenameModal(conversationId = null) {
        const targetId = conversationId || this.currentConversationId;
        if (!targetId) return;
        
        this.renameModalOverlay.dataset.conversationId = targetId;
        
        // 獲取當前標題
        const conversationItem = document.querySelector(`[data-conversation-id="${targetId}"]`);
        const currentTitle = conversationItem ? 
            conversationItem.querySelector('.conversation-title').textContent : 
            this.currentChatTitle.textContent;
        
        this.newTitleInput.value = currentTitle;
        this.renameModalOverlay.style.display = 'flex';
        this.newTitleInput.focus();
        this.newTitleInput.select();
    }
    
    hideRenameModal() {
        this.renameModalOverlay.style.display = 'none';
        this.newTitleInput.value = '';
        delete this.renameModalOverlay.dataset.conversationId;
    }
    
    async confirmRename() {
        const conversationId = parseInt(this.renameModalOverlay.dataset.conversationId);
        const newTitle = this.newTitleInput.value.trim();
        
        if (!newTitle) {
            this.showToast('請輸入對話標題', 'warning');
            return;
        }
        
        try {
            this.showLoading(true);
            const response = await fetch(`/api/conversations/${conversationId}/title`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: newTitle })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.hideRenameModal();
                await this.loadConversations();
                
                if (conversationId === this.currentConversationId) {
                    this.currentChatTitle.textContent = newTitle;
                    // 重新選中當前對話
                    const conversationItem = document.querySelector(`[data-conversation-id="${conversationId}"]`);
                    if (conversationItem) {
                        conversationItem.classList.add('active');
                    }
                }
                
                this.showToast('對話已重命名', 'success');
            } else {
                this.showToast('重命名失敗: ' + data.error, 'error');
            }
        } catch (error) {
            this.showToast('重命名失敗: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    confirmDeleteConversation(conversationId) {
        this.showModal(
            '刪除對話',
            '您確定要刪除這個對話嗎？此操作無法撤銷。',
            async () => {
                await this.deleteConversation(conversationId);
            }
        );
    }
    
    async deleteConversation(conversationId) {
        try {
            this.showLoading(true);
            const response = await fetch(`/api/conversations/${conversationId}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.loadConversations();
                
                if (conversationId === this.currentConversationId) {
                    this.currentConversationId = null;
                    this.currentChatTitle.textContent = '選擇或創建新對話';
                    this.chatInputContainer.style.display = 'none';
                    this.clearChatBtn.style.display = 'none';
                    this.renameChatBtn.style.display = 'none';
                    this.chatMessages.innerHTML = `
                        <div class="welcome-message">
                            <div class="welcome-icon">
                                <i class="fas fa-robot"></i>
                            </div>
                            <h2>Welcome to ChatBot</h2>
                            <p>Start a conversation or create a new chat to begin</p>
                        </div>
                    `;
                }
                
                this.showToast('對話已刪除', 'success');
            } else {
                this.showToast('刪除對話失敗: ' + data.error, 'error');
            }
        } catch (error) {
            this.showToast('刪除對話失敗: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    toggleSidebar() {
        this.sidebar.classList.toggle('open');
    }
    
    initializeTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);
    }
    
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }
    
    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        const icon = this.themeToggle.querySelector('i');
        const text = this.themeToggle.querySelector('span') || this.themeToggle;
        
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
            if (text.nodeType === Node.TEXT_NODE || text === this.themeToggle) {
                this.themeToggle.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
            }
        } else {
            icon.className = 'fas fa-moon';
            if (text.nodeType === Node.TEXT_NODE || text === this.themeToggle) {
                this.themeToggle.innerHTML = '<i class="fas fa-moon"></i> Dark Mode';
            }
        }
    }
    
    showModal(title, message, confirmCallback) {
        this.modalTitle.textContent = title;
        this.modalMessage.textContent = message;
        this.modalOverlay.style.display = 'flex';
        
        this.modalConfirm.onclick = () => {
            this.hideModal();
            if (confirmCallback) confirmCallback();
        };
    }
    
    hideModal() {
        this.modalOverlay.style.display = 'none';
        this.modalConfirm.onclick = null;
    }
    
    showLoading(show) {
        this.loadingOverlay.style.display = show ? 'flex' : 'none';
    }
    
    showToast(message, type = 'info', duration = 5000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        toast.innerHTML = `
            ${message}
            <button class="toast-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        this.toastContainer.appendChild(toast);
        
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, duration);
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// 初始化應用程式
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new ChatbotApp();
});

// 全局錯誤處理
window.addEventListener('error', (e) => {
    console.error('全局錯誤:', e.error);
    if (app) {
        app.showToast('發生未預期的錯誤', 'error');
    }
});

// 處理未處理的 Promise 拒絕
window.addEventListener('unhandledrejection', (e) => {
    console.error('未處理的 Promise 拒絕:', e.reason);
    if (app) {
        app.showToast('發生網路錯誤', 'error');
    }
});