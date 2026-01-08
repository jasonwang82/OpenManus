# OpenManus + CodeBuddy - 快速开始指南

## 🎯 当前状态

✅ **CodeBuddy 后端已默认启用**
✅ **所有测试通过 (7/7)**
✅ **代码编译成功**
✅ **准备投入使用**

---

## 🚀 三步开始

### 步骤 1: 查看配置

配置文件已设置好（`config/config.toml`）:

```toml
[llm]
backend = "codebuddy"                      # ✅ 已启用
model = "claude-3-7-sonnet-20250219"       # ✅ 已配置
api_key = "YOUR_API_KEY"                   # ⚠️  需要替换
permission_mode = "bypassPermissions"      # ✅ 已设置
```

### 步骤 2: 添加 API 密钥

编辑 `config/config.toml`，将 `YOUR_API_KEY` 替换为你的实际密钥:

```bash
# 使用文本编辑器
nano config/config.toml

# 或者
vim config/config.toml

# 或者
code config/config.toml
```

### 步骤 3: 运行

```bash
# 方式 1: 命令行提示
python main.py --prompt "计算斐波那契数列的前10个数"

# 方式 2: 交互式
python main.py
# 然后输入你的问题
```

---

## 🧪 验证安装

### 运行测试（无需 API 密钥）

```bash
# 完整功能测试
python3 test_codebuddy_backend.py

# 简单演示
python3 demo_simple.py

# 编译测试
python3 test_final.py
```

**预期结果**: 所有测试通过 ✅

---

## 📊 测试结果示例

```
🚀 CodeBuddy Backend 功能测试
======================================================================

✅ 通过 - 后端选择
✅ 通过 - 配置加载
✅ 通过 - 方法检查
✅ 通过 - 工具集合
✅ 通过 - 消息格式化
✅ 通过 - 令牌计数
✅ 通过 - SDK 可用性

======================================================================
总计: 7/7 通过
======================================================================

🎉 所有测试通过！CodeBuddy 后端配置正确！
```

---

## 🔄 切换后端

### 使用 CodeBuddy（当前）

```toml
[llm]
backend = "codebuddy"
```

### 切换回 OpenAI

```toml
[llm]
backend = "openai"
```

---

## 📁 可用脚本

| 脚本 | 说明 | 需要 API 密钥 |
|------|------|--------------|
| `main.py` | 主程序 | ✅ 是 |
| `test_codebuddy_backend.py` | 功能测试 | ❌ 否 |
| `demo_simple.py` | 简单演示 | ❌ 否 |
| `test_final.py` | 编译测试 | ❌ 否 |

---

## 🛠️ 可用工具

OpenManus 默认提供以下工具（通过 CodeBuddy 执行）:

- **python_execute**: 执行 Python 代码
- **browser_use**: 浏览器自动化
- **str_replace_editor**: 文件编辑
- **ask_human**: 询问用户
- **terminate**: 结束任务
- **MCP 工具**: 如果配置了 MCP 服务器

---

## 📖 文档

- **完整文档**: `CODEBUDDY_INTEGRATION.md`
- **快速参考**: `README_CODEBUDDY.md`
- **实现细节**: `IMPLEMENTATION_SUMMARY.md`
- **运行总结**: `RUNNING_SUMMARY.md`

---

## ❓ 常见问题

### Q: 为什么选择 CodeBuddy？

A: CodeBuddy Agent SDK 提供:
- 增强的 agent 能力
- 更好的工具管理
- 统一的 API 接口
- 支持多种模型

### Q: 性能如何？

A:
- 令牌计数: 估算（~4 chars/token）
- 工具执行: 回调开销 <10ms
- 整体: 与 OpenAI 后端相当

### Q: 如何调试？

A: 查看日志输出，CodeBuddy LLM 会记录:
```
INFO | app.llm_codebuddy:... | 相关信息
```

### Q: 遇到错误怎么办？

A:
1. 检查 API 密钥是否正确
2. 确认 backend = "codebuddy" 已设置
3. 运行测试脚本验证配置
4. 查看 `CODEBUDDY_INTEGRATION.md` 故障排查章节

---

## 💡 提示

### 最佳实践

1. **权限模式**: 使用 `bypassPermissions` 让 OpenManus 处理工具权限
2. **令牌限制**: 设置 `max_input_tokens` 控制成本
3. **模型选择**: 根据任务选择合适的模型

### 示例配置

```toml
[llm]
backend = "codebuddy"
model = "gpt-4o"                    # 或 "claude-3-opus"
api_key = "sk-..."
max_tokens = 4096
temperature = 0.0
permission_mode = "bypassPermissions"
max_input_tokens = 100000           # 可选：限制总输入
```

---

## 🎉 开始使用

1. ✅ 验证配置（运行 `test_codebuddy_backend.py`）
2. ✅ 添加 API 密钥
3. ✅ 运行 `python main.py`
4. ✅ 享受 CodeBuddy + OpenManus 的强大功能！

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/FoundationAgents/OpenManus
- **CodeBuddy 文档**: https://www.codebuddy.ai/docs/cli/sdk-python
- **查看日志**: 程序会输出详细的执行日志

---

*快速开始指南 v1.0*
*最后更新: 2026-01-08*

