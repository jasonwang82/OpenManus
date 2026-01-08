"""
Adapters for integrating external agent systems with OpenManus.

This package contains adapters for translating between OpenManus's internal
representations and external agent SDK formats.
"""

from app.adapters.codebuddy_response import CodeBuddyResponseTranslator
from app.adapters.codebuddy_tool_mapper import CodeBuddyToolMapper

__all__ = [
    "CodeBuddyResponseTranslator",
    "CodeBuddyToolMapper",
]

