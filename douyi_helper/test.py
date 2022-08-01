# -*- coding: utf-8 -*-
import cv2

vc = cv2.VideoCapture("D:\\10059.mp4")
ret, frame = vc.read()

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
        sobelx = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
        sobelx = cv2.convertScaleAbs(sobelx)
        sobely = cv2.Scharr(gray, cv2.CV_64F, 0, 1)
        sobely = cv2.convertScaleAbs(sobely)
        sobelxy = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)

        cv2.imshow('result', sobelxy)

        if cv2.waitKey(10) & 0xFF == 27:
            break
vc.release()
cv2.destroyAllWindows()
