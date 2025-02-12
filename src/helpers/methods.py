import moviepy as m


def generate_new_name(filename: str) -> str:

    return filename[filename.index(filename[0]) : filename.index(".")] + ".mp4"


def verify_avi_format(filename: str) -> bool:

    return filename.endswith(".avi")


def converting_video(filename: str) -> bool:
    # clip = m.VideoClip(filename)

    new_filename = generate_new_name(filename)

    # clip.write_videofile(new_filename)

    print(new_filename)

    return True
