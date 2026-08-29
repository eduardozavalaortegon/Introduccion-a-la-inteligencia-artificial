# Ejercicio 1 — Mi cueva del Mundo de Wumpus

## Mi cueva (`config/mi_cueva_4x4.yaml`)

```
 4 | P  P  .  .
 3 | .  .  W  .
 2 | .  G  .  P
 1 | >  .  .  .
      1  2  3  4
```

- Agente: `[1, 1]`, mirando al este
- Wumpus: `[3, 3]`
- Pits: `[4, 2]`, `[2, 4]`, `[1, 4]`
- Oro: `[2, 2]`

Camino seguro: `[1,1] -> [2,1] -> [2,2]` (agarrar oro) `-> [2,1] -> [1,1]` (subir).

## Pregunta 1 — ¿Qué agentes lograron salir con el oro y cuáles no?

| Agente | Resultado | Pasos | Score |
|---|---|---|---|
| Simple reflex (`02`) | **No** consiguio el oro | 200 (limite) | -200.0 |
| Model-based (`03`) | Si, salio con el oro | 11 | 989.0 |
| Goal-based (`04`) | Si, salio con el oro | 11 | 989.0 |
| Utility-based (`05`) | Si, salio con el oro | 16 | 974.0 |
| Learning (`06`, 1500 episodios) | Si, salio con el oro | 9 | 991.0 |

Los cuatro agentes con memoria/planificacion (model-based, goal-based, utility-based y learning) resolvieron la cueva. Solo el agente de reflejo simple fallo.

## Pregunta 2 — ¿Por qué el agente de reflejo simple falla en este diseño?

El agente de reflejo simple (`agents/simple_reflex.py`) decide su accion **solo con la percepcion del instante actual**, sin guardar nada de lo que paso antes:

```python
if percept.glitter: return Action.GRAB
if percept.bump: return Action.TURN_LEFT
if percept.breeze or percept.stench: return Action.TURN_RIGHT
return Action.FORWARD
```

No sabe en que casilla esta, no recuerda cuales visito, no sabe donde quedo la entrada ni el oro una vez que sale de su vista. En mi cueva, en cuanto percibe *breeze* o *stench* gira a la derecha en vez de avanzar, y como nunca recuerda haber girado antes, puede quedar dando vueltas en el mismo lugar indefinidamente. Por eso agoto los 200 pasos permitidos (`max_steps`) sin llegar nunca al oro: termino con score -200 (solo penalizaciones por paso, `stopped without gold`).

No es cuestion de "mala suerte": con esta arquitectura, sin memoria, no hay forma de que el agente construya un plan para llegar al oro y regresar a la salida. Su unico exito posible seria toparse con el oro por casualidad estando ya "de frente" a el, lo cual no ocurrio en esta cueva.

## Pregunta 3 — ¿Cómo cambia el resultado del agente basado en modelo si acercas un pit a la casilla inicial?

Se creo una variante (`config/mi_cueva_4x4_pit_cercano.yaml`) moviendo el pit que estaba en `[4, 2]` a `[2, 1]`, es decir, pegado a la casilla inicial `[1, 1]` y justo sobre el camino que el agente usaba para llegar al oro:

```
 4 | P  P  .  .
 3 | .  .  W  .
 2 | .  G  .  .
 1 | >  P  .  .
      1  2  3  4
```

Resultado al correr `03_model_based_agent.py` sobre esta variante:

```
Result: stopped without gold  steps=200  score=-200.0
```

El agente **no murio** (nunca avanzo hacia el pit), pero tampoco avanzo a ningun lado: se quedo girando sobre si mismo en `[1,1]` durante los 200 pasos, exactamente igual de mal que el reflejo simple, aunque por una razon totalmente distinta.

**Por que pasa esto:** en `[1,1]` el agente percibe *breeze*. Esa brisa puede venir de cualquiera de las dos casillas vecinas sin visitar: `[2,1]` o `[1,2]`. El agente no tiene forma de saber cual de las dos tiene el pit real, asi que **no puede demostrar logicamente que ninguna de las dos es segura**. Como su regla es "nunca pisar una casilla que no sepa con certeza que es segura" (ver `agents/model_based.py`, comentario `# Nothing left that is known-safe: turn in place rather than gamble`), prefiere no arriesgarse y se queda girando en el mismo lugar en vez de avanzar a cualquiera de las dos.

Comparado con el mapa original (pit mas lejos, en `[4,2]`), donde el unico vecino sin visitar de `[1,1]` era `[2,1]` (la brisa ahi solo podia significar peligro en una direccion, y `[1,2]`no daba señal de peligro por no ser vecino de una casilla con breeze), el agente si podia deducir con certeza que `[2,1]` era seguro y avanzar. Al mover el pit justo al lado de la entrada, se crea *ambiguedad* entre los dos unicos vecinos del punto de partida, y el agente queda completamente bloqueado: paso de conseguir el oro en 11 pasos (score 989) a quedarse sin moverse y terminar con score -200.

Esto ilustra bien la diferencia entre "temerario" (reflejo simple) y "excesivamente cauteloso" (model-based): ninguno de los dos consigue el oro en este mapa modificado, pero el basado en modelo al menos nunca se pone en riesgo de morir — simplemente se rehusa a actuar sin certeza logica.
