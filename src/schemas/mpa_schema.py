"""Esquemas de datos Pydantic para la Matriz de Pruebas de Aceptación (MPA)."""

import pydantic


class PasoPrueba(pydantic.BaseModel):
    numero_paso: int = pydantic.Field(
        description="Número secuencial del paso (1, 2, 3...)"
    )
    paso_automatizador: str = pydantic.Field(
        description="Acción atómica y clara que debe ejecutar el automatizador"
    )
    datos_prueba: str = pydantic.Field(
        default="N/A",
        description="Datos de entrada utilizados en este paso (ej. Usuario: 'admin', Monto: '500'). Usar 'N/A' si no aplica.",
    )
    resultado_esperado: str = pydantic.Field(
        description="Respuesta o estado esperado del sistema tras ejecutar el paso"
    )


class CasoPruebaAceptacion(pydantic.BaseModel):
    id_caso: str = pydantic.Field(
        description="Identificador único del caso de prueba (ej. MPA-001)"
    )
    titulo_caso: str = pydantic.Field(
        description="Título descriptivo del flujo o escenario analizado"
    )
    condiciones_previas: list[str] = pydantic.Field(
        description="Lista de condiciones previas necesarias para lograr ejecutar el caso"
    )
    pasos: list[PasoPrueba] = pydantic.Field(
        description="Lista secuencial de pasos y resultados esperados"
    )


class MatrizPruebasAceptacion(pydantic.BaseModel):
    proyecto: str = pydantic.Field(
        default="Proyecto QA",
        description="Nombre del módulo o sistema bajo prueba",
    )
    resumen_contexto: str = pydantic.Field(
        default="",
        description="Breve síntesis del contexto funcional obtenido de la documentación/URLs",
    )
    casos: list[CasoPruebaAceptacion] = pydantic.Field(
        description="Casos de prueba que conforman la Matriz de Pruebas de Aceptación"
    )
