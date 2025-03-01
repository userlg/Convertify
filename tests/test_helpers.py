from src.helpers import methods as m

import os

import shutil

import tempfile

import pytest


def test_verify_video_is_occupied_works_properly() -> None:

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name

    with open(temp_file_path, "r") as f:
        # Verificar que la función detecta que el archivo está ocupado
        assert m.verify_video_is_occupied(temp_file_path) == True

    os.remove(temp_file_path)


def test_verify_video_is_occupied_when_file_is_occupied() -> None:

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name

        # Verificar que el archivo no está ocupado inicialmente
        assert not m.verify_video_is_occupied(temp_file_path) == False

    os.remove(temp_file_path)


def test_verify_avi_format_when_is_true() -> None:
    """Verifica que la función verify_avi_format retorne True para un archivo .avi."""
    assert m.verify_avi_format("fake_file.avi") == True


def test_verify_avi_format_when_is_false() -> None:
    """Verifica que la función verify_avi_format retorne False para un archivo que no es .avi."""
    assert m.verify_avi_format("fake_file.mp4") == False


def test_generate_new_name_works_properly() -> None:
    """Verifica que la función generate_new_name cambie correctamente la extensión a .mp4."""
    assert m.generate_new_name("fake_name.avi") == "fake_name.mp4"


def test_converting_videos_to_mp4_when_video_no_exists() -> None:
    """Verifica que la función convert_all_videos retorne False cuando no hay archivos .avi."""
    test_directory = "temp"

    os.makedirs(test_directory, exist_ok=True)

    assert m.convert_all_videos(test_directory, []) == False

    os.rmdir(test_directory)


def test_converting_videos_to_mp4_when_video_works_properly() -> None:
    """Verifica que la función convert_all_videos retorne True cuando hay archivos .avi."""
    test_directory = "temp"
    os.makedirs(test_directory, exist_ok=True)

    shutil.copy("video_test/fake_video.avi", test_directory)

    assert m.convert_all_videos(test_directory, ["fake_video.avi"]) == True

    os.remove(os.path.join(test_directory, "fake_video.mp4"))

    os.rmdir(test_directory)


def test_converting_video_to_mp4_works_properly() -> None:
    """Verifica que la función converting_video_to_mp4 retorne True cuando la conversión es exitosa."""
    test_directory = "temp"
    os.makedirs(test_directory, exist_ok=True)

    shutil.copy("video_test/fake_video.avi", test_directory)

    assert (
        m.converting_video_to_mp4(os.path.join(test_directory, "fake_video.avi"))
        == True
    )

    os.remove(os.path.join(test_directory, "fake_video.mp4"))
    os.rmdir(test_directory)


@pytest.mark.filterwarnings("error")
def test_converting_video_to_mp4_generating_exception() -> None:
    """Verifica que la función converting_video_to_mp4 retorne una excepcion"""

    test_directory = "temp"

    os.makedirs(test_directory, exist_ok=True)

    file = open(os.path.join(test_directory, "fake_video.avi"), "w+")

    file.close()

    assert (
        m.converting_video_to_mp4(os.path.join(test_directory, "fake_video.avi"))
        == False
    )

    os.remove(os.path.join(test_directory, "fake_video.avi"))
    os.rmdir(test_directory)


def test_converting_video_to_mp4_when_is_not_avi() -> None:
    """Verifica que la función converting_video_to_mp4 retorne False cuando el archivo no es .avi."""

    test_directory = "temp"

    os.makedirs(test_directory, exist_ok=True)

    shutil.copy("video_test/fake_video.mp4", test_directory)

    assert (
        m.converting_video_to_mp4(os.path.join(test_directory, "fake_video.mp4"))
        == False
    )

    os.remove(os.path.join(test_directory, "fake_video.mp4"))

    os.rmdir(test_directory)


def test_exploring_directories_when_no_folders() -> None:
    """Verifica que la función explore_directories retorne False cuando no hay subdirectorios."""

    test_directory = "temp"

    os.makedirs(test_directory, exist_ok=True)

    assert m.explore_directories(test_directory) == False

    os.rmdir(test_directory)


def test_exploring_directories_works_properly() -> None:
    """Verifica que la función explore_directories retorne True cuando encuentra archivos .avi."""

    test_directory = "temp/vids"

    os.makedirs(test_directory, exist_ok=True)

    shutil.copy("video_test/fake_video.avi", test_directory)

    assert m.explore_directories("temp") == True

    os.remove(os.path.join(test_directory, "fake_video.mp4"))

    shutil.rmtree("temp")
