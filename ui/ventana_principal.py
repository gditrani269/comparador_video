from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QSplitter,
)
from PySide6.QtCore import Qt

from config import TITULO, VERSION, ANCHO_VENTANA, ALTO_VENTANA
from ui.panel_video import PanelVideo


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{TITULO} - v{VERSION}")
        self.resize(ANCHO_VENTANA, ALTO_VENTANA)
        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = QWidget()
        layout = QHBoxLayout()

        self.video1 = PanelVideo("Video 1")
        self.video2 = PanelVideo("Video 2")

        splitter = QSplitter(Qt.Horizontal)

        splitter.addWidget(self.video1)
        splitter.addWidget(self.video2)

        splitter.setSizes([1, 1])

        layout.addWidget(splitter)
        layout.setSpacing(20)

        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)
