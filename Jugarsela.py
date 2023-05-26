import os
import requests

def cargar_usuarios()->dict:
    usuarios = {}
    # Verifico si el archivo de usuarios existe
    if os.path.isfile('usuarios.json'):
        with open('usuarios.json', 'r') as file:
            usuarios = eval(file.read())
    return usuarios

def guardar_usuarios(usuarios):
    with open('usuarios.json', 'w') as file:
        usuarios_str = str(usuarios)
        file.write(usuarios_str)

def registrar_usuario():
    correo = input("Ingrese correo electrónico: ")
    nombre = input("Ingrese su nombre de usuario: ")
    contrasena = input("Ingrese su contraseña: ")
    dinero = float(input("Ingrese el dinero disponible: "))

    # cargo los usuarios existentes
    usuarios = cargar_usuarios()

    # guardo los datos del usuario
    usuarios[correo]=(nombre, contrasena,0, None,dinero)

    # actualizo los usuarios
    guardar_usuarios(usuarios)
    print("Registro realizado")
    #falta lo de cifrar contraseña

def iniciar_sesion():
    id_usuario = input("Ingrese su correo electrónico:")
    contrasena = input("Ingrese su contraseña: ")

    usuarios = cargar_usuarios()

    # esto tiene que ser con lo del cifrado
    if id_usuario in usuarios and usuarios[id_usuario]["contrasena"] == contrasena:
        print("Inicio de sesion realizado")
    else:
        print("Contraseña incorrecta, vuelva a intentar")

def obtener_equipos()->dict:
    url = "https://v3.football.api-sports.io/teams"
    params = {
        "league": "128",
        "country": "Argentina",
        "season": 2023
    }
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "780851d3b9e161c8b5dddd46f9e9da9a"
    }

    # solicito los equipos de la liga argentina
    respuesta = requests.get(url, params=params, headers=headers)

    # verifico estado de la solicitud
    if respuesta.status_code == 200: #si fue exitosa
        data = respuesta.json()
        equipos = data['response']
        return equipos
    else:
        print("Error en la solicitud:", respuesta.status_code)
        return []

def mostrar_menu():
    #cambiar: primero inicia sesion o se registra, y después vienen las demás opciones
    print("Ingrese una opción:")
    print("0) Salir")
    print("1) Registrarse ")
    print("2) Iniciar sesión ")
    print("3) Listar equipos de la liga argentina")
    
def ejecutar_accion(opcion:str):
    if opcion == "1":
        registrar_usuario()
    elif opcion == "2":
        iniciar_sesion()
    elif opcion == "3":
        equipos = obtener_equipos()
        print("Equipos en la liga argentina:")
        for equipo in equipos:
            print(equipo['team']['name'])
    else:
            print("Error, intente nuevamente (recuerde que debe ingresar un número)")

def main():
    finalizar = False

    while not finalizar:
        mostrar_menu()
        opcion = input()
        if opcion!= "0":
            ejecutar_accion(opcion)
        else:
            finalizar = True
            print("Hasta pronto")
           
main()
