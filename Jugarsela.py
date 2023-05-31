import os
import requests #me lo subraya, pero funciona. preguntar
from passlib.context import CryptContext #me lo subraya, pero funciona. preguntar
import json

def cargar_usuarios()-> dict:
    usuarios = {}
    archivo_usuarios ='usuarios.json'
    if os.path.isfile(archivo_usuarios):
        if os.path.getsize(archivo_usuarios) > 0: #si el archivo no está vacío
            with open(archivo_usuarios, 'r') as file:
                usuarios_str =file.read()
                if usuarios_str:
                    usuarios=json.loads(usuarios_str)
        else: #el archivo estaba vacio
            with open(archivo_usuarios, 'w') as file:
                json.dump(usuarios,file,indent=4)
    return usuarios

def guardar_usuarios(usuarios):
    with open('usuarios.json', 'w') as file:
        json.dump(usuarios,file, indent=4)

def registrar_usuario()-> bool:
    no_se_identifica_usuario:bool= True
    myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

    correo = input("Ingrese correo electrónico: ")
    nombre = input("Ingrese su nombre de usuario:")
    contrasena = myctx.hash(input("Ingrese su contraseña: "))
    dinero = float(input("Ingrese el dinero disponible:"))

    usuarios_str = str(usuarios)
    file.write(usuarios_str)

    # cargo los usuarios existentes
    usuarios = cargar_usuarios()

    usuarios[correo] = {
        'nombre': nombre,
        'contrasena': contrasena,
        'cantidad': 0, #apostada hasta el momento
        'fecha': None, #de la ultima apuesta
        'dinero': dinero
    }

    # actualizo los usuarios
    guardar_usuarios(usuarios)
    print("Registro realizado")
    return True #ver en un futuro que cosas harían que no se registre

def iniciar_sesion() -> bool:
    usuarios=cargar_usuarios()
    no_se_identifica_usuario:bool= True

    myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
    myctx.default_scheme()
    correo = input("Ingrese su correo electrónico:")
    contrasena = input("Ingrese su contraseña: ")

    if correo in usuarios and myctx.verify(contrasena, usuarios[correo]['contrasena']):
        print("Inicio de sesión realizado")
        no_se_identifica_usuario=False
    else:
        print("Contraseña incorrecta")
        no_se_identifica_usuario=True
    return no_se_identifica_usuario

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
    print("1) Listar equipos de la liga argentina") #cambiar
    print("2) ")
    print("3) ")
    
def ejecutar_accion(opcion:str):
    if opcion == "1": #unicamente para testear, no es por si solo una consigna

        equipos = obtener_equipos()
        print("Equipos en la liga argentina:")
        for equipo in equipos:
            print(equipo['team']['name'])

    elif opcion == "2":
        pass
    elif opcion == "3":
        pass
    else:
        print("Error, intente nuevamente (recuerde que debe ingresar un número)")

def main():   
    finalizar = False
    no_se_identifica_usuario:bool= True
    while (no_se_identifica_usuario):
        print("Tiene una cuenta? 1: Si, otro caracter: no")
        if(input() == "1"):
            no_se_identifica_usuario = iniciar_sesion()
        else:
            no_se_identifica_usuario= registrar_usuario()

    while not finalizar:
        mostrar_menu()
        opcion = input()
        if opcion!= "0":
            ejecutar_accion(opcion)
        else:
            finalizar = True
            print("Hasta pronto")
           
main()
