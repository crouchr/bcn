import socket
import json
import time
from pprint import pprint


# TODO : add a check that all metric values are not strings
def send_metrics(endpoint_ip, metrics, verbose):
    try:
        if verbose:
            print()
            print(time.ctime())
            pprint(metrics)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = json.dumps(metrics).encode()
        # pprint(msg)
        sock.sendto(msg, (endpoint_ip, 8094))
        sock.close()

    except socket.error as e:
        print(f'Error: {e}')
