# 🐾 Pasaporte Médico Digital para Mascotas

Aplicación web monolítica para gestionar el historial médico de mascotas: vacunas, desparasitaciones, cirugías y más.

> **Proyecto Integrado 1 — IU Digital (2026)**

---

## 📋 Tabla de Contenidos

- [Stack Tecnológico](#-stack-tecnológico)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación Paso a Paso](#-instalación-paso-a-paso)
- [Configuración de la Base de Datos](#-configuración-de-la-base-de-datos)
- [Ejecutar la Aplicación](#-ejecutar-la-aplicación)
- [¿Cómo Funciona el Proyecto?](#-cómo-funciona-el-proyecto)
- [Guía para Contribuir](#-guía-para-contribuir)
- [Problemas Comunes](#-problemas-comunes)

---

## 🛠 Stack Tecnológico

| Tecnología | Uso | Versión |
|------------|-----|---------|
| **Python** | Lenguaje principal | 3.10+ |
| **Flask** | Framework web (backend) | 3.1 |
| **psycopg2** | Conector a PostgreSQL (precompilado) | 2.9 |
| **PostgreSQL** | Base de datos relacional (en Supabase) | 15+ |
| **Bootstrap 5** | Framework CSS (vía CDN, sin Node.js) | 5.3 |
| **Jinja2** | Motor de plantillas HTML (incluido con Flask) | — |

---

## 📁 Estructura del Proyecto

```
Proyecto Integrado 1 IU Digital/
│
├── app.py                  # Archivo principal de Flask
├── requirements.txt        # Dependencias de Python
├── .env.example            # Plantilla de variables de entorno
├── .gitignore              # Archivos ignorados por Git
├── README.md               # Este archivo
│
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
│   └── css/
│       └── estilos.css     # Estilos personalizados
│
└── templates/              # Plantillas HTML (Jinja2)
    ├── base.html           # Plantilla base (navbar + footer + Bootstrap)
    ├── index.html           # Página de inicio
    └── errores/
        ├── 404.html         # Página "No encontrada"
        └── 500.html         # Página "Error del servidor"
```

---

## ✅ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

1. **Python 3.10 o superior**
   - Descárgalo de [python.org](https://www.python.org/downloads/)
   - Durante la instalación en Windows, **marca la casilla "Add Python to PATH"**
   - Verifica con:
     ```bash
     python --version
     ```

2. **Git**
   - Descárgalo de [git-scm.com](https://git-scm.com/downloads)
   - Verifica con:
     ```bash
     git --version
     ```

3. **Acceso a la base de datos PostgreSQL** (la URL de Supabase y la contraseña los compartirá el líder del equipo)

---

## 🚀 Instalación Paso a Paso

### 1. Clonar el repositorio

```bash
git clone <URL-DEL-REPOSITORIO>
cd "Proyecto Integrado 1 IU Digital"
```

### 2. Crear un entorno virtual

El entorno virtual aísla las dependencias del proyecto para no afectar tu instalación global de Python.

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> 💡 Sabrás que el entorno está activo porque verás `(venv)` al inicio de tu terminal.

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

```bash
# Windows (CMD)
copy .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Luego **abre el archivo `.env`** con tu editor de texto y llena los datos reales:

```env
FLASK_SECRET_KEY=una-clave-secreta-cualquiera
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.kwgoxdgdsvxmkcokfydf.supabase.co:5432/postgres
```

> ⚠️ **NUNCA subas el archivo `.env` a Git.** Ya está incluido en el `.gitignore`.

---

## 🗄 Configuración de la Base de Datos

La conexión a PostgreSQL está configurada en `app.py` y lee los datos desde el archivo `.env`. Usamos **psycopg2-binary** como conector a Supabase.

### Crear las tablas (ejemplo inicial)

Conéctate a tu base de datos PostgreSQL en Supabase (usando el SQL Editor de su panel web, DBeaver, o la terminal) y ejecuta el script SQL que el equipo defina. Por ejemplo:

```sql
CREATE DATABASE IF NOT EXISTS pasaporte_medico;
USE pasaporte_medico;

-- Ejemplo de tabla de mascotas
CREATE TABLE IF NOT EXISTS mascotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(100),
    fecha_nacimiento DATE,
    nombre_dueno VARCHAR(150) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

> 📌 Este es solo un ejemplo. La estructura real de las tablas se definirá conforme avance el proyecto.

---

## ▶️ Ejecutar la Aplicación

Con el entorno virtual activado y el `.env` configurado:

```bash
python app.py
```

Abre tu navegador en: **[http://localhost:5000](http://localhost:5000)**

El servidor se reinicia automáticamente cada vez que guardes un cambio en el código (modo `debug`).

Para detener el servidor, presiona `Ctrl + C` en la terminal.

---

## 🧩 ¿Cómo Funciona el Proyecto?

### Flujo básico de una petición

```
Usuario → Navegador → Flask (app.py) → PostgreSQL → Flask → Jinja2 (HTML) → Navegador
```

1. El usuario visita una URL (ej: `/`).
2. Flask busca la ruta correspondiente en `app.py`.
3. Si la ruta necesita datos, se consulta PostgreSQL en Supabase con psycopg2.
4. Flask renderiza una plantilla HTML con Jinja2 y le pasa los datos.
5. El navegador muestra la página con Bootstrap 5.

### Sistema de plantillas (Jinja2)

- `base.html` → Plantilla madre con la estructura común (navbar, footer, Bootstrap).
- Las demás páginas **heredan** de `base.html` usando `{% extends "base.html" %}`.
- Cada página define su contenido dentro del bloque `{% block contenido %}`.

### Ejemplo: Crear una nueva página

1. Crea un archivo en `templates/`, por ejemplo `templates/mascotas.html`:

```html
{% extends "base.html" %}

{% block titulo %}Mascotas{% endblock %}

{% block contenido %}
<h1>Lista de Mascotas</h1>
<p>Aquí irá el listado de mascotas.</p>
{% endblock %}
```

2. Agrega la ruta en `app.py`:

```python
@app.route('/mascotas')
def mascotas():
    return render_template('mascotas.html')
```

3. Visita `http://localhost:5000/mascotas`.

### Ejemplo: Consultar la base de datos

```python
@app.route('/mascotas')
def mascotas():
    db = obtener_db()
    if db is None:
        return "Error de conexión a la base de datos", 500

    # Usamos DictCursor para que los resultados sean diccionarios y no tuplas
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM mascotas")
    lista = cursor.fetchall()
    cursor.close()

    return render_template('mascotas.html', mascotas=lista)
```

---

## 🤝 Guía para Contribuir

### Flujo de trabajo con Git

1. **Siempre trabaja en una rama nueva**, nunca directamente en `main`:
   ```bash
   git checkout -b feature/nombre-de-tu-funcionalidad
   ```

2. **Haz commits claros y descriptivos:**
   ```bash
   git add .
   git commit -m "Agrega página de listado de mascotas"
   ```

3. **Sube tu rama al repositorio:**
   ```bash
   git push origin feature/nombre-de-tu-funcionalidad
   ```

4. **Crea un Pull Request** para que el equipo revise tu código.

### Convenciones del equipo

- 📝 Todo el código y comentarios van en **español**.
- 🐍 Nombres de variables y funciones en **snake_case** (ej: `obtener_conexion`).
- 📂 Las nuevas plantillas HTML van en la carpeta `templates/`.
- 🎨 Los archivos CSS o JS propios van en `static/css/` o `static/js/`.
- 🚫 **Nunca subas el archivo `.env`** ni la carpeta `venv/` al repositorio.

---

## ❓ Problemas Comunes

### "No se pudo conectar a PostgreSQL"
- Verifica que los datos de tu Supabase en el archivo `.env` sean correctos (fíjate en el puerto, suele ser `5432` o `6543`).
- Verifica que no haya problemas de conectividad de red con el host de Supabase.

### "ModuleNotFoundError: No module named 'flask'"
- Asegúrate de tener el entorno virtual **activado** (debes ver `(venv)` en tu terminal).
- Ejecuta `pip install -r requirements.txt` de nuevo.

### "El archivo `.env` no se encuentra"
- Copia el archivo de ejemplo: `copy .env.example .env` (Windows) o `cp .env.example .env` (Mac/Linux).

### "PermissionError al activar el entorno virtual en PowerShell"
- Ejecuta este comando **una sola vez** como administrador:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```