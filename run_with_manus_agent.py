#!/usr/bin/env python3
"""
使用完整的 Manus Agent 运行 OpenManus + CodeBuddy SDK
支持多步骤执行和工具调用（包括 browser_use 和 computer_use）
"""

import argparse
import asyncio
import os
import sys

# 设置 CodeBuddy 环境变量
os.environ['CODEBUDDY_CODE_PATH'] = "/Users/jasonwang/.nvm/versions/node/v22.15.1/bin/codebuddy"
os.environ['CODEBUDDY_API_KEY'] = "ck_f9gwukdhccn4.j1twF8hHyb_wXzr8pnmeCoSYlA9OF5F8M7RBZvsLeb8"
os.environ['CODEBUDDY_INTERNET_ENVIRONMENT'] = "internal"

# 确保 output 目录存在
output_dir = "/Users/jasonwang/workspace/OpenManus/output"
os.makedirs(output_dir, exist_ok=True)

print('🚀 OpenManus Manus Agent + CodeBuddy SDK')
print('=' * 70)
print(f'📁 输出目录: {output_dir}')
print('=' * 70)

from app.agent.manus import Manus
from app.logger import logger

async def run_with_codebuddy(prompt: str):
    """
    使用 Manus Agent 运行任务（自动支持所有工具，包括 browser_use 和 computer_use）

    Args:
        prompt: 用户输入的提示词
    """
    agent = None
    try:
        # 创建 Manus agent（会自动使用配置的 CodeBuddy 后端）
        logger.info("创建 Manus agent...")
        agent = await Manus.create()

        # 检查使用的 LLM 类型
        llm_type = type(agent.llm).__name__
        logger.info(f"使用的 LLM: {llm_type}")

        if llm_type != "CodeBuddyLLM":
            logger.warning(f"⚠️  警告: 期望 CodeBuddyLLM，但得到 {llm_type}")

        # 显示可用工具
        tool_names = [tool.name for tool in agent.available_tools.tools]
        logger.info(f"可用工具: {', '.join(tool_names)}")

        # 检查 browser_use 和 computer_use 是否在工具列表中
        has_browser = any('browser' in name.lower() for name in tool_names)
        has_computer = any('computer' in name.lower() for name in tool_names)

        if has_browser:
            logger.info("✅ BrowserUseTool 已注册")
        else:
            logger.warning("⚠️  BrowserUseTool 未找到")

        if has_computer:
            logger.info("✅ ComputerUseTool 已注册")
        else:
            logger.info("ℹ️  ComputerUseTool 未注册（可能需要 sandbox 环境）")

        # 注意：工作目录由 CodeBuddy SDK 的 cwd 选项控制
        # 不需要修改 config.workspace_root（它是只读的）

        print(f'\n💬 任务: {prompt}')
        print('-' * 70)
        print()
        print('🤖 Manus 开始工作...\n')
        print('=' * 70)

        # 运行任务（Manus agent 会自动处理工具调用）
        await agent.run(prompt)

        print()
        print('-' * 70)
        logger.info(f"📁 检查 {output_dir} 目录查看生成的文件")

        # 列出生成的文件
        import glob
        output_files = glob.glob(f"{output_dir}/*")
        if output_files:
            logger.info(f"📄 生成的文件:")
            for f in output_files:
                if os.path.isfile(f):
                    logger.info(f"   - {os.path.basename(f)}")
                elif os.path.isdir(f):
                    logger.info(f"   - {os.path.basename(f)}/ (目录)")

        return True

    except Exception as e:
        logger.error(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if agent:
            await agent.cleanup()

async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='OpenManus Manus Agent with CodeBuddy SDK',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python run_with_manus_agent.py --prompt "实现一个北京三日游的地图路书"
  python run_with_manus_agent.py --prompt "创建一个Python爬虫程序"
  python run_with_manus_agent.py  # 交互式输入
        '''
    )

    parser.add_argument(
        '--prompt',
        type=str,
        help='输入任务描述（如果不提供，将提示用户输入）'
    )

    args = parser.parse_args()

    # 获取提示词
    if args.prompt:
        prompt = args.prompt
    else:
        print('\n请输入您的任务描述:')
        prompt = input('> ').strip()

        if not prompt:
            logger.warning("未提供任务描述，退出。")
            print('\n💡 用法: python run_with_manus_agent.py --prompt "你的任务"')
            return

    # 运行任务
    success = await run_with_codebuddy(prompt)

    print('\n' + '=' * 70)
    if success:
        print('🎉 任务成功完成！')
        print(f'📁 查看生成的文件: {output_dir}')
    else:
        print('❌ 任务执行失败，请查看错误信息')
    print('=' * 70)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n\n⚠️  操作被用户中断')
        sys.exit(0)
    except Exception as e:
        print(f"程序错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

