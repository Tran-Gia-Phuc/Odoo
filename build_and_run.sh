#!/bin/bash
set -e

echo "================================================"
echo "=== BẮT ĐẦU DEPLOY ODOO 17 ==="
echo "================================================"

echo "=== [1/3] Pulling latest code ==="
cd /zoo17
git pull origin main

echo "=== [2/3] Restart Odoo only ==="
docker restart zoo17-odoo17-1

echo "=== [3/3] Check containers ==="
docker ps

echo "================================================"
echo "=== DEPLOY HOÀN THÀNH ==="
echo "================================================"