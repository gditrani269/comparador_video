import cv2


class LectorVideo:
    """Abre un video y permite leer y posicionarse por número de frame."""

    def __init__(self, ruta):
        self.ruta = ruta
        self.video = cv2.VideoCapture(ruta)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_actual = -1

        if not self.video.isOpened():
            self.release()
            raise RuntimeError(f"No se pudo abrir el video: {ruta}")

        if self.fps <= 0:
            self.fps = 25.0

    @property
    def duracion_segundos(self):
        if self.total_frames <= 0:
            return 0.0
        return self.total_frames / self.fps

    def obtener_frame(self):
        correcto, frame = self.video.read()
        if correcto:
            # CAP_PROP_POS_FRAMES indica el próximo frame que se leerá.
            self.frame_actual = max(0, int(self.video.get(cv2.CAP_PROP_POS_FRAMES)) - 1)
            return frame
        return None

    def ir_a_frame(self, numero):
        if self.total_frames <= 0:
            return None

        numero = max(0, min(int(numero), self.total_frames - 1))
        self.video.set(cv2.CAP_PROP_POS_FRAMES, numero)
        correcto, frame = self.video.read()

        if correcto:
            self.frame_actual = numero
            return frame
        return None

    def release(self):
        if getattr(self, "video", None) is not None:
            self.video.release()

    def ir_a_posicion(self, posicion):

        total = self.video.get(
            cv2.CAP_PROP_FRAME_COUNT
        )

        frame = (
            total * posicion / 1000
        )

        self.video.set(
            cv2.CAP_PROP_POS_FRAMES,
            int(frame)
        )