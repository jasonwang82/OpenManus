#!/usr/bin/env python3
"""
调试提示格式
"""

import asyncio
import os

os.environ['CODEBUDDY_CODE_PATH'] = "/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy"
os.environ['CODEBUDDY_API_KEY'] = "ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8"
os.environ['CODEBUDDY_INTERNET_ENVIRONMENT'] = "internal"

from app.llm import LLM
from app.schema import Message

print('🔍 调试提示格式')
print('=' * 70)

async def test():
    llm = LLM(config_name="default")

    messages = [Message.user_message("计算 5 + 3")]
    system_msgs = [Message.system_message("你是一个数学助手")]

    # 格式化消息
    if system_msgs:
        system_msgs_formatted = llm.format_messages(system_msgs, supports_images=False)
        messages_formatted = system_msgs_formatted + llm.format_messages(messages, supports_images=False)
    else:
        messages_formatted = llm.format_messages(messages, supports_images=False)

    print('\n格式化后的消息:')
    for i, msg in enumerate(messages_formatted):
        print(f'{i+1}. {msg}')

    # 转换为提示
    if hasattr(llm, '_messages_to_prompt'):
        prompt = llm._messages_to_prompt(messages_formatted)
        print(f'\n转换后的提示:')
        print(f'"{prompt}"')
        print(f'\n提示长度: {len(prompt)} 字符')

    # 测试直接 SDK 调用
    print('\n' + '=' * 70)
    print('测试: 直接 SDK 调用（使用转换后的提示）')
    print('=' * 70)

    from codebuddy_agent_sdk import query

    async for message in query(prompt=prompt):
        msg_type = type(message).__name__
        print(f'[{msg_type}]', end=' ')

        if msg_type == "AssistantMessage":
            if hasattr(message, 'content'):
                for block in message.content:
                    if type(block).__name__ == "TextBlock" and hasattr(block, 'text'):
                        print(block.text, end='')

        elif msg_type == "ResultMessage":
            print()
            break

asyncio.run(test())

