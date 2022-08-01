# -*- coding: utf-8 -*-
import cv2


def main(args=None, test=False):
    vc = cv2.VideoCapture("D:\\10059.mp4")
    if vc.isOpened():
        o, frame = vc.read()
    else:
        o = False

    while o:
        ret, frame = vc.read()
        if frame is None:
            break
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('result', gray)
            if cv2.waitKey(10) & 0xFF == 27:
                break
    vc.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
