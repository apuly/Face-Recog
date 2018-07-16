#! /usr/bin/python3

import sys
import cv2 as cv
import numpy as np

import ImageObjects
import Detection
import ColorTools
from FaceDisplay import *


def main(argv):

    SHOW_FRAME = True

    dt = Detection.Recog()
    cv.namedWindow("canvas")

    renderer = AutoScalingSingleScreenFaceDisplay((720,1440))

    vc = cv.VideoCapture(0)
    vc.set(3,1920)
    vc.set(4,1080)


    while True:
        
        rval, frame = vc.read()
        if not rval:
            continue

        frame = cv.resize(frame, (1440, 720))

        faces = dt.detectFaces(frame)

        #print(faces)
        loaded = load_faces(frame, faces)
        renderer.clear()
        renderer.add_face(loaded)
        images = renderer.render()

        cv.imwrite("over.jpg", images.next())

        i = 0
        for image in images:
            cv.imwrite("{:>05}.jpg".format(i), image)
            i += 0
        

def load_faces(frame, faces):
    
    for (x,y,w,h) in faces:
       
        img = frame[y:y+h, x:x+w]
        yield ImageObjects.Face(img, (x,y,w,h))


if __name__ == "__main__":
    main(sys.argv)