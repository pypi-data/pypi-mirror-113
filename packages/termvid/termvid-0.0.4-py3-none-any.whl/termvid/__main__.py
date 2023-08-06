import cv2
import sys
from termvid import frame as boxes
import socket
import threading
from termvid import runner
import time
import blessed

t = blessed.Terminal()
box = boxes.HDFrame((0, 0), (t.width - 30, t.height))
small_frame = boxes.HDFrame((t.width - 30, 0), (30, t.height))

# print('1. Host\n2. Client')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    if len(sys.argv) <= 1:
        cap = cv2.VideoCapture(0)
        s.bind(('', 7009))
        s.listen()
        print('listening on port 7009 for all connections...')
        o=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        o.connect(('8.8.8.8', 80))
        local_ip = o.getsockname()[0]
        o.close()
        print(f'to connect, just run \n\ttermvid {local_ip}\non a computer connected to the local network!')
        sock, addr = s.accept()
        with sock:
            get = threading.Thread(
                target=runner.get,
                daemon=False,
                args=(sock, box),
                name="Thread(host, get)"
            )
            send = threading.Thread(
                target=runner.send,
                daemon=False,
                args=(sock, cap, small_frame),
                name="Thread(host, send)"
            )
            send.start()
            get.start()
            get.join()
    else:
        print('joining meeting...')
        cap = cv2.VideoCapture(0)
        s.connect((sys.argv[1], 7009))
        time.sleep(1)
        if input('connect with camera? (y/n)') != 'y':
            print('Okay, no problem. Try again later!')
            exit(0)
        get = threading.Thread(
            target=runner.get,
            daemon=False,
            args=(s, box),
            name="Thread(client, get)"
        )
        send = threading.Thread(
            target=runner.send,
            daemon=False,
            args=(s, cap, small_frame),
            name="Thread(client, send)"
        )
        get.start()
        send.start()
        send.join()
