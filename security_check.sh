#!/bin/bash

# 安全檢查腳本 - 檢查專案中是否包含敏感資訊

echo "🔒 開始安全檢查..."

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 檢查結果計數
WARNINGS=0
ERRORS=0

# 檢查 .env 檔案是否在 .gitignore 中
echo "📋 檢查 .gitignore 配置..."
if [ -f ".gitignore" ]; then
    if grep -q "\.env" .gitignore; then
        echo -e "${GREEN}✅ .env 檔案已在 .gitignore 中${NC}"
    else
        echo -e "${RED}❌ .env 檔案未在 .gitignore 中${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}❌ 缺少 .gitignore 檔案${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 檢查是否存在 .env.example
echo "📄 檢查環境變數範例檔案..."
if [ -f ".env.example" ]; then
    echo -e "${GREEN}✅ .env.example 檔案存在${NC}"
else
    echo -e "${YELLOW}⚠️  建議創建 .env.example 檔案${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# 檢查敏感資訊模式
echo "🔍 掃描敏感資訊..."

SENSITIVE_PATTERNS=(
    "password"
    "secret"
    "key"
    "token"
    "api_key"
    "private"
    "credential"
)

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    # 在 Python 檔案中搜尋
    results=$(find . -name "*.py" -not -path "./tests/*" -not -path "./.git/*" -exec grep -l -i "$pattern" {} \; 2>/dev/null)
    if [ ! -z "$results" ]; then
        echo -e "${YELLOW}⚠️  在以下檔案中發現可能的敏感資訊 ($pattern):${NC}"
        echo "$results"
        WARNINGS=$((WARNINGS + 1))
    fi
done

# 檢查硬編碼的 IP 地址
echo "🌐 檢查硬編碼的 IP 地址..."
ip_results=$(find . -name "*.py" -not -path "./tests/*" -not -path "./.git/*" -exec grep -n -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" {} + 2>/dev/null)
if [ ! -z "$ip_results" ]; then
    echo -e "${YELLOW}⚠️  發現硬編碼的 IP 地址:${NC}"
    echo "$ip_results"
    WARNINGS=$((WARNINGS + 1))
fi

# 檢查硬編碼的端口號
echo "🔌 檢查硬編碼的端口號..."
port_results=$(find . -name "*.py" -not -path "./tests/*" -not -path "./.git/*" -exec grep -n -E ":[0-9]{4,5}" {} + 2>/dev/null | grep -v "http://localhost" | grep -v "127.0.0.1")
if [ ! -z "$port_results" ]; then
    echo -e "${YELLOW}⚠️  發現硬編碼的端口號:${NC}"
    echo "$port_results"
    WARNINGS=$((WARNINGS + 1))
fi

# 檢查資料庫檔案是否在 .gitignore 中
echo "🗄️  檢查資料庫檔案..."
if [ -f ".gitignore" ]; then
    if grep -q "\.db" .gitignore && grep -q "\.sqlite" .gitignore; then
        echo -e "${GREEN}✅ 資料庫檔案已在 .gitignore 中${NC}"
    else
        echo -e "${YELLOW}⚠️  建議將資料庫檔案加入 .gitignore${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# 檢查日誌檔案是否在 .gitignore 中
echo "📝 檢查日誌檔案..."
if [ -f ".gitignore" ]; then
    if grep -q "\.log" .gitignore; then
        echo -e "${GREEN}✅ 日誌檔案已在 .gitignore 中${NC}"
    else
        echo -e "${YELLOW}⚠️  建議將日誌檔案加入 .gitignore${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# 檢查是否存在測試用的敏感資料
echo "🧪 檢查測試檔案..."
test_sensitive=$(find ./tests -name "*.py" -exec grep -l -E "(password|secret|key|token)" {} \; 2>/dev/null)
if [ ! -z "$test_sensitive" ]; then
    echo -e "${YELLOW}⚠️  測試檔案中可能包含敏感資訊:${NC}"
    echo "$test_sensitive"
    WARNINGS=$((WARNINGS + 1))
fi

# 檢查 requirements.txt 中是否有安全版本
echo "📦 檢查依賴套件安全性..."
if [ -f "requirements.txt" ]; then
    # 檢查是否有版本固定
    unfixed_deps=$(grep -v "==" requirements.txt | grep -v "^#" | grep -v "^$")
    if [ ! -z "$unfixed_deps" ]; then
        echo -e "${YELLOW}⚠️  建議固定以下套件版本:${NC}"
        echo "$unfixed_deps"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${RED}❌ 缺少 requirements.txt 檔案${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 檢查 Flask 配置
echo "🌶️  檢查 Flask 安全配置..."
debug_check=$(find . -name "*.py" -exec grep -n "debug.*=.*True" {} + 2>/dev/null)
if [ ! -z "$debug_check" ]; then
    echo -e "${YELLOW}⚠️  發現 Debug 模式可能在生產環境中啟用:${NC}"
    echo "$debug_check"
    WARNINGS=$((WARNINGS + 1))
fi

# 檢查是否有未使用的檔案
echo "🗑️  檢查未使用的檔案..."
backup_files=$(find . -name "*.bak" -o -name "*.backup" -o -name "*~" -o -name "*.orig" 2>/dev/null)
if [ ! -z "$backup_files" ]; then
    echo -e "${YELLOW}⚠️  發現備份檔案，建議清理:${NC}"
    echo "$backup_files"
    WARNINGS=$((WARNINGS + 1))
fi

# 檢查檔案權限
echo "🔐 檢查檔案權限..."
if [ -f ".env" ]; then
    env_perm=$(stat -c "%a" .env 2>/dev/null || stat -f "%OLp" .env 2>/dev/null)
    if [ "$env_perm" = "644" ] || [ "$env_perm" = "600" ]; then
        echo -e "${GREEN}✅ .env 檔案權限正確${NC}"
    else
        echo -e "${YELLOW}⚠️  .env 檔案權限建議設為 600 或 644${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# 生成報告
echo ""
echo "📊 安全檢查報告"
echo "=================="
echo -e "錯誤: ${RED}$ERRORS${NC}"
echo -e "警告: ${YELLOW}$WARNINGS${NC}"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}🎉 恭喜！沒有發現安全問題${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  發現 $WARNINGS 個警告，建議處理後再上傳${NC}"
    exit 1
else
    echo -e "${RED}❌ 發現 $ERRORS 個錯誤，必須修復後才能上傳${NC}"
    exit 2
fi