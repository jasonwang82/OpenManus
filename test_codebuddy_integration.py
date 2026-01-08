"""
Test script to verify CodeBuddy SDK integration with OpenManus.

This script tests basic functionality of the CodeBuddy LLM adapter.
"""

import asyncio
import sys

from app.config import config
from app.llm import LLM
from app.logger import logger
from app.schema import Message


async def test_basic_query():
    """Test basic query without tools."""
    logger.info("=" * 50)
    logger.info("Test 1: Basic Query (No Tools)")
    logger.info("=" * 50)

    try:
        # This will use whatever backend is configured
        llm = LLM(config_name="default")
        logger.info(f"LLM type: {type(llm).__name__}")
        logger.info(f"Model: {llm.model}")

        messages = [
            Message.user_message("What is 2 + 2? Please answer briefly.")
        ]

        response = await llm.ask(messages, stream=False)
        logger.info(f"Response: {response}")

        return True
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        return False


async def test_with_tools():
    """Test query with tool calls."""
    logger.info("=" * 50)
    logger.info("Test 2: Query with Tools")
    logger.info("=" * 50)

    try:
        from app.tool import PythonExecute, Terminate, ToolCollection

        llm = LLM(config_name="default")
        logger.info(f"LLM type: {type(llm).__name__}")

        # Create a simple tool collection
        tools = ToolCollection(
            PythonExecute(),
            Terminate(),
        )

        # If it's CodeBuddy LLM, set the tool collection
        if hasattr(llm, "set_tool_collection"):
            llm.set_tool_collection(tools)
            logger.info("Tool collection set on CodeBuddy LLM")

        messages = [
            Message.user_message(
                "Calculate the factorial of 5 using Python. Show your work."
            )
        ]

        system_msgs = [
            Message.system_message(
                "You are a helpful assistant that can execute Python code."
            )
        ]

        response = await llm.ask_tool(
            messages=messages,
            system_msgs=system_msgs,
            tools=tools.to_params(),
        )

        logger.info(f"Response type: {type(response)}")
        if response:
            logger.info(f"Response content: {response.content}")
            if hasattr(response, "tool_calls") and response.tool_calls:
                logger.info(f"Tool calls: {len(response.tool_calls)}")
                for tool_call in response.tool_calls:
                    logger.info(f"  - {tool_call.function.name}: {tool_call.function.arguments}")

        return True
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        return False


async def test_config_detection():
    """Test that the correct backend is loaded based on configuration."""
    logger.info("=" * 50)
    logger.info("Test 3: Configuration Detection")
    logger.info("=" * 50)

    try:
        llm = LLM(config_name="default")
        logger.info(f"Loaded LLM type: {type(llm).__name__}")
        logger.info(f"Model: {llm.model}")

        # Check configuration
        llm_config = config.llm.get("default", config.llm["default"])
        logger.info(f"Configured backend: {llm_config.backend if hasattr(llm_config, 'backend') else 'openai (default)'}")

        # Verify correct type is loaded
        from app.llm_codebuddy import CodeBuddyLLM

        if hasattr(llm_config, "backend") and llm_config.backend == "codebuddy":
            if isinstance(llm, CodeBuddyLLM):
                logger.info("✓ Correctly loaded CodeBuddy LLM")
                return True
            else:
                logger.error(f"✗ Expected CodeBuddy LLM, got {type(llm).__name__}")
                return False
        else:
            if not isinstance(llm, CodeBuddyLLM):
                logger.info("✓ Correctly loaded OpenAI LLM (default)")
                return True
            else:
                logger.error(f"✗ Expected OpenAI LLM, got CodeBuddy LLM")
                return False
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        return False


async def main():
    """Run all tests."""
    logger.info("Starting CodeBuddy SDK Integration Tests")
    logger.info("=" * 70)

    results = []

    # Test 1: Config detection
    result1 = await test_config_detection()
    results.append(("Config Detection", result1))

    # Test 2: Basic query
    result2 = await test_basic_query()
    results.append(("Basic Query", result2))

    # Test 3: Tools (optional - might not work without proper setup)
    try:
        result3 = await test_with_tools()
        results.append(("Query with Tools", result3))
    except Exception as e:
        logger.warning(f"Tool test skipped: {e}")
        results.append(("Query with Tools", None))

    # Print summary
    logger.info("=" * 70)
    logger.info("TEST SUMMARY")
    logger.info("=" * 70)
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL" if result is False else "⊘ SKIP"
        logger.info(f"{test_name}: {status}")

    # Overall result
    passed = sum(1 for _, r in results if r is True)
    failed = sum(1 for _, r in results if r is False)
    skipped = sum(1 for _, r in results if r is None)

    logger.info("=" * 70)
    logger.info(f"Total: {passed} passed, {failed} failed, {skipped} skipped")

    return failed == 0


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Tests failed with error: {e}", exc_info=True)
        sys.exit(1)

