from src.helpers import methods as m

import os

import shutil


def test_verify_avi_format_when_is_true() -> None:

    assert m.verify_avi_format("fake_file.avi") == True


def test_verify_avi_format_when_is_false() -> None:

    assert m.verify_avi_format("fake_file.mp4") == False


def test_generate_new_name_works_properly() -> None:

    assert m.generate_new_name("fake_name.avi") == "fake_name.mp4"


def test_converting_videos_to_mp4_when_video_no_exists() -> None:

    test_directory = "temp"

    os.makedirs(test_directory)

    assert m.convert_all_videos(test_directory) == False

    os.rmdir(test_directory)


def test_converting_videos_to_mp4_when_video_works_properly() -> None:

    test_directory = "temp"

    os.makedirs(test_directory)

    shutil.copy("video_test/fake_video.avi", test_directory)

    assert m.convert_all_videos(test_directory) == True

    os.remove(test_directory + "/fake_video.mp4")

    os.rmdir(test_directory)


def test_converting_video_to_mp4_works_properly() -> None:

    test_directory = "temp"

    os.makedirs(test_directory)

    shutil.copy("video_test/fake_video.avi", test_directory)

    assert m.converting_video_to_mp4(test_directory + "/fake_video.avi") == True


def test_converting_video_to_mp4_when_is_not_avi() -> None:

    test_directory = "temp"

    assert m.converting_video_to_mp4(test_directory + "/fake_video.mp4") == False

    os.remove(test_directory + "/fake_video.mp4")

    os.rmdir(test_directory)

def test_exploring_directories_when_no_folders() -> None:

    test_directory = "temp"

    os.makedirs(test_directory)

    assert m.exploring_directories(os.getcwd() + '/' + test_directory) == False

    os.rmdir(test_directory)

def test_exploring_directories_works_properly() -> None:

    test_directory = "temp/vids"

    os.makedirs(test_directory)

    shutil.copy("video_test/fake_video.avi", test_directory)

    assert m.exploring_directories('temp') == True

    os.remove(test_directory + "/fake_video.mp4")

    shutil.rmtree('temp')
