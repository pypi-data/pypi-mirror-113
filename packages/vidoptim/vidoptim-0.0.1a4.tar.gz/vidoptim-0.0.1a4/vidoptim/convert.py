from typing import Any

import ffmpeg

from vidoptim.probe import media_probe
from vidoptim.progress import show_progress


def export_as_h264() -> None:
    return None


def get_output_filename(infile: str) -> str:
    pass


def video_convert(infile: str) -> Any:
    video_file = ffmpeg.input(infile)

    probe_info = media_probe(infile)

    output_audio = video_file.audio

    # .filter("aecho", 0.8, 0.9, 1000, 0.3)

    output_video = video_file.video

    # .hflip()

    # output_video.

    video_out = ffmpeg.output(output_audio, output_video, "out.mp4", vcodec="hevc")

    with show_progress(100) as socket_filename:

        video_out = video_out.global_args(
            "-progress", "unix://{}".format(socket_filename)
        ).overwrite_output()

        video_out.run(capture_stdout=True, capture_stderr=True)

    return video_out
