# Framework Multiagente Generador de Matrices de Pruebas de Aceptación (MPA)

Framework multiagente en Python que transforma grabaciones de video de pruebas o sesiones de usuario, junto con documentación funcional y URLs, en **Matrices de Pruebas de Aceptación (MPA)** estructuradas paso a paso en formato Markdown (`.md`).

---

## Características Principales

- **Arquitectura Multiagente Jerárquica**:
  - **Agente Orquestador (`INTERACTIVE`)**: Conversa con el usuario, recopila instrucciones y coordina el flujo completo entre herramientas locales y subagentes.
  - **Subagente Investigador de Contexto (`investigador_contexto`)**: Procesa documentación local (`.md`, `.pdf`, `.txt`) y URLs externas para extraer reglas de negocio, glosario de interfaz y precondiciones implícitas.
  - **Subagente Inspector Visual (`inspector_visual_opencv`)**: Analiza capturas de pantalla extraídas con OpenCV en marcas de tiempo específicas para desambiguar frases del audio (*"doy clic aquí"*, *"lleno estos datos"*) e identificar etiquetas reales y datos de prueba.
  - **Subagente Analista QA (`analista_qa_estructurador`)**: Cruza la transcripción, el contexto funcional y la inspección visual para construir los casos de prueba paso a paso.
  - **Subagente Crítico de Reflexión (`critico_reflexion_mpa`)**: Aplica el **Patrón de Reflexión** auditando la atomicidad de cada fila (una sola acción por paso), la continuidad lógica del flujo y la separación limpia de la columna `Datos de Prueba`.
- **Procesamiento Local de Audio y Video**:
  - Extracción de audio local mediante **FFmpeg** (WAV mono 16kHz) y transcripción con marcas de tiempo mediante **Faster-Whisper** (`int8` + filtro VAD).
  - Sistema de **caché automático de transcripciones** en `data/outputs/transcripts/` para evitar reprocesar videos en ejecuciones posteriores.
  - Extracción precisa de fotogramas clave (`.png`) por segundo exacto mediante **OpenCV**.
- **Diseño Basado en Agent Skills y Contratos Pydantic**:
  - Conocimiento procedimental desacoplado en `skills/*/SKILL.md` (*Progressive Disclosure*) y estándares globales en `.agents/rules/qa_standards.md`.
  - Validación estricta de la matriz con **Pydantic** antes de exportar la tabla final a Markdown (`.md`).

---

## Arquitectura y Flujo de Trabajo

```text
[Usuario] (Video + Documentación/URLs + Instrucciones)
   │
   ▼
┌──────────────────────────────────────────────────────────────────────┐
│ 1. Agente Orquestador (INTERACTIVE)                                  │
│    Coordina la conversación con el usuario, herramientas y agentes   │
└──┬──────────────────┬────────────────────┬────────────────────────┬──┘
   │                  │                    │                        │
   ▼ (Subagente 1)    ▼ (Tools Python)     ▼ (Subagente 2)          ▼ (Tool Python)
┌────────────────┐ ┌────────────────────┐ ┌──────────────────────┐ ┌───────────────────┐
│ investigador_  │ │ 1. transcribe_     │ │ analista_qa_         │ │ exportar_matriz_  │
│ contexto       │ │    video_local()   │ │ estructurador        │ │ markdown()        │
│ - Lee URLs     │ │  (ffmpeg + whisper)│ │                      │ │ - Valida Pydantic │
│ - Lee PDFs/MDs │ │ 2. extract_        │ │  ├─► inspector_visual│ │ - Genera tabla    │
│ - Extrae reglas│ │    keyframes_      │ │  │   _opencv (PNGs)  │ │   final en .md    │
│   de negocio   │ │    opencv()        │ │  └─► critico_        │ └───────────────────┘
└────────────────┘ └────────────────────┘ │      reflexion_mpa   │
                                          └──────────────────────┘
```

---

## Estructura del Proyecto

```text
mpa_video_agents/
├── .agents/
│   └── rules/
│       └── qa_standards.md               # Reglas globales inmutables del estándar QA
├── skills/                               # Catálogo de Agent Skills cargado vía skills_paths
│   ├── context-synthesis/
│   │   └── SKILL.md                      # Síntesis de documentación y URLs
│   ├── mpa-drafting/
│   │   ├── SKILL.md                      # Metodología de redacción de pasos y datos de prueba
│   │   └── examples/
│   │       └── mpa_gold_standard.md      # Ejemplo Few-Shot de referencia
│   ├── visual-disambiguation/
│   │   └── SKILL.md                      # Cruce de timestamps de audio con frames de OpenCV
│   └── mpa-reflection/
│       └── SKILL.md                      # Checklist del Patrón de Reflexión (atomicidad y huecos)
├── src/
│   ├── config/
│   │   └── settings.py                   # Configuración centralizada de rutas y modelo Whisper
│   ├── schemas/
│   │   └── mpa_schema.py                 # Esquemas Pydantic de la Matriz de Pruebas de Aceptación
│   ├── tools/
│   │   ├── audio_reader.py               # Transcripción local FFmpeg + Faster-Whisper con caché
│   │   ├── video_frame_reader.py         # Extracción de fotogramas PNG con OpenCV
│   │   ├── context_reader.py             # Lector e inventario de archivos en data/inputs/
│   │   └── md_exporter.py                # Exportador validado a Markdown (.md)
│   └── agents/
│       ├── subagents.py                  # Definición de los 4 subagentes especializados
│       └── orchestrator.py               # Configuración del Agente Orquestador
├── data/
│   ├── inputs/
│   │   ├── videos/                       # Videos de entrada (.mp4, .mkv, .mov, .avi)
│   │   └── context_docs/                 # Documentos funcionales, historias de usuario, PDFs
│   └── outputs/
│       ├── transcripts/                  # Transcripciones .txt con marcas de tiempo (caché)
│       ├── frames/                       # Capturas .png extraídas por OpenCV por video
│       └── matrices/                     # Matrices finales generadas en formato .md
├── main.py                               # Punto de entrada interactivo por consola
└── requirements.txt                      # Dependencias de Python
```

---

## Requisitos Previos

1. **Python 3.10+**
2. **FFmpeg** instalado en el sistema y disponible en la variable de entorno `PATH`:
   - Windows (Winget): `winget install Gyan.FFmpeg`
   - Linux (Ubuntu/Debian): `sudo apt install ffmpeg`
   - macOS (Homebrew): `brew install ffmpeg`
3. **API Key de Gemini** configurada en la variable de entorno `GEMINI_API_KEY`.

---

## Instalación y Configuración

1. Clonar el repositorio y acceder al directorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd mpa_video_agents
   ```

2. Crear un entorno virtual e instalar las dependencias:
   ```bash
   python -m venv .venv
   # En Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # En Linux/macOS:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. Configurar la variable de entorno `GEMINI_API_KEY`:
   ```powershell
   # En Windows (PowerShell)
   $env:GEMINI_API_KEY="tu_api_key_aqui"
   ```
   ```bash
   # En Linux / macOS
   export GEMINI_API_KEY="tu_api_key_aqui"
   ```

---

## Uso

1. Coloca tus archivos de video en `data/inputs/videos/` y cualquier documento de contexto adicional en `data/inputs/context_docs/`.
2. Inicia la consola interactiva del Agente Orquestador:
   ```bash
   python main.py
   ```
3. Ejemplo de instrucción para el Orquestador:
   > *"Revisa los videos y documentos disponibles en la carpeta de entradas, consulta además la documentación en https://ejemplo.com/reglas-facturacion y genera la Matriz de Pruebas de Aceptación usando el prefijo MPA-FAC-001."*

---

## Estructura de Salida de la Matriz (`.md`)

Las matrices generadas se almacenan en `data/outputs/matrices/` con las siguientes 6 columnas estandarizadas:

| ID del Caso | Condiciones Previas | N° Paso | Paso a Seguir (Automatizador) | Datos de Prueba | Resultado Esperado |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **MPA-FAC-001**<br>*(Emisión exitosa de factura nacional)* | • Usuario autenticado con rol `Contabilidad_Emisor`<br>• Cliente registrado con RFC activo | 1 | Desplegar el menú lateral izquierdo y hacer clic en la opción "Facturación". | `N/A` | Se carga el panel principal de facturación mostrando el historial y el botón "Nueva Factura". |
| `MPA-FAC-001` | *(Ver paso 1)* | 2 | Ingresar el nombre del cliente en el campo "Cliente Receptor" y seleccionar la coincidencia. | `Cliente: "Acme Corp S.A. de C.V." \| RFC: "ACO1405209A1"` | El sistema autocompleta automáticamente la Razón Social, el Régimen Fiscal y el Código Postal. |