from __future__ import annotations
import re
from typing import Any, Dict, List
from agent.exceptions import PlanningError
from utils.parsing import extract_numbers, split_instructions


class RuleBasedPlanner:
    """
    A simple planner that converts a user query into a sequence of tool actions.
    It is intentionally developed modular so it can later be replaced by an LLM-based planner.
    """

    def create_plan(self, query: str) -> List[Dict[str, Any]]:
        instructions = split_instructions(query)
        if not instructions:
            raise PlanningError("No executable instructions found in the query.")

        plan: List[Dict[str, Any]] = []
        has_string_seed = False
        has_numeric_seed = False

        for index, instruction in enumerate(instructions):
            lowered = instruction.lower().strip()

            if lowered.startswith("take ") or lowered.startswith("start with "):
                seed = re.sub(r"^(take|start with)\s+", "", instruction, flags=re.IGNORECASE).strip().strip('"')
                numbers = extract_numbers(seed)
                if numbers and seed.replace(str(numbers[0]).rstrip("0").rstrip("."), "").strip() in {"", "."}:
                    plan.append({"tool": "set_value", "args": {"value": numbers[0]}})
                    has_numeric_seed = True
                else:
                    plan.append({"tool": "set_value", "args": {"value": seed}})
                    has_string_seed = True
                continue

            if any(word in lowered for word in ["add", "subtract", "multiply", "divide"]):
                plan.extend(self._parse_math_step(lowered, index == 0 and not has_numeric_seed))
                has_numeric_seed = True
                continue

            if any(word in lowered for word in ["uppercase", "lowercase", "reverse", "replace"]):
                plan.extend(self._parse_string_step(instruction))
                has_string_seed = True
                continue

            raise PlanningError(f"Unsupported instruction: '{instruction}'")

        return plan

    def _parse_math_step(self, instruction: str, require_seed_from_step: bool) -> List[Dict[str, Any]]:
        numbers = extract_numbers(instruction)

        if "add" in instruction:
            if require_seed_from_step:
                if len(numbers) < 2:
                    raise PlanningError("Add step needs two numbers for the first arithmetic action.")
                return [{"tool": "add", "args": {"a": numbers[0], "b": numbers[1]}}]
            if len(numbers) < 1:
                raise PlanningError("Add step needs a number.")
            return [{"tool": "add", "args": {"a": "$current", "b": numbers[0]}}]

        if "subtract" in instruction:
            if require_seed_from_step:
                if len(numbers) < 2:
                    raise PlanningError("Subtract step needs two numbers for the first arithmetic action.")
                return [{"tool": "subtract", "args": {"a": numbers[0], "b": numbers[1]}}]
            if len(numbers) < 1:
                raise PlanningError("Subtract step needs a number.")
            return [{"tool": "subtract", "args": {"a": "$current", "b": numbers[0]}}]

        if "multiply" in instruction:
            if require_seed_from_step:
                if len(numbers) < 2:
                    raise PlanningError("Multiply step needs two numbers for the first arithmetic action.")
                return [{"tool": "multiply", "args": {"a": numbers[0], "b": numbers[1]}}]
            if len(numbers) < 1:
                raise PlanningError("Multiply step needs a number.")
            return [{"tool": "multiply", "args": {"a": "$current", "b": numbers[0]}}]

        if "divide" in instruction:
            if require_seed_from_step:
                if len(numbers) < 2:
                    raise PlanningError("Divide step needs two numbers for the first arithmetic action.")
                return [{"tool": "divide", "args": {"a": numbers[0], "b": numbers[1]}}]
            if len(numbers) < 1:
                raise PlanningError("Divide step needs a number.")
            return [{"tool": "divide", "args": {"a": "$current", "b": numbers[0]}}]

        raise PlanningError(f"Could not parse math instruction: '{instruction}'")

    def _parse_string_step(self, instruction: str) -> List[Dict[str, Any]]:
        lowered = instruction.lower().strip()

        if lowered.startswith("take ") or lowered.startswith("start with "):
            seed = re.sub(r"^(take|start with)\s+", "", instruction, flags=re.IGNORECASE).strip().strip('"')
            return [{"tool": "set_value", "args": {"value": seed}}]

        if "uppercase" in lowered:
            return [{"tool": "uppercase", "args": {"text": "$current"}}]

        if "lowercase" in lowered:
            return [{"tool": "lowercase", "args": {"text": "$current"}}]

        if "reverse" in lowered:
            return [{"tool": "reverse", "args": {"text": "$current"}}]

        if "replace" in lowered:
            match = re.search(r"replace\s+(.+?)\s+with\s+(.+)$", instruction, flags=re.IGNORECASE)
            if not match:
                raise PlanningError("Replace step must follow the format: replace X with Y")
            old = match.group(1).strip().strip('"')
            new = match.group(2).strip().strip('"')
            return [{"tool": "replace", "args": {"text": "$current", "old": old, "new": new}}]

        raise PlanningError(f"Could not parse string instruction: '{instruction}'")