from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel
)
from PyQt6.QtGui import QFont, QPixmap, QBrush, QPalette
from PyQt6.QtCore import Qt
from conexion import conectar


class GestionProveedores(QWidget):
    def __init__(self):
        super().__init__()

        self.ruta_fondo = "C:/Users/David Herrera/Downloads/Almacen_contable/imagenes/Imagen de WhatsApp 2025-05-21 a las 09.18.54_15ff6b97.jpg"
        self.setWindowTitle("Gestión de Productos")
        self.setGeometry(200, 100, 1000, 600)
        self.establecer_fondo(self.ruta_fondo)


        self.setWindowTitle("Gestión de Proveedores")
        self.setGeometry(100, 100, 1000, 600)

        layout_principal = QVBoxLayout()

        # --- Título ---
        titulo = QLabel("Gestión de Proveedores")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        titulo.setStyleSheet("color: white;")
        layout_principal.addWidget(titulo)

        # --- Fila de entrada ---
        fila_entradas = QHBoxLayout()

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")
        fila_entradas.addWidget(self.input_nombre)

        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Teléfono")
        fila_entradas.addWidget(self.input_telefono)

        self.input_direccion = QLineEdit()
        self.input_direccion.setPlaceholderText("Dirección")
        fila_entradas.addWidget(self.input_direccion)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")
        fila_entradas.addWidget(self.input_email)

        layout_principal.addLayout(fila_entradas)

        # --- Botones ---
        fila_botones = QHBoxLayout()

        btn_guardar = QPushButton("+ Agregar proveedor")
        btn_guardar.setStyleSheet("background-color: #002244; color: white; padding: 10px; border-radius: 10px;")
        btn_guardar.clicked.connect(self.guardar_proveedor)
        fila_botones.addWidget(btn_guardar)

        btn_eliminar = QPushButton("− Eliminar proveedor")
        btn_eliminar.setStyleSheet("background-color: #002244; color: white; padding: 10px; border-radius: 10px;")
        btn_eliminar.clicked.connect(self.eliminar_proveedor)
        fila_botones.addWidget(btn_eliminar)

        layout_principal.addLayout(fila_botones)

        # --- Tabla ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono", "Dirección", "Email"])
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                font-weight: bold;
                padding: 5px;
            }
        """)

        layout_principal.addWidget(self.tabla)

        self.setLayout(layout_principal)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # Fondo transparente para usar imagen

        self.mostrar_proveedores()

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

    def guardar_proveedor(self):
        nombre = self.input_nombre.text()
        telefono = self.input_telefono.text()
        direccion = self.input_direccion.text()
        email = self.input_email.text()

        if nombre and telefono and direccion and email:
            conexion = conectar()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    sql = """
                        INSERT INTO proveedores (nombre, telefono, direccion, email)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(sql, (nombre, telefono, direccion, email))
                    conexion.commit()
                    cursor.close()
                    conexion.close()
                    QMessageBox.information(self, "Éxito", "Proveedor guardado correctamente")
                    self.input_nombre.clear()
                    self.input_telefono.clear()
                    self.input_direccion.clear()
                    self.input_email.clear()
                    self.mostrar_proveedores()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo guardar el proveedor: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios")

    def mostrar_proveedores(self):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id, nombre, telefono, direccion, email FROM proveedores ORDER BY id ASC")
                resultados = cursor.fetchall()
                self.tabla.setRowCount(0)
                for row_num, row_data in enumerate(resultados):
                    self.tabla.insertRow(row_num)
                    for col_num, data in enumerate(row_data):
                        self.tabla.setItem(row_num, col_num, QTableWidgetItem(str(data)))
                cursor.close()
                conexion.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudieron mostrar los proveedores: {e}")

    def eliminar_proveedor(self):
        fila = self.tabla.currentRow()
        if fila != -1:
            id_proveedor = self.tabla.item(fila, 0).text()
            conexion = conectar()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("DELETE FROM proveedores WHERE id = %s", (id_proveedor,))
                    conexion.commit()
                    cursor.close()
                    conexion.close()
                    QMessageBox.information(self, "Éxito", "Proveedor eliminado correctamente")
                    self.mostrar_proveedores()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar el proveedor: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona un proveedor para eliminar")
