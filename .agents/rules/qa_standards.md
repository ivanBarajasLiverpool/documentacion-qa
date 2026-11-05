---
trigger: always_on
description: "Estándares globales inmutables para la creación de Matrices de Pruebas de Aceptación (MPA) a partir de videos y documentación."
---

# Reglas de Estándar QA — Matriz de Pruebas de Aceptación (MPA)

1. **Estructura Obligatoria de Columnas**:
   Toda Matriz de Pruebas de Aceptación debe contener exactamente estas 6 columnas:
   - `ID del Caso`
   - `Condiciones Previas`
   - `N° Paso`
   - `Paso a Seguir (Automatizador)`
   - `Datos de Prueba`
   - `Resultado Esperado`

2. **Prohibición de Selectores Técnicos**:
   No se debe incluir una columna de selectores sugeridos (XPath, CSS, IDs de DOM) ni mezclar selectores técnicos crudos dentro del paso del automatizador. El paso debe referirse a los elementos visuales por su etiqueta o nombre funcional en la interfaz.

3. **Separación de Datos de Prueba**:
   Los valores literales ingresados en formularios o buscadores deben extraerse a la columna `Datos de Prueba` (ej. `Cliente: "Acme Corp"`), manteniendo la columna `Paso a Seguir (Automatizador)` enfocada en la acción reproducible. Si un paso no requiere datos de entrada, usar `N/A`.

4. **Patrón de Reflexión (Sin Observabilidad Técnica)**:
   La revisión crítica del borrador debe validar únicamente:
   - **Atomicidad**: Una sola acción del automatizador por fila.
   - **Coherencia Lógica**: Ausencia de huecos entre pasos consecutivos.
   - **Precisión Visual y Contextual**: Que ninguna fila conserve referencias ambiguas del audio ("dar clic aquí", "llenar esto").
