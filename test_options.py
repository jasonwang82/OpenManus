#!/usr/bin/env python3
"""
测试不同的 CodeBuddy options
"""

import asyncio
import os

os.environ['CODEBUDDY_CODE_PATH'] = "/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy"
os.environ['CODEBUDDY_API_KEY'] = "ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8"
os.environ['CODEBUDDY_INTERNET_ENVIRONMENT'] = "internal"

from codebuddy_agent_sdk import query, CodeBuddyAgentOptions

print('🔍 测试不同的 CodeBuddy Options')
print('=' * 70)

async def test_no_options():
    """无选项"""
    print('\n测试 1: 无选项（默认）')
    print('-' * 70)

    async for message in query(prompt='What is 5 + 3?'):
        msg_type = type(message).__name__
        if msg_type == "AssistantMessage":
            for block in message.content:
                if type(block).__name__ == "TextBlock":
                    print(f'✅ 响应: {block.text}')
        elif msg_type == "ResultMessage":
            break

async def test_with_model():
    """指定模型"""
    print('\n测试 2: 指定模型')
    print('-' * 70)

    options = CodeBuddyAgentOptions(
        model="claude-3-7-sonnet-20250219"
    )

    async for message in query(prompt='What is 5 + 3?', options=options):
        msg_type = type(message).__name__
        if msg_type == "AssistantMessage":
            for block in message.content:
                if type(block).__name__ == "TextBlock":
                    print(f'✅ 响应: {block.text}')
        elif msg_type == "ResultMessage":
            break

async def test_with_permission():
    """指定权限模式"""
    print('\n测试 3: 指定权限模式')
    print('-' * 70)

    options = CodeBuddyAgentOptions(
        model="claude-3-7-sonnet-20250219",
        permission_mode="bypassPermissions"
    )

    async for message in query(prompt='What is 5 + 3?', options=options):
        msg_type = type(message).__name__
        if msg_type == "AssistantMessage":
            for block in message.content:
                if type(block).__name__ == "TextBlock":
                    print(f'✅ 响应: {block.text}')
        elif msg_type == "ResultMessage":
            break

async def test_with_all_options():
    """所有选项"""
    print('\n测试 4: 所有选项（类似 OpenManus）')
    print('-' * 70)

    options = CodeBuddyAgentOptions(
        model="claude-3-7-sonnet-20250219",
        permission_mode="bypassPermissions",
        max_turns=1,
        include_partial_messages=True
    )

    async for message in query(prompt='What is 5 + 3?', options=options):
        msg_type = type(message).__name__
        print(f'[{msg_type}]', end=' ')
        if msg_type == "AssistantMessage":
            for block in message.content:
                if type(block).__name__ == "TextBlock":
                    print(f'{block.text}', end='')
        elif msg_type == "ResultMessage":
            print()
            break

async def main():
    await test_no_options()
    await test_with_model()
    await test_with_permission()
    await test_with_all_options()

    print('\n' + '=' * 70)
    print('测试完成')
    print('=' * 70)

asyncio.run(main())

