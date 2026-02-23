# ==============================
# SISTEMA DE LOGS
# ==============================
import json

def registrar_evento(tipo, descripcion, usuario=None):
    """Registra un evento en el archivo de logs"""
    try:
        with open("logs.json", "r") as archivo:
            logs = json.load(archivo)
    except FileNotFoundError:
        logs = []
    
    log_entry = {
        "tipo": tipo,
        "usuario": usuario,
        "descripcion": descripcion
    }
    
    logs.append(log_entry)
    
    with open("logs.json", "w") as archivo:
        json.dump(logs, archivo, indent=4)


def ver_logs_recientes(cantidad=10):
    """Muestra los ultimos N eventos registrados"""
    print("\n=== ULTIMOS EVENTOS ===\n")
    
    try:
        with open("logs.json", "r") as archivo:
            logs = json.load(archivo)
    except FileNotFoundError:
        print("No hay eventos registrados.")
        return
    
    if not logs:
        print("No hay eventos registrados.")
        return
    
    total = len(logs)
    inicio = total - cantidad if total > cantidad else 0
    
    for i in range(inicio, total):
        log = logs[i]
        usuario_info = " | Usuario: " + log["usuario"] if log["usuario"] else ""
        print("[" + log["tipo"] + "]" + usuario_info + " - " + log["descripcion"])


def ver_logs_por_tipo(tipo):
    """Filtra logs por tipo de evento"""
    print("\n=== EVENTOS DE TIPO: " + tipo + " ===\n")
    
    try:
        with open("logs.json", "r") as archivo:
            logs = json.load(archivo)
    except FileNotFoundError:
        print("No hay eventos registrados.")
        return
    
    encontrado = False
    for log in logs:
        if log["tipo"] == tipo:
            usuario_info = " | Usuario: " + log["usuario"] if log["usuario"] else ""
            print("[" + log["tipo"] + "]" + usuario_info + " - " + log["descripcion"])
            encontrado = True
    
    if not encontrado:
        print("No hay eventos de tipo " + tipo + ".")


def ver_logs_por_usuario(id_usuario):
    """Filtra logs por usuario especifico"""
    print("\n=== EVENTOS DEL USUARIO: " + id_usuario + " ===\n")
    
    try:
        with open("logs.json", "r") as archivo:
            logs = json.load(archivo)
    except FileNotFoundError:
        print("No hay eventos registrados.")
        return
    
    encontrado = False
    for log in logs:
        if log["usuario"] == id_usuario:
            print("[" + log["tipo"] + "] - " + log["descripcion"])
            encontrado = True
    
    if not encontrado:
        print("No hay eventos del usuario " + id_usuario + ".")