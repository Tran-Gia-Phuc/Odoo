#!/bin/bash
set -e

echo "================================================"
echo "=== BẮT ĐẦU DEPLOY ODOO 17 ==="
echo "================================================"

echo "=== [1/3] Sync code từ Jenkins workspace vào /zoo17 ==="
cp -r $WORKSPACE/addons/. /zoo17/addons/

echo "=== [2/3] Restart Odoo ==="
docker restart zoo17-odoo17-1

echo "=== [3/3] Check containers ==="
docker ps

echo "================================================"
echo "=== DEPLOY HOÀN THÀNH ==="
echo "================================================"