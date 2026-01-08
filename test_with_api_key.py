#!/usr/bin/env python3
"""
使用实际 API 密钥测试 CodeBuddy SDK
"""

import asyncio
import os
from app.llm import LLM
from app.schema import Message

async def test_fibonacci():
    """测试斐波那契数列计算"""
    print('=' * 70)
    print('🚀 CodeBuddy SDK 实际 API 调用测试')
    print('=' * 70)

    # 检查环境变量
    api_key = os.getenv('CODEBUDDY_API_KEY')
    env = os.getenv('CODEBUDDY_INTERNET_ENVIRONMENT')

    print(f'\n📋 环境变量:')
    print(f'   CODEBUDDY_API_KEY: {"已设置 (***" + api_key[-8:] + ")" if api_key else "未设置"}')
    print(f'   CODEBUDDY_INTERNET_ENVIRONMENT: {env if env else "未设置"}')

    if not api_key:
        print('\n⚠️  警告: CODEBUDDY_API_KEY 未设置')
        print('请运行: export CODEBUDDY_API_KEY="your-key"')
        return False

    try:
        print('\n💬 测试问题: 计算斐波那契数列的前10个数字')
        print('-' * 70)

        # 创建 LLM 实例
        llm = LLM(config_name="default")
        print(f'✅ LLM 类型: {type(llm).__name__}')

        # 准备消息
        messages = [
            Message.user_message("计算斐波那契数列的前10个数字")
        ]

        system_msgs = [
            Message.system_message("你是一个数学助手。请直接给出答案。")
        ]

        print('\n🔄 正在调用 CodeBuddy SDK API...')
        print('-' * 70)

        # 调用 API
        response = await llm.ask(
            messages=messages,
            system_msgs=system_msgs,
            stream=True
        )

        print('\n' + '-' * 70)
        print(f'\n✅ API 调用成功!')
        print(f'\n📝 完整响应:\n{response}')

        # 显示统计
        if hasattr(llm, 'total_input_tokens'):
            print(f'\n📊 令牌统计:')
            print(f'   输入: {llm.total_input_tokens}')
            print(f'   输出: {llm.total_completion_tokens}')
            print(f'   总计: {llm.total_input_tokens + llm.total_completion_tokens}')

        return True

    except Exception as e:
        print(f'\n❌ 错误: {e}')
        import traceback
        traceback.print_exc()
        return False

async def main():
    success = await test_fibonacci()

    print('\n' + '=' * 70)
    if success:
        print('🎉 测试成功！CodeBuddy SDK + OpenManus 正常工作！')
    else:
        print('⚠️  测试失败，请检查配置和环境变量')
    print('=' * 70)

if __name__ == "__main__":
    asyncio.run(main())

