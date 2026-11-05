"""Módulo de lectura visual de video y extracción de fotogramas por timestamp con OpenCV."""

from pathlib import Path
import cv2
from src.config.settings import OUTPUT_FRAMES_DIR, ensure_directories


def extract_keyframes_opencv(
    video_path: str,
    timestamps_seconds: list[float],
) -> str:
    """Extrae capturas de pantalla (frames PNG) de un video en segundos específicos usando OpenCV.

    Guarda los fotogramas organizados en `data/outputs/frames/<nombre_video>/`.

    Args:
        video_path: Ruta del archivo de video.
        timestamps_seconds: Lista de segundos exactos donde se requiere inspeccionar la pantalla (ej. [12.5, 18.0]).

    Returns:
        Resumen con las rutas absolutas de las imágenes PNG generadas en `data/outputs/frames/`.
    """
    ensure_directories()
    resolved_video = Path(video_path).resolve()

    if not resolved_video.exists():
        return f"Error: No se encontró el archivo de video en '{resolved_video}'."

    video_frames_dir = OUTPUT_FRAMES_DIR / resolved_video.stem
    video_frames_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(resolved_video))
    if not cap.isOpened():
        return f"Error: OpenCV no pudo abrir el archivo de video '{resolved_video}'."

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0.0

    saved_files = []
    for ts in timestamps_seconds:
        if ts < 0 or (duration > 0 and ts > duration):
            saved_files.append(
                f"- [{ts:.2f}s]: Fuera de rango (duración del video: {duration:.2f}s)"
            )
            continue

        cap.set(cv2.CAP_PROP_POS_MSEC, ts * 1000.0)
        success, frame = cap.read()
        if success:
            frame_filename = f"frame_{ts:07.2f}s.png".replace(".", "_", 1)
            frame_path = (video_frames_dir / frame_filename).resolve()
            cv2.imwrite(str(frame_path), frame)
            saved_files.append(f"- [{ts:.2f}s]: {frame_path}")
        else:
            saved_files.append(f"- [{ts:.2f}s]: No se pudo decodificar el fotograma.")

    cap.release()
    return (
        f"Fotogramas extraídos en '{video_frames_dir}':\n" + "\n".join(saved_files)
    )
