from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt


class BarraTiempo(QSlider):

    def __init__(self):
        super().__init__(Qt.Horizontal)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            valor = self.minimum() + (
                (self.maximum() - self.minimum())
                * event.position().x()
                / self.width()
            )

            self.setValue(int(valor))

        super().mousePressEvent(event)