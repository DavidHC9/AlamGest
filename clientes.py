import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QBrush, QPalette
from PyQt6.QtGui import QFont, QColor, QPalette
from conexion import conectar

class GestionClientes(QWidget):
    def __init__(self):
        super().__init__()
        self.ruta_fondo = "C:/Users/David Herrera/Downloads/Almacen_contable/imagenes/Imagen de WhatsApp 2025-05-21 a las 09.18.54_15ff6b97.jpg"
        self.setWindowTitle("Gestión de Productos")
        self.setGeometry(200, 100, 1000, 600)
        self.establecer_fondo(self.ruta_fondo)

        layout_principal = QVBoxLayout()

        self.setWindowTitle("Gestión de Clientes")
        self.setGeometry(150, 150, 900, 600)

        self.initUI()
        self.cargar_clientes()

    def initUI(self):
        layout = QVBoxLayout()

        # Título
        titulo = QLabel("Gestión de Clientes")
        titulo.setStyleSheet("color: white")
        titulo.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Fila de entradas
        fila_formulario = QHBoxLayout()

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")
        fila_formulario.addWidget(self.input_nombre)

        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Teléfono")
        fila_formulario.addWidget(self.input_telefono)

        self.input_direccion = QLineEdit()
        self.input_direccion.setPlaceholderText("Dirección")
        fila_formulario.addWidget(self.input_direccion)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")
        fila_formulario.addWidget(self.input_email)

        layout.addLayout(fila_formulario)

        # Fila de botones
        fila_botones = QHBoxLayout()

        self.boton_guardar = QPushButton("+ Agregar Cliente")
        self.boton_guardar.setStyleSheet("background-color: #004080; color: white; padding: 10px; font-weight: bold;")
        self.boton_guardar.clicked.connect(self.guardar_cliente)
        fila_botones.addWidget(self.boton_guardar)

        self.boton_eliminar = QPushButton("- Eliminar Cliente")
        self.boton_eliminar.setStyleSheet("background-color: #800000; color: white; padding: 10px; font-weight: bold;")
        self.boton_eliminar.clicked.connect(self.eliminar_cliente)
        fila_botones.addWidget(self.boton_eliminar)

        layout.addLayout(fila_botones)

        # Tabla de clientes
        self.tabla_clientes = QTableWidget()
        self.tabla_clientes.setColumnCount(5)
        self.tabla_clientes.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono", "Dirección", "Email"])
        self.tabla_clientes.horizontalHeader().setStretchLastSection(True)
        self.tabla_clientes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_clientes.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_clientes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.tabla_clientes)

        self.setLayout(layout)

    def guardar_cliente(self):
        nombre = self.input_nombre.text()
        telefono = self.input_telefono.text()
        direccion = self.input_direccion.text()
        email = self.input_email.text()

        if nombre and telefono and direccion and email:
            conexion = conectar()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    sql = "INSERT INTO clientes (nombre, telefono, direccion, email, deuda) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (nombre, telefono, direccion, email, 0.00))
                    conexion.commit()
                    cursor.close()
                    conexion.close()
                    QMessageBox.information(self, "Éxito", "Cliente guardado correctamente")
                    self.input_nombre.clear()
                    self.input_telefono.clear()
                    self.input_direccion.clear()
                    self.input_email.clear()
                    self.cargar_clientes()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo guardar el cliente: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios")

    # --- Fondo de pantalla ---
    def establecer_fondo(self, ruta_imagen):
        self.ruta_fondo = ruta_imagen
        self.actualizar_fondo()

    def actualizar_fondo(self):
        if hasattr(self, 'ruta_fondo'):
            fondo = QPixmap(self.ruta_fondo).scaled(
                self.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            paleta = QPalette()
            paleta.setBrush(QPalette.ColorRole.Window, QBrush(fondo))
            self.setAutoFillBackground(True)
            self.setPalette(paleta)

    def resizeEvent(self, event):
        self.actualizar_fondo()
        super().resizeEvent(event)

    def cargar_clientes(self):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id, nombre, telefono, direccion, email FROM clientes")
                clientes = cursor.fetchall()

                self.tabla_clientes.setRowCount(len(clientes))
                for i, cliente in enumerate(clientes):
                    for j, dato in enumerate(cliente):
                        item = QTableWidgetItem(str(dato))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.tabla_clientes.setItem(i, j, item)

                cursor.close()
                conexion.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar la lista de clientes: {e}")

    def eliminar_cliente(self):
        fila = self.tabla_clientes.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Advertencia", "Selecciona un cliente para eliminar.")
            return

        id_cliente = self.tabla_clientes.item(fila, 0).text()

        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar al cliente con ID {id_cliente}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        

        if confirmacion == QMessageBox.StandardButton.Yes:
            conexion = conectar()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
                    conexion.commit()
                    cursor.close()
                    conexion.close()
                    QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente")
                    self.cargar_clientes()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar el cliente: {e}")
