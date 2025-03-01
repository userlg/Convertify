from moviepy import VideoFileClip

import os

import ctypes

import psutil


def process_video(video_path: str) -> bool:

    if not verify_video_is_occupied(video_path):
        converting_video_to_mp4(video_path)

    return True


def generate_new_name(filename: str) -> str:
    """Genera un nuevo nombre de archivo cambiando la extensión a .mp4."""
    return os.path.splitext(filename)[0] + ".mp4"


def verify_avi_format(filename: str) -> bool:
    """Verifica si un archivo tiene la extensión .avi."""
    return filename.lower().endswith(".avi")


def explore_directories(location: str) -> bool:
    """Explora directorios y convierte archivos .avi a .mp4."""

    for root, dirs, files in os.walk(location):
        # Ignorar directorios ocultos
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        # Filtrar archivos .avi
        avi_files = [f for f in files if verify_avi_format(f)]

        if avi_files:
            convert_all_videos(root, avi_files)

    if len(avi_files) > 0 or len(dirs) > 0:
        return True
    else:
        return False


def convert_all_videos(location: str, videos: list[str]) -> bool:
    """Convierte todos los archivos .avi en una ubicación a .mp4."""

    if len(videos) == 0:
        return False

    for video in videos:
        process_video(os.path.join(location, video))

    return True


def converting_video_to_mp4(file: str) -> bool:
    """Convierte un archivo .avi a .mp4 y elimina el original."""
    if not verify_avi_format(file):
        return False

    try:
        clip = VideoFileClip(file)
        new_filename = generate_new_name(file)
        clip.write_videofile(new_filename)
        clip.close()
        os.remove(file)
        return True
    except Exception as e:
        print(f"Error al convertir {file}: {e}")
        return False


def verify_video_is_occupied(file_path: str) -> bool:

    if not isinstance(file_path, str) or not file_path:
        raise ValueError("El parámetro file_path debe ser una cadena de texto válida.")

    GENERIC_READ = 0x80000000
    FILE_SHARE_READ = (
        0x00000001 | 0x00000002 | 0x00000004
    )  # Combina permisos de lectura, escritura y eliminación
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x80

    # Intentar abrir el archivo con CreateFile de la API de Windows
    handle = ctypes.windll.kernel32.CreateFileW(
        file_path,
        GENERIC_READ,
        FILE_SHARE_READ,
        None,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        None,
    )

    if handle == -1:
        return True  # Archivo en uso

    ctypes.windll.kernel32.CloseHandle(handle)
    file_lower = file_path.lower()

    # Optimizar la iteración de procesos usando generator para mejorar rendimiento
    try:
        for proc in psutil.process_iter(["open_files"]):
            if proc.info["open_files"] and any(
                f.path.lower() == file_lower for f in proc.info["open_files"]
            ):
                return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

    return False
