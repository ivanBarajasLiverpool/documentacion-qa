---
name: mpa-reflection
description: "Checklist de revisión crítica (Patrón de Reflexión) para auditar y corregir borradores de la Matriz de Pruebas de Aceptación garantizando atomicidad, orden lógico y separación de datos de prueba."
---

# Skill: Auditoría y Reflexión de Matriz de Pruebas de Aceptación

Utiliza esta guía para revisar críticamente cualquier borrador de MPA antes de exportarlo a Markdown.

## Checklist de Reflexión (3 Criterios Estrictos)

1. **Verificación de Atomicidad**:
   - Revisa cada fila de `paso_automatizador`.
   - Si encuentras conjunciones que unen dos acciones distintas (ej. *"Seleccionar el cliente, agregar el producto y dar clic en Guardar"*), **divídelas en filas independientes** renumerando secuencialmente `numero_paso` y asignando el `resultado_esperado` intermedio a cada una.

2. **Detección de Huecos Lógicos**:
   - Verifica que la transición entre el Paso $N$ y el Paso $N+1$ sea continua.
   - Si el Paso $N$ está en el Dashboard y el Paso $N+1$ llena un campo dentro de un modal sin haber indicado el clic que abre dicho modal, inserta el paso faltante.

3. **Limpieza de `datos_prueba`**:
   - Verifica que los valores literales estén expresados en `datos_prueba` y que ningún paso tenga valores vacíos (debe decir `"N/A"` cuando no hay entrada de datos).
   - **Importante**: No evalúes ni exijas criterios de observabilidad técnica a nivel código ni agregues selectores CSS/XPath.
