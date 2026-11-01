pip install PySide6         #python -m pip install PySide6
pip install opencv-python   #python -m pip install opencv-python

# Comparador de Videos — versión 0.1.7

## Funcionalidades
- Abrir un video independiente en cada panel.
- Play / pausa.
- Stop (vuelve al primer frame).
- Avance y retroceso de un frame.
- Barra de progreso para posicionarse en el video.
- Indicador de tiempo actual y duración total.
- Liberación de recursos al cerrar o reemplazar un video.

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate       # Debian/Linux
# .venv\\Scripts\\Activate.ps1  # Windows PowerShell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

En Debian, si Qt no puede iniciar el plugin gráfico XCB:

```bash
sudo apt install libxcb-cursor0
```

OpenCV se instala en variante headless porque la interfaz gráfica la proporciona PySide6.