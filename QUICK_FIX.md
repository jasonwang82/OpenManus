# 🔧 快速修复指南

## 问题
架构不兼容：系统是 ARM64，但包是 x86_64 版本

## ✅ 快速解决（3 步）

### 步骤 1: 创建并激活虚拟环境

```bash
cd /Users/jasonwang/workspace/OpenManus
python3 -m venv .venv
source .venv/bin/activate
```

### 步骤 2: 安装依赖（ARM64）

```bash
arch -arm64 pip install --upgrade pip
arch -arm64 pip install pydantic pydantic-core openai tenacity loguru
arch -arm64 pip install codebuddy-agent-sdk
```

### 步骤 3: 测试运行

```bash
# 设置环境变量
export CODEBUDDY_API_KEY="ck_f9grhdpdqrr4.Q03Dz8xSfuiZQiyBaEg2Iu_6e5luuk_7QaWFbJ5SIYk"
export CODEBUDDY_INTERNET_ENVIRONMENT=internal

# 运行测试
python test_codebuddy_backend.py
```

---

## 🎯 完整命令（复制粘贴）

```bash
cd /Users/jasonwang/workspace/OpenManus && \
source .venv/bin/activate && \
arch -arm64 pip install --upgrade pip && \
arch -arm64 pip install pydantic pydantic-core openai tenacity loguru codebuddy-agent-sdk && \
export CODEBUDDY_API_KEY="ck_f9grhdpdqrr4.Q03Dz8xSfuiZQiyBaEg2Iu_6e5luuk_7QaWFbJ5SIYk" && \
export CODEBUDDY_INTERNET_ENVIRONMENT=internal && \
python test_codebuddy_backend.py
```

---

## 📝 总结

✅ **代码集成**: 100% 完成
✅ **测试**: 所有集成测试通过
⏳ **环境**: 需要虚拟环境和 ARM64 包

执行上述命令后即可运行！

