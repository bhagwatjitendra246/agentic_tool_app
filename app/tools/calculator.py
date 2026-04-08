from __future__ import annotations
from typing import Any
from tools.base import BaseTool


class AddTool(BaseTool):
    name = "add"
    description = "Add two numbers. Args: a, b"

    def run(self, **kwargs: Any) -> float:
        return float(kwargs["a"]) + float(kwargs["b"])


class SubtractTool(BaseTool):
    name = "subtract"
    description = "Subtract b from a. Args: a, b"

    def run(self, **kwargs: Any) -> float:
        return float(kwargs["a"]) - float(kwargs["b"])


class MultiplyTool(BaseTool):
    name = "multiply"
    description = "Multiply two numbers. Args: a, b"

    def run(self, **kwargs: Any) -> float:
        return float(kwargs["a"]) * float(kwargs["b"])


class DivideTool(BaseTool):
    name = "divide"
    description = "Divide a by b. Args: a, b"

    def run(self, **kwargs: Any) -> float:
        divisor = float(kwargs["b"])
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return float(kwargs["a"]) / divisor