from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
)

from config import ANCHO_VIDEO, ALTO_VIDEO, INTERVALO_TIMER_MS
from video.lector_video import LectorVideo
from ui.barra_tiempo import BarraTiempo


class PanelVideo(QWidget):
    def __init__(self, titulo):
        super().__init__()

        self.titulo = titulo
        self.lector = None
        self.reanudar_despues_seek = False
        self.buscando = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_frame)

        self.crear_interfaz()

    def crear_interfaz(self):
        layout = QVBoxLayout()

        self.video = QLabel(f"{self.titulo}\n\nSin video")
        self.video.setMinimumSize(ANCHO_VIDEO, ALTO_VIDEO)
        self.video.setAlignment(Qt.AlignCenter)
        self.video.setStyleSheet(
            "QLabel { border: 2px solid gray; background-color: black; color: white; }"
        )

        self.boton_abrir = QPushButton(f"Abrir {self.titulo}")
        self.boton_abrir.clicked.connect(self.abrir_video)

        controles = QHBoxLayout()
        self.boton_anterior = QPushButton("|◀")
        self.boton_anterior.setToolTip("Frame anterior")
        self.boton_anterior.clicked.connect(self.frame_anterior)

        self.boton_play = QPushButton("▶ Play")
        self.boton_play.clicked.connect(self.alternar_reproduccion)

        self.boton_stop = QPushButton("■ Stop")
        self.boton_stop.clicked.connect(self.detener)

        self.boton_siguiente = QPushButton("▶|")
        self.boton_siguiente.setToolTip("Frame siguiente")
        self.boton_siguiente.clicked.connect(self.frame_siguiente)

        for boton in (
            self.boton_anterior,
            self.boton_play,
            self.boton_stop,
            self.boton_siguiente,
        ):
            controles.addWidget(boton)

        self.etiqueta_tiempo = QLabel("00:00 / 00:00")
        self.etiqueta_tiempo.setAlignment(Qt.AlignRight)

        layout.addWidget(self.video)
        self.barra = BarraTiempo()
        self.barra.sliderPressed.connect(
            self.iniciar_busqueda
        )

        self.barra.sliderReleased.connect(
            self.finalizar_busqueda
        )
        self.barra.valueChanged.connect(
            self.preview_busqueda
        )
        layout.addWidget(self.barra)
        layout.addWidget(self.boton_abrir)
        layout.addLayout(controles)

        layout.addWidget(self.etiqueta_tiempo)
        self.setLayout(layout)

        self.actualizar_estado_controles(False)

    def abrir_video(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar video",
            "",
            "Videos (*.mp4 *.avi *.mkv *.mov *.wmv);;Todos los archivos (*)",
        )

        if not archivo:
            return

        self.timer.stop()
        self.liberar_lector()

        try:
            nuevo_lector = LectorVideo(archivo)
        except RuntimeError as error:
            self.video.setText(str(error))
            self.actualizar_estado_controles(False)
            return

        self.lector = nuevo_lector
        frame = self.lector.obtener_frame()

        if frame is None:
            self.liberar_lector()
            self.video.setText("No se pudo leer el video")
            self.actualizar_estado_controles(False)
            return

        self.mostrar_frame(frame)
        self.barra.setRange(
            0,
            max(0, self.lector.total_frames - 1)
        )

        self.barra.setValue(0)

        self.barra.setEnabled(
            self.lector.total_frames > 1
        )
        self.actualizar_etiqueta_tiempo(0)
        self.actualizar_estado_controles(True)
        self.boton_play.setText("▶ Play")

    def mostrar_frame(self, frame):
        alto, ancho, canales = frame.shape
        imagen = QImage(
            frame.data,
            ancho,
            alto,
            ancho * canales,
            QImage.Format_BGR888,
        ).copy()

        pixmap = QPixmap.fromImage(imagen).scaled(
            self.video.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.video.setPixmap(pixmap)

    def actualizar_frame(self):
        if self.lector is None:
            self.timer.stop()
            return

        frame = self.lector.obtener_frame()
        if frame is None:
            self.timer.stop()
            self.boton_play.setText("▶ Play")
            return

        self.mostrar_frame(frame)
        self.actualizar_slider(self.lector.frame_actual)

    def alternar_reproduccion(self):
        if self.lector is None:
            return

        if self.timer.isActive():
            self.timer.stop()
            self.boton_play.setText("▶ Play")
            return

        # Si llegó al final, Play vuelve a comenzar desde el primer frame.
        if self.lector.frame_actual >= self.lector.total_frames - 1:
            frame = self.lector.ir_a_frame(0)
            if frame is not None:
                self.mostrar_frame(frame)
                self.actualizar_slider(0)

        intervalo = max(1, round(1000 / self.lector.fps))
        if intervalo <= 0:
            intervalo = INTERVALO_TIMER_MS
        self.timer.start(intervalo)
        self.boton_play.setText("❚❚ Pausa")

    def detener(self):
        if self.lector is None:
            return

        self.timer.stop()
        frame = self.lector.ir_a_frame(0)
        if frame is not None:
            self.mostrar_frame(frame)
        self.actualizar_slider(0)
        self.boton_play.setText("▶ Play")

    def frame_anterior(self):
        self.mover_un_frame(-1)

    def frame_siguiente(self):
        self.mover_un_frame(1)

    def mover_un_frame(self, desplazamiento):
        if self.lector is None:
            return

        estaba_reproduciendo = self.timer.isActive()
        self.timer.stop()

        destino = self.lector.frame_actual + desplazamiento
        frame = self.lector.ir_a_frame(destino)
        if frame is not None:
            self.mostrar_frame(frame)
            self.actualizar_slider(self.lector.frame_actual)

        if estaba_reproduciendo:
            self.timer.start(max(1, round(1000 / self.lector.fps)))
            self.boton_play.setText("❚❚ Pausa")
        else:
            self.boton_play.setText("▶ Play")

    def iniciar_busqueda(self):
        self.buscando = True
        self.reanudar_despues_seek = self.timer.isActive()
        if self.reanudar_despues_seek:
            self.timer.stop()

    def finalizar_busqueda(self):
        self.buscando = False
        if self.lector is None:
            return

        frame = self.lector.ir_a_frame(self.barra.value())
        if frame is not None:
            self.mostrar_frame(frame)
            self.actualizar_slider(self.lector.frame_actual)

        if self.reanudar_despues_seek:
            self.timer.start(max(1, round(1000 / self.lector.fps)))
            self.boton_play.setText("❚❚ Pausa")
        self.reanudar_despues_seek = False

    def actualizar_tiempo_desde_slider(self, valor):
        if self.lector is not None:
            self.actualizar_etiqueta_tiempo(valor)

    def actualizar_slider(self, valor):
        self.barra.blockSignals(True)

        self.barra.setValue(valor)

        self.barra.blockSignals(False)

        self.actualizar_etiqueta_tiempo(valor)

    def actualizar_etiqueta_tiempo(self, numero_frame):
        if self.lector is None:
            self.etiqueta_tiempo.setText("00:00 / 00:00")
            return

        actual = numero_frame / self.lector.fps
        duracion = self.lector.duracion_segundos
        self.etiqueta_tiempo.setText(
            f"{self.formatear_tiempo(actual)} / {self.formatear_tiempo(duracion)}"
        )

    @staticmethod
    def formatear_tiempo(segundos):
        segundos = max(0, int(segundos))
        horas, resto = divmod(segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        if horas:
            return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        return f"{minutos:02d}:{segundos:02d}"

    def actualizar_estado_controles(self, habilitado):
        for control in (
            self.boton_anterior,
            self.boton_play,
            self.boton_stop,
            self.boton_siguiente,
        ):
            control.setEnabled(habilitado)

    def liberar_lector(self):
        if self.lector is not None:
            self.lector.release()
            self.lector = None

    def closeEvent(self, event):
        self.timer.stop()
        self.liberar_lector()
        super().closeEvent(event)

    def mover_video(self, posicion):

        if hasattr(self, "lector"):

            self.lector.ir_a_posicion(
                posicion
            )

            frame = self.lector.obtener_frame()

            if frame is not None:

                self.mostrar_frame(frame)

    def preview_busqueda(self, valor):

        if not self.buscando:
            return

        if self.lector is None:
            return

        valor = min(
            valor,
            self.lector.total_frames - 1
        )

        frame = self.lector.ir_a_frame(valor)

        if frame is not None:
            self.mostrar_frame(frame)