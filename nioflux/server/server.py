import asyncio
import logging

from nioflux.pipeline.stage import PipelineStage
from nioflux.pipeline.pipeline import Pipeline
from nioflux.util.readsuntil import readsuntil

logger = logging.getLogger('nioflux.server')


class Server:
    def __init__(self, host: str, port: int, timeout: float, buffer_size: int,
                 eot: bytes, pipeline: list[PipelineStage], extra: str):
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

    async def channel_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        _peer_host, _peer_port = writer.get_extra_info('peername')
        logger.debug(f'Receiving data from {_peer_host}:{_peer_port}')
        try:
            data = await readsuntil(reader=reader, buffer_size=self._buffer_size,
                                    until=self._eot, timeout=self._timeout)
            _, self._extra, _ = await Pipeline(queue=self.pipeline, data=data, extra=self._extra,
                                               io_ctx=(reader, writer), eot=self._eot).launch()
        except TimeoutError:
            logger.warning(f'Read timeout on channel {_peer_host}:{_peer_port}')
        finally:
            writer.close()
            await writer.wait_closed()

    async def run(self, buffer_size: int = 65536):
        server = await asyncio.start_server(client_connected_cb=self.channel_handler,
                                            host=self.host, port=self.port, limit=buffer_size)
        async with server:
            await server.serve_forever()
