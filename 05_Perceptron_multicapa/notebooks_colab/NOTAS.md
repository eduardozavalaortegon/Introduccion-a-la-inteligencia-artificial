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

**Qué te toca hacer tú:**
1. Sube ambos `.ipynb` a [Google Colab](https://colab.research.google.com/) (Archivo → Subir notebook).
2. `Runtime → Run all` en cada uno.
3. Captura: la curva de error original, la curva profunda (o la combinada que ya grafica
   ambas), y en Keras los dos `model.summary()` (original ya estaba, profundo es nuevo).
4. Guarda esas capturas en `05_Perceptron_multicapa/ejercicio_01/`.
5. Con los números reales (error final original vs. profundo, en NumPy y en Keras),
   dime los valores y armamos el reporte comparativo.

No se probó `05` localmente (necesita TensorFlow); si Colab marca algún error de sintaxis
avísame y lo reviso.
