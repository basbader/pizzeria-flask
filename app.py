from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para usar flash

# Función para conectar a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('pizzeria.db')
    conn.row_factory = sqlite3.Row  # Para acceder a los resultados como diccionarios
    return conn

# Crear la base de datos y la tabla de pedidos (si no existe)
def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS pedidos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT,
                            telefono TEXT,
                            direccion TEXT,
                            correo TEXT,
                            tipo_pizza TEXT,
                            tamano TEXT,
                            promo INTEGER,
                            condiciones INTEGER
                        )''')
    conn.close()

# Ruta de la página principal (inicio.html)
@app.route('/')
def inicio():
    return render_template('inicio.html')

# Ruta de la página del menú (menu.html)
@app.route('/menu')
def menu():
    return render_template('menu.html')

# Ruta de la página de nosotros (nosotros.html)
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# Ruta de la página de pedido (pedido.html)
@app.route('/pedido', methods=['GET', 'POST'])
def pedido():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        correo = request.form.get('correo')
        tipo_pizza = request.form.get('tipo_pizza')
        tamano = request.form.get('tamano')

        # Verificar si el checkbox de información está marcado
        info = 1 if request.form.get('info') == 'on' else 0

        # Verificar si el checkbox de condiciones está marcado
        condiciones = 1 if request.form.get('condiciones') == 'on' else 0

        # Verificar si se aceptaron los términos
        if condiciones == 0:
            flash("Debe aceptar los términos y condiciones para continuar.", 'danger')
            return redirect(url_for('pedido'))

        # Guardar el pedido en la base de datos
        try:
            conn = get_db_connection()
            conn.execute(''' 
                INSERT INTO pedidos (nombre, telefono, direccion, correo, tipo_pizza, tamano, promo, condiciones) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (nombre, telefono, direccion, correo, tipo_pizza, tamano, info, condiciones)
            )
            conn.commit()
            conn.close()

            flash('¡Tu pedido ha sido recibido con éxito! 🎉', 'success')
            return redirect(url_for('pedido'))
        except Exception as e:
            flash(f"Hubo un error al guardar el pedido: {str(e)}", 'danger')
            return redirect(url_for('pedido'))

    return render_template('pedido.html')

if __name__ == '__main__':
    init_db()  # Crear la base de datos si no existe
    app.run(debug=True)
