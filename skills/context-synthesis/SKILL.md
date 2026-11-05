---
name: context-synthesis
description: "Procedimiento para extraer y sintetizar reglas de negocio, glosario funcional y precondiciones desde documentos locales (MD, TXT, PDF) o URLs externas."
---

# Skill: Síntesis de Contexto Funcional para MPA

Utiliza esta guía cuando el usuario proporcione documentación adicional, archivos de requerimientos o URLs para complementar el análisis del video.

## Estructura del Resumen de Contexto
Extrae y entrega al Analista QA únicamente los elementos que impactan la Matriz de Pruebas de Aceptación:
1. **Glosario de UI y Entidades**: Nombres oficiales de módulos, pantallas, roles de usuario y estados del sistema.
2. **Precondiciones Implícitas**: Requisitos que la documentación marca como obligatorios aunque el locutor del video no los mencione en voz alta (ej. permisos de rol, catálogos activos).
3. **Reglas de Negocio para Resultados Esperados**: Cálculos automáticos (impuestos, descuentos), validaciones de campos obligatorios y mensajes esperados según la especificación.
