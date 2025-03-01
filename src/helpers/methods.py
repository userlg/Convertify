from moviepy import VideoFileClip

import os

import threading

import psutil


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

    def process_video(video_path: str) -> None:
        if not verify_video_is_occupied(video_path):
            converting_video_to_mp4(video_path)

    threads = []
    for video in videos:
        video_path = os.path.join(location, video)
        thread = threading.Thread(target=process_video, args=(video_path,))
        thread.start()
        threads.append(thread)

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

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

    file_path = file_path.lower()

    # Itera sobre todos los procesos en ejecución
    for process in psutil.process_iter(["pid", "name", "open_files"]):
        try:
            # Obtiene los archivos abiertos por el proceso
            open_files = process.info["open_files"]

            if open_files:
                for file in open_files:
                    if file.path.lower() == file_path:
                        return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Si hay un error con el proceso, se ignora y se continúa con el siguiente
            continue

    return False
