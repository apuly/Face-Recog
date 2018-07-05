import numpy as np
import cv2 as cv
from abc import ABC

class ImageObect(ABC):
    def __init__(self, image, pos_data):
        self._image = image
        self._pos = pos_data

    @property
    def image(self):
        return self._image


class Face(ImageObect):
    """
    Holds the face of a person, together with any related data
    """
    pass

class Shirt(ImageObect):
    def average_color(self):
        r_sum = g_sum = b_sum = 0
        for row in self._image:
            for column in row:
                r_sum += column[0]
                g_sum += column[1]
                b_sum += column[2]
        x = len(self._image) * len(self._image[0]) #get the total size of the image
        return (r_sum//x, g_sum//x, b_sum//x)