from moviepy import VideoFileClip

import os


def generate_new_name(filename: str) -> str:

    return filename[filename.index(filename[0]) : filename.index(".")] + ".mp4"


def verify_avi_format(filename: str) -> bool:

    return filename.endswith(".avi")


def exploring_directories(location: str) -> bool:

    directories = os.listdir(location)

    flag = False

    new_directories = []

    for directory in directories:
        if not directory.startswith("."):

            new_name = location + "/" + directory

            if os.path.isdir(new_name):

                new_directories.append(directory)

                exploring_directories(new_name)

            if directory.endswith(".avi") and not flag:
                convert_all_videos(location)
                flag = True

    return True


def convert_all_videos(location: str) -> True:

    files = os.listdir(location)

    print(location)

    videos = []

    for file in files:
        if file.endswith(".avi"):
            videos.append(file)

    for video in videos:
        converting_video_to_mp4(location + "/" + video)

    return True


def converting_video_to_mp4(file: str) -> bool:

    if verify_avi_format(file):

        clip = VideoFileClip(file)

        new_filename = generate_new_name(file)

        clip.write_videofile(new_filename)

        clip.close()

        os.remove(file)

        return True
    else:
        return False
