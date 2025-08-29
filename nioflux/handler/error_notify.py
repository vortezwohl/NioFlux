import asyncio
import logging
from typing_extensions import Any
from typing_extensions import override

from nioflux.pipeline.stage import PipelineStage

logger = logging.getLogger('nioflux.server')


class ErrorNotify(PipelineStage):
    def __init__(self, label: str = 'error_notifier'):
        super().__init__(label)

    @override
    async def __call__(self, data: Any, extra: Any, err: list[Exception],
                       fire: bool, io_ctx: tuple[asyncio.StreamReader, asyncio.StreamWriter] | None,
                       eot: bytes) -> tuple[Any, Any, list[Exception], bool]:
        reader, _ = io_ctx
        peer = reader.get_extra_info('peername')
        if len(err) > 0:
            err_log = f'Error occurred on channel {peer[0]}:{peer[1]}'
            for e in err:
                err_log += f'\n- {type(e).__name__}: {e}'
            logger.error(err_log)
        return data, extra, err, fire
