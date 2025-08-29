import asyncio
from abc import abstractmethod
from typing_extensions import Any, List


class PipelineStage:
    def __init__(self, label: str):
        self._label: str = label

    @property
    def label(self) -> str:
        return self._label

    @abstractmethod
    async def __call__(self, data: Any, extra: Any, err: List[Exception],
                       fire: bool, io_ctx: tuple[asyncio.StreamReader, asyncio.StreamWriter] | None,
                       eot: bytes) -> tuple[Any, Any, List[Exception], bool]:
        # data, extra, err, fire
        ...
