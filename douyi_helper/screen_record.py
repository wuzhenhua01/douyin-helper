import struct
import sys
import threading
from socket import create_connection

import numpy as np
import cv2
from collections import OrderedDict


class ScreenRecord:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def iter_minicap(self):
        ws = create_connection((self._host, self._port))
        try:
            while 1:
                msg = ws.recv(4096)
                if isinstance(msg, str):
                    a = map(lambda b: struct.unpack('B', b), msg)
                    img_array = np.array(a, dtype=np.uint8)
                    img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
                    cv2.imshow('img', img)
                    cv2.waitKey(10)

        finally:
            ws.close()


if __name__ == '__main__':
    mc = ScreenRecord('localhost', 1717)
    mc.iter_minicap()
