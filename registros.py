from db import obtener_conexion


def insertar_citas(nombre, ApellidoPaterno,ApellidoMaterno,email,TipoSangre,numero, direccion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO pacientes(nombre, ApellidoPaterno, ApellidoMaterno,email,TipoSangre,numero,direccion) VALUES (%s, %s, %s,%s, %s, %s, %s)",
                        (nombre, ApellidoPaterno,ApellidoMaterno,email,TipoSangre,numero, direccion))
    conexion.commit()
    conexion.close()


def obtener_citas():
    conexion = obtener_conexion()
    citas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, ApellidoPaterno,ApellidoMaterno,email,TipoSangre,numero, direccion FROM pacientes")
        citas = cursor.fetchall()
    conexion.close()
    return citas


def eliminar_cita(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM pacientes WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_citas_por_id(id):
    conexion = obtener_conexion()
    cita = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT  id, nombre, ApellidoPaterno,ApellidoMaterno,email,TipoSangre,numero, direccion FROM pacientes WHERE id = %s", (id,))
        cita = cursor.fetchone()
    conexion.close()
    return cita


def actualizar_cita(nombre, ApellidoPaterno,ApellidoMaterno,email,TipoSangre,numero, direccion,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE pacientes SET nombre = %s, ApellidoPaterno = %s, ApellidoMaterno = %s, email = %s, TipoSangre = %s, numero = %s, direccion = %s WHERE id = %s",
                        (nombre, ApellidoPaterno,ApellidoMaterno,email,TipoSangre,numero, direccion, id))
    conexion.commit()
    conexion.close()