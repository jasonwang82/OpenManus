#!/bin/bash
# OpenManus + CodeBuddy 一键运行脚本

set -e

cd /Users/jasonwang/workspace/OpenManus
source .venv/bin/activate

# 设置 CodeBuddy 环境变量
export CODEBUDDY_CODE_PATH="/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy"
export CODEBUDDY_API_KEY="ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8"
export CODEBUDDY_INTERNET_ENVIRONMENT=internal

echo "🚀 OpenManus + CodeBuddy SDK"
echo "========================================================================"
echo ""
echo "✅ CodeBuddy CLI: v$(${CODEBUDDY_CODE_PATH} --version)"
echo "✅ API Key: ***${CODEBUDDY_API_KEY: -8}"
echo "✅ Environment: ${CODEBUDDY_INTERNET_ENVIRONMENT}"
echo ""

# 运行 OpenManus
echo "运行命令: $@"
echo "========================================================================"
echo ""

python main.py "$@"

