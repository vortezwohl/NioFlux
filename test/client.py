from nioflux.util import tcp_send

if __name__ == '__main__':
    for _ in range(10):
        tcp_send(f'hello world {_}'.encode('utf-8'), '127.0.0.1', 2386, wait=False)
