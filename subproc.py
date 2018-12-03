import asyncio.subprocess
import sys
import os
import asyncio
from subprocess import Popen, PIPE


async def connect_read_pipe(file):
    loop = asyncio.get_event_loop()
    stream_reader = asyncio.StreamReader(loop=loop)

    def factory():
        return asyncio.StreamReaderProtocol(stream_reader)
    transport, _ = await loop.connect_read_pipe(factory, file)
    return stream_reader, transport

async def read_last_ln(file):
    reader, _ = await connect_read_pipe(file)
    item = await reader.readline()
    print(item)
    return item


async def start_sub(loop):
    path = os.path.abspath("logic.py")
    p = Popen([sys.executable, path],
              stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return p



