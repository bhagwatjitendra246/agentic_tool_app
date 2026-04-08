from __future__ import annotations
from typing import Any
from tools.base import BaseTool


class UppercaseTool(BaseTool):
    name = "uppercase"
    description = "Convert text to uppercase. Args: text"

    def run(self, **kwargs: Any) -> str:
        return str(kwargs["text"]).upper()


class LowercaseTool(BaseTool):
    name = "lowercase"
    description = "Convert text to lowercase. Args: text"

    def run(self, **kwargs: Any) -> str:
        return str(kwargs["text"]).lower()


class ReverseStringTool(BaseTool):
    name = "reverse"
    description = "Reverse a string. Args: text"

    def run(self, **kwargs: Any) -> str:
        return str(kwargs["text"])[::-1]


class ReplaceStringTool(BaseTool):
    name = "replace"
    description = "Replace text. Args: text, old, new"

    def run(self, **kwargs: Any) -> str:
        return str(kwargs["text"]).replace(str(kwargs["old"]), str(kwargs["new"]))
