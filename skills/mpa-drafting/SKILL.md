---
name: mpa-drafting
description: "Metodología estandarizada para transformar transcripciones de video, fotogramas e información de contexto en una Matriz de Pruebas de Aceptación (MPA) paso a paso."
---

# Skill: Redacción y Estructuración de Matriz de Pruebas de Aceptación (MPA)

Utiliza esta guía siempre que debas articular o redactar casos de prueba a partir de la transcripción de un video y su contexto funcional.

## 1. Identificación del Caso y Condiciones Previas
- **`id_caso`**: Utiliza el prefijo indicado por el usuario o por el módulo (ej. `MPA-FAC-001`).
- **`condiciones_previas`**: Extrae todo lo que debe existir o estar configurado *antes* del Paso 1 (roles de usuario, permisos, catálogos precargados, estado del ambiente). No coloques precondiciones como pasos de ejecución.

## 2. Redacción de `paso_automatizador`
- Redacta en infinitivo o imperativo directo orientado al ingeniero de automatización (ej. *"Hacer clic en el botón..."*, *"Ingresar el criterio de búsqueda en el campo..."*, *"Seleccionar la opción... en la lista desplegable..."*).
- **Un paso = Una acción atómica**. Nunca combines navegación, llenado de múltiples secciones distantes y envío de formulario en la misma fila.

## 3. Extracción de `datos_prueba`
- Extrae todo dato literal mencionado en el audio o visto en los fotogramas de OpenCV en formato `Campo: "Valor"` separado por ` | ` cuando haya múltiples campos en el mismo paso (ej. `Cantidad: "1" | Precio Unitario: "15000.00"`).
- Si el paso es únicamente una acción de navegación o clic sin entrada de datos, asigna `"N/A"`.

## 4. Redacción de `resultado_esperado`
- Cada fila debe tener su propio resultado esperado inmediato tras ejecutar la acción del paso.
- Si deseas consultar un ejemplo completo de referencia, revisa el archivo `examples/mpa_gold_standard.md` dentro de esta skill.
