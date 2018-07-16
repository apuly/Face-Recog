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

    @property
    def position(self):
        return self._pos


class Face(ImageObect):
    """
    Holds the face of a person, together with any related data
    """
    pass