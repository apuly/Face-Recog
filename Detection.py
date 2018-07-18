import cv2 as cv
import numpy as np

class Recog(object):
    def __init__(self):
        self.face_cascade = cv.CascadeClassifier('frontalface-cascade.xml')
        #self.eye_cascade = cv.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_eye.xml')
        #self.face_cascade = cv.CascadeClassifier('haarcascade4.xml')
    def detectFaces(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        yield from self.face_cascade.detectMultiScale(gray, 1.3, 5)
        # faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        # for (x,y,w,h) in faces:
        #     face_img = gray[y:y+h, x:x+w]
        #     eyes = self.eye_cascade.detectMultiScale(face_img)
        #     if len(eyes) == 2:
        #         yield (x,y,w,h)