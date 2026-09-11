"""Heuristic h(n) = haversine distance from city n to the destination.

haversine() adapted from `Mexico map/generate_mexico_graph.py`. It is admissible
and consistent here because the graph's own edge weights are also haversine
distances (great-circle distance never overestimates road distance, and it
satisfies the triangle inequality).
"""

from __future__ import annotations

import math
from collections.abc import Callable

from mexico.graph import MexicoGraph

EARTH_KM = 6371.0


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * EARTH_KM * math.asin(math.sqrt(min(1.0, a)))


def heuristic_for(graph: MexicoGraph, goal_id: int) -> Callable[[int], float]:
    goal = graph.city(goal_id)
    glat, glon = goal["lat"], goal["lon"]

    def h(city_id: int) -> float:
        c = graph.city(city_id)
        return haversine(c["lat"], c["lon"], glat, glon)

    return h
