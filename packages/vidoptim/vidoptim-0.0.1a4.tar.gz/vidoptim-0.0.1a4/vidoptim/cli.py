"""
vidoptim

(c) 2021 - Nik Cubrilovic
"""
import typer

from vidoptim.convert import video_convert
from vidoptim.probe import media_probe


def main(infile: str) -> None:
    typer.echo(f"Reading file {infile}")
    mediainfo = media_probe(infile)

    for s in mediainfo.streams:
        typer.echo(
            "{} => {} ({}) {}w x {}h at  {}fps".format(
                s.codec_type,
                s.codec_name,
                s.pix_fmt,
                s.width,
                s.height,
                s.frame_rate,
            )
        )

    video_convert(infile)


def cli() -> None:
    typer.run(main)


if __name__ == "__main__":
    cli()
