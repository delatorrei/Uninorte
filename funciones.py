import sqlite3


def sql(query):
    # with sqlite3.connect("test_pass.db") as con:
    with sqlite3.connect("base.sqlite3") as con:
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return data


def check_login(**kwargs):
    nombre = kwargs['Usuario']
    password = kwargs['contrasena']
    query = f'SELECT nombre,password FROM usuario WHERE email="{nombre}"'
    with sqlite3.connect("base.sqlite3") as con:
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchone()
        if not data:
            return False  # si no encuentra coincidencias
        if password == data[1]:
            return True  # si coninciden la contraseña
        return False  # no coincidio la contraseña
