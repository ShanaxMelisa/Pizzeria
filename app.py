from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pizzerianueva'

mysql = MySQL(app)

# Configuración secreta
app.secret_key = 'mysecretkey'

@app.route('/')
def inicio():
    return render_template('inicio.html')
@app.route('/recepcion')
def recepcion():
    return render_template('recepcion.html')

@app.route('/inicio')
def login():
    return render_template('inicio.html')

@app.route('/registro')
def register():
    return render_template('registro.html')


@app.route('/catalogo')
def catalogo_pizzas(): 
    return render_template('catalogo.html')

@app.route('/hacer_pedido')
def hacer_pedido():
    return render_template('hacer_pedido.html')


@app.route('/recibir_pedido', methods=['POST'])
def recibir_pedido():
    if request.method == 'POST':
        nombre = request.form.get('nombre')  
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        producto = request.form.get('producto')
        cantidad = request.form.get('cantidad')

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO pedidos (nombre, direccion, telefono, producto, cantidad) VALUES (%s, %s, %s, %s, %s)', 
                    (nombre, direccion, telefono, producto, cantidad))
        mysql.connection.commit()
        cur.close()
        
        flash('El registro fue un exito')
        
        return render_template('hacer_pedido.html')

@app.route('/pedidos')
def pedidos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pedidos')
    pedido = cur.fetchall()
    return render_template('pedidos.html', pedidos=pedido)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    cliente = cur.fetchall()
    return render_template('clientes.html',clientes=cliente)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000, debug=True)
