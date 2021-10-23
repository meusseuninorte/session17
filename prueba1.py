from db import seleccion
from werkzeug.security import check_password_hash

usu = 'ntorres'
pwd = 'Papa25'

sql = f'SELECT id, nombre, correo, clave FROM usuario WHERE usuario="{usu}"'
# Ejecutar la consulta
print(sql)
res = seleccion(sql)
print(res)
# Proceso la respuesta
if len(res)==0:
    print("No se recueperaron datos de la base de datos")
else:
    # Recupero el valor de la clave
    cbd = res[0][3]
    print(cbd)
    if check_password_hash(cbd, pwd):
        print("Acceso concedido")
    else:
        print("Acceso denegado")