from __future__ import annotations
from typing import Dict
from tools.base import BaseTool
from tools.calculator import AddTool, DivideTool, MultiplyTool, SubtractTool
from tools.string_tools import LowercaseTool, ReplaceStringTool, ReverseStringTool, UppercaseTool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered.")
        return self._tools[name]

    def list_tools(self) -> Dict[str, str]:
        return {name: tool.description for name, tool in self._tools.items()}


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    for tool in [
            AddTool(),
            SubtractTool(),
            MultiplyTool(),
            DivideTool(),
            UppercaseTool(),
            LowercaseTool(),
            ReverseStringTool(),
            ReplaceStringTool(),
        ]:
        registry.register(tool)
    return registry
