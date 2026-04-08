from __future__ import annotations
import argparse
import json

from agent.core import Agent


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the agentic tool app.")
    parser.add_argument("--query", required=True, help="Natural language instruction for the agent")
    args = parser.parse_args()

    agent = Agent()
    result = agent.run(args.query)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
