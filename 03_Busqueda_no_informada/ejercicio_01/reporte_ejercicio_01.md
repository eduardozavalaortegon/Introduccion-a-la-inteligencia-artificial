# Ejercicio 1 — Reporte: BFS, UCS, DFS, DLS e IDS en el mapa de Rumania

## 1. Pareja origen–destino elegida

**Timisoara → Bucharest** (distinta de la pareja por defecto Arad → Bucharest, misma pareja usada en el ejercicio de búsqueda informada para poder comparar).

## 2. Subgrafo relevante (ciudades de ambos caminos, con km)

```
Timisoara
   |
  118 km
   v
  Arad
   |
  140 km
   v
  Sibiu ------80 km-----> Rimnicu Vilcea
   |                            |
  99 km                       97 km
   v                            v
 Fagaras                    Pitesti
   |                            |
  211 km                      101 km
   v                            v
Bucharest <--------------------+
```

Rama de la izquierda (Arad–Sibiu–Fagaras) = camino de **BFS, DFS, DLS(limit=4) e IDS** (568 km, 4 carreteras).
Rama de la derecha (Sibiu–Rimnicu Vilcea–Pitesti) = camino de **UCS** (536 km, 5 carreteras).

## 3. Tabla comparativa

| Algoritmo | Status | Path | Depth | Cost | Expanded | Generated |
|---|---|---|---|---|---|---|
| BFS | success | Timisoara → Arad → Sibiu → Fagaras → Bucharest | 4 | 568 km | 7 | 17 |
| UCS | success | Timisoara → Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest | 5 | **536 km** | 12 | 31 |
| DFS | success | Timisoara → Arad → Sibiu → Fagaras → Bucharest | 4 | 568 km | 4 | 12 |
| DLS (limit=2) | **cutoff** | — | — | — | 3 | 8 |
| DLS (limit=4) | success | Timisoara → Arad → Sibiu → Fagaras → Bucharest | 4 | 568 km | 4 | 6 |
| IDS | success | Timisoara → Arad → Sibiu → Fagaras → Bucharest | 4 | 568 km | 14 | 34 |

## 4. Reporte (análisis)

**¿BFS encontró el camino con menos carreteras? ¿UCS el de menos km?**
Sí a ambas. BFS encontró el camino de **menor profundidad** (4 carreteras: Timisoara→Arad→Sibiu→Fagaras→Bucharest), que es justo lo que BFS garantiza — minimiza el número de aristas, no los km. Ese camino cuesta 568 km. UCS, en cambio, encontró el camino de **menor costo real** (536 km), que necesita una carretera más (5 en vez de 4) pasando por Rimnicu Vilcea y Pitesti. Los dos caminos son distintos porque optimizan cosas distintas: BFS cuenta aristas, UCS suma kilómetros.

**¿Por qué DFS puede devolver un camino más largo aunque el grafo sea el mismo?**
Porque DFS no tiene ninguna garantía de optimalidad: baja por la **primera** rama que encuentra (aquí, en orden alfabético) y solo retrocede si esa rama no lleva a ningún lado. En esta instancia particular, DFS **coincidió** con el camino de BFS (568 km, 4 carreteras) — pero fue casualidad de que el orden alfabético llevara directo a la meta sin necesidad de retroceder: desde Timisoara, el vecino alfabéticamente primero es Arad; desde Arad, Sibiu; desde Sibiu, Fagaras; desde Fagaras, Bucharest. Si el orden alfabético hubiera llevado primero por una rama sin salida (por ejemplo, hacia Zerind u Oradea), DFS habría tenido que retroceder y explorar mucho más, pudiendo terminar en un camino bastante más largo que el óptimo — DFS simplemente no considera el costo ni la profundidad al decidir por dónde bajar.

**¿Con qué `--limit` DLS pasó de cutoff a solución, y cómo se relaciona con la profundidad de BFS/IDS?**
Con `--limit 2` DLS da `cutoff` (el límite es menor que la profundidad de cualquier solución alcanzable). Con `--limit 4` ya encuentra solución, y es exactamente la misma profundidad (4 carreteras) que encontró BFS/IDS — no es casualidad: BFS e IDS garantizan encontrar la solución de **menor profundidad posible**, así que el límite mínimo con el que DLS puede tener éxito es justo esa profundidad óptima. Cualquier límite menor (0, 1, 2, 3) da `cutoff` sin excepción; el límite 4 es el primero donde existe una solución alcanzable.

**Conexión con el ejercicio de búsqueda informada:** el camino que encontró UCS aquí (536 km, vía Rimnicu Vilcea–Pitesti) es **idéntico** al que encontró A* en el ejercicio 1 de `Búsqueda informada` para la misma pareja Timisoara→Bucharest. Esto confirma la propiedad esperada: cuando `h` es admisible, el costo óptimo de A* coincide con el de UCS — A* simplemente llega ahí expandiendo menos nodos (10 vs 12) gracias a la guía de la heurística.

## 5. Evidencia (salida de terminal)

```
Algorithm: Breadth-first search
Problem:   Timisoara → Bucharest
Status:    success
Path:      Timisoara → Arad → Sibiu → Fagaras → Bucharest
Depth:     4 roads
Cost:      568 km
Expanded:  7 nodes
Generated: 17 nodes
Frontier:  max size 5

Algorithm: Uniform-cost search
Problem:   Timisoara → Bucharest
Status:    success
Path:      Timisoara → Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest
Depth:     5 roads
Cost:      536 km
Expanded:  12 nodes
Generated: 31 nodes
Frontier:  max size 4

Algorithm: Depth-first search
Problem:   Timisoara → Bucharest
Status:    success
Path:      Timisoara → Arad → Sibiu → Fagaras → Bucharest
Depth:     4 roads
Cost:      568 km
Expanded:  4 nodes
Generated: 12 nodes
Frontier:  max size 5

Algorithm: Depth-limited search
Problem:   Timisoara → Bucharest
Status:    cutoff
Detail:    limit=2
Expanded:  3 nodes
Generated: 8 nodes
Frontier:  max size 5

Algorithm: Depth-limited search
Problem:   Timisoara → Bucharest
Status:    success
Detail:    limit=4
Path:      Timisoara → Arad → Sibiu → Fagaras → Bucharest
Depth:     4 roads
Cost:      568 km
Expanded:  4 nodes
Generated: 6 nodes
Frontier:  max size 7

Algorithm: Iterative deepening search
Problem:   Timisoara → Bucharest
Status:    success
Detail:    last_limit=4
Path:      Timisoara → Arad → Sibiu → Fagaras → Bucharest
Depth:     4 roads
Cost:      568 km
Expanded:  14 nodes
Generated: 34 nodes
Frontier:  max size 7
```
