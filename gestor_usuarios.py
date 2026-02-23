# ==============================
# GESTION DE USUARIOS
# ==============================
import json 
from gestor_logs import registrar_evento

def cargar_usuarios():
    try:
        with open("usuarios.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}

def guardar_usuarios(usuarios):
    with open("usuarios.json", "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

def registrar_usuario(usuarios, usuario_actual=None):
    print("\n1. Registrar usuario\n")

    # Validar identificacion
    identificacion = input("Ingresa tu # identificacion: ").strip()
    
    if not identificacion:
        print("Error: La identificacion no puede estar vacia.")
        return
    
    if not identificacion.isdigit():
        print("Error: La identificacion debe contener solo numeros.")
        return
    
    if len(identificacion) < 6 or len(identificacion) > 15:
        print("Error: La identificacion debe tener entre 6 y 15 digitos.")
        return

    if identificacion in usuarios:
        print("Error: ya existe un usuario con esa identificacion.")
        registrar_evento("ERROR", "Intento de registrar usuario con ID duplicado: " + identificacion, usuario_actual)
        return

    # Validar nombre
    nombre = input("Nombre: ").strip()
    
    if not nombre:
        print("Error: El nombre no puede estar vacio.")
        return
    
    if not nombre.replace(" ", "").isalpha():
        print("Error: El nombre debe contener solo letras.")
        return
    
    if len(nombre) < 2:
        print("Error: El nombre debe tener al menos 2 caracteres.")
        return
    
    # Validar apellido
    apellido = input("Apellido: ").strip()
    
    if not apellido:
        print("Error: El apellido no puede estar vacio.")
        return
    
    if not apellido.replace(" ", "").isalpha():
        print("Error: El apellido debe contener solo letras.")
        return
    
    if len(apellido) < 2:
        print("Error: El apellido debe tener al menos 2 caracteres.")
        return
    
    # Validar telefono
    telefono = input("Telefono (10 digitos): ").strip()
    
    if not telefono:
        print("Error: El telefono no puede estar vacio.")
        return
    
    if not telefono.isdigit():
        print("Error: El telefono debe contener solo numeros.")
        return
    
    if len(telefono) != 10:
        print("Error: El telefono debe tener exactamente 10 digitos.")
        return
    
    # Validar direccion
    direccion = input("Direccion: ").strip()
    
    if not direccion:
        print("Error: La direccion no puede estar vacia.")
        return
    
    if len(direccion) < 5:
        print("Error: La direccion debe tener al menos 5 caracteres.")
        return
    
    tipos_validos = ["residente", "administrador"]
    tipo = input("Tipo (residente/administrador): ").lower()
    
    if tipo not in tipos_validos:
        print("Error: Tipo de usuario invalido. Opciones: residente, administrador")
        return

    usuarios[identificacion] = {
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "direccion": direccion,
        "tipo": tipo
    }

    guardar_usuarios(usuarios)
    print("Usuario registrado correctamente.")
    registrar_evento("INFO", "Usuario registrado: " + identificacion + " - " + nombre + " " + apellido + " (" + tipo + ")", usuario_actual)

def listar_usuarios(usuarios):
    print("\n2. Listar usuarios\n")

    if not usuarios:
        print("No hay usuarios registrados.")
        return

    for identificacion, usuario in usuarios.items():
        print("\nID: " + identificacion)
        print("Nombre: " + usuario['nombre'] + " " + usuario['apellido'])
        print("Telefono: " + usuario['telefono'])
        print("Direccion: " + usuario['direccion'])
        print("Tipo: " + usuario['tipo'])
        print("---------------------------")

def consultar_usuario(usuarios):
    identificacion = input("Ingrese la identificacion: ")

    if identificacion not in usuarios:
        print("Usuario no encontrado.")
        return
    
    usuario = usuarios[identificacion]

    print("\nID: " + identificacion)
    print("Nombre: " + usuario['nombre'] + " " + usuario['apellido'])
    print("Telefono: " + usuario['telefono'])
    print("Direccion: " + usuario['direccion'])
    print("Tipo: " + usuario['tipo'])

def actualizar_usuario(usuarios, usuario_actual=None):
    identificacion = input("Ingrese la identificacion: ").strip()

    if identificacion not in usuarios:
        print("Usuario no encontrado.")
        return

    usuario = usuarios[identificacion]

    # Validar nuevo nombre
    nuevo_nombre = input("Nuevo nombre (Enter para mantener): ").strip()
    if nuevo_nombre:
        if not nuevo_nombre.replace(" ", "").isalpha():
            print("Advertencia: El nombre debe contener solo letras. Ignorado.")
            nuevo_nombre = ""
        elif len(nuevo_nombre) < 2:
            print("Advertencia: El nombre debe tener al menos 2 caracteres. Ignorado.")
            nuevo_nombre = ""
    
    # Validar nuevo apellido
    nuevo_apellido = input("Nuevo apellido (Enter para mantener): ").strip()
    if nuevo_apellido:
        if not nuevo_apellido.replace(" ", "").isalpha():
            print("Advertencia: El apellido debe contener solo letras. Ignorado.")
            nuevo_apellido = ""
        elif len(nuevo_apellido) < 2:
            print("Advertencia: El apellido debe tener al menos 2 caracteres. Ignorado.")
            nuevo_apellido = ""
    
    # Validar nuevo telefono
    nuevo_telefono = input("Nuevo telefono (10 digitos, Enter para mantener): ").strip()
    if nuevo_telefono:
        if not nuevo_telefono.isdigit():
            print("Advertencia: El telefono debe contener solo numeros. Ignorado.")
            nuevo_telefono = ""
        elif len(nuevo_telefono) != 10:
            print("Advertencia: El telefono debe tener exactamente 10 digitos. Ignorado.")
            nuevo_telefono = ""
    
    # Validar nueva direccion
    nueva_direccion = input("Nueva direccion (Enter para mantener): ").strip()
    if nueva_direccion:
        if len(nueva_direccion) < 5:
            print("Advertencia: La direccion debe tener al menos 5 caracteres. Ignorado.")
            nueva_direccion = ""
    
    nuevo_tipo = input("Nuevo tipo (residente/administrador, Enter para mantener): ").strip().lower()

    if nuevo_nombre:
        usuario["nombre"] = nuevo_nombre
    if nuevo_apellido:
        usuario["apellido"] = nuevo_apellido
    if nuevo_telefono:
        usuario["telefono"] = nuevo_telefono
    if nueva_direccion:
        usuario["direccion"] = nueva_direccion
    if nuevo_tipo:
        tipos_validos = ["residente", "administrador"]
        if nuevo_tipo in tipos_validos:
            usuario["tipo"] = nuevo_tipo
        else:
            print("Advertencia: Tipo invalido.")

    guardar_usuarios(usuarios)
    print("Usuario actualizado correctamente.")
    registrar_evento("INFO", "Usuario " + identificacion + " actualizado", usuario_actual)

def eliminar_usuario(usuarios, usuario_actual=None):
    identificacion = input("Ingrese la identificacion: ")

    if identificacion not in usuarios:
        print("Usuario no encontrado.")
        return

    confirmacion = input("¿Esta seguro de eliminar al usuario " + usuarios[identificacion]['nombre'] + " " + usuarios[identificacion]['apellido'] + "? (s/n): ").lower()
    
    if confirmacion != 's':
        print("Operacion cancelada.")
        return

    usuario_eliminado = usuarios[identificacion]
    del usuarios[identificacion]
    guardar_usuarios(usuarios)
    print("Usuario eliminado correctamente.")
    registrar_evento("INFO", "Usuario eliminado: " + identificacion + " - " + usuario_eliminado['nombre'] + " " + usuario_eliminado['apellido'], usuario_actual)