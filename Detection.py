import cv2 as cv
import numpy as np

class Recog(object):
    def __init__(self):
        self.face_cascade = cv.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

    def detectFaces(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces