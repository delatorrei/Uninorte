import os
from flask import Flask, render_template, request, jsonify, redirect, session


from funciones import *
 
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
    print(data)
    res, colums = check_login(Usuario=data['Usuario'], contrasena=data['contrasena'])
    if res:
        session["tipo"] = colums[0]
        session["materia"] = colums[1]
        return redirect('/dashboard')
    return redirect('/?error=1')


@app.route("/dashboard", methods=['GET'])
def home2():
    logueado = session.get("tipo", None)
    if logueado==2:
        registros = returnActivity(session["materia"])
        print(registros)
        return render_template('inicio_profesor.html', pendientes=registros)
    elif logueado==3:
        return render_template('inicio_estudiante.html')
    return "<h1>No te has logueado</h1>"

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('registrarse.html')
    return jsonify({'msg': 'peticion por post', 'valor': True, 'valor2': None})


@app.route("/Crear_actividad", methods=['GET', 'POST'])
def crearActividad():
    if request.method== "GET" and session.get("tipo") == 2:
        return render_template('crear_actividad.html')
    elif request.method== "GET":    
        return "Usted No tiene permiso a este recurso"
    elif request.method == "POST" and session.get("tipo") == 2:
        id_materia = session.get("materia")
        if not id_materia:
            return "<h1> Error en Datos de asignatura</h1>"
        data = dict(request.form).copy()
        archivo = request.files.get("file")
        if archivo:
            archivo.save(os.getcwd() +"/static/media/"+archivo.filename)
            data["position"] = "/media/" + archivo.filename
        addActivity(data, id_materia)
        return render_template('crear_actividad.html')


@app.route("/actividades/Detalles/<checkin>")
def detalle(checkin):
    

    if not session.get("tipo"):
        return "<h1>No has iniciado Sesion<h1>"
    detail, datail2 = detalleActividad(checkin) # Detail1 toma un valor bool y detail 2 son detalles de actividad
    if detail:
        return render_template("ver_actividad.html", data=datail2)
    else:
        return "No existe la actividad"

app.run(debug=True)
#cursor.execute('SELECT * FROM estudiantes')
#data = cursor.fetchall()
#data[0] = list(data[0])
# print(data)
