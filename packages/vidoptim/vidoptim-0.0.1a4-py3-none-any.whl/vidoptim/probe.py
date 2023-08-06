import logging

import ffmpeg
from pydantic import ValidationError

from vidoptim.schemas.probe import MediaFile

logger = logging.getLogger("vidoptim")


def media_probe(file_source: str) -> MediaFile:
    """Get info for video file format and return video metadata"""
    probe = ffmpeg.probe(file_source)

    # video_info = next(s for s in probe["streams"] if s["codec_type"] == "video")

    probe_object = None

    try:
        probe_object = MediaFile(**probe)

    except ValidationError as e:
        logger.error("Could not validate probe info: {}".format(e))
        raise

    return probe_object
