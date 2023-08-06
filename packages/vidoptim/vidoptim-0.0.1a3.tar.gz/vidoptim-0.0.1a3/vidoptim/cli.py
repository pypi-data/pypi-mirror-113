"""
vidoptim

(c) 2021 - Nik Cubrilovic
"""
import typer

from vidoptim.probe import video_info


def main(infile: str) -> None:
    typer.echo(f"Reading file {infile}")
    d = video_info(infile)
    typer.echo(d)


def cli() -> None:
    typer.run(main)
