import moviepy as m


def converting_video(filename: str) -> None:
    clip = m.VideoClip(filename)
    new_filename = filename + "mp4"
    clip.write_videofile()
    print("Converting")
