"""Configuración centralizada de rutas y parámetros del framework MPA."""

from pathlib import Path

# Raíz del proyecto
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

# Directorio de Skills para cargar en LocalAgentConfig(skills_paths=...)
SKILLS_DIR: Path = BASE_DIR / "skills"

# Directorios de Entrada (Inputs)
DATA_DIR: Path = BASE_DIR / "data"
INPUT_VIDEOS_DIR: Path = DATA_DIR / "inputs" / "videos"
INPUT_CONTEXT_DOCS_DIR: Path = DATA_DIR / "inputs" / "context_docs"

# Directorios de Salida (Outputs)
OUTPUT_TRANSCRIPTS_DIR: Path = DATA_DIR / "outputs" / "transcripts"
OUTPUT_FRAMES_DIR: Path = DATA_DIR / "outputs" / "frames"
OUTPUT_MATRICES_DIR: Path = DATA_DIR / "outputs" / "matrices"

# Parámetros por defecto de transcripción local
DEFAULT_WHISPER_MODEL: str = "small"
DEFAULT_WHISPER_COMPUTE_TYPE: str = "int8"
DEFAULT_LANGUAGE: str = "es"


def ensure_directories() -> None:
    """Garantiza que toda la estructura de carpetas de entrada y salida exista."""
    for folder in (
        INPUT_VIDEOS_DIR,
        INPUT_CONTEXT_DOCS_DIR,
        OUTPUT_TRANSCRIPTS_DIR,
        OUTPUT_FRAMES_DIR,
        OUTPUT_MATRICES_DIR,
    ):
        folder.mkdir(parents=True, exist_ok=True)
