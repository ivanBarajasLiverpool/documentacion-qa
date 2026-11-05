"""Configuración centralizada de rutas y parámetros del framework MPA."""

import os
from pathlib import Path

# Raíz del proyecto
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent


def _load_env_file(env_path: Path) -> None:
    """Carga variables del archivo .env usando python-dotenv o un parser nativo como respaldo."""
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path)
    except ImportError:
        if not env_path.is_file():
            return
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


# Carga automática de variables definidas en el archivo .env
_load_env_file(BASE_DIR / ".env")

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

# Parámetros por defecto de transcripción local (configurables desde .env)
DEFAULT_WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "small")
DEFAULT_WHISPER_COMPUTE_TYPE: str = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
DEFAULT_LANGUAGE: str = os.getenv("WHISPER_LANGUAGE", "es")


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
