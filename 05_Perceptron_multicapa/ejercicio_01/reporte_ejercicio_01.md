# Ejercicio 1 — Reporte: más capas en el perceptrón multicapa (Iris)

Corrido localmente (autorizado por el profesor) en `C:\venvs\mlp` — venv con NumPy, scikit-learn,
pandas y TensorFlow/Keras (CPU; esta máquina no tiene GPU NVIDIA, ver notas del ejercicio 6 sobre
por qué). Ambas notebooks se ejecutaron de punta a punta dos veces, sin errores, con
`Runtime`≈"Run all" vía `nbconvert --execute` (equivalente local a correr todas las celdas).

Notebooks modificadas: [`04 Multilayer perceptron (modificado).ipynb`](../notebooks_colab/04%20Multilayer%20perceptron%20(modificado).ipynb)
y [`05 Keras - multilayer perceptron - iris (modificado).ipynb`](../notebooks_colab/05%20Keras%20-%20multilayer%20perceptron%20-%20iris%20(modificado).ipynb).

De paso se corrigió un bug real de la notebook **original** (no introducido por el ejercicio):
`generate_weights()` usaba `np.random.rand(1)` para llenar un escalar, algo que NumPy ≥ 2.0 ya no
permite (`ValueError: setting an array element with a sequence`). Se cambió a `np.random.rand()`
— mismo comportamiento estadístico, solo compatible con NumPy moderno. Sin este arreglo la notebook
ni siquiera corre la topología original.

## 1. Topologías

- **Original**: 4×3×3 (una capa oculta de 3 + salida de 3).
- **Profunda**: 4×3×3×3×3 (tres capas ocultas de 3 + salida de 3) — dos capas extra, como pide el
  ejercicio. Mismo `η = 0.03`, mismas 500 épocas, sigmoide en todas las capas, en ambas
  implementaciones.

## 2. Resultados numéricos (error/pérdida final tras 500 épocas)

| Implementación | Original (4×3×3) | Profunda (4×3×3×3×3) |
|---|---|---|
| NumPy a mano (MSE) | 0.112 | **0.377** |
| Keras (MSE) | 0.146 | **0.222** |

En **ambas** implementaciones la red profunda termina con error más alto que la original — no
aprendió mejor, aprendió peor.

`model.summary()` (Keras) confirma la arquitectura pedida — ver
[`keras_model_summaries.txt`](keras_model_summaries.txt):
- Original: 2 capas `Dense` (`layer1`, `layer2`), **27** parámetros totales.
- Profunda: **4** capas `Dense` (`layer1`…`layer4`), **51** parámetros totales.

## 3. Reporte (análisis)

**¿Bajó más el error al añadir dos capas, o se estancó/empeoró? ¿Igual en NumPy y en Keras?**

Se estancó/empeoró en ambas. Mirando las curvas (`numpy_curva_comparacion.png`,
`keras_curva_comparacion.png`), la red profunda pasa un tramo largo prácticamente plana —en NumPy
se queda pegada en ~0.67 desde la época 0 hasta cerca de la 380, y en Keras baja mucho más lento
que la original durante todo el entrenamiento y se aplana cerca de 0.22— antes de que el error
empiece a moverse. La versión original, en cambio, desciende de forma mucho más consistente en
ambas implementaciones. El patrón es el mismo en NumPy y en Keras: más profundidad no ayudó en
este problema con esta configuración.

**¿Las curvas de la notebook 01 (NumPy) y de Keras se parecen con la misma topología? Si no, ¿qué
podría explicarlo?**

Se parecen en la **forma cualitativa** (ambas muestran a la red profunda estancada frente a la
original bajando con más fluidez), pero no en la escala: NumPy arranca con error ~0.8-0.9 y termina
la original en 0.11, mientras Keras arranca en ~0.25-0.30 y termina en 0.15. Las diferencias
probables: la inicialización de pesos es distinta (NumPy usa `np.random.rand()-0.5`, Keras usa su
inicializador `glorot_uniform` por defecto), el orden de actualización (NumPy actualiza pesos
ejemplo por ejemplo dentro de cada época — SGD "puro"; Keras con `model.fit` por defecto también
hace mini-batches pero con su propio manejo interno vectorizado), y el cálculo interno de MSE puede
diferir ligeramente en normalización. Ninguna de las dos es "más correcta"; son dos implementaciones
del mismo algoritmo con detalles numéricos distintos.

**Con sigmoides apiladas y MSE, ¿tiene sentido que una red más profunda no aprenda mejor en Iris?**

Sí, tiene sentido, y las gráficas lo muestran directamente. Iris es un problema chico (150 ejemplos)
y casi linealmente separable — no necesita profundidad. Al apilar 3 sigmoides seguidas con MSE, el
gradiente que se retropropaga es un producto de varios términos `h(1-h)` (cada uno ≤ 0.25), así que
se va haciendo cada vez más pequeño según llega a las capas iniciales — el clásico **gradiente que
se desvanece**. Eso explica exactamente el tramo plano largo que se ve en ambas curvas: las primeras
capas casi no reciben señal de error durante cientos de épocas, hasta que algo (una fluctuación en
los pesos) las saca de ese estancamiento. Con más neuronas o más datos tal vez la red profunda
alcanzaría al final a la original, pero en este experimento (3 ocultas de 3 neuronas, 500 épocas)
no lo logra.

## 4. Evidencias

- [`numpy_curva_original.png`](numpy_curva_original.png) — curva de error, NumPy, topología 4×3×3.
- [`numpy_curva_comparacion.png`](numpy_curva_comparacion.png) — original vs. profunda, NumPy (mismo gráfico).
- [`keras_curva_original.png`](keras_curva_original.png) — curva de loss, Keras, topología 4×3×3.
- [`keras_curva_comparacion.png`](keras_curva_comparacion.png) — original vs. profunda, Keras.
- [`keras_model_summaries.txt`](keras_model_summaries.txt) — `model.summary()` original (2 `Dense`,
  27 params) y profundo (4 `Dense`, 51 params).
