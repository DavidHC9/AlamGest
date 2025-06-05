from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from conexion import conectar
from datetime import datetime
from collections import defaultdict
from math import exp
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


class GestionFacturas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Facturas")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        self.input_cliente_id = QLineEdit()
        self.input_cliente_id.setPlaceholderText("ID del cliente")
        layout.addWidget(self.input_cliente_id)

        # Campo total oculto porque se calculará automáticamente
        self.input_total = QLineEdit()
        self.input_total.setPlaceholderText("Total")
        self.input_total.setVisible(False)  # Lo ocultamos
        layout.addWidget(self.input_total)

        self.input_producto_id = QLineEdit()
        self.input_producto_id.setPlaceholderText("ID del producto")
        layout.addWidget(self.input_producto_id)

        self.input_cantidad = QLineEdit()
        self.input_cantidad.setPlaceholderText("Cantidad")
        layout.addWidget(self.input_cantidad)

        btn_guardar = QPushButton("Guardar Factura")
        btn_guardar.clicked.connect(self.guardar_factura)
        layout.addWidget(btn_guardar)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Cliente ID", "Fecha", "Total", "Producto ID", "Cantidad", "Precio Unitario"
        ])
        layout.addWidget(self.tabla)

        btn_eliminar = QPushButton("Eliminar Factura Seleccionada")
        btn_eliminar.clicked.connect(self.eliminar_factura)
        layout.addWidget(btn_eliminar)

        btn_grafica = QPushButton("Ver Gráfica de Ventas Mensuales")
        btn_grafica.clicked.connect(self.mostrar_grafica_ventas)
        layout.addWidget(btn_grafica)

        btn_proyeccion = QPushButton("Ver Proyecciones")
        btn_proyeccion.clicked.connect(self.mostrar_proyecciones)
        layout.addWidget(btn_proyeccion)

        btn_imprimir = QPushButton("Imprimir Factura Seleccionada")
        btn_imprimir.clicked.connect(self.imprimir_factura)
        layout.addWidget(btn_imprimir)

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.mostrar_facturas()

    def guardar_factura(self):
        cliente_id = self.input_cliente_id.text()
        producto_id = self.input_producto_id.text()
        cantidad = self.input_cantidad.text()

        if all([cliente_id, producto_id, cantidad]):
            conexion = conectar()
            if conexion:
                try:
                    cursor = conexion.cursor()

                    # Obtener precio unitario y stock desde la tabla productos
                    cursor.execute("SELECT precio_unitario, stock FROM productos WHERE id = %s", (producto_id,))
                    resultado = cursor.fetchone()
                    if not resultado:
                        QMessageBox.warning(self, "Advertencia", "Producto no encontrado.")
                        return

                    precio_unitario, stock_actual = resultado
                    cantidad_int = int(cantidad)

                    if cantidad_int > stock_actual:
                        QMessageBox.warning(self, "Advertencia", "No hay suficiente stock para esa cantidad.")
                        return

                    total = precio_unitario * cantidad_int
                    fecha_actual = datetime.now()

                    # Insertar la factura con el total calculado
                    sql = """
                        INSERT INTO facturas 
                        (cliente_id, fecha, total, producto_id, cantidad, precio_unitario)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        int(cliente_id), fecha_actual, total,
                        int(producto_id), cantidad_int, precio_unitario
                    ))

                    # Actualizar el stock del producto restando la cantidad vendida
                    nuevo_stock = stock_actual - cantidad_int
                    cursor.execute("UPDATE productos SET stock = %s WHERE id = %s", (nuevo_stock, producto_id))

                    conexion.commit()
                    cursor.close()
                    conexion.close()

                    QMessageBox.information(self, "Éxito", "Factura guardada correctamente")
                    self.input_cliente_id.clear()
                    self.input_total.clear()
                    self.input_producto_id.clear()
                    self.input_cantidad.clear()
                    self.mostrar_facturas()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo guardar la factura: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Complete todos los campos")

    def mostrar_facturas(self):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""
                    SELECT factura_id, cliente_id, fecha, total, producto_id, cantidad, precio_unitario
                    FROM facturas
                    ORDER BY factura_id ASC
                """)
                resultados = cursor.fetchall()
                self.tabla.setRowCount(0)
                for row_num, row_data in enumerate(resultados):
                    self.tabla.insertRow(row_num)
                    for col_num, data in enumerate(row_data):
                        self.tabla.setItem(row_num, col_num, QTableWidgetItem(str(data)))
                cursor.close()
                conexion.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudieron mostrar las facturas: {e}")

    def eliminar_factura(self):
        fila = self.tabla.currentRow()
        if fila != -1:
            id_factura = self.tabla.item(fila, 0).text()
            conexion = conectar()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("DELETE FROM facturas WHERE factura_id = %s", (id_factura,))
                    conexion.commit()
                    cursor.close()
                    conexion.close()
                    QMessageBox.information(self, "Éxito", "Factura eliminada correctamente")
                    self.mostrar_facturas()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar la factura: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona una factura para eliminar")

    def mostrar_grafica_ventas(self):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT fecha, total FROM facturas")
                resultados = cursor.fetchall()
                cursor.close()
                conexion.close()

                ventas_mensuales = defaultdict(float)
                for fecha, total in resultados:
                    mes = fecha.strftime('%Y-%m')
                    ventas_mensuales[mes] += float(total)

                if not ventas_mensuales:
                    QMessageBox.information(self, "Sin datos", "No hay datos de ventas para graficar.")
                    return

                meses_ordenados = sorted(ventas_mensuales.keys())
                totales = [ventas_mensuales[mes] for mes in meses_ordenados]

                self.canvas.figure.clear()
                ax = self.canvas.figure.add_subplot(111)
                ax.plot(meses_ordenados, totales, marker='o', linestyle='-', color='green')
                ax.set_title("Ventas Mensuales")
                ax.set_xlabel("Mes")
                ax.set_ylabel("Total Vendido")
                ax.grid(True)
                self.canvas.draw()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo generar la gráfica: {e}")

    def mostrar_proyecciones(self):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT SUM(total) FROM facturas")
                resultado = cursor.fetchone()
                cursor.close()
                conexion.close()

                if resultado and resultado[0]:
                    c0 = float(resultado[0])
                    K = 0.5
                    t = 1
                    c1 = c0 * exp(K * t)

                    self.canvas.figure.clear()
                    ax = self.canvas.figure.add_subplot(111)
                    ax.bar(["Ingreso Actual", "Proyección 1 Año"], [c0, c1], color=["blue", "orange"])
                    ax.set_title("Proyección de Ingresos a 1 Año")
                    ax.set_ylabel("Total Proyectado")
                    for i, val in enumerate([c0, c1]):
                        ax.text(i, val + val * 0.02, f"${val:,.2f}", ha='center')
                    self.canvas.draw()
                else:
                    QMessageBox.information(self, "Sin datos", "No hay ventas registradas para proyectar.")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo calcular la proyección: {e}")

    def imprimir_factura(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Advertencia", "Selecciona una factura para imprimir")
            return

        id_factura = self.tabla.item(fila, 0).text()
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""
                    SELECT f.factura_id, f.cliente_id, f.fecha, f.total,
                           f.producto_id, f.cantidad, f.precio_unitario,
                           c.nombre, p.nombre
                    FROM facturas f
                    JOIN clientes c ON f.cliente_id = c.id
                    JOIN productos p ON f.producto_id = p.id
                    WHERE f.factura_id = %s
                """, (id_factura,))
                factura = cursor.fetchone()
                cursor.close()
                conexion.close()

                if factura:
                    (factura_id, cliente_id, fecha, total,
                     producto_id, cantidad, precio_unitario,
                     nombre_cliente, nombre_producto) = factura

                    nombre_archivo = f"factura_{factura_id}.pdf"
                    ruta = os.path.join(os.getcwd(), nombre_archivo)

                    c = canvas.Canvas(ruta, pagesize=letter)
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(50, 750, "Almacén y Variedades Ned Sport")
                    c.setFont("Helvetica", 12)
                    c.drawString(50, 735, f"Factura #: {factura_id}")
                    c.drawString(50, 720, f"Fecha: {fecha.strftime('%Y-%m-%d %H:%M')}")
                    c.drawString(50, 705, f"Cliente ID: {cliente_id}")
                    c.drawString(50, 690, f"Nombre del Cliente: {nombre_cliente}")
                    c.drawString(50, 670, "Detalle de Producto:")

                    c.drawString(60, 650, f"Producto: {nombre_producto} (ID: {producto_id})")
                    c.drawString(60, 635, f"Cantidad: {cantidad}")
                    c.drawString(60, 620, f"Precio Unitario: ${precio_unitario:,.2f}")

                    c.drawString(50, 600, f"Total: ${total:,.2f}")
                    c.drawString(50, 570, "Gracias por su compra.")
                    c.save()

                    QMessageBox.information(self, "Factura Generada", f"Se generó '{nombre_archivo}'.")
                    os.startfile(ruta)  # Solo para Windows
                else:
                    QMessageBox.warning(self, "Error", "No se encontró la factura.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo imprimir la factura: {e}")
