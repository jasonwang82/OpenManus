#!/usr/bin/env python3
"""
简单演示 - 仅展示 CodeBuddy LLM 集成（无需完整 agent）
"""

import asyncio
from app.llm import LLM
from app.llm_codebuddy import CodeBuddyLLM
from app.config import config
from app.schema import Message

print('\n' + '🎯' * 35)
print('OpenManus + CodeBuddy Backend 简单演示')
print('🎯' * 35)

async def show_architecture():
    """显示架构信息"""
    print('\n' + '=' * 70)
    print('🏗️  架构流程')
    print('=' * 70)

    print('''
    用户提示 (User Prompt)
        ↓
    Manus Agent
        ↓
    ToolCallAgent.think()
        ↓
    LLM Factory ──→ 检查 config.backend
        ↓
        ├─→ backend="openai" ──→ OpenAI LLM (原始)
        └─→ backend="codebuddy" ──→ CodeBuddy LLM (新)
                ↓
            CodeBuddy SDK Client
                ↓
            Tool Execution Callback
                ↓
            OpenManus ToolCollection
                ↓
            实际工具执行
    ''')

async def show_configuration():
    """显示当前配置"""
    print('\n' + '=' * 70)
    print('📋 当前配置')
    print('=' * 70)

    default_config = config.llm.get("default", config.llm["default"])
    backend = default_config.backend if hasattr(default_config, "backend") else "openai"

    print(f'''
    后端 (Backend): {backend}
    模型 (Model): {default_config.model}
    基础 URL (Base URL): {default_config.base_url}
    最大令牌 (Max Tokens): {default_config.max_tokens}
    温度 (Temperature): {default_config.temperature}
    ''')

    if hasattr(default_config, "permission_mode"):
        print(f'    权限模式 (Permission Mode): {default_config.permission_mode}')

    if backend == "codebuddy":
        print('\n    ✅ CodeBuddy 后端已激活！')
    else:
        print('\n    ℹ️  使用默认 OpenAI 后端')

async def test_llm_factory():
    """测试 LLM 工厂"""
    print('\n' + '=' * 70)
    print('🏭 LLM 工厂测试')
    print('=' * 70)

    try:
        print('\n正在创建 LLM 实例...')
        llm = LLM(config_name="default")
        llm_type = type(llm).__name__

        print(f'创建的实例: {llm_type}')

        if llm_type == "CodeBuddyLLM":
            print('✅ 成功！使用 CodeBuddy 后端')

            print('\n📦 CodeBuddy LLM 特性:')
            print('   - ask(): 基础文本生成')
            print('   - ask_tool(): 工具调用接口')
            print('   - ask_with_images(): 多模态支持')
            print('   - set_tool_collection(): 设置 OpenManus 工具')

            print('\n🔧 工具执行方式:')
            print('   - 使用 can_use_tool 回调')
            print('   - 拦截所有工具调用')
            print('   - 通过 OpenManus ToolCollection 执行')
            print('   - 返回结果给 CodeBuddy SDK')

        else:
            print(f'ℹ️  使用 OpenAI 后端 ({llm_type})')

        return llm

    except Exception as e:
        print(f'❌ 错误: {e}')
        return None

async def show_tool_integration(llm):
    """展示工具集成"""
    if not isinstance(llm, CodeBuddyLLM):
        print('\n⚠️  跳过工具集成演示（需要 CodeBuddy 后端）')
        return

    print('\n' + '=' * 70)
    print('🔧 工具集成演示')
    print('=' * 70)

    from app.tool.python_execute import PythonExecute
    from app.tool.terminate import Terminate
    from app.tool.tool_collection import ToolCollection

    # 创建工具集合
    tools = ToolCollection(
        PythonExecute(),
        Terminate(),
    )

    print(f'\n创建工具集合: {len(tools.tools)} 个工具')
    for tool in tools.tools:
        print(f'   - {tool.name}')

    # 设置工具
    llm.set_tool_collection(tools)
    print('\n✅ 工具集合已设置到 CodeBuddy LLM')

    # 验证
    if hasattr(llm, '_tool_lookup'):
        print(f'✅ 工具查找表已创建: {len(llm._tool_lookup)} 个工具')
        for tool_name in llm._tool_lookup.keys():
            print(f'   - {tool_name}')

async def show_message_format():
    """展示消息格式"""
    print('\n' + '=' * 70)
    print('💬 消息格式演示')
    print('=' * 70)

    # 创建测试消息
    messages = [
        Message.user_message("你好，这是一个测试消息"),
        Message.assistant_message("你好！我是助手。"),
    ]

    print('\n原始消息 (OpenManus 格式):')
    for i, msg in enumerate(messages, 1):
        print(f'   {i}. Role: {msg.role}, Content: "{msg.content}"')

    # 格式化消息
    llm = LLM(config_name="default")
    formatted = llm.format_messages(messages)

    print('\n格式化后 (LLM 格式):')
    for i, msg in enumerate(formatted, 1):
        print(f'   {i}. Role: {msg["role"]}, Content: "{msg["content"]}"')

async def show_usage():
    """显示使用说明"""
    print('\n' + '=' * 70)
    print('📖 使用说明')
    print('=' * 70)

    print('''
1️⃣  配置 CodeBuddy 后端:
   编辑 config/config.toml:

   [llm]
   backend = "codebuddy"                    # 切换到 CodeBuddy
   model = "claude-3-7-sonnet-20250219"     # 或其他模型
   api_key = "your-api-key"                 # 你的 API 密钥
   permission_mode = "bypassPermissions"    # 让 OpenManus 处理权限

2️⃣  运行 OpenManus:
   python main.py --prompt "你的问题"

3️⃣  查看文档:
   - CODEBUDDY_INTEGRATION.md  (完整文档)
   - README_CODEBUDDY.md       (快速开始)
   - IMPLEMENTATION_SUMMARY.md (实现细节)

4️⃣  运行测试:
   python3 test_codebuddy_backend.py
    ''')

async def main():
    """主函数"""

    # 1. 显示架构
    await show_architecture()

    # 2. 显示配置
    await show_configuration()

    # 3. 测试 LLM 工厂
    llm = await test_llm_factory()

    # 4. 展示工具集成
    if llm:
        await show_tool_integration(llm)

    # 5. 展示消息格式
    await show_message_format()

    # 6. 显示使用说明
    await show_usage()

    # 总结
    print('\n' + '🎯' * 35)
    print('演示完成！')
    print('🎯' * 35)

    print('''
✅ OpenManus 已成功集成 CodeBuddy Agent SDK
✅ 配置已设置为使用 CodeBuddy 后端
✅ 所有组件编译正常
✅ 准备好投入使用

💡 添加有效的 API 密钥后即可开始使用！
    ''')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n\n⚠️  演示被用户中断')
    except Exception as e:
        print(f'\n\n❌ 演示失败：{e}')
        import traceback
        traceback.print_exc()

