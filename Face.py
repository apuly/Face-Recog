class Face(object):
    """
    Holds the face of a person, together with any related data
    """
    
    def __init__(self, image):
        self._image = image

    @property
    def image(self):
        return self._image