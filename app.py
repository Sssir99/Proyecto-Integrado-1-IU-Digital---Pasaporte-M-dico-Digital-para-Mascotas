"""
============================================
Pasaporte Médico Digital para Mascotas
Archivo principal de la aplicación Flask
============================================
"""

import os
from flask import Flask, render_template, g
import pymysql
from dotenv import load_dotenv

# -----------------------------------------------
# 1. Cargar variables de entorno desde el archivo .env
# -----------------------------------------------
load_dotenv()

# -----------------------------------------------
# 2. Crear y configurar la aplicación Flask
# -----------------------------------------------
app = Flask(__name__)

# Clave secreta necesaria para sesiones y protección CSRF
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'clave-por-defecto-cambiar-en-produccion')

# Configuración de conexión a MySQL (leída desde .env)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'pasaporte_medico')


# -----------------------------------------------
# 3. Funciones para manejar la conexión a MySQL
# -----------------------------------------------
def obtener_conexion():
    """
    Crea y retorna una conexión a la base de datos MySQL.
    Usa PyMySQL con cursores tipo diccionario para que los
    resultados se devuelvan como dict en lugar de tuplas.
    """
    conexion = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        port=app.config['MYSQL_PORT'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # Resultados como diccionarios
    )
    return conexion


def obtener_db():
    """
    Obtiene la conexión a la BD para la petición actual.
    Si ya existe una conexión abierta en 'g', la reutiliza.
    'g' es un objeto especial de Flask que dura una sola petición HTTP.
    """
    if 'db' not in g:
        try:
            g.db = obtener_conexion()
        except pymysql.MySQLError as e:
            print(f"[ERROR] No se pudo conectar a MySQL: {e}")
            g.db = None
    return g.db


@app.teardown_appcontext
def cerrar_conexion(exception):
    """
    Cierra automáticamente la conexión a la BD al finalizar
    cada petición HTTP. Flask llama esta función por nosotros.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


# -----------------------------------------------
# 4. Rutas de la aplicación
# -----------------------------------------------
@app.route('/')
def index():
    """
    Ruta principal — Renderiza la página de inicio.
    """
    return render_template('index.html')


# -----------------------------------------------
# 5. Manejo de errores comunes
# -----------------------------------------------
@app.errorhandler(404)
def pagina_no_encontrada(error):
    """Se muestra cuando el usuario visita una URL que no existe."""
    return render_template('errores/404.html'), 404


@app.errorhandler(500)
def error_interno(error):
    """Se muestra cuando ocurre un error inesperado en el servidor."""
    return render_template('errores/500.html'), 500


# -----------------------------------------------
# 6. Punto de entrada de la aplicación
# -----------------------------------------------
if __name__ == '__main__':
    # debug=True recarga el servidor automáticamente al guardar cambios.
    # ¡IMPORTANTE! Desactivar debug en producción.
    app.run(debug=True, port=5000)
