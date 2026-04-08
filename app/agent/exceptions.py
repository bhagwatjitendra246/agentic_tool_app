class PlanningError(Exception):
    """Raised when the planner cannot convert a query into executable actions."""


class ExecutionError(Exception):
    """Raised when execution fails for a planned step."""

