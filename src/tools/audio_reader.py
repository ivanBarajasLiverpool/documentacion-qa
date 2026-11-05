"""Módulo de lectura de audio y transcripción local (FFmpeg/PyAV + Faster-Whisper) con caché en disco."""

import itertools
import os
from pathlib import Path
import subprocess
import tempfile
import av
from faster_whisper import WhisperModel
import numpy as np
from src.config.settings import (
    DEFAULT_LANGUAGE,
    DEFAULT_WHISPER_COMPUTE_TYPE,
    DEFAULT_WHISPER_MODEL,
    OUTPUT_TRANSCRIPTS_DIR,
    ensure_directories,
)


def _decode_audio_pyav(file_path: str, sampling_rate: int = 16000) -> np.ndarray:
    """Decodifica el flujo de audio de un video a un arreglo float32 mono a 16kHz usando PyAV."""
    resampler = av.audio.resampler.AudioResampler(
        format="s16",
        layout="mono",
        rate=sampling_rate,
    )
    frames_list: list[np.ndarray] = []
    with av.open(file_path, mode="r") as container:
        if not container.streams.audio:
            raise ValueError("El archivo de video no contiene pistas de audio.")
        audio_stream = container.streams.audio[0]
        for frame in container.decode(audio_stream):
            for resampled_frame in resampler.resample(frame):
                frames_list.append(resampled_frame.to_ndarray())
        for resampled_frame in resampler.resample(None):
            frames_list.append(resampled_frame.to_ndarray())

    if not frames_list:
        return np.zeros(0, dtype=np.float32)

    pcm_data = np.concatenate(frames_list, axis=1).reshape(-1)
    return pcm_data.astype(np.float32) / 32768.0


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
        # 1. Decodificar audio a memoria a 16kHz mono (compatible con cualquier versión de PyAV y sin requerir ffmpeg.exe externo)
        audio_input = _decode_audio_pyav(str(resolved_video), sampling_rate=16000)

        # 2. Transcribir localmente con faster-whisper
        model = WhisperModel(
            model_size,
            device="cpu",
            compute_type=DEFAULT_WHISPER_COMPUTE_TYPE,
        )
        segments, info = model.transcribe(
            audio_input,
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
