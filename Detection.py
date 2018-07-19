import cv2 as cv
import numpy as np

class Recog(object):
    def __init__(self):
        self.face_cascade = cv.CascadeClassifier('frontalface-cascade.xml')
        #self.eye_cascade = cv.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_eye.xml')
        #self.face_cascade = cv.CascadeClassifier('haarcascade4.xml')

    def detectFaces(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.2, maxSize=(80,80))
        for (x, y, w, h) in faces: #filters false positives from final product
            #if w > 80 or h > 80:  #pretty much a hack time constraints don't allow for proper implementation
            #    continue
            if x < 400 or x > 850:
                continue
            if x > 740 and y < 90:
                continue
            yield (x,y,w,h)