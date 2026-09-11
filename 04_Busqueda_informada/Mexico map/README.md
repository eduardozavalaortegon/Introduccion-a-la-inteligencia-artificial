# Mexico as a 1,000-city graph

A geographic graph of Mexico: **1,000 cities** pinned to real latitude/longitude, linked by proximity rather than a force-directed layout.

Open [`mexico_map.html`](mexico_map.html) in a browser to explore it. Search a city, filter by state, hover a node for its neighborhood, and pan/zoom the map. Circle size is log population.

| | |
| --- | --- |
| Nodes | 1,000 |
| Edges | 2,565 |
| Mean edge | 31.55 km |
| MST bridges | 10 |

## How the graph is built

1. Load Mexican populated places from [GeoNames `cities1000`](https://download.geonames.org/export/dump/) (`data/cities1000.txt`).
2. Keep the most populous 1,000 places with at least **3 km** of separation, so stacked suburbs do not collapse into one pixel.
3. Connect each city to its **4 nearest neighbors** by haversine distance. That local mesh already looks like a road sketch.
4. Union a **minimum spanning tree** so remote ends (Baja California, Yucatán, the northern border) stay in one connected component. Ten of those MST edges are bridges that were not already in the 4-NN mesh.

Layout is longitude × latitude, not a scramble.

## Finding a route (A*) — Ejercicio 2

Reuses A* from [`../project/search/astar.py`](../project/search/astar.py) (the
same algorithm from Ejercicio 1's Romania map). State = city `id`. Heuristic
`h(n)` = haversine distance from `n` to the destination (admissible and
consistent here, because the graph's own edges are also haversine distances).

**CLI:**

```bash
cd "Mexico map"
..\project\venv\Scripts\python.exe find_route.py --from-city Tijuana --to Cancún
```

Reports Status, Path, Depth (hops), Cost (km), Expanded, and the heuristic
used. If a city name is ambiguous (~39 names repeat, e.g. `Puebla`), it prints
every match with its state and population instead of guessing — pass
`--from-state STATE` / `--to-state STATE` to disambiguate:

```bash
python find_route.py --from-city Puebla --from-state Puebla --to "Mexico City"
```

Code: [`find_route.py`](find_route.py) (CLI) and the [`mexico/`](mexico) package
(`graph.py` loads the JSON graph, `heuristics.py` is haversine, `problem.py` is
the route-finding problem — the Mexico equivalents of `romania/map.py`,
`romania/heuristics.py`, `romania/problem.py`).

**In the map:** open [`mexico_map.html`](mexico_map.html), use the **"Find
route (A\*)"** box in the sidebar (From / To, with a `Name (State)` suggestion
list for duplicates), click **Find route**. The path highlights on the map
and the panel shows cost (km), hops, and nodes expanded. This is a JS port of
the same A* (see the `aStarRoute` function in the page's `<script>`), running
against the graph already embedded in the HTML — no server needed.

⚠️ **Do not re-run `generate_mexico_graph.py`** after editing `mexico_map.html`
by hand — it rewrites the file from `HTML_TEMPLATE` and would erase the route
UI.

## Regenerating

Python 3, no extra packages for the graph and HTML:

```bash
python3 generate_mexico_graph.py
```

That writes:

- `mexico_cities_graph.json` — nodes, edges, coast outline, and metadata
- `mexico_map.html` — self-contained interactive map (graph JSON inlined)

Optional static PNG (needs matplotlib):

```bash
python3 emit_viz.py
```

Writes `mexico_graph_preview.png` from the current graph JSON.

## Files

```
generate_mexico_graph.py   build graph, HTML, and adjacency matrix
emit_viz.py                PNG preview from mexico_cities_graph.json
mexico_map.html            interactive map
mexico_cities_graph.json   graph payload
data/cities1000.txt        GeoNames dump (CC-BY 3.0)
data/mexico.geojson        country outline
```

## Data

City coordinates and populations come from [GeoNames](https://www.geonames.org/) `cities1000`, licensed [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). Admin-1 codes in that dump are the historic GeoNames numbering, mapped to state names in `generate_mexico_graph.py`.
