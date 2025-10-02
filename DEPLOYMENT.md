# 部署指南

本文檔提供了在不同環境中部署 AI 聊天機器人的詳細指南。

## 📋 部署前檢查清單

- [ ] 已設置正確的環境變數（`.env` 檔案）
- [ ] LLM API 服務器可訪問
- [ ] 資料庫目錄有寫入權限
- [ ] 防火牆已正確配置
- [ ] SSL 憑證已準備（生產環境）

## 🐳 Docker 部署

### 創建 Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴檔案
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式檔案
COPY . .

# 創建資料庫目錄
RUN mkdir -p database

# 暴露端口
EXPOSE 5001

# 啟動命令
CMD ["python", "app.py"]
```

### 創建 docker-compose.yml

```yaml
version: '3.8'

services:
  chatbot:
    build: .
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    env_file:
      - .env
    volumes:
      - ./database:/app/database
    restart: unless-stopped
```

### 構建和運行

```bash
# 構建映像
docker build -t ai-chatbot .

# 運行容器
docker run -d \
  --name ai-chatbot \
  -p 5001:5001 \
  --env-file .env \
  -v $(pwd)/database:/app/database \
  ai-chatbot

# 或使用 docker-compose
docker-compose up -d
```

## ☁️ 雲端部署

### AWS EC2

1. **啟動 EC2 實例**
   ```bash
   # 選擇 Ubuntu 20.04 LTS
   # 實例類型：t3.medium 或更高
   # 安全組：開放 80, 443, 5001 端口
   ```

2. **安裝依賴**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip nginx
   
   # 安裝 PM2（可選）
   sudo npm install -g pm2
   ```

3. **部署應用**
   ```bash
   git clone <your-repo-url>
   cd chatbot
   pip3 install -r requirements.txt
   
   # 配置環境變數
   cp .env.example .env
   nano .env
   
   # 使用 PM2 運行
   pm2 start app.py --name chatbot --interpreter python3
   ```

### Google Cloud Platform

1. **使用 Cloud Run**
   ```bash
   # 構建並推送到 Container Registry
   gcloud builds submit --tag gcr.io/PROJECT_ID/chatbot
   
   # 部署到 Cloud Run
   gcloud run deploy chatbot \
     --image gcr.io/PROJECT_ID/chatbot \
     --platform managed \
     --port 5001 \
     --allow-unauthenticated
   ```

### Heroku

1. **準備 Heroku 檔案**
   
   創建 `Procfile`：
   ```
   web: gunicorn --worker-class eventlet -w 1 app:app
   ```
   
   創建 `runtime.txt`：
   ```
   python-3.9.18
   ```

2. **部署**
   ```bash
   heroku create your-app-name
   heroku config:set LLM_API_URL=your-api-url
   heroku config:set LLM_API_KEY=your-api-key
   heroku config:set SECRET_KEY=your-secret-key
   git push heroku main
   ```

## 🔒 SSL/TLS 配置

### 使用 Let's Encrypt

```bash
# 安裝 certbot
sudo apt install certbot python3-certbot-nginx

# 獲取憑證
sudo certbot --nginx -d yourdomain.com

# 自動續期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Nginx 配置

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL 配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /socket.io {
        proxy_pass http://127.0.0.1:5001/socket.io;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔍 監控與日誌

### 使用 PM2

```bash
# 查看狀態
pm2 status

# 查看日誌
pm2 logs chatbot

# 重啟應用
pm2 restart chatbot

# 設置自啟動
pm2 startup
pm2 save
```

### 日誌配置

創建 `logging.conf`：

```ini
[loggers]
keys=root,chatbot

[handlers]
keys=fileHandler,consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=fileHandler,consoleHandler

[logger_chatbot]
level=DEBUG
handlers=fileHandler
qualname=chatbot

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('logs/chatbot.log',)

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## 📊 效能優化

### 資料庫優化

```python
# 在 config/config.py 中添加
class ProductionConfig(Config):
    # 使用 PostgreSQL 或 MySQL
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/chatbot')
    
    # 連接池配置
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True
    }
```

### 快取配置

```python
# 安裝 Redis
# pip install redis flask-caching

from flask_caching import Cache

cache = Cache()
cache.init_app(app, config={'CACHE_TYPE': 'redis'})

# 快取對話列表
@cache.memoize(timeout=300)
def get_cached_conversations():
    return db_manager.get_conversations()
```

## 🚨 故障排除

### 常見部署問題

1. **端口衝突**
   ```bash
   # 查看端口使用情況
   sudo netstat -tlnp | grep :5001
   
   # 殺死佔用端口的進程
   sudo kill -9 <PID>
   ```

2. **權限問題**
   ```bash
   # 設置正確的檔案權限
   sudo chown -R www-data:www-data /path/to/chatbot
   sudo chmod -R 755 /path/to/chatbot
   ```

3. **記憶體不足**
   ```bash
   # 創建 swap 檔案
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### 健康檢查

創建 `health_check.py`：

```python
#!/usr/bin/env python3
import requests
import sys

def health_check():
    try:
        response = requests.get('http://localhost:5001/api/status', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 應用程式運行正常")
                return True
        print("❌ 應用程式狀態異常")
        return False
    except Exception as e:
        print(f"❌ 健康檢查失敗: {e}")
        return False

if __name__ == "__main__":
    if not health_check():
        sys.exit(1)
```

## 📞 支援

如果在部署過程中遇到問題：

1. 檢查日誌檔案
2. 驗證環境變數配置
3. 確認網路連接
4. 查看防火牆設定
5. 提交 GitHub Issue 尋求幫助