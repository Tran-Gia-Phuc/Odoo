#!/bin/bash 
set -e 
 
# ========================================== 
# CẤU HÌNH 
# ========================================== 
DB_NAME="test" 
ODOO_CONTAINER="zoo17-odoo17-1" 
DB_CONTAINER="zoo17-db-1" 
ADDONS_DIR="/zoo17/addons" 
 
# Telegram 
TELEGRAM_TOKEN="8891955831:AAFlT0DQtN4pednHINba87bKRya3PH_Pi9o" 
TELEGRAM_CHAT_ID="5594081068" 
 
# ========================================== 
# HÀM THÔNG BÁO TELEGRAM 
# ========================================== 
send_telegram() { 
    local message=$1 
    if [ "$TELEGRAM_TOKEN" != "YOUR_BOT_TOKEN" ]; then 
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \ 
            -d chat_id="$TELEGRAM_CHAT_ID" \ 
            -d text="$message" > /dev/null 
    fi 
} 
 
echo "================================================" 
echo "=== BẮT ĐẦU DEPLOY ODOO 17 ===" 
echo "================================================" 
send_telegram "🚀 Bắt đầu deploy Odoo... 
Commit: $GIT_COMMIT 
Branch: $GIT_BRANCH" 
 
# ========================================== 
# BƯỚC 1 — Kiểm tra thay đổi 
# ========================================== 
echo "=== [1/3] Kiểm tra thay đổi ===" 
 
CHANGED=$(git -C $WORKSPACE diff --name-only HEAD~1 HEAD 2>/dev/null | grep "^addons/" || true) 
 
if [ -z "$CHANGED" ]; then 
    echo "Không có thay đổi trong addons, bỏ qua deploy." 
    send_telegram "ℹ️ Không có thay đổi addons 
Bỏ qua deploy." 
    exit 0 
fi 
 
send_telegram "📂 Phát hiện thay đổi: 
$CHANGED" 
 
# ========================================== 
# BƯỚC 2 — Sync addons 
# ========================================== 
echo "=== [2/3] Sync addons ===" 
mkdir -p $ADDONS_DIR 
cp -r $WORKSPACE/addons/. $ADDONS_DIR/ 
 
send_telegram "📦 Sync addons xong 
✅ Code mới đã được copy vào server" 
 
# ========================================== 
# BƯỚC 3 — Restart + Update App List 
# ========================================== 
echo "=== [3/3] Restart và update app list ===" 
docker restart $ODOO_CONTAINER 
send_telegram "🔄 Docker restart zoo17-odoo17-1... 
⏳ Đợi Odoo khởi động (20s)" 
 
sleep 20

# Update app list (base module để refresh danh sách module)
docker exec $ODOO_CONTAINER odoo -u base -d $DB_NAME --stop-after-init 
 
send_telegram "✅ Update app list xong 
🟢 Odoo đã sẵn sàng!" 
 
echo "=== Check containers ===" 
docker ps 
 
echo "================================================" 
echo "=== DEPLOY HOÀN THÀNH ===" 
echo "================================================" 
send_telegram "🎉 DEPLOY HOÀN THÀNH! 
────────────────── 
🗄️ Database: $DB_NAME 
📌 Commit: $GIT_COMMIT 
⏱️ Thời gian: $(date '+%H:%M:%S %d/%m/%Y')"