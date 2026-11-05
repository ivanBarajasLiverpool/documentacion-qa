"""Módulo de exportación de la Matriz de Pruebas de Aceptación a formato Markdown (.md)."""

from pathlib import Path
from src.config.settings import OUTPUT_MATRICES_DIR, ensure_directories
from src.schemas.mpa_schema import MatrizPruebasAceptacion


def exportar_matriz_markdown(
    matriz_json: str,
    filename: str = "Matriz_Pruebas_Aceptacion.md",
) -> str:
    """Valida el JSON contra el esquema MatrizPruebasAceptacion y escribe la tabla final en `data/outputs/matrices/`.

    Args:
        matriz_json: Cadena JSON válida según el esquema MatrizPruebasAceptacion.
        filename: Nombre del archivo `.md` que se guardará dentro de `data/outputs/matrices/`.

    Returns:
        Confirmación y ruta absoluta del archivo Markdown generado.
    """
    ensure_directories()

    try:
        matriz = MatrizPruebasAceptacion.model_validate_json(matriz_json)
    except Exception as e:
        return f"Error de validación Pydantic en el JSON de la matriz: {str(e)}"

    clean_name = Path(filename).name
    if not clean_name.endswith(".md"):
        clean_name += ".md"

    output_path = (OUTPUT_MATRICES_DIR / clean_name).resolve()

    md_lines = [
        f"# Matriz de Pruebas de Aceptación (MPA) — {matriz.proyecto}",
        "",
    ]

    if matriz.resumen_contexto:
        md_lines.extend([
            "## Contexto Funcional y Documentación de Referencia",
            f"> {matriz.resumen_contexto}",
            "",
        ])

    md_lines.extend([
        "## Tabla Consolidada de Casos de Prueba",
        "",
        "| ID del Caso | Condiciones Previas | N° Paso | Paso a Seguir (Automatizador) | Datos de Prueba | Resultado Esperado |",
        "| :--- | :--- | :---: | :--- | :--- | :--- |",
    ])

    for caso in matriz.casos:
        precondiciones_html = (
            "<br>".join([f"• {c}" for c in caso.condiciones_previas])
            if caso.condiciones_previas
            else "Ninguna"
        )

        for idx, paso in enumerate(caso.pasos):
            id_col = (
                f"**{caso.id_caso}**<br>*({caso.titulo_caso})*"
                if idx == 0
                else f"`{caso.id_caso}`"
            )
            pre_col = precondiciones_html if idx == 0 else "*(Ver paso 1)*"

            accion = paso.paso_automatizador.replace("|", "\\|")
            datos = paso.datos_prueba.replace("|", "\\|")
            esperado = paso.resultado_esperado.replace("|", "\\|")

            md_lines.append(
                f"| {id_col} | {pre_col} | {paso.numero_paso} | {accion} | `{datos}` | {esperado} |"
            )

    output_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return f"Matriz exportada exitosamente en: {output_path}"
