# ==============================
# GESTION DE PRESTAMOS
# ==============================
import json 
from gestor_herramientas import guardar_herramientas
from gestor_logs import registrar_evento

def validar_formato_fecha(fecha):
    """Valida que la fecha tenga formato YYYY-MM-DD y sea valida"""
    if len(fecha) != 10:
        return False
    
    if fecha[4] != "-" or fecha[7] != "-":
        return False
    
    partes = fecha.split("-")
    if len(partes) != 3:
        return False
    
    ano = partes[0]
    mes = partes[1]
    dia = partes[2]
    
    # Verificar que sean numeros
    if not ano.isdigit() or not mes.isdigit() or not dia.isdigit():
        return False
    
    ano = int(ano)
    mes = int(mes)
    dia = int(dia)
    
    # Validar rangos
    if ano < 2020 or ano > 2100:
        return False
    
    if mes < 1 or mes > 12:
        return False
    
    if dia < 1 or dia > 31:
        return False
    
    # Validar dias por mes
    if mes in [4, 6, 9, 11] and dia > 30:
        return False
    
    if mes == 2:
        # Año bisiesto
        es_bisiesto = (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0)
        if es_bisiesto and dia > 29:
            return False
        if not es_bisiesto and dia > 28:
            return False
    
    return True

def cargar_prestamos():
    try:
        with open("prestamos.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}

def guardar_prestamos(prestamos):
    with open("prestamos.json", "w") as archivo:
        json.dump(prestamos, archivo, indent=4)


def cargar_solicitudes():
    """Carga las solicitudes de prestamo pendientes"""
    try:
        with open("solicitudes.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}


def guardar_solicitudes(solicitudes):
    """Guarda las solicitudes de prestamo"""
    with open("solicitudes.json", "w") as archivo:
        json.dump(solicitudes, archivo, indent=4)


def solicitar_prestamo(solicitudes, usuarios, inventario, usuario_actual):
    """Permite a un usuario residente crear una solicitud de prestamo"""
    print("\n=== SOLICITAR PRESTAMO DE HERRAMIENTA ===\n")

    # Generar ID de solicitud automatico
    if solicitudes:
        ids = []
        for k in solicitudes.keys():
            if k.startswith("SOL"):
                num = int(k.replace("SOL", ""))
                ids.append(num)
        if ids:
            ultimo_id = max(ids)
            codigo = "SOL" + str(ultimo_id + 1).zfill(4)
        else:
            codigo = "SOL0001"
    else:
        codigo = "SOL0001"

    print("ID de solicitud: " + codigo)

    id_herramienta = input("Ingrese ID de la herramienta: ")
    if id_herramienta not in inventario:
        print("La herramienta no existe.")
        registrar_evento("ERROR", "Solicitud fallida - Herramienta " + id_herramienta + " no existe", usuario_actual)
        return
    
    if inventario[id_herramienta]["estado"] != "activa":
        print("Herramienta no disponible. Estado actual: " + inventario[id_herramienta]['estado'])
        registrar_evento("WARNING", "Solicitud fallida - Herramienta " + id_herramienta + " no activa", usuario_actual)
        return
    
    try:
        cantidad = int(input("Cantidad a solicitar: "))
    except ValueError:
        print("Error: Debe ingresar un numero valido.")
        return
    
    if cantidad <= 0:
        print("Error: Cantidad invalida.")
        return
    
    if cantidad > inventario[id_herramienta]["cantidad"]:
        print("No hay suficiente cantidad disponible. Disponible: " + str(inventario[id_herramienta]['cantidad']))
        registrar_evento("WARNING", "Solicitud fallida - Cantidad insuficiente para " + id_herramienta, usuario_actual)
        return

    fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ").strip()
    
    # Validar formato de fecha
    if not validar_formato_fecha(fecha_inicio):
        print("Error: Formato de fecha invalido. Use YYYY-MM-DD (Ejemplo: 2026-02-17)")
        return
    
    fecha_devolucion = input("Fecha estimada devolucion (YYYY-MM-DD): ").strip()
    
    if not validar_formato_fecha(fecha_devolucion):
        print("Error: Formato de fecha invalido. Use YYYY-MM-DD (Ejemplo: 2026-02-20)")
        return
    
    # Validar que fecha_devolucion sea posterior a fecha_inicio
    if fecha_devolucion <= fecha_inicio:
        print("Error: La fecha de devolucion debe ser posterior a la fecha de inicio.")
        return
    
    observaciones = input("Observaciones: ").strip()

    solicitudes[codigo] = {
        "usuario": usuario_actual,
        "herramienta": id_herramienta,
        "cantidad": cantidad,
        "fecha_inicio": fecha_inicio,
        "fecha_devolucion": fecha_devolucion,
        "estado": "pendiente",
        "observaciones": observaciones
    }

    guardar_solicitudes(solicitudes)
    print("\nSolicitud " + codigo + " creada correctamente.")
    print("Espere la aprobacion del administrador.")
    registrar_evento("INFO", "Solicitud de prestamo creada: " + codigo + " - Herramienta " + id_herramienta, usuario_actual)


def listar_solicitudes_pendientes(solicitudes, inventario, usuarios):
    """Lista todas las solicitudes pendientes de aprobacion"""
    print("\n=== SOLICITUDES PENDIENTES ===\n")

    pendientes = {}
    for k, v in solicitudes.items():
        if v["estado"] == "pendiente":
            pendientes[k] = v

    if not pendientes:
        print("No hay solicitudes pendientes.")
        return

    for codigo, solicitud in pendientes.items():
        if solicitud["usuario"] in usuarios:
            usuario = usuarios[solicitud["usuario"]]
            nombre_usuario = usuario['nombre'] + " " + usuario['apellido']
        else:
            nombre_usuario = "Desconocido"
        
        if solicitud["herramienta"] in inventario:
            herramienta = inventario[solicitud["herramienta"]]
            nombre_herramienta = herramienta['nombre']
        else:
            nombre_herramienta = "Desconocida"
        
        print("\nID Solicitud: " + codigo)
        print("Usuario: " + nombre_usuario + " (" + solicitud['usuario'] + ")")
        print("Herramienta: " + nombre_herramienta + " (" + solicitud['herramienta'] + ")")
        print("Cantidad: " + str(solicitud['cantidad']))
        print("Fecha inicio: " + solicitud['fecha_inicio'])
        print("Fecha devolucion: " + solicitud['fecha_devolucion'])
        print("Observaciones: " + solicitud['observaciones'])
        print("-" * 50)


def aprobar_solicitud(solicitudes, prestamos, inventario, usuario_actual):
    """Permite a un administrador aprobar una solicitud de prestamo"""
    print("\n=== APROBAR SOLICITUD DE PRESTAMO ===\n")

    codigo_solicitud = input("Ingrese ID de la solicitud: ")

    if codigo_solicitud not in solicitudes:
        print("Solicitud no encontrada.")
        return
    
    solicitud = solicitudes[codigo_solicitud]

    if solicitud["estado"] != "pendiente":
        print("Esta solicitud ya fue " + solicitud["estado"] + ".")
        return

    id_herramienta = solicitud["herramienta"]
    cantidad = solicitud["cantidad"]

    if inventario[id_herramienta]["estado"] != "activa":
        print("Error: La herramienta ya no esta activa. Estado: " + inventario[id_herramienta]['estado'])
        return

    if cantidad > inventario[id_herramienta]["cantidad"]:
        print("Error: Ya no hay suficiente cantidad. Disponible: " + str(inventario[id_herramienta]['cantidad']))
        return

    # Generar ID de prestamo
    if prestamos:
        ids = []
        for k in prestamos.keys():
            if k.startswith("PRES"):
                num = int(k.replace("PRES", ""))
                ids.append(num)
        if ids:
            ultimo_id = max(ids)
            codigo_prestamo = "PRES" + str(ultimo_id + 1).zfill(4)
        else:
            codigo_prestamo = "PRES0001"
    else:
        codigo_prestamo = "PRES0001"

    # Crear prestamo
    inventario[id_herramienta]["cantidad"] = inventario[id_herramienta]["cantidad"] - cantidad

    prestamos[codigo_prestamo] = {
        "usuario": solicitud["usuario"],
        "herramienta": solicitud["herramienta"],
        "cantidad": cantidad,
        "fecha_inicio": solicitud["fecha_inicio"],
        "fecha_devolucion": solicitud["fecha_devolucion"],
        "estado": "activo",
        "observaciones": solicitud["observaciones"]
    }

    # Actualizar solicitud
    solicitud["estado"] = "aprobada"
    solicitud["prestamo_id"] = codigo_prestamo

    guardar_herramientas(inventario)
    guardar_prestamos(prestamos)
    guardar_solicitudes(solicitudes)

    print("\nSolicitud " + codigo_solicitud + " aprobada.")
    print("Prestamo " + codigo_prestamo + " creado correctamente.")
    registrar_evento("PRESTAMO", "Prestamo aprobado: " + codigo_prestamo + " - Usuario " + solicitud['usuario'] + " - Herramienta " + id_herramienta, usuario_actual)


def rechazar_solicitud(solicitudes, usuario_actual):
    """Permite a un administrador rechazar una solicitud de prestamo"""
    print("\n=== RECHAZAR SOLICITUD DE PRESTAMO ===\n")

    codigo_solicitud = input("Ingrese ID de la solicitud: ")

    if codigo_solicitud not in solicitudes:
        print("Solicitud no encontrada.")
        return
    
    solicitud = solicitudes[codigo_solicitud]

    if solicitud["estado"] != "pendiente":
        print("Esta solicitud ya fue " + solicitud["estado"] + ".")
        return

    motivo = input("Motivo del rechazo: ")

    solicitud["estado"] = "rechazada"
    solicitud["motivo_rechazo"] = motivo

    guardar_solicitudes(solicitudes)

    print("\nSolicitud " + codigo_solicitud + " rechazada.")
    registrar_evento("WARNING", "Solicitud rechazada: " + codigo_solicitud + " - Motivo: " + motivo, usuario_actual)


def prestamo_herramienta_directo(prestamos, usuarios, inventario, usuario_actual):
    """Permite a un administrador crear un prestamo directamente"""
    print("\n=== PRESTAMO DIRECTO DE HERRAMIENTA ===\n")

    # Generar ID de prestamo automatico
    if prestamos:
        ids = []
        for k in prestamos.keys():
            if k.startswith("PRES"):
                num = int(k.replace("PRES", ""))
                ids.append(num)
        if ids:
            ultimo_id = max(ids)
            codigo = "PRES" + str(ultimo_id + 1).zfill(4)
        else:
            codigo = "PRES0001"
    else:
        codigo = "PRES0001"

    print("ID del prestamo: " + codigo)

    id_usuario = input("Ingrese ID del usuario: ")
    if id_usuario not in usuarios:
        print("El usuario no existe.")
        return

    id_herramienta = input("Ingrese ID de la herramienta: ")
    if id_herramienta not in inventario:
        print("La herramienta no existe.")
        return
    
    if inventario[id_herramienta]["estado"] != "activa":
        print("Herramienta no disponible. Estado: " + inventario[id_herramienta]['estado'])
        return
    
    try:
        cantidad = int(input("Cantidad a prestar: "))
    except ValueError:
        print("Error: Debe ingresar un numero valido.")
        return

    if cantidad <= 0:
        print("Error: Cantidad invalida.")
        return
    
    if cantidad > inventario[id_herramienta]["cantidad"]:
        print("No hay suficiente cantidad disponible. Disponible: " + str(inventario[id_herramienta]['cantidad']))
        return

    fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ").strip()
    
    # Validar formato de fecha
    if not validar_formato_fecha(fecha_inicio):
        print("Error: Formato de fecha invalido. Use YYYY-MM-DD (Ejemplo: 2026-02-17)")
        return
    
    fecha_devolucion = input("Fecha estimada devolucion (YYYY-MM-DD): ").strip()
    
    if not validar_formato_fecha(fecha_devolucion):
        print("Error: Formato de fecha invalido. Use YYYY-MM-DD (Ejemplo: 2026-02-20)")
        return
    
    # Validar que fecha_devolucion sea posterior a fecha_inicio
    if fecha_devolucion <= fecha_inicio:
        print("Error: La fecha de devolucion debe ser posterior a la fecha de inicio.")
        return
    
    observaciones = input("Observaciones: ").strip()

    # Restar del inventario
    inventario[id_herramienta]["cantidad"] = inventario[id_herramienta]["cantidad"] - cantidad

    prestamos[codigo] = {
        "usuario": id_usuario,
        "herramienta": id_herramienta,
        "cantidad": cantidad,
        "fecha_inicio": fecha_inicio,
        "fecha_devolucion": fecha_devolucion,
        "estado": "activo",
        "observaciones": observaciones
    }

    guardar_herramientas(inventario)
    guardar_prestamos(prestamos)
    print("\nPrestamo " + codigo + " registrado correctamente.")
    registrar_evento("PRESTAMO", "Prestamo directo creado: " + codigo + " - Usuario " + id_usuario + " - Herramienta " + id_herramienta, usuario_actual)


def devolver_herramienta(prestamos, inventario, usuario_actual):
    print("\n=== DEVOLVER HERRAMIENTA ===\n")

    codigo = input("Ingrese codigo del prestamo: ")

    if codigo not in prestamos:
        print("Codigo del prestamo no existe.")
        registrar_evento("ERROR", "Intento de devolucion - Prestamo " + codigo + " no existe", usuario_actual)
        return
    
    prestamo = prestamos[codigo]

    if prestamo["estado"] == "devuelto":
        print("Este prestamo ya fue devuelto.")
        return

    id_herramienta = prestamo["herramienta"]
    cantidad = prestamo["cantidad"]

    inventario[id_herramienta]["cantidad"] = inventario[id_herramienta]["cantidad"] + cantidad

    prestamo["estado"] = "devuelto"

    guardar_herramientas(inventario)
    guardar_prestamos(prestamos)

    print("\nHerramienta devuelta correctamente.")
    print("Cantidad restaurada: " + str(cantidad) + " unidad(es) de " + inventario[id_herramienta]['nombre'])
    registrar_evento("DEVOLUCION", "Herramienta devuelta - Prestamo " + codigo + " - Herramienta " + id_herramienta, usuario_actual)


def mis_prestamos(prestamos, inventario, usuario_actual):
    """Muestra los prestamos del usuario actual"""
    print("\n=== MIS PRESTAMOS (Usuario: " + usuario_actual + ") ===\n")

    mis_prestamos_lista = {}
    for k, v in prestamos.items():
        if v["usuario"] == usuario_actual:
            mis_prestamos_lista[k] = v

    if not mis_prestamos_lista:
        print("No tienes prestamos registrados.")
        return

    print("ID Prestamo    Herramienta              Cantidad    F. Inicio      F. Devolucion     Estado")
    print("-" * 97)

    for codigo, prestamo in mis_prestamos_lista.items():
        if prestamo["herramienta"] in inventario:
            herramienta_nombre = inventario[prestamo["herramienta"]]["nombre"]
        else:
            herramienta_nombre = "Desconocida"
        
        print(codigo.ljust(15) + herramienta_nombre.ljust(25) + str(prestamo['cantidad']).ljust(12) + 
              prestamo['fecha_inicio'].ljust(15) + prestamo['fecha_devolucion'].ljust(18) + prestamo['estado'])

    print("-" * 97)
    
    activos = 0
    for p in mis_prestamos_lista.values():
        if p["estado"] == "activo":
            activos = activos + 1
    
    print("\nTotal: " + str(len(mis_prestamos_lista)) + " | Activos: " + str(activos))