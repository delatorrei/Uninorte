import sqlite3


def sql(query):
    with sqlite3.connect("base.sqlite3") as con:
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return data


def check_login(**kwargs):
    nombre = kwargs['Usuario']
    password = kwargs['contrasena']
    query = f'SELECT u.nombre,u.password,u.tipo,(m.id) as materia FROM usuario u inner JOIN materias m on u.id=m.id_usuario AND u.email="{nombre}"'
    with sqlite3.connect("base.sqlite3") as con:
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchone()
        if not data:
            return False, None  # si no encuentra coincidencias
        if password == data[1]:
            return True, data[2:4] # si coninciden la contraseña
        return False, None  # no coincidio la contraseña


def addActivity(datos, idMaterias):
    print(datos)
    var_file = datos.get("position","")
    var_act = datos["Nombre_de_la_Actividad"]
    var_date = datos["fecha_de_inicio"]
    var_date_end = datos["fecha_de_Entrega"]
    var_description = datos["Descripcion"]

    dbquery = f'INSERT INTO actividades (nombre,fecha_inicio,fecha_fin, id_materia,description, path_files) VALUES ("{var_act}","{var_date}","{var_date_end}",{idMaterias}, "{var_description}", "{var_file}")'

    with sqlite3.connect("base.sqlite3") as con:
        cur = con.cursor()
        cur.execute(dbquery)
        con.commit()

def returnActivity(idMateria):
    dbquery = f"SELECT id, nombre, description, r_image FROM actividades WHERE id_materia={idMateria}" 
    return sql(dbquery)
           

def detalleActividad(id_actividad):
    try:
        dbquery = f"""SELECT (activities.nombre) as Titulo, activities.fecha_fin, activities.path_files, activities.description ,activities.r_image, users.nombre FROM 
    ((actividades activities INNER JOIN materias subjects ON activities.id_materia=subjects.id) INNER JOIN
    usuario users ON users.id=subjects.id_usuario ) WHERE activities.id={id_actividad}"""
        return True, sql(dbquery)[0] 
    except IndexError:
        return False, None