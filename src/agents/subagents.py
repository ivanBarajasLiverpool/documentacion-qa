"""Definición modular de los 4 subagentes especializados del framework MPA."""

from google.antigravity import types

# 1. Subagente Investigador de Contexto (activa skill: context-synthesis)
investigador_contexto_subagent = types.SubagentConfig(
    name="investigador_contexto",
    description=(
        "Recopila y sintetiza contexto funcional adicional desde documentación local "
        "(`data/inputs/context_docs/`) o URLs externas usando la skill `context-synthesis`. "
        "Extrae reglas de negocio, glosario de UI y precondiciones para la MPA."
    ),
    capabilities=types.SubagentCapabilities(
        agent_behavior=types.AgentBehavior.AUTONOMOUS,
        enabled_tools=[
            types.BuiltinTools.VIEW_FILE,
            types.BuiltinTools.FIND_FILE,
            types.BuiltinTools.LIST_DIR,
            types.BuiltinTools.READ_URL_CONTENT,
            types.BuiltinTools.SEARCH_WEB,
        ],
    ),
)

# 2. Subagente Inspector Visual OpenCV (activa skill: visual-disambiguation)
inspector_visual_subagent = types.SubagentConfig(
    name="inspector_visual_opencv",
    description=(
        "Inspecciona los fotogramas PNG guardados en `data/outputs/frames/` usando la "
        "skill `visual-disambiguation`. Resuelve expresiones ambiguas del audio "
        "identificando nombres reales de botones, campos y valores para `datos_prueba`."
    ),
    capabilities=types.SubagentCapabilities(
        agent_behavior=types.AgentBehavior.AUTONOMOUS,
        enabled_tools=[
            types.BuiltinTools.VIEW_FILE,
        ],
    ),
)

# 3. Subagente Crítico de Reflexión (activa skill: mpa-reflection)
critico_reflexion_subagent = types.SubagentConfig(
    name="critico_reflexion_mpa",
    description=(
        "Audita el borrador de la Matriz de Pruebas de Aceptación aplicando la skill "
        "`mpa-reflection` (Patrón de Reflexión). Verifica exclusivamente atomicidad de "
        "pasos, ausencia de huecos lógicos y separación limpia de `datos_prueba` "
        "(sin evaluar observabilidad técnica ni selectores)."
    ),
    capabilities=types.SubagentCapabilities(
        agent_behavior=types.AgentBehavior.AUTONOMOUS,
        enabled_tools=[
            types.BuiltinTools.VIEW_FILE,
        ],
    ),
)

# 4. Subagente Analista QA Estructurador (activa skill: mpa-drafting)
analista_qa_subagent = types.SubagentConfig(
    name="analista_qa_estructurador",
    description=(
        "Articula la Matriz de Pruebas de Aceptación paso a paso aplicando la skill "
        "`mpa-drafting`. Combina la transcripción, el contexto funcional y las "
        "observaciones de `inspector_visual_opencv`, y valida su borrador con "
        "`critico_reflexion_mpa` antes de devolver el JSON final."
    ),
    capabilities=types.SubagentCapabilities(
        agent_behavior=types.AgentBehavior.AUTONOMOUS,
        enabled_tools=[
            types.BuiltinTools.VIEW_FILE,
            types.BuiltinTools.START_SUBAGENT,
        ],
        allowed_subagents=[
            "inspector_visual_opencv",
            "critico_reflexion_mpa",
        ],
    ),
)

ALL_SUBAGENTS: list[types.SubagentConfig] = [
    investigador_contexto_subagent,
    analista_qa_subagent,
    inspector_visual_subagent,
    critico_reflexion_subagent,
]
