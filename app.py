from flask import Flask,render_template,request,redirect,session
import mysql.connector
import registros

conexion = mysql.connector.connect(host='localhost',
                                    user='root',
                                    password ='tupassword',
                                    db = 'myDB',
                            )

cursor = conexion.cursor()
app = Flask(__name__)
app.secret_key="pbkdf2:sha256"

@app.route('/')
def index_():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/index2.html')
def index2():

    return render_template('index2.html')

@app.route('/index3.html')
def index3():
    return render_template('index3.html', email=session['email'])

@app.route('/citas.html')
def citas():
    pacientes = registros.obtener_citas()
    return render_template('citas.html', pacientes=pacientes, email=session['email'])


#LOGIN
@app.route("/guardar", methods=["POST"])
def guardar():
    email = request.form["email"]
    password= request.form["password"]
    save = f"INSERT INTO usuarios(email, password) VALUES (%s, %s)"
    cursor.execute(save, (email,password))
    conexion.commit()
    cursor.reset()
    return redirect("index2.html")

@app.route('/login', methods=['GET','POST'])
def loginuser():
    msg=''
    if request.method=='POST':
        email =request.form['email']
        password = request.form["password"]
        cursor.execute("SELECT email, password FROM usuarios  WHERE email=%s AND password=%s",(email, password))
        record = cursor.fetchone()
        if record:
            session['logeado']=True
            session['email']= record[0]
            return redirect("/index3.html")
        else:
            msg='no se encontró el usuario o contraseña incorrecto' 
    return render_template('index.html', msg=msg) 

#CRUD
@app.route('/guardar_citas', methods=['POST'])
def guardar_citas():
    nombre = request.form['nombre']
    ApellidoPaterno = request.form['apellido_paterno']
    ApellidoMaterno = request.form['apellido_materno']
    email = request.form['email']
    TipoSangre = request.form['tipo_sangre']
    numero = request.form['numero']
    direccion = request.form['direccion']
    registros.insertar_citas(nombre, ApellidoPaterno ,ApellidoMaterno, email, TipoSangre, numero, direccion)
    return redirect('citas.html')

@app.route('/eliminar_cita', methods=['POST'])
def eliminar_cita():
    registros.eliminar_cita(request.form['id'])
    return redirect ('citas.html')


@app.route("/formulario_editar_cita/<int:id>")
def editar_cita(id):
    cita = registros.obtener_citas_por_id(id)
    return render_template("editar_cita.html", cita=cita)

@app.route("/actualizar_cita", methods=["POST"])
def actualizar_cita():
    id = request.form['id']
    nombre = request.form['nombre']
    apellido_paterno = request.form['apellido_paterno']
    apellido_materno = request.form['apellido_materno']
    email = request.form['email']
    tipo_sangre = request.form['tipo_sangre']
    numero = request.form['numero']
    direccion = request.form['direccion']
    registros.actualizar_cita(nombre, apellido_paterno ,apellido_materno, email, tipo_sangre, numero, direccion, id)
    return redirect("/citas.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)