#!/usr/bin/env python3
"""
OpenManus + CodeBuddy SDK 运行脚本
支持命令行参数和交互式输入
"""

import argparse
import asyncio
import os
import sys

# 设置 CodeBuddy 环境变量
os.environ['CODEBUDDY_CODE_PATH'] = "/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy"
os.environ['CODEBUDDY_API_KEY'] = "ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8"
os.environ['CODEBUDDY_INTERNET_ENVIRONMENT'] = "internal"

from app.llm import LLM
from app.schema import Message
from app.logger import logger

print('🚀 OpenManus + CodeBuddy SDK')
print('=' * 70)

async def run_query(prompt: str):
    """
    使用 CodeBuddy SDK 运行查询

    Args:
        prompt: 用户输入的提示词
    """
    try:
        # 创建 LLM 实例（会自动使用 CodeBuddy 后端）
        logger.info("初始化 CodeBuddy LLM...")
        llm = LLM(config_name="default")
        llm_type = type(llm).__name__

        logger.info(f"使用的 LLM: {llm_type}")

        if llm_type != "CodeBuddyLLM":
            logger.warning(f"⚠️  警告: 期望 CodeBuddyLLM，但得到 {llm_type}")
            logger.warning("请检查 config/config.toml 中 backend = 'codebuddy' 是否设置")

        # 准备消息
        messages = [Message.user_message(prompt)]
        system_msgs = [Message.system_message("你是一个有帮助的AI助手，可以帮助用户完成各种任务。")]

        print(f'\n💬 问题: {prompt}')
        print('-' * 70)
        print()

        # 调用 API（流式响应）
        response = await llm.ask(
            messages=messages,
            system_msgs=system_msgs,
            stream=True
        )

        print()
        print('-' * 70)
        logger.info(f"✅ 查询完成！响应长度: {len(response)} 字符")

        # 显示令牌统计
        if hasattr(llm, 'total_input_tokens'):
            logger.info(
                f"📊 令牌统计: "
                f"输入={llm.total_input_tokens}, "
                f"输出={llm.total_completion_tokens}, "
                f"总计={llm.total_input_tokens + llm.total_completion_tokens}"
            )

        return True

    except Exception as e:
        logger.error(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='OpenManus with CodeBuddy SDK Backend',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python run_manus_codebuddy.py --prompt "计算斐波那契数列的前10个数字"
  python run_manus_codebuddy.py --prompt "创建一个2048小游戏"
  python run_manus_codebuddy.py  # 交互式输入
        '''
    )

    parser.add_argument(
        '--prompt',
        type=str,
        help='输入提示词（如果不提供，将提示用户输入）'
    )

    args = parser.parse_args()

    # 获取提示词
    if args.prompt:
        prompt = args.prompt
    else:
        # 交互式输入
        print('\n请输入您的问题（按 Enter 结束）:')
        prompt = input('> ').strip()

        if not prompt:
            logger.warning("未提供提示词，退出。")
            print('\n💡 用法: python run_manus_codebuddy.py --prompt "你的问题"')
            return

    # 运行查询
    success = await run_query(prompt)

    print('\n' + '=' * 70)
    if success:
        print('🎉 查询成功完成！')
    else:
        print('❌ 查询失败，请查看错误信息')
    print('=' * 70)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n\n⚠️  操作被用户中断')
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序错误: {e}")
        sys.exit(1)

