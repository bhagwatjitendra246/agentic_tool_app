from __future__ import annotations
from typing import Any, Dict
from agent.exceptions import ExecutionError, PlanningError
from agent.planner import RuleBasedPlanner
from agent.state import AgentState, AgentStep
from tools.registry import ToolRegistry, build_default_registry

class Agent:
    def __init__(self, registry: ToolRegistry | None = None, planner: RuleBasedPlanner | None = None) -> None:
        self.registry = registry or build_default_registry()
        self.planner = planner or RuleBasedPlanner()

    def run(self, query: str) -> Dict[str, Any]:
        state = AgentState(original_query=query)

        try:
            state.plan = self.planner.create_plan(query)
            while state.plan:
                action = state.plan.pop(0)
                self._execute_action(state, action)
            state.success = True
        except (PlanningError, ExecutionError, KeyError, ZeroDivisionError, ValueError, TypeError) as exc:
            state.success = False
            state.error = str(exc)

        return {
            "success": state.success,
            "input": state.original_query,
            "final_output": state.current_value,
            "steps": [
                {"tool": step.tool, "args": step.args, "result": step.result}
                for step in state.history
            ],
            "error": state.error,
        }

    def _execute_action(self, state: AgentState, action: Dict[str, Any]) -> None:
        tool_name = action["tool"]
        args = self._resolve_args(state, action.get("args", {}))

        if tool_name == "set_value":
            state.current_value = args["value"]
            state.history.append(AgentStep(tool=tool_name, args=args, result=state.current_value))
            return

        try:
            tool = self.registry.get(tool_name)
            result = tool.run(**args)
        except Exception as exc:
            raise ExecutionError(f"Tool '{tool_name}' failed: {exc}") from exc

        state.current_value = result
        state.history.append(AgentStep(tool=tool_name, args=args, result=result))

    def _resolve_args(self, state: AgentState, args: Dict[str, Any]) -> Dict[str, Any]:
        resolved: Dict[str, Any] = {}
        for key, value in args.items():
            if value == "$current":
                if state.current_value is None:
                    raise ExecutionError("The plan referenced the current value before it was initialized.")
                resolved[key] = state.current_value
            else:
                resolved[key] = value
        return resolved
