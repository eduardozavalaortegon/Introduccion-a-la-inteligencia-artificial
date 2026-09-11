#!/usr/bin/env python3
"""Find the shortest route (km) between two Mexican cities using A*.

Reuses `a_star_search` from `../project/search/astar.py` (Ejercicio 1's
Romania A*, which is already generic: it only needs a problem object with
start/actions/result/step_cost/is_goal and a heuristic function). Only the
problem (mexico/problem.py, state = city id) and the heuristic
(mexico/heuristics.py, haversine instead of a fixed table) are specific to
this graph.

Usage:
    python find_route.py --from-city Tijuana --to Cancún
    python find_route.py --from-city Puebla --from-state Puebla --to Mexico City
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "project"))

from search.astar import a_star_search  # noqa: E402

from mexico.graph import MexicoGraph  # noqa: E402
from mexico.heuristics import heuristic_for  # noqa: E402
from mexico.problem import MexicoRouteProblem  # noqa: E402


def resolve_city(graph: MexicoGraph, label: str, name: str, state: str | None) -> int:
    matches = graph.find_by_name(name, state)
    if not matches:
        where = f" in state {state!r}" if state else ""
        raise SystemExit(f"{label}: no city named {name!r} found{where}.")
    if len(matches) > 1:
        lines = "\n".join(
            f"    id={c['id']:<5} {c['name']} ({c['state']}), population={c['population']}"
            for c in sorted(matches, key=lambda c: -c["population"])
        )
        flag = "--from-state" if label == "From" else "--to-state"
        raise SystemExit(
            f"{label}: {name!r} is ambiguous, {len(matches)} cities share that name.\n"
            f"Pass {flag} STATE to disambiguate, or pick one of:\n{lines}"
        )
    return matches[0]["id"]


def main() -> None:
    parser = argparse.ArgumentParser(description="A* route search on the Mexico cities graph.")
    parser.add_argument("--from-city", dest="start_name", required=True, help="Start city name")
    parser.add_argument("--from-state", dest="start_state", default=None, help="Disambiguate start by state")
    parser.add_argument("--to", dest="goal_name", required=True, help="Goal city name")
    parser.add_argument("--to-state", dest="goal_state", default=None, help="Disambiguate goal by state")
    args = parser.parse_args()

    graph = MexicoGraph()
    start_id = resolve_city(graph, "From", args.start_name, args.start_state)
    goal_id = resolve_city(graph, "To", args.goal_name, args.goal_state)

    problem = MexicoRouteProblem(graph, start_id, goal_id)
    h = heuristic_for(graph, goal_id)
    result = a_star_search(problem, h)

    start_city = graph.city(start_id)
    goal_city = graph.city(goal_id)

    print("Algorithm: A* search")
    print(f"Problem:   {start_city['name']} ({start_city['state']}) -> {goal_city['name']} ({goal_city['state']})")
    print("Heuristic: haversine distance to destination (km)")
    print(f"Status:    {result.status}")

    if result.node is None:
        print(f"Expanded:  {result.nodes_expanded} nodes")
        return

    names = [graph.city(cid)["name"] for cid in result.path]
    print(f"Depth:     {result.depth} hops")
    print(f"Cost:      {result.cost:.1f} km")
    if len(names) <= 12:
        print(f"Path:      {' -> '.join(names)}")
    else:
        head = " -> ".join(names[:4])
        tail = " -> ".join(names[-4:])
        print(f"Path:      {head} -> ... ({len(names)} cities total) ... -> {tail}")
    print(f"Expanded:  {result.nodes_expanded} nodes")
    print(f"Generated: {result.nodes_generated} nodes")
    print(f"Frontier:  max size {result.max_frontier}")


if __name__ == "__main__":
    main()
