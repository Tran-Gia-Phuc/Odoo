#!/bin/bash
set -e

# ==========================================
# CẤU HÌNH
# ==========================================
DB_NAME="test"
ODOO_CONTAINER="zoo17-odoo17-1"
DB_CONTAINER="zoo17-db-1"
ADDONS_DIR="/zoo17/addons"
BACKUP_DIR="/zoo17/backup"

# Telegram (tạo bot xong điền vào đây)
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
# BƯỚC 1 — Chỉ deploy khi addons thay đổi
# ==========================================
echo "=== [1/4] Kiểm tra thay đổi ==="

CHANGED=$(git -C $WORKSPACE diff --name-only HEAD~1 HEAD 2>/dev/null | grep "^addons/" || true)

if [ -z "$CHANGED" ]; then
    echo "Không có thay đổi trong addons, bỏ qua deploy."
    send_telegram "ℹ️ Không có thay đổi addons, bỏ qua restart."
    exit 0
fi

echo "Có thay đổi:"
echo "$CHANGED"

# ==========================================
# BƯỚC 2 — Backup database
# ==========================================
echo "=== [2/4] Backup database '$DB_NAME' ==="
mkdir -p $BACKUP_DIR

BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
docker exec $DB_CONTAINER pg_dump -U odoo $DB_NAME > $BACKUP_FILE

echo "Backup xong: $BACKUP_FILE"

# Chỉ giữ lại 5 bản backup gần nhất
ls -t $BACKUP_DIR/*.sql | tail -n +6 | xargs -r rm
echo "Đã xóa backup cũ, giữ lại 5 bản mới nhất."

# ==========================================
# BƯỚC 3 — Sync code mới vào /zoo17/addons
# ==========================================
echo "=== [3/4] Sync addons ==="
mkdir -p $ADDONS_DIR
cp -r $WORKSPACE/addons/. $ADDONS_DIR/
echo "Sync xong."

# ==========================================
# BƯỚC 4 — Restart Odoo + Update tất cả module
# ==========================================
echo "=== [4/4] Restart và update modules ==="
docker restart $ODOO_CONTAINER

echo "Đợi Odoo khởi động..."
sleep 20

docker exec $ODOO_CONTAINER odoo -u all -d $DB_NAME --stop-after-init
echo "Update modules xong."

echo "=== Check containers ==="
docker ps

echo "================================================"
echo "=== DEPLOY HOÀN THÀNH ==="
echo "================================================"
send_telegram "✅ Deploy Odoo thành công!
Commit: $GIT_COMMIT"