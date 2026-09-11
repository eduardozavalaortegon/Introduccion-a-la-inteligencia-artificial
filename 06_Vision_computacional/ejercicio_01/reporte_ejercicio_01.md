# Ejercicio 1 — Reporte: cambiar la imagen de predicción en YOLO

Corrido localmente (autorizado por el profesor), con la notebook
[`13 YOLO ultralytics (modificado) - EJECUTADA.ipynb`](../notebooks_colab/13%20YOLO%20ultralytics%20(modificado)%20-%20EJECUTADA.ipynb)
verificada de punta a punta (Ultralytics 8.4.147, torch 2.14 CPU — sin GPU NVIDIA en esta máquina,
ver notas de la sección de Perceptrón multicapa sobre por qué).

## 1. Foto usada

Foto real propia (`mi_foto.png`): selfie nocturna con 3 personas, dos haciendo seña de paz. No es
`zidane.jpg` ni `bus.jpg`, y muestra objetos que COCO sabe nombrar (**person** claramente; también
hay una botella en primer plano, clase COCO "bottle").

## 2. Qué se modificó

Un solo cambio de código, como pide el ejercicio: la fuente de la imagen en ambas celdas de
predicción (`MI_FOTO = 'mi_foto.png'`). Modelo (`yolov8n.pt`), épocas (`epochs=3`) y dataset
(`coco128.yaml`) quedaron intactos.

Adicionalmente fue necesario un arreglo de **entorno**, no de lógica: dentro del kernel de Jupyter
local, el comando `yolo` no estaba en el PATH del subproceso (mismo tipo de problema que tuvimos con
`python` al inicio de este curso). Se resolvió apuntando a la ruta completa de `yolo.exe` vía
`sys.executable` — esto afecta también a la celda **original** de Zidane, que sin este arreglo fallaba
silenciosamente en local (en Colab no hace falta, ahí `yolo` sí está en el PATH).

## 3. Entrenamiento (3 épocas, coco128)

| Época | mAP50 | mAP50-95 |
|---|---|---|
| 1 | 0.619 | 0.460 |
| 2 | 0.646 | 0.482 |
| 3 | 0.654 | 0.486 |

## 4. Reporte (análisis)

**¿Qué clases detectó YOLO en las fotos de Ultralytics y cuáles en la tuya?**

| Imagen | Modelo usado | Detecciones |
|---|---|---|
| `zidane.jpg` (CLI) | `yolov8n.pt` preentrenado | 2 persons, 1 tie |
| `bus.jpg` (`model()`) | fine-tuned 3 épocas en coco128 | 4 persons, 1 bus, 1 stop sign |
| `mi_foto.png` (CLI) | `yolov8n.pt` preentrenado | **4 persons** (0.85, 0.66, ~0.6 y una caja adicional superpuesta) |
| `mi_foto.png` (`model()`) | fine-tuned 3 épocas en coco128 | **3 persons** (0.86, 0.65, 0.38) |

En mi foto, YOLO solo etiquetó personas — ninguna otra clase COCO, aunque el resultado tiene sentido
dado el encuadre (selfie nocturna, tres personas ocupando casi todo el cuadro).

**¿Algún objeto evidente de tu foto no salió etiquetado? ¿Por qué podría pasar?**

Sí: hay una **botella verde** claramente visible en primer plano (parte inferior de la foto, "bottle"
sí es una clase de COCO) y **no se detectó** en ninguna de las dos corridas. Las razones más probables,
combinando las pistas del enunciado: es un objeto **chico** dentro del encuadre, está en la zona más
**oscura/con menos luz** de la foto (es de noche, con un solo foco de luz arriba), y está parcialmente
**cortado/en primer plano borroso**. Cualquiera de esas tres condiciones basta para que la confianza
caiga por debajo del umbral por defecto (0.25) y la caja ni se dibuje.

**¿La predicción de la celda CLI y la de `model(...)` coinciden sobre tu misma imagen?**

**No coinciden del todo**: el CLI detectó 4 "person" y `model()` detectó 3. La razón es identificable
y es la misma que se observa entre Zidane y el bus en la notebook original: la celda CLI carga
`yolov8n.pt` **preentrenado tal cual** (`model=yolov8n.pt`, proceso nuevo cada vez), mientras que la
celda `model(...)` reutiliza el objeto `model` de Python que **ya fue reentrenado** 3 épocas sobre
`coco128` en la celda anterior. El fine-tune corto cambió ligeramente el comportamiento del detector
sobre esta imagen fuera de su dominio de entrenamiento (una selfie nocturna no se parece a las 128
imágenes de `coco128`), y terminó siendo *más conservador* aquí (descartó una de las cuatro cajas).
También cambiaron las confianzas: la persona de la derecha (más borrosa, con el brazo en movimiento)
pasó de 0.60 (CLI) a 0.38 (`model()`) — la más insegura en ambos casos, coherente con que es la
imagen con más desenfoque de movimiento.

## 5. Evidencia

- [`resultado_zidane_original.jpg`](resultado_zidane_original.jpg) — Zidane, CLI, modelo base.
- [`resultado_bus_finetuned.jpg`](resultado_bus_finetuned.jpg) — bus, `model()`, modelo afinado.
- [`resultado_mifoto_cli.jpg`](resultado_mifoto_cli.jpg) — mi foto, CLI, modelo base (4 personas).
- [`resultado_mifoto_model.jpg`](resultado_mifoto_model.jpg) — mi foto, `model()`, modelo afinado
  (3 personas, confianzas distintas a las del CLI).
