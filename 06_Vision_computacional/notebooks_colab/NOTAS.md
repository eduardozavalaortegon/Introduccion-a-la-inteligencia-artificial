# Notas sobre esta notebook

Es una copia de `Visión computacional/Notebooks/13 YOLO ultralytics.ipynb` del repo de
referencia, con celdas nuevas al final (las originales de Zidane/bus quedaron intactas):

- Una celda `MI_FOTO = 'mi_foto.jpg'` — **aquí es donde pones tu imagen**.
- Una celda que corre `!yolo predict ... source='{MI_FOTO}'` (la misma predicción CLI que
  Zidane) y muestra el resultado directo en la notebook.
- Una celda que corre `model(MI_FOTO, save=True)` (la misma predicción por Python que el
  bus) sobre la misma foto, muestra el resultado, y además imprime cada clase detectada
  con su confianza (útil para el reporte).

**Actualización — corrido localmente (autorizado por el profesor):** venv en `C:\venvs\yolo`
(ultralytics + torch CPU — no hay GPU NVIDIA en esta máquina, ver notas de Perceptrón multicapa).
Verificado de punta a punta dos veces. Se encontraron y arreglaron 2 bugs reales de entorno:

1. Dentro del kernel de Jupyter local, `!yolo ...` no encontraba el comando (no está en el PATH
   del subproceso) — afectaba **también** a la celda original de Zidane, no solo a las nuevas.
   Se arregló resolviendo la ruta completa de `yolo.exe` vía `sys.executable`.
2. La lógica para mostrar "la imagen más reciente" en `runs/detect/predict*/` tomaba el primer
   archivo que encontraba `glob`, no el más nuevo — se corrigió usando `max(..., key=os.path.getmtime)`.

**Imagen final usada: `mi_foto.png`** (foto real propia, selfie con 3 personas). El reporte y las
4 capturas ya están en `06_Vision_computacional/ejercicio_01/`. La versión ejecutada completa (con
todas las salidas) quedó guardada como `13 YOLO ultralytics (modificado) - EJECUTADA.ipynb`.
