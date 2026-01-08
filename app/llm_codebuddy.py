"""
CodeBuddy LLM adapter for OpenManus.

This module provides a CodeBuddy Agent SDK backend that implements the same
interface as the OpenAI-based LLM class.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional, Union

from openai.types.chat import ChatCompletionMessage

from app.adapters.codebuddy_response import CodeBuddyResponseTranslator
from app.adapters.codebuddy_tool_mapper import CodeBuddyToolMapper
from app.config import LLMSettings
from app.exceptions import TokenLimitExceeded
from app.logger import logger
from app.schema import TOOL_CHOICE_TYPE, Message, ToolChoice
from app.tool.base import BaseTool
from app.tool.tool_collection import ToolCollection

try:
    from codebuddy_agent_sdk import (
        CodeBuddyAgentOptions,
        CodeBuddySDKClient,
        PermissionResult,
        PermissionResultAllow,
        PermissionResultDeny,
    )
    CODEBUDDY_AVAILABLE = True
except ImportError:
    logger.warning("CodeBuddy Agent SDK not installed. Install with: pip install codebuddy-agent-sdk")
    CODEBUDDY_AVAILABLE = False
    # Create mock classes for type hints
    class CodeBuddyAgentOptions:
        pass
    class CodeBuddySDKClient:
        pass
    class PermissionResult:
        pass
    class PermissionResultAllow:
        pass
    class PermissionResultDeny:
        pass


class CodeBuddyLLM:
    """
    CodeBuddy Agent SDK adapter that implements the LLM interface.

    This class provides the same interface as the OpenAI LLM class but uses
    CodeBuddy Agent SDK under the hood.
    """

    def __init__(
        self, config_name: str = "default", llm_config: Optional[LLMSettings] = None
    ):
        """
        Initialize CodeBuddy LLM adapter.

        Args:
            config_name: Name of the configuration to use
            llm_config: Optional LLM configuration settings
        """
        if not CODEBUDDY_AVAILABLE:
            raise ImportError(
                "CodeBuddy Agent SDK is not installed. "
                "Install with: pip install codebuddy-agent-sdk"
            )

        from app.config import config
        llm_config = llm_config or config.llm
        llm_config = llm_config.get(config_name, llm_config["default"])

        self.config_name = config_name
        self.model = llm_config.model
        self.max_tokens = llm_config.max_tokens
        self.temperature = llm_config.temperature
        self.base_url = llm_config.base_url
        self.api_key = llm_config.api_key

        # CodeBuddy-specific settings
        self.codebuddy_code_path = llm_config.codebuddy_code_path
        self.permission_mode = llm_config.permission_mode or "bypassPermissions"

        # Token counting
        self.total_input_tokens = 0
        self.total_completion_tokens = 0
        self.max_input_tokens = (
            llm_config.max_input_tokens
            if hasattr(llm_config, "max_input_tokens")
            else None
        )

        # Tool management
        self._current_tools: Optional[ToolCollection] = None
        self._tool_lookup: Dict[str, BaseTool] = {}

        # Response translator
        self.translator = CodeBuddyResponseTranslator()

        # SDK client (will be created per request due to async nature)
        self.client: Optional[CodeBuddySDKClient] = None

        logger.info(f"Initialized CodeBuddy LLM with model: {self.model}")

    def _build_options(
        self,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: TOOL_CHOICE_TYPE = ToolChoice.AUTO,
    ) -> CodeBuddyAgentOptions:
        """
        Build CodeBuddy Agent options from settings.

        Args:
            tools: Optional list of tool definitions
            tool_choice: Tool choice strategy

        Returns:
            CodeBuddyAgentOptions instance
        """
        options_dict = {
            # Don't specify model here - let CodeBuddy use default or config
            # Specifying model in options seems to cause empty responses
            "max_turns": 20,  # Allow CodeBuddy to perform multi-step reasoning
            "permission_mode": self.permission_mode,
            "cwd": "/Users/jasonwang/workspace/OpenManus/output",  # Set working directory to output
        }

        # Add CodeBuddy CLI path if specified
        if self.codebuddy_code_path:
            options_dict["codebuddy_code_path"] = self.codebuddy_code_path

        # Add tool configuration
        if tools and self._tool_lookup:
            # Build list of allowed tool names for CodeBuddy SDK
            # This tells CodeBuddy which tools are available
            allowed_tool_names = list(self._tool_lookup.keys())
            options_dict["allowed_tools"] = allowed_tool_names
            logger.info(f"Registered {len(allowed_tool_names)} tools with CodeBuddy: {allowed_tool_names}")

        # Handle tool choice
        if tool_choice == ToolChoice.NONE:
            options_dict["disallowed_tools"] = ["*"]  # Disable all tools
        elif tool_choice == ToolChoice.REQUIRED:
            # We'll validate this after the response
            pass

        # Add callback for tool execution only if we have tools
        # Don't add callback for simple queries as it may interfere
        if tools and self._tool_lookup:
            options_dict["can_use_tool"] = self._create_tool_callback()
            logger.info("Tool execution callback registered")

        return CodeBuddyAgentOptions(**options_dict)

    def _create_tool_callback(self):
        """
        Create a callback for intercepting tool calls from CodeBuddy.

        Returns:
            Async function that handles tool permission and execution
        """
        async def can_use_tool(tool_name: str, tool_input: Dict[str, Any], options: Any) -> PermissionResult:
            """
            Intercept tool calls from CodeBuddy and execute via OpenManus tools.

            Args:
                tool_name: Name of the tool to execute
                tool_input: Tool input parameters
                options: Additional options from CodeBuddy

            Returns:
                PermissionResult indicating whether to allow or deny
            """
            logger.info(f"🔧 can_use_tool callback invoked: tool_name='{tool_name}', tool_input={tool_input}")

            # Check if we have this tool in our collection
            if tool_name not in self._tool_lookup:
                logger.warning(f"Tool '{tool_name}' not found in OpenManus tool collection. Available tools: {list(self._tool_lookup.keys())}")
                return PermissionResultDeny(
                    message=f"Tool '{tool_name}' is not available",
                    behavior="deny",
                )

            try:
                # Execute the tool via OpenManus
                tool = self._tool_lookup[tool_name]
                logger.info(f"🚀 Executing tool '{tool_name}' via OpenManus with input: {tool_input}")
                result = await tool.execute(**tool_input)

                # Convert result to string
                result_str = str(result)
                logger.info(f"✅ Executed tool '{tool_name}' via OpenManus: {result_str[:200]}...")

                # Store the result in the tool input so CodeBuddy can access it
                # CodeBuddy SDK expects the result to be available after tool execution
                # We'll store it in a way that CodeBuddy can retrieve it
                updated_input = tool_input.copy()
                # Add result to input for CodeBuddy to process
                # Note: CodeBuddy SDK may handle results differently, but this ensures
                # the result is available in the callback context

                # Allow the tool execution
                # The actual result will be returned through the normal tool execution flow
                return PermissionResultAllow(
                    updated_input=updated_input,
                    behavior="allow",
                )
            except Exception as e:
                logger.error(f"❌ Error executing tool '{tool_name}': {e}", exc_info=True)
                return PermissionResultDeny(
                    message=f"Tool execution failed: {str(e)}",
                    behavior="deny",
                )

        return can_use_tool

    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        # Simple estimation: ~4 characters per token
        return len(text) // 4 if text else 0

    def count_message_tokens(self, messages: List[dict]) -> int:
        """
        Estimate token count for messages.

        Args:
            messages: List of message dictionaries

        Returns:
            Estimated token count
        """
        total = 0
        for msg in messages:
            if "content" in msg:
                content = msg["content"]
                if isinstance(content, str):
                    total += self.count_tokens(content)
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and "text" in item:
                            total += self.count_tokens(item["text"])
        return total

    def update_token_count(self, input_tokens: int, completion_tokens: int = 0) -> None:
        """Update token counts."""
        self.total_input_tokens += input_tokens
        self.total_completion_tokens += completion_tokens
        logger.info(
            f"Token usage: Input={input_tokens}, Completion={completion_tokens}, "
            f"Cumulative Input={self.total_input_tokens}, Cumulative Completion={self.total_completion_tokens}, "
            f"Total={input_tokens + completion_tokens}, Cumulative Total={self.total_input_tokens + self.total_completion_tokens}"
        )

    def check_token_limit(self, input_tokens: int) -> bool:
        """Check if token limits are exceeded."""
        if self.max_input_tokens is not None:
            return (self.total_input_tokens + input_tokens) <= self.max_input_tokens
        return True

    def get_limit_error_message(self, input_tokens: int) -> str:
        """Generate error message for token limit exceeded."""
        if (
            self.max_input_tokens is not None
            and (self.total_input_tokens + input_tokens) > self.max_input_tokens
        ):
            return f"Request may exceed input token limit (Current: {self.total_input_tokens}, Needed: {input_tokens}, Max: {self.max_input_tokens})"
        return "Token limit exceeded"

    @staticmethod
    def format_messages(
        messages: List[Union[dict, Message]], supports_images: bool = False
    ) -> List[dict]:
        """
        Format messages for CodeBuddy SDK.

        Args:
            messages: List of messages
            supports_images: Whether images are supported

        Returns:
            List of formatted message dictionaries
        """
        formatted_messages = []

        for message in messages:
            # Convert Message objects to dictionaries
            if isinstance(message, Message):
                message = message.to_dict()

            if isinstance(message, dict):
                if "role" not in message:
                    raise ValueError("Message dict must contain 'role' field")

                # Handle base64 images if present and supported
                if supports_images and message.get("base64_image"):
                    if not message.get("content"):
                        message["content"] = []
                    elif isinstance(message["content"], str):
                        message["content"] = [
                            {"type": "text", "text": message["content"]}
                        ]

                    message["content"].append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{message['base64_image']}"
                            },
                        }
                    )
                    del message["base64_image"]
                elif not supports_images and message.get("base64_image"):
                    del message["base64_image"]

                if "content" in message or "tool_calls" in message:
                    formatted_messages.append(message)

        return formatted_messages

    async def ask(
        self,
        messages: List[Union[dict, Message]],
        system_msgs: Optional[List[Union[dict, Message]]] = None,
        stream: bool = True,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Send a prompt to CodeBuddy and get the response.

        Args:
            messages: List of conversation messages
            system_msgs: Optional system messages to prepend
            stream: Whether to stream the response
            temperature: Sampling temperature for the response

        Returns:
            str: The generated response

        Raises:
            TokenLimitExceeded: If token limits are exceeded
            ValueError: If messages are invalid or response is empty
        """
        try:
            # Format messages
            if system_msgs:
                system_msgs = self.format_messages(system_msgs, supports_images=False)
                messages = system_msgs + self.format_messages(messages, supports_images=False)
            else:
                messages = self.format_messages(messages, supports_images=False)

            # Calculate input token count
            input_tokens = self.count_message_tokens(messages)

            # Check if token limits are exceeded
            if not self.check_token_limit(input_tokens):
                error_message = self.get_limit_error_message(input_tokens)
                raise TokenLimitExceeded(error_message)

            # Build CodeBuddy options
            options = self._build_options()

            # Create prompt from messages
            prompt = self._messages_to_prompt(messages)

            # Query CodeBuddy SDK
            from codebuddy_agent_sdk import query

            collected_text = []
            message_count = 0
            async for message in query(prompt=prompt, options=options):
                message_type = type(message).__name__
                message_count += 1
                logger.info(f"Message {message_count}: {message_type}")

                if message_type == "AssistantMessage":
                    # Extract text from content blocks
                    if hasattr(message, "content"):
                        logger.info(f"AssistantMessage has {len(message.content)} content blocks")
                        for i, block in enumerate(message.content):
                            block_type = type(block).__name__
                            logger.info(f"Block {i}: {block_type}")
                            if block_type == "TextBlock" and hasattr(block, "text"):
                                text = block.text
                                logger.info(f"Extracted text (len={len(text)}): {text[:100]}")
                                if stream:
                                    print(text, end="", flush=True)
                                collected_text.append(text)
                    else:
                        logger.warning("AssistantMessage has no content attribute")

                elif message_type == "ResultMessage":
                    # Result message indicates completion
                    logger.info(f"Result message received, collected {len(collected_text)} text blocks")
                    if stream and collected_text:
                        print()  # Newline after streaming
                    break

            logger.info(f"Total messages received: {message_count}")
            logger.info(f"Total text blocks collected: {len(collected_text)}")

            # Update token counts
            self.update_token_count(input_tokens)

            full_response = "\n".join(collected_text).strip()
            if not full_response:
                raise ValueError("Empty response from CodeBuddy SDK")

            return full_response

        except TokenLimitExceeded:
            raise
        except Exception as e:
            logger.error(f"Error in CodeBuddy ask: {e}")
            raise

    async def ask_tool(
        self,
        messages: List[Union[dict, Message]],
        system_msgs: Optional[List[Union[dict, Message]]] = None,
        timeout: int = 300,
        tools: Optional[List[dict]] = None,
        tool_choice: TOOL_CHOICE_TYPE = ToolChoice.AUTO,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> ChatCompletionMessage | None:
        """
        Ask CodeBuddy using tools and return the response.

        Args:
            messages: List of conversation messages
            system_msgs: Optional system messages to prepend
            timeout: Request timeout in seconds
            tools: List of tools to use
            tool_choice: Tool choice strategy
            temperature: Sampling temperature for the response
            **kwargs: Additional completion arguments

        Returns:
            ChatCompletionMessage: The model's response

        Raises:
            TokenLimitExceeded: If token limits are exceeded
            ValueError: If tools, tool_choice, or messages are invalid
        """
        try:
            # Format messages
            if system_msgs:
                system_msgs = self.format_messages(system_msgs, supports_images=False)
                messages = system_msgs + self.format_messages(messages, supports_images=False)
            else:
                messages = self.format_messages(messages, supports_images=False)

            # Calculate input token count
            input_tokens = self.count_message_tokens(messages)

            # Add tool description tokens
            if tools:
                for tool in tools:
                    input_tokens += self.count_tokens(str(tool))

            # Check if token limits are exceeded
            if not self.check_token_limit(input_tokens):
                error_message = self.get_limit_error_message(input_tokens)
                raise TokenLimitExceeded(error_message)

            # Build tool lookup from tools parameter
            if tools:
                # Tools are in OpenAI format, we need to build a lookup
                # But for now, we'll rely on the tool collection being set externally
                pass

            # Build CodeBuddy options with tools
            options = self._build_options(tools=tools, tool_choice=tool_choice)

            # Create prompt from messages
            prompt = self._messages_to_prompt(messages)

            # If we have tools, append tool descriptions to the prompt
            # This helps CodeBuddy understand what tools are available
            if tools and self._tool_lookup:
                tool_descriptions = []
                for tool_name in self._tool_lookup.keys():
                    tool = self._tool_lookup[tool_name]
                    tool_descriptions.append(f"- {tool_name}: {tool.description}")

                if tool_descriptions:
                    prompt += f"\n\n可用工具:\n" + "\n".join(tool_descriptions)
                    logger.info(f"Added tool descriptions to prompt: {len(tool_descriptions)} tools")

            # Query CodeBuddy SDK
            from codebuddy_agent_sdk import query

            assistant_messages = []
            async for message in query(prompt=prompt, options=options):
                message_type = type(message).__name__
                logger.info(f"📨 Received message type: {message_type}")

                if message_type == "AssistantMessage":
                    assistant_messages.append(message)
                    # Log tool use blocks if present
                    if hasattr(message, "content"):
                        for i, block in enumerate(message.content):
                            block_type = type(block).__name__
                            if block_type == "ToolUseBlock":
                                logger.info(f"🔧 Found ToolUseBlock {i}: tool={getattr(block, 'name', 'unknown')}, input={getattr(block, 'input', {})}")
                            elif block_type == "TextBlock":
                                text = getattr(block, 'text', '')[:100]
                                logger.info(f"📝 Found TextBlock {i}: {text}...")

                elif message_type == "ResultMessage":
                    # Result message indicates completion
                    logger.info("✅ Received ResultMessage, query completed")
                    break
                else:
                    logger.info(f"ℹ️  Other message type: {message_type}")

            # Update token counts
            self.update_token_count(input_tokens)

            # Translate the last assistant message to OpenAI format
            if assistant_messages:
                last_message = assistant_messages[-1]
                openai_message = self.translator.translate_message(last_message)
                return openai_message

            return None

        except TokenLimitExceeded:
            raise
        except Exception as e:
            logger.error(f"Error in CodeBuddy ask_tool: {e}")
            raise

    async def ask_with_images(
        self,
        messages: List[Union[dict, Message]],
        images: List[Union[str, dict]],
        system_msgs: Optional[List[Union[dict, Message]]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Send a prompt with images to CodeBuddy and get the response.

        Args:
            messages: List of conversation messages
            images: List of image URLs or image data dictionaries
            system_msgs: Optional system messages to prepend
            stream: Whether to stream the response
            temperature: Sampling temperature for the response

        Returns:
            str: The generated response

        Raises:
            TokenLimitExceeded: If token limits are exceeded
            ValueError: If messages are invalid or response is empty
        """
        # For CodeBuddy, we need to format images into the messages
        # Similar to OpenAI implementation

        # Format messages with image support
        formatted_messages = self.format_messages(messages, supports_images=True)

        # Ensure the last message is from the user to attach images
        if not formatted_messages or formatted_messages[-1]["role"] != "user":
            raise ValueError(
                "The last message must be from the user to attach images"
            )

        # Process the last user message to include images
        last_message = formatted_messages[-1]

        # Convert content to multimodal format if needed
        content = last_message["content"]
        multimodal_content = (
            [{"type": "text", "text": content}]
            if isinstance(content, str)
            else content
            if isinstance(content, list)
            else []
        )

        # Add images to content
        for image in images:
            if isinstance(image, str):
                multimodal_content.append(
                    {"type": "image_url", "image_url": {"url": image}}
                )
            elif isinstance(image, dict) and "url" in image:
                multimodal_content.append({"type": "image_url", "image_url": image})
            elif isinstance(image, dict) and "image_url" in image:
                multimodal_content.append(image)
            else:
                raise ValueError(f"Unsupported image format: {image}")

        # Update the message with multimodal content
        last_message["content"] = multimodal_content

        # Add system messages if provided
        if system_msgs:
            all_messages = (
                self.format_messages(system_msgs, supports_images=True)
                + formatted_messages
            )
        else:
            all_messages = formatted_messages

        # Use the regular ask method with the formatted messages
        return await self.ask(all_messages, stream=stream, temperature=temperature)

    def _messages_to_prompt(self, messages: List[dict]) -> str:
        """
        Convert a list of messages to a single prompt string for CodeBuddy.

        Args:
            messages: List of message dictionaries

        Returns:
            Combined prompt string
        """
        # Extract system and user messages
        # CodeBuddy SDK works best with a combined prompt string
        system_parts = []
        user_messages = []

        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "system":
                if isinstance(content, str):
                    system_parts.append(content)
                elif isinstance(content, list):
                    # Extract text from content blocks
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict) and "text" in item:
                            text_parts.append(item["text"])
                        elif isinstance(item, str):
                            text_parts.append(item)
                    if text_parts:
                        system_parts.append(' '.join(text_parts))
            elif role == "user":
                if isinstance(content, str):
                    user_messages.append(content)
                elif isinstance(content, list):
                    # Extract text from content blocks
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict) and "text" in item:
                            text_parts.append(item["text"])
                        elif isinstance(item, str):
                            text_parts.append(item)
                    if text_parts:
                        user_messages.append(' '.join(text_parts))

        # Combine system and user messages
        prompt_parts = []
        if system_parts:
            prompt_parts.append('\n'.join(system_parts))
        if user_messages:
            prompt_parts.append('\n'.join(user_messages))

        # Return combined prompt or last user message
        return '\n\n'.join(prompt_parts) if prompt_parts else (user_messages[-1] if user_messages else "")

    def set_tool_collection(self, tools: ToolCollection) -> None:
        """
        Set the tool collection for this LLM instance.

        This is used to enable tool execution via OpenManus's tools.

        Args:
            tools: ToolCollection containing available tools
        """
        self._current_tools = tools
        self._tool_lookup = {tool.name: tool for tool in tools.tools}
        logger.info(f"Set tool collection with {len(self._tool_lookup)} tools")

