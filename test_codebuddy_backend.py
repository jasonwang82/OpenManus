#!/usr/bin/env python3
"""
测试 CodeBuddy 后端的完整功能
Test CodeBuddy Backend Functionality
"""

import asyncio
from app.llm import LLM
from app.llm_codebuddy import CodeBuddyLLM
from app.config import config
from app.schema import Message
from app.tool.python_execute import PythonExecute
from app.tool.terminate import Terminate
from app.tool.tool_collection import ToolCollection
from app.logger import logger

print('🚀 CodeBuddy Backend 功能测试')
print('=' * 70)

async def test_backend_selection():
    """测试后端选择"""
    print('\n📋 测试 1: 后端选择')
    print('-' * 70)

    try:
        llm = LLM(config_name="default")
        llm_type = type(llm).__name__

        print(f'   创建的实例类型: {llm_type}')

        if llm_type == "CodeBuddyLLM":
            print('   ✅ 成功！使用 CodeBuddy 后端')
            return True, llm
        else:
            print(f'   ❌ 错误：期望 CodeBuddyLLM，得到 {llm_type}')
            print(f'   提示：请确保 config.toml 中设置了 backend = "codebuddy"')
            return False, None
    except Exception as e:
        print(f'   ❌ 错误：{e}')
        return False, None

async def test_configuration():
    """测试配置加载"""
    print('\n📋 测试 2: 配置加载')
    print('-' * 70)

    try:
        default_config = config.llm.get("default", config.llm["default"])

        print(f'   后端 (Backend): {default_config.backend if hasattr(default_config, "backend") else "未设置"}')
        print(f'   模型 (Model): {default_config.model}')
        print(f'   基础URL (Base URL): {default_config.base_url}')
        print(f'   最大令牌数 (Max Tokens): {default_config.max_tokens}')
        print(f'   温度 (Temperature): {default_config.temperature}')

        if hasattr(default_config, "permission_mode"):
            print(f'   权限模式 (Permission Mode): {default_config.permission_mode}')

        if hasattr(default_config, "backend") and default_config.backend == "codebuddy":
            print('   ✅ CodeBuddy 配置正确')
            return True
        else:
            print('   ⚠️  backend 未设置为 "codebuddy"')
            return False
    except Exception as e:
        print(f'   ❌ 错误：{e}')
        return False

async def test_methods():
    """测试 LLM 方法"""
    print('\n📋 测试 3: LLM 方法检查')
    print('-' * 70)

    try:
        llm = LLM(config_name="default")

        required_methods = [
            'ask',
            'ask_tool',
            'ask_with_images',
            'count_tokens',
            'count_message_tokens',
            'update_token_count',
            'check_token_limit',
        ]

        all_present = True
        for method in required_methods:
            if hasattr(llm, method):
                print(f'   ✅ {method}()')
            else:
                print(f'   ❌ {method}() 缺失')
                all_present = False

        # CodeBuddy 特有方法
        if type(llm).__name__ == "CodeBuddyLLM":
            if hasattr(llm, 'set_tool_collection'):
                print(f'   ✅ set_tool_collection() [CodeBuddy 特有]')
            else:
                print(f'   ❌ set_tool_collection() 缺失')
                all_present = False

        if all_present:
            print('   ✅ 所有必需方法都存在')
            return True
        else:
            print('   ❌ 部分方法缺失')
            return False
    except Exception as e:
        print(f'   ❌ 错误：{e}')
        return False

async def test_tool_collection():
    """测试工具集合设置"""
    print('\n📋 测试 4: 工具集合设置')
    print('-' * 70)

    try:
        llm = LLM(config_name="default")

        if not isinstance(llm, CodeBuddyLLM):
            print('   ⚠️  跳过：不是 CodeBuddy 后端')
            return True

        # 创建工具集合
        tools = ToolCollection(
            PythonExecute(),
            Terminate(),
        )

        print(f'   创建工具集合：{len(tools.tools)} 个工具')

        # 设置工具集合
        llm.set_tool_collection(tools)
        print(f'   ✅ 工具集合设置成功')

        # 验证工具已设置
        if hasattr(llm, '_tool_lookup') and len(llm._tool_lookup) > 0:
            print(f'   ✅ 工具查找表已创建：{len(llm._tool_lookup)} 个工具')
            for tool_name in llm._tool_lookup.keys():
                print(f'      - {tool_name}')
            return True
        else:
            print(f'   ⚠️  工具查找表为空')
            return False
    except Exception as e:
        print(f'   ❌ 错误：{e}')
        import traceback
        traceback.print_exc()
        return False

async def test_message_formatting():
    """测试消息格式化"""
    print('\n📋 测试 5: 消息格式化')
    print('-' * 70)

    try:
        llm = LLM(config_name="default")

        # 测试消息
        messages = [
            Message.user_message("测试消息"),
            Message.assistant_message("测试响应"),
        ]

        # 格式化消息
        formatted = llm.format_messages(messages)

        print(f'   原始消息数: {len(messages)}')
        print(f'   格式化后: {len(formatted)}')

        for i, msg in enumerate(formatted):
            print(f'   消息 {i+1}: role={msg["role"]}, content={msg["content"][:50]}...')

        print('   ✅ 消息格式化成功')
        return True
    except Exception as e:
        print(f'   ❌ 错误：{e}')
        return False

async def test_token_counting():
    """测试令牌计数"""
    print('\n📋 测试 6: 令牌计数')
    print('-' * 70)

    try:
        llm = LLM(config_name="default")

        test_text = "这是一个测试文本，用于验证令牌计数功能。This is a test text for token counting."

        token_count = llm.count_tokens(test_text)
        print(f'   测试文本: "{test_text}"')
        print(f'   令牌数 (估算): {token_count}')

        # 测试消息令牌计数
        messages = [
            {"role": "user", "content": test_text},
            {"role": "assistant", "content": "响应文本"}
        ]

        message_tokens = llm.count_message_tokens(messages)
        print(f'   消息令牌总数 (估算): {message_tokens}')

        print('   ✅ 令牌计数功能正常')
        return True
    except Exception as e:
        print(f'   ❌ 错误：{e}')
        return False

async def test_sdk_availability():
    """测试 CodeBuddy SDK 可用性"""
    print('\n📋 测试 7: CodeBuddy SDK 可用性')
    print('-' * 70)

    try:
        from codebuddy_agent_sdk import query, CodeBuddySDKClient
        print('   ✅ CodeBuddy SDK 已安装')
        print('   ✅ 可以导入 query 函数')
        print('   ✅ 可以导入 CodeBuddySDKClient 类')
        return True
    except ImportError as e:
        print(f'   ❌ CodeBuddy SDK 未安装: {e}')
        print('   提示：运行 pip install codebuddy-agent-sdk')
        return False

async def main():
    """运行所有测试"""
    print('\n' + '=' * 70)
    print('开始测试...')
    print('=' * 70)

    results = []

    # 测试 1: 后端选择
    result1, llm = await test_backend_selection()
    results.append(("后端选择", result1))

    # 如果后端选择失败，显示配置说明
    if not result1:
        print('\n' + '=' * 70)
        print('⚠️  配置说明')
        print('=' * 70)
        print('\n请在 config/config.toml 中添加：')
        print('```toml')
        print('[llm]')
        print('backend = "codebuddy"')
        print('permission_mode = "bypassPermissions"')
        print('```')
        return

    # 测试 2-7
    result2 = await test_configuration()
    results.append(("配置加载", result2))

    result3 = await test_methods()
    results.append(("方法检查", result3))

    result4 = await test_tool_collection()
    results.append(("工具集合", result4))

    result5 = await test_message_formatting()
    results.append(("消息格式化", result5))

    result6 = await test_token_counting()
    results.append(("令牌计数", result6))

    result7 = await test_sdk_availability()
    results.append(("SDK 可用性", result7))

    # 打印总结
    print('\n' + '=' * 70)
    print('📊 测试总结')
    print('=' * 70)

    for test_name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        print(f'{status} - {test_name}')

    # 统计
    passed = sum(1 for _, r in results if r)
    total = len(results)

    print('\n' + '=' * 70)
    print(f'总计: {passed}/{total} 通过')
    print('=' * 70)

    if passed == total:
        print('\n🎉 所有测试通过！CodeBuddy 后端配置正确！')
        print('\n💡 下一步：')
        print('   1. 在 config/config.toml 中添加有效的 API 密钥')
        print('   2. 运行: python main.py --prompt "你的问题"')
        print('   3. 享受 CodeBuddy + OpenManus 的强大功能！')
    else:
        print(f'\n⚠️  {total - passed} 个测试失败，请检查配置')

    return passed == total

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print('\n\n⚠️  测试被用户中断')
        exit(1)
    except Exception as e:
        print(f'\n\n❌ 测试失败：{e}')
        import traceback
        traceback.print_exc()
        exit(1)

