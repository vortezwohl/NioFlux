from nioflux.server.server import DEFAULT_EOT
from nioflux.util import tcp_send

if __name__ == '__main__':
    for _ in range(50):
        tcp_send(f'hello world {_}'.encode('utf-8') + DEFAULT_EOT, '127.0.0.1', 2386, wait=False)
