from hashlib import sha512
from werkzeug.security import generate_password_hash, check_password_hash

m = sha512(b'Hola')
print(f'Hola :: {m.digest()}')
print(f'Hola :: {m.hexdigest()}')

m = sha512(b'Holo')
print(f'Holo :: {m.digest()}')
print(f'Holo :: {m.hexdigest()}')

has1 = generate_password_hash('2')
has2 = generate_password_hash('2') 
print(has1)
print(has2)

if check_password_hash(has1,'2'):
    print("Acceso concedido")
else:
    print("Acceso denegado")

if check_password_hash(has2,'2'):
    print("Acceso concedido")
else:
    print("Acceso denegado")