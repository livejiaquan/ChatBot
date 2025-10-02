from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, default='新對話')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯到訊息
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' 或 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # 關聯到對話
    conversation = relationship("Conversation", back_populates="messages")

class DatabaseManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.create_tables()
    
    def create_tables(self):
        """創建資料庫表格"""
        # 確保資料庫目錄存在
        db_dir = os.path.dirname(self.engine.url.database.replace('sqlite:///', ''))
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """獲取資料庫會話"""
        return self.SessionLocal()
    
    def create_conversation(self, title="新對話"):
        """創建新對話"""
        session = self.get_session()
        try:
            conversation = Conversation(title=title)
            session.add(conversation)
            session.commit()
            conversation_id = conversation.id
            return conversation_id
        finally:
            session.close()
    
    def get_conversations(self):
        """獲取所有對話列表"""
        session = self.get_session()
        try:
            conversations = session.query(Conversation).order_by(Conversation.updated_at.desc()).all()
            return [{
                'id': conv.id,
                'title': conv.title,
                'created_at': conv.created_at.isoformat(),
                'updated_at': conv.updated_at.isoformat(),
                'message_count': len(conv.messages)
            } for conv in conversations]
        finally:
            session.close()
    
    def get_conversation_messages(self, conversation_id):
        """獲取對話的所有訊息"""
        session = self.get_session()
        try:
            messages = session.query(Message).filter(
                Message.conversation_id == conversation_id
            ).order_by(Message.timestamp).all()
            return [{
                'id': msg.id,
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            } for msg in messages]
        finally:
            session.close()
    
    def add_message(self, conversation_id, role, content):
        """添加訊息到對話"""
        session = self.get_session()
        try:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content
            )
            session.add(message)
            
            # 更新對話的 updated_at
            conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            if conversation:
                conversation.updated_at = datetime.utcnow()
            
            session.commit()
            return message.id
        finally:
            session.close()
    
    def delete_conversation(self, conversation_id):
        """刪除對話"""
        session = self.get_session()
        try:
            conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            if conversation:
                session.delete(conversation)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def update_conversation_title(self, conversation_id, new_title):
        """更新對話標題"""
        session = self.get_session()
        try:
            conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            if conversation:
                conversation.title = new_title
                conversation.updated_at = datetime.utcnow()
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def clear_conversation(self, conversation_id):
        """清空對話訊息"""
        session = self.get_session()
        try:
            session.query(Message).filter(
                Message.conversation_id == conversation_id
            ).delete()
            
            # 更新對話的 updated_at
            conversation = session.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            if conversation:
                conversation.updated_at = datetime.utcnow()
            
            session.commit()
            return True
        finally:
            session.close()

# 創建全局資料庫管理器實例
database_url = "sqlite:///database/chatbot.db"
db_manager = DatabaseManager(database_url)