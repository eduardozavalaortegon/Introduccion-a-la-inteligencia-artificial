"""Load the Mexico cities graph: nodes with lat/lon, undirected km-weighted edges."""

from __future__ import annotations

import json
from pathlib import Path

GRAPH_PATH = Path(__file__).resolve().parent.parent / "mexico_cities_graph.json"


class MexicoGraph:
    def __init__(self, path: Path = GRAPH_PATH) -> None:
        data = json.loads(path.read_text(encoding="utf-8"))
        self.nodes: dict[int, dict] = {n["id"]: n for n in data["nodes"]}
        self._neighbors: dict[int, list[tuple[int, float]]] = {nid: [] for nid in self.nodes}
        for edge in data["edges"]:
            a, b, km = edge["source"], edge["target"], float(edge["km"])
            self._neighbors[a].append((b, km))
            self._neighbors[b].append((a, km))
        for nid in self._neighbors:
            self._neighbors[nid].sort(key=lambda pair: pair[0])

    def neighbors(self, city_id: int) -> list[tuple[int, float]]:
        return self._neighbors[city_id]

    def city(self, city_id: int) -> dict:
        return self.nodes[city_id]

    def find_by_name(self, name: str, state: str | None = None) -> list[dict]:
        name_l = name.strip().lower()
        matches = [c for c in self.nodes.values() if c["name"].lower() == name_l]
        if state:
            state_l = state.strip().lower()
            matches = [c for c in matches if c["state"].lower() == state_l]
        return matches
