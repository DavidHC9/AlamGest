import sys
import webbrowser
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt6.QtCore import Qt
from clientes import GestionClientes
from productos import GestionProductos
from facturas import GestionFacturas
from proveedores import GestionProveedores

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ALMAGEST - Más control, menos preocupaciones")
        self.setGeometry(100, 100, 900, 600)
        self.setFixedSize(900, 600)

        # Rutas de imágenes
        self.ruta_fondo = "C:/Users/David Herrera/Downloads/Almacen_contable/imagenes/Imagen de WhatsApp 2025-05-21 a las 09.18.54_15ff6b97.jpg"
        self.ruta_logo = "C:/Users/David Herrera/Downloads/Almacen_contable/imagenes/Captura de pantalla 2025-05-14 143245.png"

        self.establecer_fondo(self.ruta_fondo)

        layout_principal = QHBoxLayout()

        # --- Panel izquierdo con logo ---
        layout_izquierdo = QVBoxLayout()
        layout_izquierdo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo = QLabel()
        logo.setPixmap(QPixmap(self.ruta_logo).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo = QLabel("ALMAGEST")
        titulo.setStyleSheet("color: white; font-size: 26px; font-weight: bold;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitulo = QLabel("Más control, menos preocupaciones")
        subtitulo.setStyleSheet("color: white; font-size: 14px;")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_izquierdo.addWidget(logo)
        layout_izquierdo.addWidget(titulo)
        layout_izquierdo.addWidget(subtitulo)

        # --- Panel derecho con botones ---
        layout_derecho = QVBoxLayout()
        layout_derecho.setAlignment(Qt.AlignmentFlag.AlignCenter)

        botones = [
            ("Productos", self.abrir_gestion_productos),
            ("Clientes", self.abrir_gestion_clientes),
            ("Proveedores", self.abrir_gestion_proveedores),
            ("Facturación", self.abrir_gestion_facturas),
            ("Contáctame", self.abrir_pagina_contacto)  # ← corregido
        ]

        for texto, funcion in botones:
            boton = QPushButton(texto)
            boton.setFixedWidth(200)
            boton.setStyleSheet("""
                QPushButton {
                    color: white;
                    font-size: 16px;
                    border: none;
                    border-bottom: 1px solid white;
                    background-color: transparent;
                    padding: 10px;
                }
                QPushButton:hover {
                    color: #00ffcc;
                    border-bottom: 2px solid #00ffcc;
                }
            """)
            boton.clicked.connect(funcion)
            layout_derecho.addWidget(boton)

        layout_principal.addLayout(layout_izquierdo, 1)
        layout_principal.addLayout(layout_derecho, 1)

        self.setLayout(layout_principal)

    def establecer_fondo(self, ruta_imagen):
        fondo = QPixmap(ruta_imagen).scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        paleta = QPalette()
        paleta.setBrush(QPalette.ColorRole.Window, QBrush(fondo))
        self.setAutoFillBackground(True)
        self.setPalette(paleta)

    def resizeEvent(self, event):
        self.establecer_fondo(self.ruta_fondo)
        super().resizeEvent(event)

    def abrir_gestion_clientes(self):
        self.ventana_clientes = GestionClientes()
        self.ventana_clientes.show()

    def abrir_gestion_productos(self):
        self.ventana_productos = GestionProductos()
        self.ventana_productos.show()

    def abrir_gestion_facturas(self):
        self.ventana_facturas = GestionFacturas()
        self.ventana_facturas.show()

    def abrir_gestion_proveedores(self):
        self.ventana_proveedores = GestionProveedores()
        self.ventana_proveedores.show()

    def abrir_pagina_contacto(self):
        webbrowser.open("https://6000-firebase-studio-1747913910695.cluster-joak5ukfbnbyqspg4tewa33d24.cloudworkstations.dev/")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
