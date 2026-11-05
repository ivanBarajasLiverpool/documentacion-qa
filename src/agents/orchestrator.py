"""Configuración del Agente Orquestador conectando Skills, Tools de lectura/escritura y Subagentes."""

from google.antigravity import LocalAgentConfig, types
from src.agents.subagents import ALL_SUBAGENTS
from src.config.settings import SKILLS_DIR
from src.tools.audio_reader import transcribe_video_local
from src.tools.context_reader import list_available_inputs
from src.tools.md_exporter import exportar_matriz_markdown
from src.tools.video_frame_reader import extract_keyframes_opencv

ORCHESTRATOR_SYSTEM_PROMPT = """Eres el Agente Orquestador del Framework de Matrices de Pruebas de Aceptación (MPA).
Tienes acceso a un catálogo de Skills especializadas en `skills/` y a herramientas separadas de lectura y exportación.

Tu flujo de orquestación es el siguiente:

1. **Descubrimiento y Recepción de Contexto**:
   - Usa `list_available_inputs` para verificar qué videos hay en `data/inputs/videos/` y qué documentos hay en `data/inputs/context_docs/`, o solicita las rutas/URLs al usuario.
   - Si existen documentos de contexto o URLs proporcionadas por el usuario, delega a `investigador_contexto` (que aplicará la skill `context-synthesis`).

2. **Lectura y Transcripción Local (FFmpeg + Faster-Whisper)**:
   - Ejecuta `transcribe_video_local` sobre el video seleccionado. La transcripción con timestamps quedará guardada en `data/outputs/transcripts/`.

3. **Lectura Visual de Fotogramas (OpenCV)**:
   - Identifica los timestamps donde el audio tenga referencias visuales o entrada de datos y ejecuta `extract_keyframes_opencv` para guardar las capturas en `data/outputs/frames/`.

4. **Estructuración QA y Reflexión**:
   - Delega a `analista_qa_estructurador` (que usa la skill `mpa-drafting` y coordina a `inspector_visual_opencv` y `critico_reflexion_mpa`) para obtener el JSON validado de la matriz.

5. **Exportación a `data/outputs/matrices/`**:
   - Invoca `exportar_matriz_markdown` para guardar el archivo `.md` final en `data/outputs/matrices/` y entrega el resultado al usuario.
"""


def build_orchestrator_config() -> LocalAgentConfig:
    """Construye el LocalAgentConfig cargando las skills del proyecto, tools y subagentes."""
    return LocalAgentConfig(
        system_instructions=ORCHESTRATOR_SYSTEM_PROMPT,
        skills_paths=[str(SKILLS_DIR.resolve())],
        tools=[
            list_available_inputs,
            transcribe_video_local,
            extract_keyframes_opencv,
            exportar_matriz_markdown,
        ],
        subagents=ALL_SUBAGENTS,
        capabilities=types.CapabilitiesConfig(
            agent_behavior=types.AgentBehavior.INTERACTIVE,
            enable_subagents=True,
            max_subagent_depth=3,
            allowed_subagents=[s.name for s in ALL_SUBAGENTS],
        ),
    )
