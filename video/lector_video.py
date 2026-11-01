import cv2


class LectorVideo:

    def __init__(self, ruta):

        self.ruta = ruta

        self.video = cv2.VideoCapture(
            ruta
        )


    def obtener_frame(self):

        correcto, frame = self.video.read()

        if correcto:
            return frame

        return None