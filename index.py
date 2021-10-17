from os import error
from flask import Flask, render_template, request, jsonify, redirect
from funciones import *


import forms

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisismisecretkey"

@app.route("/", methods=['GET', 'POST'])
def home():
    error = request.args.get('error')
    if error:
        return render_template('Inicio_Sesion.html', error='1')
    return render_template('Inicio_Sesion.html', error='0')


@app.route("/login", methods=['POST'])
def login():
    data = request.form
    res = check_login(Usuario=data['usuario'], contrasena=data['contraseña'])
    if res:
        return redirect('/dashboard')
    return redirect('/?error=1')


@app.route("/dashboard", methods=['GET'])
def home2():
    return render_template('inicio.html')


@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('registrarse.html')
    return jsonify({'msg': 'peticion por post', 'valor': True, 'valor2': None})


app.run(debug=True)
#cursor.execute('SELECT * FROM estudiantes')
#data = cursor.fetchall()
#data[0] = list(data[0])
# print(data)
