#!/usr/bin/env python3
"""
CodeBuddy Backend 演示脚本
此脚本演示如何使用 CodeBuddy 作为 OpenManus 的后端
"""

import asyncio
from app.agent.manus import Manus
from app.logger import logger

async def demo_simple_query():
    """演示 1: 简单查询"""
    print('\n' + '=' * 70)
    print('演示 1: 简单查询 (无工具)')
    print('=' * 70)

    try:
        # 创建 Manus agent（会自动使用配置的 CodeBuddy 后端）
        logger.info("创建 Manus agent...")
        agent = await Manus.create()

        # 检查使用的 LLM 类型
        llm_type = type(agent.llm).__name__
        logger.info(f"Agent 使用的 LLM: {llm_type}")

        if llm_type == "CodeBuddyLLM":
            print("✅ 确认：使用 CodeBuddy 后端")
        else:
            print(f"⚠️  警告：使用的是 {llm_type} 而不是 CodeBuddy")

        # 简单的数学问题
        prompt = "请计算：2 + 2 = ?"
        print(f"\n💬 提问: {prompt}")
        print(f"\n🤖 Manus 回答:")
        print("-" * 70)

        # 注意：这需要有效的 API key 才能实际运行
        # 如果没有 API key，会显示认证错误
        try:
            await agent.run(prompt)
        except Exception as e:
            if "authentication" in str(e).lower() or "api" in str(e).lower():
                print(f"\n⚠️  API 认证错误（预期）：{e}")
                print("\n💡 要实际运行，请在 config/config.toml 中添加有效的 API 密钥")
            else:
                raise

        await agent.cleanup()

    except Exception as e:
        logger.error(f"演示失败: {e}")
        import traceback
        traceback.print_exc()

async def demo_with_tools():
    """演示 2: 带工具的查询"""
    print('\n' + '=' * 70)
    print('演示 2: 工具调用 (Python 执行)')
    print('=' * 70)

    try:
        logger.info("创建 Manus agent...")
        agent = await Manus.create()

        # 检查工具集合
        tool_count = len(agent.available_tools.tools)
        logger.info(f"可用工具数: {tool_count}")

        print(f"\n📦 可用工具 ({tool_count} 个):")
        for tool in agent.available_tools.tools:
            print(f"   - {tool.name}: {tool.description[:60]}...")

        # 需要工具的问题
        prompt = "请使用 Python 计算斐波那契数列的前 10 个数字"
        print(f"\n💬 提问: {prompt}")
        print(f"\n🤖 Manus 回答:")
        print("-" * 70)

        try:
            await agent.run(prompt)
        except Exception as e:
            if "authentication" in str(e).lower() or "api" in str(e).lower():
                print(f"\n⚠️  API 认证错误（预期）：{e}")
                print("\n💡 要实际运行，请在 config/config.toml 中添加有效的 API 密钥")
            else:
                raise

        await agent.cleanup()

    except Exception as e:
        logger.error(f"演示失败: {e}")
        import traceback
        traceback.print_exc()

async def demo_architecture():
    """演示 3: 架构信息"""
    print('\n' + '=' * 70)
    print('演示 3: 架构信息')
    print('=' * 70)

    try:
        from app.config import config

        # 显示配置
        default_config = config.llm.get("default", config.llm["default"])

        print('\n🏗️  架构流程:')
        print('   用户提示')
        print('      ↓')
        print('   Manus Agent')
        print('      ↓')
        print('   ToolCallAgent.think()')
        print('      ↓')
        print('   LLM Factory')
        print('      ↓')
        backend = default_config.backend if hasattr(default_config, "backend") else "openai"
        if backend == "codebuddy":
            print('   CodeBuddy LLM ← [您在这里]')
            print('      ↓')
            print('   CodeBuddy SDK Client')
            print('      ↓')
            print('   Tool Execution Callback')
            print('      ↓')
            print('   OpenManus ToolCollection')
            print('      ↓')
            print('   工具执行 (PythonExecute, BrowserUseTool 等)')
        else:
            print('   OpenAI LLM (默认)')

        print('\n📋 当前配置:')
        print(f'   后端: {backend}')
        print(f'   模型: {default_config.model}')
        print(f'   权限模式: {default_config.permission_mode if hasattr(default_config, "permission_mode") else "N/A"}')

        print('\n🔄 工具执行流程:')
        print('   1. Agent 调用 llm.ask_tool()')
        print('   2. CodeBuddy SDK 处理请求')
        print('   3. SDK 决定使用工具')
        print('   4. 调用 can_use_tool 回调')
        print('   5. 回调通过 OpenManus 执行工具')
        print('   6. 结果返回给 SDK')
        print('   7. SDK 返回最终响应')

    except Exception as e:
        logger.error(f"演示失败: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """主函数"""
    print('\n' + '🎯' * 35)
    print('OpenManus + CodeBuddy Backend 演示')
    print('🎯' * 35)

    # 演示 3: 架构信息（不需要 API key）
    await demo_architecture()

    print('\n' + '=' * 70)
    print('说明：以下演示需要有效的 API 密钥')
    print('=' * 70)

    # 演示 1: 简单查询
    # await demo_simple_query()

    # 演示 2: 工具调用
    # await demo_with_tools()

    print('\n' + '=' * 70)
    print('📚 更多信息')
    print('=' * 70)
    print('\n1️⃣  配置文件: config/config.toml')
    print('   当前已设置为使用 CodeBuddy 后端')
    print('   添加有效的 API 密钥即可运行')

    print('\n2️⃣  完整文档: CODEBUDDY_INTEGRATION.md')
    print('   包含详细的配置说明和使用示例')

    print('\n3️⃣  快速开始: README_CODEBUDDY.md')
    print('   3 步快速设置指南')

    print('\n4️⃣  实际运行:')
    print('   # 添加 API 密钥到 config/config.toml 后运行:')
    print('   python main.py --prompt "你的问题"')

    print('\n' + '🎯' * 35)
    print('演示完成！')
    print('🎯' * 35)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n\n⚠️  演示被用户中断')
    except Exception as e:
        print(f'\n\n❌ 演示失败：{e}')
        import traceback
        traceback.print_exc()

