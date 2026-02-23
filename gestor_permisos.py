# ==============================
# SISTEMA DE PERMISOS Y LOGIN
# ==============================
import json
from gestor_logs import registrar_evento

def cargar_credenciales():
    """Carga las credenciales de acceso al sistema"""
    try:
        with open("credenciales.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        credenciales_default = {
            "admin": {
                "password": "admin123",
                "tipo": "administrador",
                "nombre": "Administrador del Sistema"
            }
        }
        guardar_credenciales(credenciales_default)
        return credenciales_default


def guardar_credenciales(credenciales):
    """Guarda las credenciales en el archivo"""
    with open("credenciales.json", "w") as archivo:
        json.dump(credenciales, archivo, indent=4)


def login():
    """Sistema de login - Retorna (usuario_id, tipo_usuario) si exitoso, (None, None) si falla"""
    print("\n" + "="*50)
    print("SISTEMA DE GESTION DE HERRAMIENTAS COMUNITARIAS")
    print("="*50)
    print("\n--- INICIO DE SESION ---\n")
    
    credenciales = cargar_credenciales()
    
    usuario = input("Usuario: ")
    password = input("Contrasena: ")
    
    if usuario in credenciales and credenciales[usuario]["password"] == password:
        tipo = credenciales[usuario]["tipo"]
        nombre = credenciales[usuario]["nombre"]
        print("\nBienvenido " + nombre + " (" + tipo + ")")
        registrar_evento("INFO", "Login exitoso: " + nombre, usuario)
        return usuario, tipo
    else:
        print("\nUsuario o contrasena incorrectos.")
        registrar_evento("WARNING", "Intento de login fallido para usuario: " + usuario)
        return None, None


def registrar_credencial(usuarios):
    """Registra credenciales para un usuario existente"""
    print("\n=== REGISTRAR ACCESO AL SISTEMA ===\n")
    
    credenciales = cargar_credenciales()
    
    print("Usuarios registrados sin acceso al sistema:")
    usuarios_sin_acceso = []
    
    for id_usuario, datos in usuarios.items():
        if id_usuario not in credenciales:
            print("- " + id_usuario + ": " + datos['nombre'] + " " + datos['apellido'] + " (" + datos['tipo'] + ")")
            usuarios_sin_acceso.append(id_usuario)
    
    if not usuarios_sin_acceso:
        print("Todos los usuarios ya tienen acceso al sistema.")
        return
    
    print()
    id_usuario = input("ID del usuario: ")
    
    if id_usuario not in usuarios:
        print("Error: El usuario no existe.")
        registrar_evento("ERROR", "Intento de crear credencial para usuario inexistente: " + id_usuario)
        return
    
    if id_usuario in credenciales:
        print("Error: Este usuario ya tiene credenciales.")
        return
    
    password = input("Contrasena: ")
    
    if len(password) < 4:
        print("Error: La contrasena debe tener al menos 4 caracteres.")
        return
    
    credenciales[id_usuario] = {
        "password": password,
        "tipo": usuarios[id_usuario]["tipo"],
        "nombre": usuarios[id_usuario]['nombre'] + " " + usuarios[id_usuario]['apellido']
    }
    
    guardar_credenciales(credenciales)
    print("Credenciales creadas para " + credenciales[id_usuario]['nombre'])
    registrar_evento("INFO", "Credenciales creadas para usuario: " + id_usuario)


def cambiar_password(usuario_actual):
    """Permite a un usuario cambiar su contrasena"""
    print("\n=== CAMBIAR CONTRASENA ===\n")
    
    credenciales = cargar_credenciales()
    
    password_actual = input("Contrasena actual: ")
    
    if credenciales[usuario_actual]["password"] != password_actual:
        print("Error: Contrasena actual incorrecta.")
        registrar_evento("WARNING", "Intento fallido de cambio de contrasena", usuario_actual)
        return
    
    nueva_password = input("Nueva contrasena: ")
    confirmar_password = input("Confirmar nueva contrasena: ")
    
    if nueva_password != confirmar_password:
        print("Error: Las contrasenas no coinciden.")
        return
    
    if len(nueva_password) < 4:
        print("Error: La contrasena debe tener al menos 4 caracteres.")
        return
    
    credenciales[usuario_actual]["password"] = nueva_password
    guardar_credenciales(credenciales)
    
    print("Contrasena cambiada exitosamente.")
    registrar_evento("INFO", "Cambio de contrasena exitoso", usuario_actual)