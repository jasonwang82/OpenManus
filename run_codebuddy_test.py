#!/usr/bin/env python3
"""
CodeBuddy SDK 实际运行测试
使用提供的 API 密钥进行真实调用
"""

import asyncio
import os
import sys

print('🚀 CodeBuddy SDK 实际运行测试')
print('=' * 70)

# 检查环境变量
api_key = os.getenv('CODEBUDDY_API_KEY')
env = os.getenv('CODEBUDDY_INTERNET_ENVIRONMENT')

print(f'\n📋 环境变量检查:')
if api_key:
    print(f'   ✅ CODEBUDDY_API_KEY: 已设置 (***{api_key[-8:]})')
else:
    print(f'   ❌ CODEBUDDY_API_KEY: 未设置')
    print('\n   请运行:')
    print('   export CODEBUDDY_API_KEY="your-key"')
    sys.exit(1)

if env:
    print(f'   ✅ CODEBUDDY_INTERNET_ENVIRONMENT: {env}')
else:
    print(f'   ℹ️  CODEBUDDY_INTERNET_ENVIRONMENT: 未设置')

async def test_direct_sdk():
    """直接测试 CodeBuddy SDK"""
    print('\n' + '=' * 70)
    print('测试 1: 直接调用 CodeBuddy SDK')
    print('=' * 70)

    try:
        from codebuddy_agent_sdk import query
        print('✅ SDK 导入成功')

        print('\n💬 问题: What is 2 + 2? Answer briefly.')
        print('-' * 70)

        response_text = []
        async for message in query(prompt='What is 2 + 2? Answer briefly.'):
            msg_type = type(message).__name__

            if msg_type == 'AssistantMessage':
                if hasattr(message, 'content'):
                    for block in message.content:
                        block_type = type(block).__name__
                        if block_type == 'TextBlock' and hasattr(block, 'text'):
                            text = block.text
                            print(text, end='', flush=True)
                            response_text.append(text)

            elif msg_type == 'ResultMessage':
                print('\n' + '-' * 70)
                print('✅ 调用完成')
                if hasattr(message, 'duration_ms'):
                    print(f'⏱️  耗时: {message.duration_ms}ms')
                break

        full_response = ''.join(response_text)
        print(f'\n📝 完整响应: {full_response}')
        return True

    except Exception as e:
        print(f'\n❌ 错误: {e}')
        import traceback
        traceback.print_exc()
        return False

async def test_via_openmanus():
    """通过 OpenManus 的 CodeBuddy LLM 测试"""
    print('\n' + '=' * 70)
    print('测试 2: 通过 OpenManus CodeBuddyLLM 调用')
    print('=' * 70)

    try:
        from app.llm import LLM
        from app.schema import Message

        print('正在创建 LLM 实例...')
        llm = LLM(config_name="default")
        llm_type = type(llm).__name__

        print(f'✅ LLM 类型: {llm_type}')

        if llm_type != "CodeBuddyLLM":
            print(f'⚠️  警告: 期望 CodeBuddyLLM，得到 {llm_type}')
            print('   配置可能未正确加载，使用的是 OpenAI 后端')
            return False

        print('\n💬 问题: 计算 2 + 2')
        print('-' * 70)

        messages = [Message.user_message("What is 2 + 2? Please answer very briefly.")]
        response = await llm.ask(messages, stream=True)

        print('\n' + '-' * 70)
        print(f'✅ 调用成功!')
        print(f'📝 响应: {response}')

        return True

    except Exception as e:
        print(f'\n❌ 错误: {e}')
        import traceback
        traceback.print_exc()
        return False

async def main():
    print('\n' + '=' * 70)
    print('开始测试...')
    print('=' * 70)

    # 测试 1: 直接 SDK 调用
    result1 = await test_direct_sdk()

    # 测试 2: 通过 OpenManus 调用
    # result2 = await test_via_openmanus()

    # 总结
    print('\n' + '=' * 70)
    print('📊 测试总结')
    print('=' * 70)

    if result1:
        print('✅ CodeBuddy SDK 直接调用: 成功')
    else:
        print('❌ CodeBuddy SDK 直接调用: 失败')

    # if result2:
    #     print('✅ OpenManus CodeBuddyLLM 调用: 成功')
    # else:
    #     print('❌ OpenManus CodeBuddyLLM 调用: 失败')

    print('\n' + '=' * 70)
    if result1:
        print('🎉 CodeBuddy SDK 工作正常！')
        print('\n💡 下一步: 配置 OpenManus 使用 CodeBuddy 后端')
    else:
        print('⚠️  部分测试失败，请检查配置')
    print('=' * 70)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n\n⚠️  测试被用户中断')
    except Exception as e:
        print(f'\n\n❌ 测试失败: {e}')
        import traceback
        traceback.print_exc()

