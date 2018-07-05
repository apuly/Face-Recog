#! /usr/bin/python3

import sys
import cv2 as cv
import numpy as np

import ImageObjects
import Detection
import ColorTools

FACE_IMG_SIZE = (150,150)
CANVAS_SIZE = (8,5)



def main(argv):

    canvas_x = FACE_IMG_SIZE[0]*CANVAS_SIZE[0]
    canvas_y = FACE_IMG_SIZE[1]*CANVAS_SIZE[1]
    canvas = np.zeros((canvas_y, canvas_x, 3), np.uint8)

    dt = Detection.Recog()
    cv.namedWindow("frame")
    cv.namedWindow("canvas")
    cv.namedWindow("TSHIRT")

    vc = cv.VideoCapture(0)
    vc.set(3,1280)
    vc.set(4,1024)
    rval = True


    while rval:
        
        rval, frame = vc.read()
        try:
            cv.imshow('frame', frame)
        except:
            pass

        faces = dt.detectFaces(frame)
        #print(faces)
        canvas = np.zeros((canvas_y, canvas_x, 3), np.uint8) #clear canvas
        loaded = load_image_objects(frame, faces)
        canvas = draw_objects(canvas, loaded)
        cv.imshow('canvas', canvas)
        if cv.waitKey(1) == ord('q'):
            break

    cv.destroyAllWindows()

def load_image_objects(frame, faces):
    """
    Loads information about objects inside the image, based on the position of faces within the image
    """
    for (x,y,w,h) in faces:
        if y+h*2 < len(frame):
            shirt_img = frame[y+h+h:y+h*4, x-w//10:x+w+w//10]
            #cv.imshow("TSHIRT", frame[y+h+h:y+h*4, x-w//3:x+w+w//3])
            yield ImageObjects.Shirt(shirt_img, (x-w//3, y+h*2, x+w+w//3, y+h*4))
        img = frame[y:y+h, x:x+w]
        img = cv.resize(img, FACE_IMG_SIZE)
        yield ImageObjects.Face(img, (x,y,w,h))

def draw_objects(canvas, faces):
    y = 0
    #print(x)
    for face in faces:
        if type(face) == ImageObjects.Face:
            if y == CANVAS_SIZE[0]*CANVAS_SIZE[1]:
                break
            img_x = y % CANVAS_SIZE[1]
            img_y = y // FACE_IMG_SIZE[1]
            canvas[img_y:img_y+FACE_IMG_SIZE[1], img_x:img_x+FACE_IMG_SIZE[0]] = face.image
            y += 1
        else:
            color = face.average_color()
            #color = cv.cvtColor(color, cv.COLOR_BGR2HSV)
            c = np.full((20,20,3), color, dtype=np.uint8)
            print(ColorTools.closest_color(ColorTools.bgr2rgb(color)))
            cv.imshow("TSHIRT", face.image)
        
    return canvas

if __name__ == "__main__":
    main(sys.argv)