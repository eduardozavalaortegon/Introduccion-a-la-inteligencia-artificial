# Ejercicio 1 — Reporte: Greedy vs A* en el mapa de Rumania

## 1. Pareja origen–destino elegida

**Timisoara → Bucharest** (distinta de la pareja por defecto Arad → Bucharest).

Heurística usada: **distancia en línea recta (SLD) a Bucharest**, tabla AIMA (admisible y consistente), obtenida con:

```
python 02_heuristics.py --from-city Timisoara --to Bucharest
```

## 2. Subgrafo relevante (ciudades de ambos caminos, con km y h(n))

`h(n)` = distancia en línea recta de cada ciudad hasta Bucharest (tabla AIMA).

```
h=329 Timisoara
        |
        +--118 km--> h=366 Arad
        |                |
        |              140 km
        |                v
        |            h=253 Sibiu
        |                |
        |               80 km
        |                v
        |         h=193 Rimnicu Vilcea
        |                |
        |               97 km
        |                v
        +--111 km--> h=244 Lugoj              h=100 Pitesti <---+
                         |                          ^      \    |
                        70 km                      138 km   \ 101 km
                         v                            |       v
                     h=241 Mehadia               h=160 Craiova --+   h=0 Bucharest
                         |                              ^
                        75 km                           |
                         v                              |
                     h=242 Drobeta -------120 km---------+
```

Rama de arriba (Arad–Sibiu–Rimnicu Vilcea) = camino de **A\***.
Rama de abajo (Lugoj–Mehadia–Drobeta–Craiova) = camino de **Greedy**.
Ambas ramas convergen en Pitesti antes de llegar a Bucharest.

## 3. Tabla comparativa

| | Greedy best-first | A* |
|---|---|---|
| Heurística | SLD a Bucharest (tabla AIMA) | SLD a Bucharest (tabla AIMA) |
| Status | success | success |
| Path | Timisoara → Lugoj → Mehadia → Drobeta → Craiova → Pitesti → Bucharest | Timisoara → Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest |
| Depth | 6 carreteras | 5 carreteras |
| Cost | **615 km** | **536 km** |
| Expanded | 6 nodos | 10 nodos |
| Generated | 15 nodos | 27 nodos |
| Max frontier | 3 | 5 |

### Tabla g / h / f — Greedy

| Ciudad | g | h | f |
|---|---|---|---|
| Timisoara | 0 | 329 | 329 |
| Lugoj | 111 | 244 | 355 |
| Mehadia | 181 | 241 | 422 |
| Drobeta | 256 | 242 | 498 |
| Craiova | 376 | 160 | 536 |
| Pitesti | 514 | 100 | 614 |
| Bucharest | 615 | 0 | 615 |

### Tabla g / h / f — A*

| Ciudad | g | h | f |
|---|---|---|---|
| Timisoara | 0 | 329 | 329 |
| Arad | 118 | 366 | 484 |
| Sibiu | 258 | 253 | 511 |
| Rimnicu Vilcea | 338 | 193 | 531 |
| Pitesti | 435 | 100 | 535 |
| Bucharest | 536 | 0 | 536 |

## 4. Reporte (análisis)

**¿A* encontró el camino de menos km? ¿Greedy coincidió o se desvió?**
Sí, A* encontró el óptimo con 536 km. Greedy se desvió por completo hacia una ruta distinta de 615 km (79 km más cara): no fue un pequeño rodeo, tomó un camino totalmente diferente por el sur del mapa (Lugoj–Mehadia–Drobeta–Craiova) en vez de subir por Arad–Sibiu–Rimnicu Vilcea.

**¿Por qué Greedy puede devolver un camino más caro aunque h sea admisible?**
Porque Greedy ordena la frontera **solo por `h(n)`** y nunca considera `g(n)`, el costo ya gastado en llegar hasta ahí. En el primer cruce, desde Timisoara, Greedy compara `h(Lugoj)=244` contra `h(Arad)=366` y elige Lugoj porque *parece* estar más cerca de Bucharest en línea recta, sin importarle que el camino real por esa zona dé muchas vueltas. Que `h` sea admisible (nunca sobreestime la distancia real) protege la optimalidad de **A\***, no la de Greedy: Greedy simplemente no usa esa garantía porque ignora `g`.

**En el camino de A*, ¿f tiende a no disminuir? Relaciónalo con h consistente.**
Sí: a lo largo del camino de A*, `f` va 329 → 484 → 511 → 531 → 535 → 536: siempre igual o mayor, nunca baja. Esto ocurre porque la tabla SLD hacia Bucharest es **consistente** (cumple la desigualdad del triángulo: el costo real de cada arista nunca es menor que la diferencia de `h` entre sus dos extremos). Esa propiedad es justamente la que garantiza que A* nunca necesite "reabrir" un nodo ya expandido con un costo menor después — y por eso el número de `Expanded` (10) es razonable sin retrocesos.

**Punto de decisión: h(n) (Greedy) vs f(n)=g(n)+h(n) (A*).**
En Timisoara, Greedy mira solo `h`: `h(Lugoj)=244 < h(Arad)=366` → va a Lugoj y nunca vuelve atrás sobre esa decisión. A* mira `f=g+h`: `f(Lugoj)=111+244=355` también es menor que `f(Arad)=118+366=484`, así que A* **también empieza** explorando el lado de Lugoj — por eso expandió más nodos (10) que Greedy (6), invirtiendo esfuerzo en esa rama. Pero a diferencia de Greedy, A* mantiene abiertas ambas ramas en su frontera (no se compromete de forma irrevocable): en cuanto el costo acumulado `g` por el lado de Lugoj hace que su `f` supere al de la rama de Arad, A* cambia de rama y termina completando el camino óptimo por Arad–Sibiu–Rimnicu Vilcea–Pitesti. Esa es la diferencia central: Greedy decide y no reconsidera; A* siempre expande el nodo de menor `f` en **toda** la frontera, venga de la rama que venga.

**Nodos expandidos: ¿cuál algoritmo "trabajó" más?**
A* expandió más nodos (10 vs 6) porque exploró parcialmente la rama de Lugoj antes de descartarla a favor de la de Arad. Greedy "trabajó" menos, pero a costa de quedarse con la primera rama que parecía prometedora y terminar en una ruta 79 km más cara.

## 5. Evidencia de las corridas

- `python 01_romania_map.py` → ver [01_romania_map.png](01_romania_map.png)
- `python 02_heuristics.py --from-city Timisoara --to Bucharest` → ver [02_heuristics.png](02_heuristics.png)
- `python 03_greedy_best_first_search.py --from-city Timisoara --to Bucharest` → ver [03_greedy_best_first_search.png](03_greedy_best_first_search.png)
- `python 04_a_star_search.py --from-city Timisoara --to Bucharest` → ver [04_a_star_search.png](04_a_star_search.png)
