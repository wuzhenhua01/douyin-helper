# -*- coding: utf-8 -*-
import cv2

vc = cv2.VideoCapture("D:\\10059.mp4")
ret, src_img = vc.read()

if vc.isOpened():
    o, src_img = vc.read()
else:
    o = False

while o:
    ret, src_img = vc.read()
    if src_img is None:
        break
    if ret:
        gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
        _, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        tmp_img = src_img.copy()
        res = cv2.drawContours(tmp_img, contours, -1, (0, 0, 255), 2)
        cv2.imshow('res', res)

        if cv2.waitKey(1) & 0xFF == 27:
            break
vc.release()
cv2.destroyAllWindows()
