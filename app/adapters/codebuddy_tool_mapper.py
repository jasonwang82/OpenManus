"""
Tool mapper for CodeBuddy Agent SDK.

Converts OpenManus BaseTool definitions to CodeBuddy SDK's expected format.
"""

from typing import Any, Dict, List

from app.logger import logger
from app.tool.base import BaseTool


class CodeBuddyToolMapper:
    """Maps OpenManus tools to CodeBuddy SDK format."""

    @staticmethod
    def convert_tools_to_codebuddy_format(tools: List[BaseTool]) -> List[Dict[str, Any]]:
        """
        Convert a list of OpenManus BaseTool instances to CodeBuddy format.

        OpenManus tools are in OpenAI function calling format:
        {
            "type": "function",
            "function": {
                "name": "tool_name",
                "description": "...",
                "parameters": {...}  # JSON Schema
            }
        }

        CodeBuddy SDK doesn't require explicit tool registration when using
        can_use_tool callback, but we still convert them for consistency.

        Args:
            tools: List of OpenManus BaseTool instances

        Returns:
            List of tool definitions in a format suitable for CodeBuddy
        """
        codebuddy_tools = []

        for tool in tools:
            try:
                # Get OpenAI format first
                openai_format = tool.to_param()

                # Extract function definition
                if "function" in openai_format:
                    func_def = openai_format["function"]

                    codebuddy_tool = {
                        "name": func_def.get("name", tool.name),
                        "description": func_def.get("description", tool.description),
                        "inputSchema": func_def.get("parameters", tool.parameters or {}),
                    }

                    codebuddy_tools.append(codebuddy_tool)
                    logger.debug(f"Converted tool '{tool.name}' to CodeBuddy format")
                else:
                    logger.warning(
                        f"Tool '{tool.name}' has unexpected format: {openai_format}"
                    )
            except Exception as e:
                logger.error(f"Failed to convert tool '{tool.name}': {e}")
                continue

        return codebuddy_tools

    @staticmethod
    def convert_tool_params_to_codebuddy(tool_params: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert OpenAI-format tool parameters to CodeBuddy format.

        Args:
            tool_params: List of tool definitions in OpenAI format

        Returns:
            List of tool definitions in CodeBuddy format
        """
        codebuddy_tools = []

        for param in tool_params:
            try:
                if param.get("type") == "function" and "function" in param:
                    func_def = param["function"]

                    codebuddy_tool = {
                        "name": func_def.get("name"),
                        "description": func_def.get("description", ""),
                        "inputSchema": func_def.get("parameters", {}),
                    }

                    codebuddy_tools.append(codebuddy_tool)
                else:
                    logger.warning(f"Unexpected tool parameter format: {param}")
            except Exception as e:
                logger.error(f"Failed to convert tool parameter: {e}")
                continue

        return codebuddy_tools

    @staticmethod
    def build_allowed_tools_list(tools: List[BaseTool]) -> List[str]:
        """
        Build a list of tool names to be used with CodeBuddy's allowed_tools option.

        Args:
            tools: List of OpenManus BaseTool instances

        Returns:
            List of tool names
        """
        return [tool.name for tool in tools]

    @staticmethod
    def create_tool_lookup(tools: List[BaseTool]) -> Dict[str, BaseTool]:
        """
        Create a lookup dictionary mapping tool names to tool instances.

        Args:
            tools: List of OpenManus BaseTool instances

        Returns:
            Dictionary mapping tool names to BaseTool instances
        """
        return {tool.name: tool for tool in tools}

    @staticmethod
    def convert_codebuddy_input_to_openai(tool_name: str, tool_input: Dict[str, Any]) -> str:
        """
        Convert CodeBuddy tool input to OpenAI function arguments format.

        CodeBuddy provides tool input as a dict, while OpenAI expects JSON string.

        Args:
            tool_name: Name of the tool
            tool_input: Tool input from CodeBuddy (dict format)

        Returns:
            JSON string representation of the arguments
        """
        import json

        try:
            return json.dumps(tool_input)
        except Exception as e:
            logger.error(
                f"Failed to convert tool input for '{tool_name}': {e}"
            )
            return "{}"

