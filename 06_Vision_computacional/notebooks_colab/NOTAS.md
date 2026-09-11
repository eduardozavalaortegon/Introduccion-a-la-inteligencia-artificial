# Notas sobre esta notebook

Es una copia de `Visión computacional/Notebooks/13 YOLO ultralytics.ipynb` del repo de
referencia, con celdas nuevas al final (las originales de Zidane/bus quedaron intactas):

- Una celda `MI_FOTO = 'mi_foto.jpg'` — **aquí es donde pones tu imagen**.
- Una celda que corre `!yolo predict ... source='{MI_FOTO}'` (la misma predicción CLI que
  Zidane) y muestra el resultado directo en la notebook.
- Una celda que corre `model(MI_FOTO, save=True)` (la misma predicción por Python que el
  bus) sobre la misma foto, muestra el resultado, y además imprime cada clase detectada
  con su confianza (útil para el reporte).

**Qué te toca hacer tú (esto sí necesita algo tuyo — no puedo generarlo):**
1. Sube la notebook a [Google Colab](https://colab.research.google.com/).
2. `Runtime → Change runtime type → GPU (T4)`.
3. `Runtime → Run all` — esto corre primero Zidane y el bus (sin cambios).
4. Sube tu foto al panel de archivos de Colab (ícono de carpeta a la izquierda, arrastra
   el archivo), o consigue una URL pública directa a una imagen tuya. Debe verse al menos
   un objeto que COCO reconozca (persona, perro, silla, auto, taza, laptop, etc.).
5. Edita la celda `MI_FOTO = 'mi_foto.jpg'` con el nombre real de tu archivo (o la URL).
6. Corre solo esas 2 últimas celdas de código.
7. Captura las 3 salidas (Zidane, bus, tu foto) y guárdalas en
   `06_Vision_computacional/ejercicio_01/`.
8. Pásame las clases que detectó en tu foto (las imprime la última celda) y armamos el
   reporte.
