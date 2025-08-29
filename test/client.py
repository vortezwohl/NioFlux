from nioflux.server.server import DEFAULT_EOT
from nioflux.util import tcp_send

if __name__ == '__main__':
    port = int(input('Port: '))
    for _ in range(50):
        data = f'hello world {_}'.encode('utf-8') + DEFAULT_EOT
        print('Send:', data)
        tcp_send(data, '127.0.0.1', port, wait=False)
