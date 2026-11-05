"""Módulo de lectura e inventario de archivos de entrada (videos y documentos de contexto)."""

from src.config.settings import (
    INPUT_CONTEXT_DOCS_DIR,
    INPUT_VIDEOS_DIR,
    ensure_directories,
)


def list_available_inputs() -> str:
    """Lista los videos disponibles en `data/inputs/videos/` y los documentos de contexto en `data/inputs/context_docs/`.

    Returns:
        Inventario formateado con las rutas absolutas de los archivos disponibles para procesar.
    """
    ensure_directories()

    videos = [
        str(p.resolve())
        for p in sorted(INPUT_VIDEOS_DIR.iterdir())
        if p.is_file() and not p.name.startswith(".")
    ]
    docs = [
        str(p.resolve())
        for p in sorted(INPUT_CONTEXT_DOCS_DIR.iterdir())
        if p.is_file() and not p.name.startswith(".")
    ]

    lines = ["=== INVENTARIO DE ENTRADAS (data/inputs/) ==="]
    lines.append(f"\n1. Videos en '{INPUT_VIDEOS_DIR}':")
    if videos:
        lines.extend([f"   - {v}" for v in videos])
    else:
        lines.append("   (Sin archivos en data/inputs/videos/)")

    lines.append(f"\n2. Documentos de Contexto en '{INPUT_CONTEXT_DOCS_DIR}':")
    if docs:
        lines.extend([f"   - {d}" for d in docs])
    else:
        lines.append("   (Sin archivos en data/inputs/context_docs/)")

    return "\n".join(lines)
