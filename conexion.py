import psycopg2

def conectar():
    try:
        conexion = psycopg2.connect(
            dbname="almacen_ropa",
            user="postgres",
            password="David99$",  
            host="localhost",
            port="5432"
        )
        return conexion
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None


