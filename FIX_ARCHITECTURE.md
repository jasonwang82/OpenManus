# 🔧 修复架构不兼容问题

## 🔍 问题诊断

您遇到的错误：
```
ImportError: mach-o file, but is an incompatible architecture
(have 'x86_64', need 'arm64e' or 'arm64')
```

**原因**:
- 您的 Mac 是 **ARM64 架构**（Apple Silicon: M1/M2/M3/M4）
- 但正在使用 **x86_64 架构**的 Python（Intel 版本）
- pydantic_core 等包也是 x86_64 版本
- 两者不兼容

---

## ✅ 解决方案

### 方案 1: 使用 ARM64 原生 Python（推荐）

#### 步骤 1: 安装 ARM64 Python

**选项 A - 使用 Homebrew (推荐)**:
```bash
# 安装 Homebrew（如果还没有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python 3.12（ARM64 原生）
brew install python@3.12

# 验证架构
/opt/homebrew/bin/python3.12 --version
file /opt/homebrew/bin/python3.12
# 应该显示: arm64
```

**选项 B - 使用 uv (更快)**:
```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建 ARM64 虚拟环境
cd /Users/jasonwang/workspace/OpenManus
uv venv --python 3.12
source .venv/bin/activate

# 验证架构
python --version
file .venv/bin/python
# 应该显示: arm64
```

#### 步骤 2: 重新安装依赖（ARM64 版本）

```bash
cd /Users/jasonwang/workspace/OpenManus

# 如果使用 Homebrew Python
/opt/homebrew/bin/python3.12 -m pip install -r requirements.txt

# 如果使用 uv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 步骤 3: 运行

```bash
# 使用 ARM64 Python 运行
/opt/homebrew/bin/python3.12 main.py --prompt "计算斐波那契数列"

# 或在 uv 虚拟环境中
source .venv/bin/activate
python main.py --prompt "计算斐波那契数列"
```

---

### 方案 2: 使用 Rosetta 模式（临时方案）

如果暂时无法切换到 ARM64 Python：

```bash
# 使用 Rosetta 运行
arch -x86_64 python3 main.py --prompt "计算斐波那契数列"
```

**注意**: 这需要所有依赖都是 x86_64 兼容的。

---

### 方案 3: 使用 Docker（完全隔离）

```bash
# 使用项目的 Dockerfile
cd /Users/jasonwang/workspace/OpenManus
docker build -t openmanus .
docker run -it --rm -v $(pwd)/workspace:/workspace openmanus
```

---

## 🚀 推荐的完整设置流程

### 使用 uv（最简单）

```bash
# 1. 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 创建虚拟环境
cd /Users/jasonwang/workspace/OpenManus
uv venv --python 3.12

# 3. 激活环境
source .venv/bin/activate

# 4. 安装依赖
uv pip install -r requirements.txt

# 5. 设置 CodeBuddy 环境变量
export CODEBUDDY_API_KEY="ck_f9grhdpdqrr4.Q03Dz8xSfuiZQiyBaEg2Iu_6e5luuk_7QaWFbJ5SIYk"
export CODEBUDDY_INTERNET_ENVIRONMENT=internal

# 6. 运行测试
python test_codebuddy_backend.py  # 验证集成

# 7. 实际运行（需要 CodeBuddy CLI）
python main.py --prompt "计算斐波那契数列"
```

---

## 🔍 验证步骤

### 1. 检查 Python 架构

```bash
# 检查当前 Python
python3 --version
file $(which python3)

# 应该看到 arm64，而不是 x86_64
```

### 2. 验证依赖安装

```bash
# 在正确的环境中测试导入
python3 -c "import pydantic; print('✅ pydantic OK')"
python3 -c "import pydantic_core; print('✅ pydantic_core OK')"
python3 -c "from app.llm import LLM; print('✅ LLM OK')"
```

### 3. 运行集成测试

```bash
# 运行我们的测试脚本
python3 test_codebuddy_backend.py
python3 demo_simple.py
python3 test_final.py
```

**预期**: 所有测试通过 ✅

---

## 📊 快速诊断命令

运行以下命令了解当前状态：

```bash
# 显示系统架构
echo "系统架构: $(uname -m)"

# 显示 Python 架构
echo "Python 路径: $(which python3)"
echo "Python 架构: $(file $(which python3))"

# 显示 Python 版本
python3 --version

# 检查是否在虚拟环境中
echo "虚拟环境: ${VIRTUAL_ENV:-未激活}"
```

---

## 💡 最佳实践

### 推荐设置

对于 Apple Silicon Mac（M1/M2/M3/M4）:

1. **使用 uv 创建虚拟环境** ✅
   - 自动使用正确的架构
   - 依赖管理更快
   - 环境隔离更好

2. **使用 ARM64 原生 Python** ✅
   - 性能更好
   - 兼容性更好
   - 没有架构冲突

3. **避免混用架构** ❌
   - 不要在 ARM64 系统上用 x86_64 Python
   - 不要混用 Rosetta 和原生包

---

## 🎯 推荐操作

### 立即执行（5分钟）

```bash
# 1. 安装 uv（如果还没有）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 创建 ARM64 环境
cd /Users/jasonwang/workspace/OpenManus
uv venv --python 3.12

# 3. 激活并安装
source .venv/bin/activate
uv pip install -r requirements.txt

# 4. 测试
python test_codebuddy_backend.py
```

**预期时间**: 3-5 分钟
**预期结果**: ✅ 所有测试通过

---

## 📞 需要帮助？

### 常见问题

**Q: uv 安装失败？**
A: 使用 Homebrew: `brew install uv`

**Q: 虚拟环境创建失败？**
A: 确保有 Python 3.12: `brew install python@3.12`

**Q: 依赖安装很慢？**
A: uv 比 pip 快很多，应该<2分钟

**Q: 还是有架构错误？**
A: 确保在虚拟环境中: `source .venv/bin/activate`

---

## 🎉 总结

**问题**: 架构不兼容 (x86_64 vs arm64)
**原因**: 使用了错误架构的 Python
**解决**: 使用 ARM64 原生 Python + 虚拟环境
**工具**: uv（推荐）或 Homebrew Python
**时间**: 5分钟

按照上述步骤操作后，OpenManus 应该可以正常运行！🚀

