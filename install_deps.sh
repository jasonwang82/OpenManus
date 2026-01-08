#!/bin/bash
# 安装依赖脚本 - 确保架构一致

set -e

echo "🔧 OpenManus 依赖安装脚本"
echo "========================================================================"

# 激活虚拟环境
cd /Users/jasonwang/workspace/OpenManus
source .venv/bin/activate

echo ""
echo "📦 步骤 1: 升级 pip..."
pip install --upgrade pip setuptools wheel

echo ""
echo "📦 步骤 2: 安装核心依赖..."
pip install pydantic~=2.10.6
pip install pydantic-core~=2.27.2
pip install openai~=1.66.3
pip install tenacity~=9.0.0
pip install loguru~=0.7.3
pip install tiktoken~=0.9.0

echo ""
echo "📦 步骤 3: 安装 CodeBuddy SDK..."
pip install codebuddy-agent-sdk

echo ""
echo "📦 步骤 4: 安装其他必需依赖..."
pip install pyyaml aiofiles colorama

echo ""
echo "✅ 核心依赖安装完成！"
echo ""
echo "🧪 验证安装..."
python -c "import pydantic; print('✅ pydantic')"
python -c "import tiktoken; print('✅ tiktoken')"
python -c "import openai; print('✅ openai')"
python -c "from codebuddy_agent_sdk import query; print('✅ codebuddy-agent-sdk')"

echo ""
echo "========================================================================"
echo "✅ 安装成功！"
echo "========================================================================"
echo ""
echo "现在可以运行测试:"
echo "  export CODEBUDDY_API_KEY=\"your-key\""
echo "  export CODEBUDDY_INTERNET_ENVIRONMENT=internal"
echo "  python test_codebuddy_backend.py"
echo ""

