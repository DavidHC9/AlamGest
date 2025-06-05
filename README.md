# ALMAGEST 📦
*Más control, menos preocupaciones*

## 📋 Descripción del Proyecto

**ALMAGEST** es un sistema integral de gestión de almacén desarrollado en Python con PyQt6. El proyecto está diseñado para pequeñas y medianas empresas que necesitan un control eficiente de su inventario, clientes, proveedores y facturación.

## 🎯 Objetivo

Proporcionar una solución completa y fácil de usar para la gestión de almacenes, permitiendo a los usuarios:
- Controlar el inventario de productos en tiempo real
- Gestionar información de clientes y proveedores
- Generar facturas automáticamente
- Visualizar análisis de ventas y proyecciones
- Mantener un registro completo de transacciones

## 🛠️ Tecnologías Utilizadas

- **Python 3.x** - Lenguaje de programación principal
- **PyQt6** - Framework para la interfaz gráfica de usuario
- **MySQL** - Base de datos para almacenamiento de información
- **Matplotlib** - Generación de gráficos y análisis de ventas
- **ReportLab** - Generación de facturas en PDF
- **Webbrowser** - Integración con páginas web de contacto

### Librerías Python
```
PyQt6
mysql-connector-python
matplotlib
reportlab
datetime
collections
math
os
sys
```

## 📥 Instalación

### Prerrequisitos
- Python 3.8 o superior
- MySQL Server instalado y configurado
- Pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/usuario/almagest.git
   cd almagest
   ```

2. **Instalar dependencias**
   ```bash
   pip install PyQt6
   pip install mysql-connector-python
   pip install matplotlib
   pip install reportlab
   ```

3. **Configurar la base de datos**
   - Crear una base de datos MySQL llamada `almacen_db`
   - Ejecutar el script de creación de tablas (incluido en el proyecto)
   - Configurar las credenciales de conexión en el archivo `conexion.py`

4. **Configurar rutas de archivos**
   - Actualizar las rutas de las imágenes de fondo y logo en los archivos Python
   - Asegurar que las carpetas de imágenes existan en el sistema

## 🚀 Ejecución

Para ejecutar la aplicación, utilizar el siguiente comando desde la carpeta del proyecto:

```bash
python main.py
```

O ejecutar directamente el archivo principal:
```bash
python VentanaPrincipal.py
```

## 📊 Funcionalidades Principales

### 🏠 Ventana Principal
- Interfaz intuitiva con acceso directo a todos los módulos
- Diseño moderno con fondo personalizado
- Navegación sencilla entre secciones

### 📦 Gestión de Productos
- Agregar, editar y eliminar productos
- Control de stock en tiempo real
- Vinculación con proveedores
- Precios y descripciones detalladas

### 👥 Gestión de Clientes
- Registro completo de información de clientes
- Histórico de compras
- Gestión de contactos y direcciones

### 🏢 Gestión de Proveedores
- Base de datos de proveedores
- Información de contacto completa
- Vinculación con productos suministrados

### 🧾 Sistema de Facturación
- Generación automática de facturas
- Cálculo automático de totales
- Actualización automática de inventario
- Exportación a PDF
- Gráficos de ventas mensuales
- Proyecciones de ingresos

### 📈 Análisis y Reportes
- Gráficos de ventas por período
- Proyecciones de crecimiento
- Reportes de inventario
- Análisis de tendencias

## 📁 Estructura del Proyecto

```
ALMAGEST/
│
├── main.py                 # Archivo principal de ejecución
├── VentanaPrincipal.py     # Ventana principal de la aplicación
├── productos.py            # Módulo de gestión de productos
├── clientes.py             # Módulo de gestión de clientes
├── proveedores.py          # Módulo de gestión de proveedores
├── facturas.py             # Módulo de facturación y análisis
├── conexion.py             # Configuración de base de datos
├── imagenes/               # Carpeta de recursos gráficos
│   ├── fondo.jpg          # Imagen de fondo
│   └── logo.png           # Logo de la aplicación
└── README.md              # Documentación del proyecto
```

## 🗄️ Base de Datos

El sistema utiliza MySQL con las siguientes tablas principales:

- **productos**: Información de productos e inventario
- **clientes**: Datos de clientes
- **proveedores**: Información de proveedores
- **facturas**: Registro de ventas y facturación

## 🖼️ Capturas de Pantalla

*[Aquí se incluirían capturas de pantalla o GIFs mostrando la aplicación en funcionamiento]*

### Ventana Principal
- Interfaz moderna con navegación intuitiva

### Gestión de Productos
- Tabla interactiva con funciones CRUD completas

### Sistema de Facturación
- Generación automática con cálculos en tiempo real

### Análisis de Ventas
- Gráficos interactivos y proyecciones

## 🔧 Configuración Adicional

### Personalización de Rutas
Actualizar las siguientes rutas en los archivos correspondientes:
- Ruta de imágenes de fondo
- Ruta del logo
- Configuración de base de datos

### Base de Datos
```sql
-- Ejemplo de configuración en conexion.py
HOST = 'localhost'
USER = 'tu_usuario'
PASSWORD = 'tu_contraseña'
DATABASE = 'almacen_db'
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📞 Soporte y Contacto

Para soporte técnico o consultas sobre el proyecto, contactar a través de la función "Contáctame" en la aplicación o mediante los canales académicos correspondientes.

## 🔮 Futuras Mejoras

- [ ] Implementación de backup automático
- [ ] Módulo de compras a proveedores
- [ ] Sistema de alertas de stock mínimo
- [ ] Integración con códigos de barras
- [ ] Versión web responsive
- [ ] API REST para integración externa

## 📄 Licencia

Este proyecto está desarrollado con fines académicos y de aprendizaje.

---

## 👨‍💻 Créditos y Autores

**Desarrollado por:**

### David Herrera Carvajal
- **Contacto Académico:** [email académico]
- **Rol:** Desarrollador Full Stack
- **Contribuciones:** Arquitectura del sistema, interfaz gráfica, módulos de gestión

### Tomas Montoya Bolívar  
- **Contacto Académico:** [email académico]
- **Rol:** Desarrollador Full Stack
- **Contribuciones:** Base de datos, sistema de facturación, análisis de datos

---

*Proyecto desarrollado como parte del programa académico - Gestión de Sistemas de Información*

**ALMAGEST** - *Transformando la gestión de almacenes con tecnología moderna*
