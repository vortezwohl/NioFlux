import asyncio
import logging
from typing_extensions import Any

from nioflux.pipeline.stage import PipelineStage
from nioflux.pipeline.pipeline import Pipeline
from nioflux.util.readsuntil import readsuntil
from nioflux.util.transport_layer import random_port

DEFAULT_HOST = '0.0.0.0'
DEFAULT_TIMEOUT = 8.0
DEFAULT_BUFFER_SIZE = 65536
DEFAULT_EOT = b'<|eot|>'

logger = logging.getLogger('nioflux.server')


class Server:
    def __init__(self, pipeline: list[PipelineStage],
                 host: str = DEFAULT_HOST, port: int = random_port(),
                 timeout: float = DEFAULT_TIMEOUT, buffer_size: int = DEFAULT_BUFFER_SIZE,
                 eot: bytes = DEFAULT_EOT, extra: Any | None = None):
        assert len(pipeline) > 0, 'pipeline is empty'
        self._host = host
        self._port = port
        self._timeout = timeout
        self._buffer_size = buffer_size
        self._eot = eot
        self._pipeline = pipeline
        self._extra = extra

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def extra(self) -> str:
        return self._extra

    @property
    def pipeline(self) -> list[PipelineStage]:
        return self._pipeline

    @property
    def eot(self) -> bytes:
        return self._eot

    async def _channel_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        _peer_host, _peer_port = writer.get_extra_info('peername')
        logger.debug(f'Receiving data from {_peer_host}:{_peer_port}')
        try:
            data = await readsuntil(reader=reader, buffer_size=self._buffer_size,
                                    until=self._eot, timeout=self._timeout)
            _, self._extra, _ = await Pipeline(queue=self._pipeline, data=data, extra=self._extra,
                                               io_ctx=(reader, writer)).launch()
        except TimeoutError:
            logger.warning(f'Read timeout on channel {_peer_host}:{_peer_port}')
        finally:
            writer.close()
            await writer.wait_closed()

    async def run(self):
        server = await asyncio.start_server(client_connected_cb=self._channel_handler,
                                            host=self._host, port=self._port,
                                            limit=self._buffer_size)
        async with server:
            await server.serve_forever()
