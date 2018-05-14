#! /usr/bin/python3

import sys
import cv2 as cv
import numpy as np

import Face
import Detection

FACE_IMG_SIZE = (150,150)
CANVAS_SIZE = (8,5)


def main(argv):

    canvas_x = FACE_IMG_SIZE[0]*CANVAS_SIZE[0]
    canvas_y = FACE_IMG_SIZE[1]*CANVAS_SIZE[1]
    canvas = np.zeros((canvas_y, canvas_x, 3), np.uint8)

    dt = Detection.Recog()
    cv.namedWindow("frame")
    cv.namedWindow("canvas")

    vc = cv.VideoCapture(0)
    vc.set(3,1280)
    vc.set(4,1024)
    rval = True


    while rval:
        
        rval, frame = vc.read()
        faces = dt.detectFaces(frame)
        print(faces)
        canvas = np.zeros((canvas_y, canvas_x, 3), np.uint8) #clear canvas
        if faces != (): #check if any faces have been detected
            loaded = load_faces(frame, faces)
            canvas = draw_faces(canvas, loaded)
            
    
        cv.imshow('canvas', canvas)
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break

    cv.destroyAllWindows()

def load_faces(frame, faces):
    out = []
    for (x,y,w,h) in faces:
        img = frame[y:y+h, x:x+w]
        img = cv.resize(img, FACE_IMG_SIZE)
        out.append(Face.Face(img))
    return out

def draw_faces(canvas, faces):
    x = len(faces)
    y = 0
    #print(x)
    for i in range(CANVAS_SIZE[1]):
        for j in range(CANVAS_SIZE[0]):
            
            img_x = i * FACE_IMG_SIZE[0]
            img_y = j * FACE_IMG_SIZE[0]
            canvas[img_x:img_x+FACE_IMG_SIZE[0], img_y:img_y+FACE_IMG_SIZE[1]] = faces[y].image

            y += 1
            #print(y)
            if x == y:
                return canvas


    

if __name__ == "__main__":
    main(sys.argv)