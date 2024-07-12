import io
import os
import sys
import typing as tp
from pathlib import Path


def tail(filename: Path, lines_amount: int = 10, output: tp.IO[bytes] | None = None) -> None:
    """
    :param filename: file to read lines from (the file can be very large)
    :param lines_amount: number of lines to read
    :param output: stream to write requested amount of last lines from file
                   (if nothing specified stdout will be used)
    """
    len = os.path.getsize(filename)
    f = open(filename, 'rb')
    chunk_size = 128
    chunk = bytearray(chunk_size)
    count_line = 0
    count_steps = 0
    index = 0
    while count_line <= lines_amount:
        count_steps += 1
        if chunk_size * count_steps <= len:
            f.seek(-chunk_size * count_steps, io.SEEK_END)
            f.readinto(chunk)
            count_line += chunk.count(b'\n')
            index += chunk_size
        else:
            f.seek(0, io.SEEK_SET)
            chunk = bytearray(len - chunk_size * count_steps + chunk_size)
            f.readinto(chunk)
            count_line += chunk.count(b'\n')
            index += len - chunk_size * count_steps + chunk_size
            chunk_size = len - chunk_size * count_steps + chunk_size
            break
    dif = count_line - lines_amount
    left = -2
    right = chunk_size+1
    while left < right - 1:
        mid = (left + right) // 2
        if chunk[0:mid + 1].count(b'\n') < dif:
            left = mid
        else:
            right = mid
    index = index - right-1
    f.seek(-index, io.SEEK_END)
    if output is None:
        sys.stdout.buffer.write(f.read())
    else:
        output.write(f.read())
    f.close()
