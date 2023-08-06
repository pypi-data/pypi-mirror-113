# Copyright (C) 2020-2021 by Vd.
# This file is part of subwork, the simple way to work with with subprocesses.
# subwork is released under the MIT License (see LICENSE).


import sys
from select import select
from typing import Any

try:
    import ujson as json
except ImportError:
    import json


class Terminate(Exception):
    pass


class ExitCode(int):
    pass


class DecodeError(Exception):
    def __init__(self, original: str, exception: Exception):
        self._orig = original
        self._exc = exception

    @property
    def exception(self) -> Exception:
        return self._exc

    @property
    def original(self) -> str:
        return self._orig


def _process(inp: str) -> Any:
    try:
        return json.loads(inp)
    except Exception as e:
        raise DecodeError(inp, e) from None


def read(timeout: int = -1) -> Any:
    if timeout <= 0:
        return _process(sys.stdin.readline())

    rfds, _, _ = select([sys.stdin], [], [], timeout)

    if not len(rfds):
        return None

    return _process(sys.stdin.readline())


def write(data: Any):
    sys.stdout.write(json.dumps(data, ensure_ascii=False))
    sys.stdout.write('\n')
    sys.stdout.flush()
