from PySide6.QtWidgets import QSlider, QStyle, QStyleOptionSlider
from PySide6.QtCore import Qt


class BarraTiempo(QSlider):

    def __init__(self):
        super().__init__(Qt.Horizontal)


    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            opcion = QStyleOptionSlider()
            self.initStyleOption(opcion)

            rect_handle = self.style().subControlRect(
                QStyle.CC_Slider,
                opcion,
                QStyle.SC_SliderHandle,
                self
            )

            ancho_handle = rect_handle.width()

            posicion = event.position().x() - (ancho_handle / 2)

            ancho_util = self.width() - ancho_handle

            porcentaje = posicion / ancho_util

            porcentaje = max(0, min(1, porcentaje))

            valor = (
                self.minimum()
                +
                porcentaje *
                (self.maximum() - self.minimum())
            )

            self.setValue(int(valor))

        super().mousePressEvent(event)