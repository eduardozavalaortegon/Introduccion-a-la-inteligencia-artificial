"""Route-finding problem on the Mexico cities graph. State = city id (int)."""

from __future__ import annotations

from mexico.graph import MexicoGraph


class MexicoRouteProblem:
    def __init__(self, graph: MexicoGraph, start: int, goal: int) -> None:
        self.graph = graph
        self.start = start
        self.goal = goal

    def actions(self, state: int) -> list[int]:
        return [neighbor_id for neighbor_id, _km in self.graph.neighbors(state)]

    def result(self, state: int, action: int) -> int:
        return action

    def step_cost(self, state: int, action: int) -> float:
        for neighbor_id, km in self.graph.neighbors(state):
            if neighbor_id == action:
                return km
        raise ValueError(f"no edge {state} -> {action}")

    def is_goal(self, state: int) -> bool:
        return state == self.goal
