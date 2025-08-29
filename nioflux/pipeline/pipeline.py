import asyncio
from typing_extensions import Any

from nioflux.pipeline.stage import PipelineStage


class Pipeline:
    def __init__(self, queue: list[PipelineStage], data: Any, extra: Any,
                 io_ctx: tuple[asyncio.StreamReader, asyncio.StreamWriter] | None, eof: bytes):
        self._queue = queue.copy()
        self._io_ctx = io_ctx
        self._data = data
        self._extra = extra
        self._fire = True
        self._err = []
        self._eof = eof

    async def __call__(self) -> tuple[Any, Any, list[Exception]]:
        if not isinstance(self._queue, list):
            return self._data, self._extra, self._err
        if len(self._queue):
            for stage in self._queue:
                self._data, self._extra, self._err, self._fire = await stage(
                    data=self._data,
                    extra=self._extra,
                    err=self._err,
                    fire=self._fire,
                    io_ctx=self._io_ctx,
                    eof=self._eof
                )
                if not self._fire:
                    break
        return self._data, self._extra, self._err
