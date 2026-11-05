"""Módulo de lectura de audio y transcripción local (FFmpeg + Faster-Whisper) con caché en disco."""

import os
from pathlib import Path
import subprocess
import tempfile
from faster_whisper import WhisperModel
from src.config.settings import (
    DEFAULT_LANGUAGE,
    DEFAULT_WHISPER_COMPUTE_TYPE,
    DEFAULT_WHISPER_MODEL,
    OUTPUT_TRANSCRIPTS_DIR,
    ensure_directories,
)


def transcribe_video_local(
    video_path: str,
    model_size: str = DEFAULT_WHISPER_MODEL,
    language: str = DEFAULT_LANGUAGE,
    use_cache: bool = True,
) -> str:
    """Extrae el audio de un video localmente con ffmpeg y lo transcribe a texto con timestamps usando faster-whisper.

    Guarda automáticamente la transcripción en `data/outputs/transcripts/<video_stem>.txt`
    para reutilizarla en futuras ejecuciones sin reprocesar el video.

    Args:
        video_path: Ruta del archivo de video (ej. 'data/inputs/videos/sesion_01.mp4').
        model_size: Tamaño del modelo Whisper ('tiny', 'base', 'small', 'medium', 'large-v3-turbo').
        language: Código ISO del idioma ('es' por defecto).
        use_cache: Si es True y ya existe una transcripción previa en `data/outputs/transcripts/`, la devuelve de inmediato.

    Returns:
        Transcripción completa con marcas de tiempo `[inicio_seg - fin_seg]` y ruta del archivo guardado.
    """
    ensure_directories()
    resolved_video = Path(video_path).resolve()

    if not resolved_video.exists():
        return f"Error: El archivo de video no existe en la ruta '{resolved_video}'."

    transcript_file = OUTPUT_TRANSCRIPTS_DIR / f"{resolved_video.stem}_transcript.txt"

    if use_cache and transcript_file.exists():
        cached_text = transcript_file.read_text(encoding="utf-8")
        return f"[CACHÉ CARGADO DESDE: {transcript_file}]\n{cached_text}"

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
        temp_wav_path = tmp_audio.name

    try:
        # 1. Extraer audio a WAV mono 16kHz usando ffmpeg local
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(resolved_video),
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            temp_wav_path,
        ]
        subprocess.run(
            ffmpeg_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # 2. Transcribir localmente con faster-whisper
        model = WhisperModel(
            model_size,
            device="cpu",
            compute_type=DEFAULT_WHISPER_COMPUTE_TYPE,
        )
        segments, info = model.transcribe(
            temp_wav_path,
            language=language,
            beam_size=5,
            vad_filter=True,
        )

        lines = [
            f"--- Transcripción de '{resolved_video.name}' (Idioma: {info.language}, Duración: {info.duration:.1f}s) ---"
        ]
        for seg in segments:
            lines.append(f"[{seg.start:06.2f}s - {seg.end:06.2f}s] {seg.text.strip()}")

        full_transcript = "\n".join(lines)
        transcript_file.write_text(full_transcript, encoding="utf-8")

        return f"[TRANSCRIPCIÓN GUARDADA EN: {transcript_file}]\n{full_transcript}"

    except FileNotFoundError:
        return (
            "Error: No se encontró el binario 'ffmpeg' en el PATH del sistema. "
            "Verifica que ffmpeg esté instalado y accesible en la terminal."
        )
    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.decode("utf-8", errors="replace")
        return f"Error al extraer el audio con ffmpeg: {err_msg}"
    except Exception as e:
        return f"Error durante la transcripción con faster-whisper: {str(e)}"
    finally:
        if os.path.exists(temp_wav_path):
            try:
                os.remove(temp_wav_path)
            except OSError:
                pass
