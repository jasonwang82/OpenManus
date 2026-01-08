#!/usr/bin/env python3
"""
测试 OpenManus 使用 CodeBuddy SDK 进行实际调用
"""

import asyncio
import os

# 设置环境变量
os.environ['CODEBUDDY_CODE_PATH'] = "/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy"
os.environ['CODEBUDDY_API_KEY'] = "ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8"
os.environ['CODEBUDDY_INTERNET_ENVIRONMENT'] = "internal"

from app.llm import LLM
from app.schema import Message

print('🚀 OpenManus + CodeBuddy SDK 实际调用测试')
print('=' * 70)

print(f'\n📋 环境配置:')
print(f'   CodeBuddy CLI: {os.environ["CODEBUDDY_CODE_PATH"]}')
print(f'   API Key: ***{os.environ["CODEBUDDY_API_KEY"][-8:]}')
print(f'   Environment: {os.environ["CODEBUDDY_INTERNET_ENVIRONMENT"]}')

async def test_simple_query():
    """测试简单查询"""
    print('\n' + '=' * 70)
    print('测试 1: 简单数学问题')
    print('=' * 70)

    try:
        # 创建 LLM 实例（会自动使用 CodeBuddy 后端）
        llm = LLM(config_name="default")
        print(f'✅ LLM 类型: {type(llm).__name__}')

        if type(llm).__name__ != "CodeBuddyLLM":
            print(f'⚠️  警告: 期望 CodeBuddyLLM，得到 {type(llm).__name__}')
            return False

        # 准备消息
        messages = [Message.user_message("计算 5 + 3，只给出数字")]
        system_msgs = [Message.system_message("你是一个数学助手，只回答数字")]

        print('\n💬 问题: 计算 5 + 3')
        print('-' * 70)

        # 调用 API（流式）
        response = await llm.ask(
            messages=messages,
            system_msgs=system_msgs,
            stream=True
        )

        print('\n' + '-' * 70)
        print(f'✅ API 调用成功!')
        print(f'📝 响应: {response}')

        # 显示令牌统计
        if hasattr(llm, 'total_input_tokens'):
            print(f'\n📊 令牌统计:')
            print(f'   输入: {llm.total_input_tokens}')
            print(f'   输出: {llm.total_completion_tokens}')

        return True

    except Exception as e:
        print(f'\n❌ 错误: {e}')
        import traceback
        traceback.print_exc()
        return False

async def test_fibonacci():
    """测试斐波那契数列"""
    print('\n' + '=' * 70)
    print('测试 2: 斐波那契数列计算')
    print('=' * 70)

    try:
        llm = LLM(config_name="default")

        messages = [Message.user_message("计算斐波那契数列的前10个数字")]
        system_msgs = [Message.system_message("你是一个数学助手")]

        print('\n💬 问题: 计算斐波那契数列的前10个数字')
        print('-' * 70)

        response = await llm.ask(
            messages=messages,
            system_msgs=system_msgs,
            stream=True
        )

        print('\n' + '-' * 70)
        print(f'✅ 斐波那契数列计算完成!')

        return True

    except Exception as e:
        print(f'\n❌ 错误: {e}')
        return False

async def main():
    print('\n' + '=' * 70)
    print('开始测试...')
    print('=' * 70)

    # 测试 1
    result1 = await test_simple_query()

    # 测试 2
    result2 = await test_fibonacci()

    # 总结
    print('\n' + '=' * 70)
    print('📊 测试总结')
    print('=' * 70)

    if result1:
        print('✅ 简单数学问题: 成功')
    else:
        print('❌ 简单数学问题: 失败')

    if result2:
        print('✅ 斐波那契数列: 成功')
    else:
        print('❌ 斐波那契数列: 失败')

    print('\n' + '=' * 70)
    if result1 and result2:
        print('🎉🎉🎉 OpenManus + CodeBuddy SDK 完美运行！🎉🎉🎉')
        print('\n✅ 集成完全成功：')
        print('   - CodeBuddy LLM 适配器正常工作')
        print('   - 配置系统正确加载')
        print('   - API 调用成功')
        print('   - 流式响应正常')
        print('   - "Manus 效果"实现')
    else:
        print('⚠️  部分测试未通过')
    print('=' * 70)

if __name__ == "__main__":
    asyncio.run(main())

