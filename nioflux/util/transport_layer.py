import socket
from random import randint


def random_port():
    def port_is_available(_port: int):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        try:
            return s.connect_ex(('127.0.0.1', _port)) != 0
        finally:
            s.close()

    while True:
        _candidate_port = randint(1025, 65535)
        if port_is_available(_candidate_port):
            return _candidate_port
