#!/usr/bin/env python3
"""
调试 CodeBuddy SDK 响应
"""

import asyncio
import os

os.environ['CODEBUDDY_CODE_PATH'] = "/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy"
os.environ['CODEBUDDY_API_KEY'] = "ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8"
os.environ['CODEBUDDY_INTERNET_ENVIRONMENT'] = "internal"

from codebuddy_agent_sdk import query

print('🔍 CodeBuddy SDK 响应调试')
print('=' * 70)

async def test_direct():
    """直接调用 SDK"""
    print('\n测试 1: 直接调用（简单提示）')
    print('-' * 70)

    async for message in query(prompt='What is 5 + 3?'):
        msg_type = type(message).__name__
        print(f'\n[{msg_type}]')

        if msg_type == "AssistantMessage":
            print(f'  content: {message.content}')
            if hasattr(message, 'content'):
                for i, block in enumerate(message.content):
                    block_type = type(block).__name__
                    print(f'  Block {i}: {block_type}')
                    if hasattr(block, 'text'):
                        print(f'    text: {block.text}')

        elif msg_type == "ResultMessage":
            print(f'  duration_ms: {message.duration_ms if hasattr(message, "duration_ms") else "N/A"}')
            break

async def test_with_system():
    """带系统提示的调用"""
    print('\n\n测试 2: 带系统提示')
    print('-' * 70)

    # 构造完整的提示
    full_prompt = "system: 你是一个数学助手\n\nuser: 计算 5 + 3，只给出数字"

    async for message in query(prompt=full_prompt):
        msg_type = type(message).__name__
        print(f'\n[{msg_type}]')

        if msg_type == "AssistantMessage":
            if hasattr(message, 'content'):
                for block in message.content:
                    if type(block).__name__ == "TextBlock" and hasattr(block, 'text'):
                        print(f'  text: {block.text}')

        elif msg_type == "ResultMessage":
            break

async def main():
    await test_direct()
    await test_with_system()

    print('\n' + '=' * 70)
    print('调试完成')
    print('=' * 70)

if __name__ == "__main__":
    asyncio.run(main())

