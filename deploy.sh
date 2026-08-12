#!/bin/bash
# AI交付管理能力培训 — 一键部署
# 用法: ./deploy.sh

set -e
TARGET="aliyun:/var/www/training"

echo "📦 部署前端+API…"
scp src/index.html src/api.php $TARGET/

echo "📦 部署内容JSON…"
ssh aliyun "mkdir -p /var/www/training/content/lessons /var/www/training/users"
scp content/manifest.json content/matrix.json content/curriculum.json $TARGET/content/
scp content/lessons/*.json $TARGET/content/lessons/ 2>/dev/null || echo "  (no lesson files to deploy)"

echo "✅ 部署完成 → https://workbench.dgjoystar.com/training/"
