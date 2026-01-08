from app.agent.base import BaseAgent
from app.agent.mcp import MCPAgent
from app.agent.react import ReActAgent
from app.agent.swe import SWEAgent
from app.agent.toolcall import ToolCallAgent

# Lazy import BrowserAgent to avoid daytona dependency issues
def _get_browser_agent():
    try:
        from app.agent.browser import BrowserAgent
        return BrowserAgent
    except ImportError:
        return None

BrowserAgent = _get_browser_agent()

__all__ = [
    "BaseAgent",
    "BrowserAgent",
    "ReActAgent",
    "SWEAgent",
    "ToolCallAgent",
    "MCPAgent",
]
