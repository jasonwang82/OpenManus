#!/bin/bash
# OpenManus + CodeBuddy 一键设置和运行脚本

set -e

echo "🚀 OpenManus + CodeBuddy SDK 设置脚本"
echo "========================================================================"

# 1. 激活虚拟环境
echo ""
echo "📦 步骤 1: 激活虚拟环境..."
cd /Users/jasonwang/workspace/OpenManus
source .venv/bin/activate
echo "✅ 虚拟环境已激活"

# 2. 安装依赖（ARM64）
echo ""
echo "📦 步骤 2: 安装依赖（ARM64 架构）..."
echo "   这可能需要几分钟..."
arch -arm64 pip install --upgrade pip setuptools wheel -q
arch -arm64 pip install -r requirements.txt -q
echo "✅ 依赖安装完成"

# 3. 验证导入
echo ""
echo "🔍 步骤 3: 验证安装..."
python -c "import pydantic; print('   ✅ pydantic')"
python -c "from app.llm import LLM; print('   ✅ LLM')"
python -c "from app.llm_codebuddy import CodeBuddyLLM; print('   ✅ CodeBuddyLLM')"
python -c "from app.config import config; print('   ✅ config')"
echo "✅ 所有模块导入成功"

# 4. 设置环境变量
echo ""
echo "🔑 步骤 4: 设置环境变量..."
export CODEBUDDY_API_KEY="ck_f9grhdpdqrr4.Q03Dz8xSfuiZQiyBaEg2Iu_6e5luuk_7QaWFbJ5SIYk"
export CODEBUDDY_INTERNET_ENVIRONMENT=internal
echo "✅ CodeBuddy 环境变量已设置"

# 5. 运行测试
echo ""
echo "🧪 步骤 5: 运行集成测试..."
python test_codebuddy_backend.py

echo ""
echo "========================================================================"
echo "✅ 设置完成！"
echo "========================================================================"
echo ""
echo "现在可以运行 OpenManus:"
echo "  python main.py --prompt \"计算斐波那契数列\""
echo ""
echo "或运行其他测试:"
echo "  python demo_simple.py"
echo "  python demo_codebuddy_api_call.py"
echo ""

