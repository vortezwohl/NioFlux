from nioflux.util import tcp_send

if __name__ == '__main__':
    tcp_send(b'hello world', '127.0.0.1', 2386, wait=False)
