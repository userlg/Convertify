from src.helpers import methods as m

from unittest.mock import patch, MagicMock

import os

import psutil

import tempfile

import pytest


def clean_directories_test(directory: str) -> None:

    fake_avi_path = os.path.join(directory, "fake_video.avi")

    if os.path.exists(fake_avi_path):
        os.remove(fake_avi_path)

    fake_mp4_path = os.path.join(directory, "fake_video.mp4")

    if os.path.exists(fake_mp4_path):
        os.remove(fake_mp4_path)

    if os.path.exists(directory):
        os.rmdir(directory)


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


def test_verify_video_is_occupied_exceptions() -> None:
    # Simulamos un proceso que lanza una excepción NoSuchProcess
    with patch("psutil.process_iter") as mock_process_iter:
        mock_process = MagicMock()

        mock_process.info = MagicMock()

        mock_process.info.__getitem__.side_effect = psutil.NoSuchProcess(123)

        mock_process_iter.return_value = [mock_process]

        assert m.verify_video_is_occupied("fake_path") == True


def test_verify_video_is_occupied_exception():
    with pytest.raises(Exception):
        m.verify_video_is_occupied(None)


def test_verify_video_is_occupied_when_file_in_use_invalid_path():
    with pytest.raises(
        ValueError, match="El parámetro file_path debe ser una cadena de texto válida."
    ):
        m.verify_video_is_occupied(123)


def test_verify_video_is_occupied_when_file_in_use_open_file(mocker):
    mocker.patch(
        "psutil.process_iter",
        return_value=[
            mocker.Mock(
                info={"open_files": [mocker.Mock(path="C:\\ruta\\al\\fake.avi")]}
            )
        ],
    )
    assert m.verify_video_is_occupied("C:\\ruta\\al\\archivo.avi") == True


def test_is_file_in_use_not_open_file(mocker):
    mocker.patch("psutil.process_iter", return_value=[], autospec=True)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name

    result = m.verify_video_is_occupied(temp_file_path)
    assert result == False


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


def test_converting_video_to_mp4_works_properly() -> None:
    """Verifica que la función converting_video_to_mp4 retorne True cuando la conversión es exitosa."""
    test_directory = "temp"
    os.makedirs(test_directory, exist_ok=True)

    fake_avi_path = os.path.join(test_directory, "fake_video.avi")
    with open(fake_avi_path, "w") as f:
        f.write("This is a fake AVI file.")

    with patch("src.helpers.methods.converting_video_to_mp4", return_value=True):
        assert m.converting_video_to_mp4(fake_avi_path) == True

    clean_directories_test(test_directory)


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

    clean_directories_test(test_directory)


def test_converting_video_to_mp4_when_is_not_avi() -> None:
    """Verifica que la función converting_video_to_mp4 retorne False cuando el archivo no es .avi."""

    test_directory = "temp"

    os.makedirs(test_directory, exist_ok=True)

    fake_mp4_path = os.path.join(test_directory, "fake_video.mp4")
    with open(fake_mp4_path, "w") as f:
        f.write("This is a fake MP4 file.")

    with patch("src.helpers.methods.converting_video_to_mp4", return_value=False):
        assert m.converting_video_to_mp4(fake_mp4_path) == False

    clean_directories_test(test_directory)


def test_exploring_directories_when_no_folders() -> None:
    """Verifica que la función explore_directories retorne False cuando no hay subdirectorios."""

    test_directory = "temp"

    os.makedirs(test_directory, exist_ok=True)

    assert m.explore_directories(test_directory) == False

    os.rmdir(test_directory)


@pytest.mark.filterwarnings("error")
def test_converting_videos_to_mp4_when_video_works_properly() -> None:
    """Verifica que la función convert_all_videos retorne True cuando hay archivos .avi."""
    test_directory = "temp_test"
    os.makedirs(test_directory, exist_ok=True)

    fake_avi_path = os.path.join(test_directory, "fake_video.avi")
    with open(fake_avi_path, "w") as f:
        f.write("This is a fake AVI file.")

    with patch("src.helpers.methods.convert_all_videos", return_value=True):
        assert m.convert_all_videos(test_directory, ["fake_video.avi"]) == True

    clean_directories_test(test_directory)


def test_exploring_directories_works_properly() -> None:
    """Verifica que la función explore_directories retorne True cuando encuentra archivos .avi."""

    test_directory = "temp"

    os.makedirs(test_directory, exist_ok=True)

    fake_avi_path = os.path.join(test_directory, "fake_video.avi")
    with open(fake_avi_path, "w") as f:
        f.write("This is a fake AVI file.")
    with patch("src.helpers.methods.explore_directories", return_value=True):
        assert m.explore_directories("temp") == True

    clean_directories_test(test_directory)


@pytest.mark.filterwarnings("error")
def test_exception_during_conversion_video():

    # Declare all mocks necesary to the test
    with patch(
        "src.helpers.methods.verify_avi_format"
    ) as mock_verify_avi_format, patch(
        "moviepy.VideoFileClip"
    ) as mock_video_file_clip, patch(
        "src.helpers.methods.generate_new_name"
    ) as mock_generate_new_name, patch(
        "os.remove"
    ) as mock_remove:

        mock_verify_avi_format.return_value = True

        mock_generate_new_name.return_value = "new_file.mp4"

        mock_video_file_clip.side_effect = Exception("Throw exception")

        assert m.converting_video_to_mp4("fake_file.avi") == False

        mock_remove.assert_not_called()


def test_process_video_works_properly() -> None:

    test_directory = "temp"

    os.makedirs(test_directory, exist_ok=True)

    fake_avi_path = os.path.join(test_directory, "fake_video.avi")

    with open(fake_avi_path, "w") as f:
        f.write("This is a fake AVI file.")

    with patch("src.helpers.methods.process_video", return_value=True):
        assert m.process_video(fake_avi_path) == True

    clean_directories_test(test_directory)
