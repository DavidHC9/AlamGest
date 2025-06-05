import webbrowser
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo de Contacto")
        self.setGeometry(300, 200, 300, 150)

        layout = QVBoxLayout()

        boton_contacto = QPushButton("Contáctame")
        boton_contacto.setStyleSheet("background-color: #0a74da; color: white; font-weight: bold; padding: 10px; border-radius: 10px;")
        boton_contacto.clicked.connect(self.abrir_pagina_contacto)

        layout.addWidget(boton_contacto)
        self.setLayout(layout)

    def abrir_pagina_contacto(self):
        webbrowser.open("https://6000-firebase-studio-1747913910695.cluster-joak5ukfbnbyqspg4tewa33d24.cloudworkstations.dev/")

if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec()
