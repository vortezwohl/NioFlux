import asyncio

from nioflux import Server, StrDecode, StrEncode, PipelineStage


class MyHandler(PipelineStage):
    def __init__(self):
        super().__init__(label='my_handler')

    async def __call__(self, data, extra, err, fire, io_ctx):
        print('Recv:', data)
        return data, extra, err, fire


async def main():
    server = Server([StrDecode(), MyHandler(), StrEncode()], port=2386)
    print(server)
    await server.run()


if __name__ == '__main__':
    asyncio.run(main())
