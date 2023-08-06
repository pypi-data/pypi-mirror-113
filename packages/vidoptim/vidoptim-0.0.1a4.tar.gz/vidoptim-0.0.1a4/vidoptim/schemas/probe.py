from datetime import datetime
from typing import List, Optional

from vidoptim.schemas.core import BaseConfig


class MediaStreamDisposition(BaseConfig):
    attached_pic: int
    clean_effects: int
    comment: int
    default: int
    dub: int
    forced: int
    hearing_impaired: int
    karaoke: int
    lyrics: int
    original: int
    timed_thumbnails: int
    visual_impaired: int


class MediaStreamTags(BaseConfig):
    creation_time: datetime
    encoder: Optional[str]
    handler_name: str
    language: str
    vendor_id: str


class MediaStream(BaseConfig):
    avg_frame_rate: str
    bit_rate: int
    bits_per_raw_sample: Optional[int]
    channel_layout: Optional[str]  # audio
    channels: Optional[int]  # audio
    chroma_location: Optional[str]
    closed_captions: Optional[int]
    codec_long_name: str
    codec_name: str
    codec_tag: str
    codec_tag_string: str
    codec_type: str  # audio, video enum ?
    coded_height: Optional[int]
    coded_width: Optional[int]
    color_primaries: Optional[str]
    color_range: Optional[str]
    color_space: Optional[str]
    color_transfer: Optional[str]
    disposition: MediaStreamDisposition
    duration: float
    duration_ts: int
    has_b_frames: Optional[bool]
    height: Optional[int]
    index: int
    is_avc: Optional[bool]
    level: Optional[int]
    nal_length_size: Optional[int]
    nb_frames: int
    pix_fmt: Optional[str]
    profile: str
    r_frame_rate: str
    refs: Optional[int]
    sample_fmt: Optional[str]  # audio
    sample_rate: Optional[int]  # audio
    start_pts: int
    start_time: float
    tags: MediaStreamTags
    time_base: str
    width: Optional[int]

    @property
    def frame_rate(self) -> int:
        return self.r_frame_rate


class MediaFormatTags(BaseConfig):
    compatible_brands: str
    creation_time: datetime
    major_brand: str
    minor_version: int


class MediaFormat(BaseConfig):
    bit_rate: int
    duration: float
    filename: str
    format_long_name: str
    format_name: str
    nb_programs: int

    # number of streams
    nb_streams: int

    probe_score: int
    size: int
    start_time: float

    tags: MediaFormatTags


class MediaFile(BaseConfig):
    format: MediaFormat
    streams: List[MediaStream]

    @property
    def get_video(self) -> Optional[MediaStream]:
        video_lookup = list(filter(lambda x: x.codec_type == "video", self.streams))

        if len(video_lookup) < 1:
            return None

        return video_lookup.pop()
