# 🚀 如何运行 OpenManus + CodeBuddy SDK

## ✅ 已验证可用！

OpenManus 通过 CodeBuddy SDK 调用已成功测试！

---

## 📝 运行命令（3种方式）

### 方式 1: 使用 run_manus_codebuddy.py（推荐）

这个脚本支持命令行参数和交互式输入：

**命令行参数方式**:
```bash
cd /Users/jasonwang/workspace/OpenManus
source .venv/bin/activate
export CODEBUDDY_CODE_PATH="/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy"
export CODEBUDDY_API_KEY="ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8"
export CODEBUDDY_INTERNET_ENVIRONMENT=internal

# 运行（指定 prompt）
python run_manus_codebuddy.py --prompt "计算斐波那契数列的前10个数字"
```

**交互式输入方式**:
```bash
# 先设置环境
cd /Users/jasonwang/workspace/OpenManus
source .venv/bin/activate
export CODEBUDDY_CODE_PATH="/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy"
export CODEBUDDY_API_KEY="ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8"
export CODEBUDDY_INTERNET_ENVIRONMENT=internal

# 运行（会提示输入）
python run_manus_codebuddy.py
> 计算10的阶乘  # 在这里输入你的问题
```

---

### 方式 2: 运行测试脚本（已验证）

```bash
cd /Users/jasonwang/workspace/OpenManus
source .venv/bin/activate
export CODEBUDDY_CODE_PATH="/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy"
export CODEBUDDY_API_KEY="ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8"
export CODEBUDDY_INTERNET_ENVIRONMENT=internal

python test_openmanus_codebuddy.py
```

**结果**:
```
✅ 简单数学问题: 成功 (5 + 3 = 8)
✅ 斐波那契数列: 成功
🎉 OpenManus + CodeBuddy SDK 完美运行！
```

---

### 方式 3: 使用 Bash 脚本

```bash
cd /Users/jasonwang/workspace/OpenManus
chmod +x RUN.sh
./RUN.sh --prompt "你的问题"
```

---

## 💡 快速命令（复制粘贴）

### 测试计算功能
```bash
cd /Users/jasonwang/workspace/OpenManus && source .venv/bin/activate && export CODEBUDDY_CODE_PATH="/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy" && export CODEBUDDY_API_KEY="ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8" && export CODEBUDDY_INTERNET_ENVIRONMENT=internal && python run_manus_codebuddy.py --prompt "计算10的阶乘"
```

### 测试斐波那契
```bash
cd /Users/jasonwang/workspace/OpenManus && source .venv/bin/activate && export CODEBUDDY_CODE_PATH="/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy" && export CODEBUDDY_API_KEY="ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8" && export CODEBUDDY_INTERNET_ENVIRONMENT=internal && python run_manus_codebuddy.py --prompt "计算斐波那契数列的前15个数字"
```

### 测试代码生成
```bash
cd /Users/jasonwang/workspace/OpenManus && source .venv/bin/activate && export CODEBUDDY_CODE_PATH="/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy" && export CODEBUDDY_API_KEY="ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8" && export CODEBUDDY_INTERNET_ENVIRONMENT=internal && python run_manus_codebuddy.py --prompt "用Python写一个冒泡排序"
```

---

## 📋 脚本功能

**run_manus_codebuddy.py** 支持:

1. ✅ **命令行参数**: `--prompt "你的问题"`
2. ✅ **交互式输入**: 不提供参数时会提示输入
3. ✅ **流式响应**: 实时显示生成的内容
4. ✅ **错误处理**: 完整的异常处理
5. ✅ **令牌统计**: 显示输入/输出令牌数
6. ✅ **日志记录**: 详细的执行日志

---

## 🎯 示例用法

### 示例 1: 数学计算
```bash
python run_manus_codebuddy.py --prompt "计算10的阶乘"
```

### 示例 2: 生成代码
```bash
python run_manus_codebuddy.py --prompt "用Python写一个快速排序算法"
```

### 示例 3: 数据分析
```bash
python run_manus_codebuddy.py --prompt "如何用pandas读取CSV文件并分析数据"
```

### 示例 4: 交互式
```bash
python run_manus_codebuddy.py
> 请解释什么是递归  # 输入你的问题
```

---

## 📊 预期输出

运行后您会看到：

```
🚀 OpenManus + CodeBuddy SDK
======================================================================

💬 问题: 计算10的阶乘
----------------------------------------------------------------------

[AI 的回答会实时流式显示在这里...]

----------------------------------------------------------------------
✅ 查询完成！响应长度: XXX 字符
📊 令牌统计: 输入=XX, 输出=XX, 总计=XXX

======================================================================
🎉 查询成功完成！
======================================================================
```

---

## 🎊 成功！

OpenManus + CodeBuddy SDK 集成完全成功并可以实际运行！

**使用**: `run_manus_codebuddy.py`
**方式**: 命令行参数 或 交互式输入
**状态**: ✅ 已验证可用

查看 `PROJECT_COMPLETION_REPORT.md` 了解完整的集成详情！

