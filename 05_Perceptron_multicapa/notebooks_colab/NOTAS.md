# Notas sobre estas notebooks

Son copias de `Perceptrón multicapa/Notebooks/04...` y `05...` del repo de referencia,
**con la red profunda ya agregada al final** (celdas nuevas después de las originales,
que se dejaron intactas para conservar la corrida de referencia):

- **`04 Multilayer perceptron (modificado).ipynb`**: agrega `layer3_d`/`layer4_d`
  (topología 4×3×3×3×3), `init_weights_deep()`, `calculate_error_deep()`, y el ciclo de
  entrenamiento profundo con forward + backprop actualizados para 4 capas (no solo la
  inicialización). Reutiliza `generate_weights`, `net_input`, `sigmoid`, `propagate` de
  las celdas originales — no las toques ni las borres, la parte nueva depende de ellas.
- **`05 Keras - multilayer perceptron - iris (modificado).ipynb`**: agrega `model_deep`
  con 4 capas `Dense(3, activation="sigmoid")`, se entrena por separado en `history_deep`
  (sin pisar `model`/`history` originales) y grafica ambas curvas de pérdida juntas.

**Actualización — corrido localmente (autorizado por el profesor):** venv en `C:\venvs\mlp`
(numpy, scikit-learn, pandas, tensorflow/keras — CPU, sin GPU NVIDIA en esta máquina). Ambas
notebooks se ejecutaron de punta a punta dos veces, sin errores. Se corrigió además un bug real
de la notebook **original** de NumPy: `generate_weights()` usaba `np.random.rand(1)` para llenar
un escalar, incompatible con NumPy ≥ 2.0 (`ValueError`). Se cambió a `np.random.rand()` — mismo
comportamiento, solo compatible con NumPy moderno. Sin este arreglo la notebook original ni
siquiera corre.

Las versiones ejecutadas (con todas las salidas, gráficas y `model.summary()` ya incluidos)
quedaron guardadas junto a estas como `... - EJECUTADA.ipynb`. Las gráficas y el
`model.summary()` extraídos como evidencia, más el reporte completo, están en
`05_Perceptron_multicapa/ejercicio_01/`.
