"""Punto de entrada principal del Framework Multiagente MPA."""

import asyncio
import os
from google.antigravity import Agent
from src.agents.orchestrator import build_orchestrator_config
from src.config.settings import (
    INPUT_CONTEXT_DOCS_DIR,
    INPUT_VIDEOS_DIR,
    OUTPUT_FRAMES_DIR,
    OUTPUT_MATRICES_DIR,
    OUTPUT_TRANSCRIPTS_DIR,
    SKILLS_DIR,
    ensure_directories,
)


async def main() -> None:
    ensure_directories()

    print("=" * 78)
    print("  MPA MULTI-AGENT FRAMEWORK (Skills + Modular Readers + Markdown Exporter)")
    print("=" * 78)
    print(f"  • Skills cargadas desde : {SKILLS_DIR}")
    print(f"  • Entrada de Videos     : {INPUT_VIDEOS_DIR}")
    print(f"  • Entrada de Contexto   : {INPUT_CONTEXT_DOCS_DIR}")
    print(f"  • Salida Transcripciones: {OUTPUT_TRANSCRIPTS_DIR}")
    print(f"  • Salida Frames OpenCV  : {OUTPUT_FRAMES_DIR}")
    print(f"  • Salida Matrices (.md) : {OUTPUT_MATRICES_DIR}")
    print("-" * 78)

    if not os.environ.get("GEMINI_API_KEY"):
        print(
            "[AVISO] Variable GEMINI_API_KEY no detectada en el entorno.\n"
            "Consigue tu llave en: https://aistudio.google.com/app/api-keys\n"
            "En PowerShell ejecuta: $env:GEMINI_API_KEY='tu_api_key'\n"
        )

    config = build_orchestrator_config()

    async with Agent(config=config) as orchestrator:
        print("Orquestador iniciado. Escribe 'salir' para terminar.\n")
        while True:
            try:
                user_input = input("\nUsuario > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nSesión finalizada.")
                break

            if not user_input:
                continue
            if user_input.lower() in {"salir", "exit", "quit"}:
                print("Cerrando el framework MPA...")
                break

            print("\nOrquestador > ", end="", flush=True)
            response = await orchestrator.chat(user_input)
            async for chunk in response:
                print(chunk, end="", flush=True)
            print()


if __name__ == "__main__":
    asyncio.run(main())
