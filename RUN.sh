#!/bin/bash
# OpenManus + CodeBuddy SDK 一键运行脚本

cd /Users/jasonwang/workspace/OpenManus
source .venv/bin/activate

# 设置 CodeBuddy 环境变量
export CODEBUDDY_CODE_PATH="/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy"
export CODEBUDDY_API_KEY="ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8"
export CODEBUDDY_INTERNET_ENVIRONMENT=internal

echo "🚀 OpenManus + CodeBuddy SDK"
echo "========================================================================"
echo "✅ CodeBuddy CLI: $(${CODEBUDDY_CODE_PATH} --version)"
echo "✅ Backend: CodeBuddy"
echo "✅ Environment: ${CODEBUDDY_INTERNET_ENVIRONMENT}"
echo "========================================================================"
echo ""

# 运行 OpenManus（传递命令行参数）
if [ $# -eq 0 ]; then
    echo "💡 用法示例:"
    echo "  ./RUN.sh --prompt \"计算斐波那契数列的前10个数字\""
    echo "  ./RUN.sh --prompt \"创建一个2048小游戏\""
    echo ""
    echo "或运行测试:"
    echo "  python test_openmanus_codebuddy.py"
else
    python main.py "$@"
fi

