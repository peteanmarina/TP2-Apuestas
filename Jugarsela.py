import os
import requests
from passlib.context import CryptContext
import csv

def cargar_usuarios() -> dict:
    usuarios = {}
    archivo_usuarios = 'usuarios.csv'
    
    if os.path.isfile(archivo_usuarios): # si el archivo existe
        with open(archivo_usuarios, 'r', encoding='UTF-8') as archivo_csv: # modo lectura
            csv_reader = csv.reader(archivo_csv, delimiter=',')
            next(csv_reader)  # Leer la primera línea (encabezado)
            for row in csv_reader:
                correo = row[0]
                usuarios[correo] = {
                    'nombre': row[1],
                    'contrasena': row[2],
                    'cantidad': float(row[3]),
                    'fecha': row[4],
                    'dinero': float(row[5])
                }
    return usuarios

def guardar_usuarios(usuarios):
    
    with open('usuarios.csv', 'w', newline='', encoding='UTF-8') as archivo_csv:
        csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['correo', 'nombre', 'contrasena', 'cantidad', 'fecha', 'dinero'])  # Escribir el encabezado
        
        for correo, datos in usuarios.items():
            csv_writer.writerow([
                correo,
                datos['nombre'],
                datos['contrasena'],
                datos['cantidad'],
                datos['fecha'],
                datos['dinero']
            ])

def registrar_usuario()-> bool:
    no_se_identifica_usuario:bool= True
    myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

    correo = input("Ingrese correo electrónico: ")
    nombre = input("Ingrese su nombre de usuario:")
    contrasena = myctx.hash(input("Ingrese su contraseña: "))
    dinero = float(input("Ingrese el dinero disponible:"))
    
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
    return False #ver en un futuro que cosas harían que no se registre

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

def mostrar_plantel(id_equipo:int)->None:
    url = "https://v3.football.api-sports.io/players"
    params = {
        "league": "128",
        "season": 2023,
        "team": id_equipo
    }

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "780851d3b9e161c8b5dddd46f9e9da9a"
    }
    
    # solicito equipo indicado por parametro
    respuesta = requests.get(url, params=params, headers=headers)

    # verifico estado de la solicitud
    if respuesta.status_code == 200: #si fue exitosa
        data = respuesta.json()
        plantel = data['response']
        for jugador in plantel:
            print(jugador['player']['name'])
    else:
        print("Error en la solicitud:", respuesta.status_code)

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
    print("Ingrese el número correspondiente a la opción que desee:")
    print("0) Salir")
    print("1) Mostrar el plantel completo de un equipo ingresado") #incompleto
    print("2) Mostrar la tabla de posiciones de la Liga profesional, ingresando la temporada")
    print("3) Mostrar toda la información posible sobre el estadio y escudo de un equipo")
    print("4) Mostrar los goles y los minutos en los que fueron realizados para un equipo")
    print("5) Cargar dinero en cuenta de usuario")
    
def ejecutar_accion(opcion:str):
    if opcion == "1": #unicamente para testear, no es por si solo una consigna

        equipos = obtener_equipos()
        print("Equipos de la Liga Profesional correspondiente a la temporada 2023:")
        for equipo in equipos:
            print(equipo['team']['name'])
            print(equipo['team']['id'])
        print("Ingrese nombre del equipo que desee ver el plantel")
        equipo_elegido= input()
        for equipo in equipos:
            if(equipo_elegido == equipo['team']['name']):
                print()
                print(f"Elegiste ver plantel de ",equipo['team']['name'])
                id=equipo['team']['id']
        mostrar_plantel(id)
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