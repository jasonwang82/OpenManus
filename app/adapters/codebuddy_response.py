"""
Response translator for CodeBuddy Agent SDK.

Translates CodeBuddy SDK message types to OpenAI ChatCompletionMessage format
that OpenManus expects.
"""

from typing import Any, Dict, List, Optional, Union

from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion_message import FunctionCall
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)

from app.logger import logger


class CodeBuddyResponseTranslator:
    """Translates CodeBuddy SDK responses to OpenAI format."""

    @staticmethod
    def translate_message(message: Any) -> Optional[ChatCompletionMessage]:
        """
        Translate a CodeBuddy message to OpenAI ChatCompletionMessage format.

        Args:
            message: A message from CodeBuddy SDK (AssistantMessage, UserMessage, etc.)

        Returns:
            ChatCompletionMessage compatible with OpenManus, or None if not translatable
        """
        message_type = type(message).__name__

        if message_type == "AssistantMessage":
            return CodeBuddyResponseTranslator._translate_assistant_message(message)
        elif message_type == "UserMessage":
            return CodeBuddyResponseTranslator._translate_user_message(message)
        elif message_type == "SystemMessage":
            # System messages are typically not returned in responses
            return None
        elif message_type == "ResultMessage":
            # ResultMessage contains metadata, not content to translate
            return None
        elif message_type == "StreamEvent":
            # Stream events are handled separately in streaming mode
            return None
        else:
            logger.warning(f"Unknown CodeBuddy message type: {message_type}")
            return None

    @staticmethod
    def _translate_assistant_message(message: Any) -> ChatCompletionMessage:
        """
        Translate CodeBuddy AssistantMessage to OpenAI format.

        CodeBuddy AssistantMessage has:
        - content: list[ContentBlock]
        - model: str
        - parent_tool_use_id: Optional[str]
        - error: Optional[str]

        OpenAI ChatCompletionMessage has:
        - content: Optional[str]
        - role: str
        - tool_calls: Optional[List[ChatCompletionMessageToolCall]]
        """
        content_blocks = message.content if hasattr(message, "content") else []

        # Extract text content
        text_parts = []
        tool_calls = []

        for block in content_blocks:
            block_type = type(block).__name__

            if block_type == "TextBlock":
                if hasattr(block, "text"):
                    text_parts.append(block.text)

            elif block_type == "ThinkingBlock":
                # Include thinking as part of the response
                if hasattr(block, "thinking"):
                    text_parts.append(f"[Thinking: {block.thinking}]")

            elif block_type == "ToolUseBlock":
                # Convert to OpenAI tool call format
                tool_call = CodeBuddyResponseTranslator._translate_tool_use_block(block)
                if tool_call:
                    tool_calls.append(tool_call)

        # Combine text content
        content = "\n".join(text_parts) if text_parts else None

        # Handle error messages
        if hasattr(message, "error") and message.error:
            if content:
                content = f"{content}\n\nError: {message.error}"
            else:
                content = f"Error: {message.error}"

        # Create ChatCompletionMessage
        # Note: ChatCompletionMessage is a TypedDict-like class from openai package
        result = ChatCompletionMessage(
            role="assistant",
            content=content,
            tool_calls=tool_calls if tool_calls else None,
        )

        return result

    @staticmethod
    def _translate_tool_use_block(block: Any) -> Optional[ChatCompletionMessageToolCall]:
        """
        Translate CodeBuddy ToolUseBlock to OpenAI ChatCompletionMessageToolCall.

        CodeBuddy ToolUseBlock has:
        - id: str
        - name: str
        - input: dict

        OpenAI ChatCompletionMessageToolCall has:
        - id: str
        - type: str (always "function")
        - function: Function(name: str, arguments: str)
        """
        if not hasattr(block, "id") or not hasattr(block, "name"):
            return None

        import json

        # Convert input dict to JSON string
        arguments = json.dumps(block.input) if hasattr(block, "input") else "{}"

        return ChatCompletionMessageToolCall(
            id=block.id,
            type="function",
            function=Function(
                name=block.name,
                arguments=arguments,
            ),
        )

    @staticmethod
    def _translate_user_message(message: Any) -> ChatCompletionMessage:
        """Translate CodeBuddy UserMessage to OpenAI format."""
        content = message.content if hasattr(message, "content") else ""

        # Handle different content formats
        if isinstance(content, list):
            # Extract text from content blocks
            text_parts = []
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
                elif isinstance(item, str):
                    text_parts.append(item)
            content = "\n".join(text_parts)
        elif not isinstance(content, str):
            content = str(content)

        return ChatCompletionMessage(
            role="user",
            content=content,
        )

    @staticmethod
    def extract_text_from_messages(messages: List[Any]) -> str:
        """
        Extract plain text from a list of CodeBuddy messages.

        Args:
            messages: List of CodeBuddy messages

        Returns:
            Combined text content from all messages
        """
        text_parts = []

        for message in messages:
            message_type = type(message).__name__

            if message_type == "AssistantMessage":
                if hasattr(message, "content"):
                    for block in message.content:
                        block_type = type(block).__name__
                        if block_type == "TextBlock" and hasattr(block, "text"):
                            text_parts.append(block.text)

            elif message_type == "UserMessage":
                content = message.content if hasattr(message, "content") else ""
                if isinstance(content, str):
                    text_parts.append(content)
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and "text" in item:
                            text_parts.append(item["text"])
                        elif isinstance(item, str):
                            text_parts.append(item)

        return "\n".join(text_parts)

    @staticmethod
    def extract_tool_calls_from_messages(
        messages: List[Any],
    ) -> List[ChatCompletionMessageToolCall]:
        """
        Extract all tool calls from a list of CodeBuddy messages.

        Args:
            messages: List of CodeBuddy messages

        Returns:
            List of OpenAI-format tool calls
        """
        tool_calls = []

        for message in messages:
            message_type = type(message).__name__

            if message_type == "AssistantMessage" and hasattr(message, "content"):
                for block in message.content:
                    block_type = type(block).__name__
                    if block_type == "ToolUseBlock":
                        tool_call = CodeBuddyResponseTranslator._translate_tool_use_block(
                            block
                        )
                        if tool_call:
                            tool_calls.append(tool_call)

        return tool_calls

