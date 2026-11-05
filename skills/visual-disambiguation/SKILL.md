---
name: visual-disambiguation
description: "Guía para inspeccionar fotogramas (frames PNG) extraídos con OpenCV y resolver referencias ambiguas del audio ('clic aquí', 'lleno esto') identificando etiquetas y datos de prueba reales."
---

# Skill: Desambiguación Visual con Fotogramas de OpenCV

Activa esta skill cuando analices capturas de pantalla (`frame_*.png`) extraídas de un video para complementar la transcripción de audio.

## Procedimiento de Inspección
1. **Cruzar Timestamp con Fotograma**:
   Relaciona cada imagen `frame_<segundos>s.png` con la línea de la transcripción correspondiente a ese instante `[inicio - fin]`.
2. **Reemplazar Expresiones Deícticas**:
   - Cuando el locutor diga *"doy clic aquí"* o *"presiono este botón"*, identifica en la imagen el texto exacto del botón, pestaña o enlace donde se encuentra el cursor o el foco visual.
   - Cuando el locutor diga *"lleno estos campos"* o *"pongo este cliente"*, lee los valores literales escritos dentro de los inputs en la imagen para poblar con precisión la columna `datos_prueba`.
   - Cuando el locutor diga *"me sale este mensaje"*, transcribe el texto exacto de la alerta, modal o notificación visible en el fotograma para enriquecer la columna `resultado_esperado`.
