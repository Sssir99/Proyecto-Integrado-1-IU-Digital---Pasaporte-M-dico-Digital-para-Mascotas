"""
============================================
Pasaporte Médico Digital para Mascotas
Archivo principal de la aplicación Flask
============================================
"""

import os
from flask import Flask, render_template, g
import psycopg2
import psycopg2.extras
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

# Configuración de conexión a PostgreSQL (leída desde .env)
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/postgres')


# -----------------------------------------------
# 3. Funciones para manejar la conexión a PostgreSQL
# -----------------------------------------------
def obtener_conexion():
    """
    Crea y retorna una conexión a la base de datos PostgreSQL.
    """
    conexion = psycopg2.connect(app.config['DATABASE_URL'])
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
        except psycopg2.Error as e:
            print(f"[ERROR] No se pudo conectar a PostgreSQL: {e}")
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
