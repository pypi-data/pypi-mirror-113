#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import contextlib
import os
import shutil
import socket
import sys
import tempfile
import textwrap

import ffmpeg
import gevent
import gevent.monkey
from tqdm import tqdm

gevent.monkey.patch_all(thread=False)


@contextlib.contextmanager
def _tmpdir_scope():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


def _do_watch_progress(filename, sock, handler):
    """Function to run in a separate gevent greenlet to read progress
    events from a unix-domain socket."""
    connection, client_address = sock.accept()
    data = b""
    try:
        while True:
            more_data = connection.recv(16)
            if not more_data:
                break
            data += more_data
            lines = data.split(b"\n")
            for line in lines[:-1]:
                line = line.decode()
                parts = line.split("=")
                key = parts[0] if len(parts) > 0 else None
                value = parts[1] if len(parts) > 1 else None
                handler(key, value)
            data = lines[-1]
    finally:
        connection.close()


@contextlib.contextmanager
def _watch_progress(handler):
    """Context manager for creating a unix-domain socket and listen for
    ffmpeg progress events.
    The socket filename is yielded from the context manager and the
    socket is closed when the context manager is exited.
    Args:
        handler: a function to be called when progress events are
            received; receives a ``key`` argument and ``value``
            argument. (The example ``show_progress`` below uses tqdm)
    Yields:
        socket_filename: the name of the socket file.
    """
    with _tmpdir_scope() as tmpdir:
        socket_filename = os.path.join(tmpdir, "sock")
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        with contextlib.closing(sock):
            sock.bind(socket_filename)
            sock.listen(1)
            child = gevent.spawn(_do_watch_progress, socket_filename, sock, handler)
            try:
                yield socket_filename
            except:
                gevent.kill(child)
                raise


@contextlib.contextmanager
def show_progress(total_duration):
    """Create a unix-domain socket to watch progress and render tqdm
    progress bar."""
    with tqdm(total=round(total_duration, 2)) as bar:

        def handler(key, value):
            if key == "out_time_ms":
                time = round(float(value) / 1000000.0, 2)
                bar.update(time - bar.n)
            elif key == "progress" and value == "end":
                bar.update(bar.total - bar.n)

        with _watch_progress(handler) as socket_filename:
            yield socket_filename


# if __name__ == "__main__":
#     args = parser.parse_args()
#     total_duration = float(ffmpeg.probe(args.in_filename)["format"]["duration"])

#     with show_progress(total_duration) as socket_filename:
#         # See https://ffmpeg.org/ffmpeg-filters.html#Examples-44
#         sepia_values = [0.393, 0.769, 0.189, 0, 0.349, 0.686, 0.168, 0, 0.272, 0.534, 0.131]
#         try:
#             (
#                 ffmpeg.input(args.in_filename)
#                 .colorchannelmixer(*sepia_values)
#                 .output(args.out_filename)
#                 .global_args("-progress", "unix://{}".format(socket_filename))
#                 .overwrite_output()
#                 .run(capture_stdout=True, capture_stderr=True)
#             )
#         except ffmpeg.Error as e:
#             print(e.stderr, file=sys.stderr)
#             sys.exit(1)
