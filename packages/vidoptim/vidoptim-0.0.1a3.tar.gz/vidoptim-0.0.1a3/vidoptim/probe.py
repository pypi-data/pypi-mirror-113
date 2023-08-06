from typing import Any, Dict

import ffmpeg


def video_info(file_source: str) -> Dict[str, Any]:
    """Get info for video file format and return video metadata"""
    probe = ffmpeg.probe(file_source)
    video_info = next(s for s in probe["streams"] if s["codec_type"] == "video")
    width = int(video_info["width"])
    height = int(video_info["height"])
    num_frames = int(video_info["nb_frames"])

    from pprint import pprint

    pprint(video_info)

    return {
        "width": width,
        "height": height,
        "num_frames": num_frames,
    }
