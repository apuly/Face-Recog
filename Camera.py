from abc import ABC, abstractmethod
import cv2 as cv
import urllib.request as request
import base64
import numpy as np

class Camera(ABC):

    @abstractmethod
    def read_image(self):
        pass

class URLCam(Camera):

    def __init__(self, url):
        self._url = url

    def read_image(self):
        req = request.urlopen(self._url)
        img_arr = np.array(bytearray(req.read()), dtype=np.uint8)
        img = cv.imdecode(img_arr, -1)
        return img

class NULLCam(Camera):
    """
    always returns an empty image of 400 by 300 pixels
    """
    def read_image(self):
        return np.zeros((400,300,3))

class WebCam(Camera):
    """
    returns images from webcam
    """
    def __init__(self, cam_index):
        self._vc = cv.VideoCapture(0)
        self._vc.set(3,1280)
        self._vc.set(4,720)

    def read_image(self):
        rval, frame = self._vc.read()
        if rval:
            return frame
        else:
            return None

    