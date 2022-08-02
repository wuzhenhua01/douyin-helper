import socket
import struct
import sys
import numpy as np
import cv2
from collections import OrderedDict


class Banner:
    def __init__(self):
        self.__banner = OrderedDict(
            [('version', 0),
             ('length', 0),
             ('pid', 0),
             ('realWidth', 0),
             ('realHeight', 0),
             ('virtualWidth', 0),
             ('virtualHeight', 0),
             ('orientation', 0),
             ('quirks', 0)
             ])

    def __setitem__(self, key, value):
        self.__banner[key] = value

    def __getitem__(self, key):
        return self.__banner[key]

    def keys(self):
        return self.__banner.keys()

    def __str__(self):
        return str(self.__banner)


class Minicap:
    BUFFER_SIZE = 4096

    def __init__(self, host, port, banner):
        self.host = host
        self.port = port
        self.banner = banner

    def connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print(e)
            sys.exit(1)
        self.__socket.connect((self.host, self.port))

    def on_image_transfered(self, data):
        img_array = np.array(data, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        draw_contours = cv2.drawContours(img, contours, -1, (0, 0, 255), 2)
        cv2.imshow('img', draw_contours)
        cv2.waitKey(10)


    def consume(self):
        read_banner_bytes = 0
        banner_length = 24
        read_frame_bytes = 0
        frame_body_length = 0
        data = []
        while 1:
            try:
                chunk = self.__socket.recv(self.BUFFER_SIZE)
            except socket.error as e:
                print("Error receiving data: %s" % e)
                sys.exit(1)
            cursor = 0
            buf_len = len(chunk)
            while cursor < buf_len:
                if read_banner_bytes < banner_length:
                    map(lambda i, val: self.banner.__setitem__(self.banner.keys()[i], val),
                        [i for i in range(len(self.banner.keys()))], struct.unpack("<2b5ibB", chunk))
                    cursor = buf_len
                    read_banner_bytes = banner_length
                    print(self.banner)
                elif read_frame_bytes < 4:
                    frame_body_length += (chunk[cursor] << (read_frame_bytes * 8)) >> 0
                    cursor += 1
                    read_frame_bytes += 1
                else:
                    print("frame length:%d buf_len:%d cursor:%d" % (frame_body_length, buf_len, cursor))
                    # pic end
                    if buf_len - cursor >= frame_body_length:
                        data.extend(chunk[cursor:cursor + frame_body_length])

                        self.on_image_transfered(data)

                        cursor += frame_body_length
                        frame_body_length = read_frame_bytes = 0
                        data = []
                    else:
                        data.extend(chunk[cursor:buf_len])
                        frame_body_length -= buf_len - cursor
                        read_frame_bytes += buf_len - cursor
                        cursor = buf_len


if '__main__' == __name__:
    mc = Minicap('localhost', 1717, Banner())
    mc.connect()
    mc.consume()
