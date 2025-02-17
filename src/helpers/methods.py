from moviepy import VideoFileClip
import os


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
            print(f"Location: {root}")
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
        video_path = os.path.join(location, video)
        converting_video_to_mp4(video_path)
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
        #print(f"Error al convertir {file}: {e}")
        return False
