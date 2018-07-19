from abc import ABC, abstractmethod
import types
import numpy as np
import cv2 as cv

class Display(object):
    def __init__(self, resolution):
        self._res = resolution

    @property
    def resolution(self):
        return self._res

class FaceDisplay(object):
    _faces = []
    
    def add_face(self, face):
        if isinstance(face, types.GeneratorType):
            self._faces += list(face)
        elif isinstance(face, list):
            self._faces += face
        else:
            self._faces.append(face)

    @abstractmethod
    def clear(self):
        self._faces = []

    @abstractmethod
    def render(self):
        pass


class MultiScreenFaceDisplay(FaceDisplay):
    def __init__(self, displays):
        self._displays = displays
        self._screens = [AutoScalingSingleScreenFaceDisplay(display.resolution) \
            for display in self._displays]

    def render(self, frame):
        face_len = len(self._faces)

        if face_len < len(self._displays) and face_len != 0:
            faces = self._extend_array()
        else:
            faces = self._faces

        screens = self._screens
        for screen in screens:
            screen.clear()
        for i in range(len(faces)):
            j = i%len(self._screens)
            screens[j].add_face(faces[i])
        for screen in screens:
            yield screen.render()

    def _extend_array(self):
        n = len(self._displays)
        m = len(self._faces)
        out = []
        for i in range(n):
            face = self._faces[i%m]
            out.append(face)
        return out



class OverlayScreenFaceDisplay(FaceDisplay):
    """screen overlay that shows positions of faces over the frame"""

    LINE_COLOR = (0,0,255)
    
    def render(self, frame):
        canvas = np.copy(frame)
        for face in self._faces:
            (x,y,w,h) = face.position
            cv.rectangle(canvas, (x,y), (x+w,y+h), self.LINE_COLOR,3)
        return canvas

class SingleScreenFaceDisplay(FaceDisplay):
    def __init__(self, resolution, faces_per_row):
        """
        @param resolution: the resolution of the screen
        @param faces_per_row: the amount of faces that will be displayed in a single row
        """
        self._resolution = resolution
        self._num_per_row = faces_per_row
        self._faces = []
        self.clear()

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, val):
        if val is tuple and len(val) == 2 and val[0] is int is val[1]:
            self._resolution = val
            self.clear()

    def render(self):

        canvas = np.zeros(self._resolution+(3,), np.uint8)
        face_width = self._resolution[1] // self._num_per_row
        face_height = face_width

        y = 0
        for face in self._faces:

            img_x = (y % self._num_per_row)*face_width
            img_y = (y // self._num_per_row)*face_height

            y += 1
            #ensure an image is only fully rendered if it fully fits on the screen
            if img_y + face_height > self._resolution[1]:
                break   
          
            img = cv.resize(face.image, (face_width, face_height))
            canvas[img_y:img_y+face_height, img_x:img_x+face_width] = img

        return canvas
    
class AutoScalingSingleScreenFaceDisplay(FaceDisplay):
    """
    Automatically scales faces over the canvas
    currently limited to 3 faces per display
    """

    def __init__(self, resolution):
        self._res = resolution

    def render(self):
        canvas = np.zeros(self._res+(3,), dtype=np.uint8)
        x,y,w,h = 0,0,self._res[1], self._res[0]
        num_faces = len(self._faces)
        if num_faces == 1:
            face = self._faces[0]
            n = min(h, w)
            w = w-n
            img = cv.resize(face.image, (n,n))
            canvas[y:y+n, x+w//2:x+w//2+n] = img
        elif num_faces == 2:
            w //= 2
            n = min(h, w)
            for i in range(num_faces): #iterate through faces
                img = cv.resize(self._faces[i].image, (n,n))
                canvas[y:y+n, x+w*i:x+w*i+n] = img
        elif num_faces >= 3:
            w //= 3
            n = min(h,w)
            for i in range(3): #ensures that only 3 faces are rendered (renderer can't handle more) 
                img = cv.resize(self._faces[i].image, (n,n))
                canvas[y+h//6:y+n+h//6, x+w*i:x+w*i+n] = img

        return canvas

                


            