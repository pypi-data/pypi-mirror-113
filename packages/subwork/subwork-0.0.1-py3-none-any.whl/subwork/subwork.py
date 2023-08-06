# Copyright (C) 2020-2021 by Vd.
# This file is part of subwork, the simple way to work with with subprocesses.
# subwork is released under the MIT License (see LICENSE).


import sys
from asyncio import TimeoutError
from asyncio import create_subprocess_exec, wait_for
from asyncio.subprocess import PIPE, DEVNULL
from contextlib import suppress
from json import JSONDecodeError
from typing import AsyncGenerator, Any

from .utils import ExitCode, Terminate

try:
    import ujson as json
except ImportError:
    import json


async def subwork(cmd: str,
                  *args: str,
                  data: Any = None,
                  timeout: float = 1,
                  stderr: bool = True,
                  exit_code: bool = False
                  ) -> AsyncGenerator[Any, None]:
    """"""

    at_exit = False

    try:
        sp = await create_subprocess_exec(cmd, *args, stdin=PIPE, stdout=PIPE, stderr=sys.stderr if stderr else DEVNULL)

        async def write_ln(d: Any):
            if d is not None:
                sp.stdin.write(json.dumps(d).encode())
                sp.stdin.write(b'\n')
                await sp.stdin.drain()

        await write_ln(data)

        while True:
            try:
                inp = await wait_for(sp.stdout.readline(), timeout)

                try:
                    inp = json.loads(inp)
                except (JSONDecodeError, ValueError):
                    inp = None

                await write_ln((yield inp))

                if sp.stdout.at_eof():
                    break

            except Terminate:
                break

            except TimeoutError:
                await write_ln((yield None))
                continue

    except GeneratorExit as e:
        at_exit = True
        return

    finally:
        with suppress(Exception):
            if sp.returncode is not None and not at_exit and exit_code:  # noqa
                yield ExitCode(sp.returncode)
                return

        with suppress(Exception):
            sp.terminate()
            with suppress(TimeoutError):
                code = await wait_for(sp.wait(), timeout)
                if not at_exit and exit_code:
                    yield ExitCode(code)

                return

            sp.kill()
            code = await sp.wait()
            if not at_exit and exit_code:
                yield ExitCode(code)
