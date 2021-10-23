from flask import Flask, render_template, redirect, session, flash, request, send_file
from flask.helpers import make_response
import requests
import json
from forms import Login, Registro
from markupsafe import escape
import os
from utils import login_valido, pass_valido, email_valido
from werkzeug.security import check_password_hash, generate_password_hash
from db import accion, seleccion
import traceback
import hashlib
app = Flask(__name__)

app.secret_key = os.urandom(24)
@app.route('/ip')
def ip():
    session['ip'] = request.remote_addr
    response = make_response(redirect('/cookie'))
    response.set_cookie('nombre_cliente', 'MisionTic')
    return response

@app.route('/cookie')
def cookie():
    if session.get('id'):
        ip = session['ip']
    else:
        ip = 'nula'
    
    
    nombre_cliente = request.cookies.get('nombre_cliente')
    if nombre_cliente == None:
        nombre_cliente = 'N/A'
    return f'tu ip es {ip} y tu nombre es {nombre_cliente}'
    


    

@app.route('/')
@app.route('/home/')
@app.route('/index/')
def inicio():
    frm=Login()
    print(generate_password_hash('Mm123456'))
    return render_template('login.html', prueba=frm, titulo='Iniciar Sesión')

@app.route('/', methods=['POST'])
def login():
    frm=Login()
    
    # Recuperar los datos del formulario de forma segura
    usu = escape(frm.usu.data.strip())
    pwd = escape(frm.cla.data.strip())
    # Preparar la consulta
    sql = f'SELECT id, nombre, correo, clave FROM usuario WHERE usuario="{usu}"'
    # Ejecutar la consulta
    res = seleccion(sql)
    # Proceso la respuesta
    if len(res)==0:
        flash('ERROR: Usuario o clave invalidas')
        return render_template('login.html', prueba=frm, titulo='Iniciar Sesión')
    else:
        # Recupero el valor de la clave
        cbd = res[0][3]
        if check_password_hash(cbd, pwd):
            session.clear()
            session['id'] = res[0][0]
            session['nom'] = res[0][1]
            session['usr'] = usu
            session['cla'] = pwd
            session['ema'] = res[0][2]
            return redirect('/message/')
        else:
            flash('ERROR: Usuario o clave invalidas')
            return render_template('login.html', prueba=frm, titulo='Iniciar Sesión')

@app.route('/message/')
def messages():
    usu = session['id']
    print(usu)
    # Preparar la consulta
    sql = f'SELECT de, para, asunto, mensaje FROM mensajes WHERE para={usu}'
    # Ejecutar la consulta
    res = seleccion(sql)
    # Proceso la respuesta
    if len(res)==0:
        return render_template('mensajes.html', titulo=f"No hay mensajes para {session['nom']}", messages=res)
    else:
        return render_template('mensajes.html', titulo=f"Se muestran los mensajes para {session['nom']}", messages=res)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

@app.route('/downloadpdf/')
def downloadpdf():
    return send_file('resource/vision.pdf', as_attachment=True)

@app.route('/downloadimg/')
def downloadimg():
    return send_file('resource/vision.png', as_attachment=True)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    frm = Registro()
    if request.method == 'GET':
        return render_template('registro.html', prueba=frm, titulo='Registro de datos')
    else:
        # Recuperar los datos del formulario
        nom = escape(request.form['nom'])
        usu = escape(request.form['usu'])
        ema = escape(request.form['ema'])
        cla = escape(request.form['cla'])
        ver = escape(request.form['ver'])
        # Validar los datos
        swerror = False
        if nom==None or len(nom)==0:
            flash('ERROR: Debe suministrar un nombre de usuario')
            swerror = True
        if usu==None or len(usu)==0 or not login_valido(usu):
            flash('ERROR: Debe suministrar un usuario válido ')
            swerror = True
        if ema==None or len(ema)==0 or not email_valido(ema):
            flash('ERROR: Debe suministrar un email válido')
            swerror = True
        if cla==None or len(cla)==0 or not pass_valido(cla):
            flash('ERROR: Debe suministrar una clave válida')
            swerror = True
        if ver==None or len(ver)==0 or not pass_valido(ver):
            flash('ERROR: Debe suministrar una verificación de clave válida')
            swerror = True
        if cla!=ver:
            flash('ERROR: La clave y la verificación no coinciden')
            swerror = True
        if not swerror:
            # Preparar la consulta
            sql = "INSERT INTO USUARIO(nombre, usuario, correo, clave) VALUEs (?, ?, ?, ?)"
            # Ejecutar la consulta
            pwd = generate_password_hash(cla)
            res = accion(sql,(nom, usu, ema, pwd))
            # Procesar la respuesta
            if res!=0:
                flash('INFO: Datos almacenados con exito')
            else:
                flash('ERROR: Por favor reintente')
        return render_template('registro.html', prueba=frm, titulo='Registro de datos')

@app.route('/hash')
def hash():
    try:
        hashmd5 = hashlib.md5()
        with open('vision.pdf', "rb") as f:
            for bloque in iter(lambda: f.read(4096), b""):
                hashmd5.update(bloque)
        return hashmd5.hexdigest()
    except Exception as e:
        print("Error: %s" % (e))
        return ""
    except:

        print(traceback.print_exc())
        return ""

if __name__ == '__main__':
    app.run(debug=True, port=5000)


