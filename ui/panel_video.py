from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
)

from PySide6.QtCore import Qt


class PanelVideo(QWidget):

    def __init__(self, titulo):
        super().__init__()

        self.titulo = titulo

        self.crear_interfaz()


    def crear_interfaz(self):

        layout = QVBoxLayout()

        self.video = QLabel(
            f"{self.titulo}\n\nSin video"
        )

        self.video.setMinimumSize(640, 360)

        self.video.setAlignment(Qt.AlignCenter)

        self.video.setStyleSheet(
            """
            QLabel {
                border: 2px solid gray;
                background-color: black;
                color: white;
            }
            """
        )

        self.boton = QPushButton(
            f"Abrir {self.titulo}"
        )

        self.boton.clicked.connect(
            self.abrir_video
        )

        layout.addWidget(self.video)
        layout.addWidget(self.boton)

        self.setLayout(layout)


    def abrir_video(self):

        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar video",
            "",
            "Videos (*.mp4 *.avi *.mkv)"
        )

        if archivo:

            self.video.setText(
                archivo
            )