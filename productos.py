from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QBrush, QPalette
from conexion import conectar


class GestionProductos(QWidget):
    def __init__(self):
        super().__init__()
        self.ruta_fondo = "C:/Users/David Herrera/Downloads/Almacen_contable/imagenes/Imagen de WhatsApp 2025-05-21 a las 09.18.54_15ff6b97.jpg"
        self.setWindowTitle("Gestión de Productos")
        self.setGeometry(200, 100, 1000, 600)
        self.establecer_fondo(self.ruta_fondo)

        layout_principal = QVBoxLayout()

        # --- Título ---
        titulo = QLabel("Gestión de Productos")
        titulo.setStyleSheet("color: white")
        titulo.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo)

        # --- Formulario de ingreso de productos ---
        formulario_layout = QHBoxLayout()
        self.inputs = {
            "nombre": QLineEdit(),
            "descripcion": QLineEdit(),
            "precio_unitario": QLineEdit(),
            "stock": QLineEdit(),
            "proveedor_id": QLineEdit(),
        }

        for key, input_ in self.inputs.items():
            input_.setPlaceholderText(key.capitalize())
            input_.setFixedWidth(150)
            formulario_layout.addWidget(input_)

        layout_principal.addLayout(formulario_layout)

        # --- Botones ---
        botones_layout = QHBoxLayout()
        self.boton_agregar = QPushButton("＋ Agregar producto")
        self.boton_agregar.setStyleSheet("background-color: #071d35; color: white; padding: 10px; font-weight: bold; border-radius: 10px;")
        self.boton_agregar.clicked.connect(self.guardar_producto)
        botones_layout.addWidget(self.boton_agregar)

        self.boton_eliminar = QPushButton("－ Eliminar Producto")
        self.boton_eliminar.setStyleSheet("background-color: #071d35; color: white; padding: 10px; font-weight: bold; border-radius: 10px;")
        self.boton_eliminar.clicked.connect(self.eliminar_producto)
        botones_layout.addWidget(self.boton_eliminar)

        layout_principal.addLayout(botones_layout)

        # --- Tabla de productos ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Precio_unitario", "Stock", "Proveedor ID"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout_principal.addWidget(self.tabla)

        self.setLayout(layout_principal)
        self.mostrar_productos()

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

    # --- Guardar producto ---
    def guardar_producto(self):
        valores = {k: v.text() for k, v in self.inputs.items()}
        if all(valores.values()):
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                sql = "INSERT INTO productos (nombre, descripcion, precio_unitario, stock, proveedor_id) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (
                    valores["nombre"],
                    valores["descripcion"],
                    float(valores["precio_unitario"]),
                    int(valores["stock"]),
                    int(valores["proveedor_id"]) if valores["proveedor_id"].isdigit() else None
                ))
                conexion.commit()
                cursor.close()
                conexion.close()
                QMessageBox.information(self, "Éxito", "Producto guardado correctamente")
                for v in self.inputs.values():
                    v.clear()
                self.mostrar_productos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el producto: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Todos los campos deben estar completos")

    # --- Mostrar productos ---
    def mostrar_productos(self):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, descripcion, precio_unitario, stock, proveedor_id FROM productos")
            resultados = cursor.fetchall()
            self.tabla.setRowCount(0)
            for fila, datos in enumerate(resultados):
                self.tabla.insertRow(fila)
                for columna, valor in enumerate(datos):
                    self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))
            cursor.close()
            conexion.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los productos: {e}")

    # --- Eliminar producto ---
    def eliminar_producto(self):
        fila = self.tabla.currentRow()
        if fila != -1:
            id_producto = self.tabla.item(fila, 0).text()
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
                conexion.commit()
                cursor.close()
                conexion.close()
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
                self.mostrar_productos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un producto para eliminar")
