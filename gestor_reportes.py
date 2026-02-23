# ==============================
# REPORTES Y CONSULTAS
# ==============================
import json

def cargar_datos():
    """Carga todos los datos necesarios para reportes"""
    try:
        with open("herramientas.json", "r") as f:
            herramientas = json.load(f)
    except FileNotFoundError:
        herramientas = {}
    
    try:
        with open("usuarios.json", "r") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        usuarios = {}
    
    try:
        with open("prestamos.json", "r") as f:
            prestamos = json.load(f)
    except FileNotFoundError:
        prestamos = {}
    
    return herramientas, usuarios, prestamos


def reporte_stock_bajo(inventario, limite=3):
    """Genera reporte de herramientas con stock bajo"""
    print("\n" + "="*60)
    print("REPORTE: HERRAMIENTAS CON STOCK BAJO (< " + str(limite) + " unidades)")
    print("="*60 + "\n")
    
    herramientas_bajo_stock = []
    
    for codigo, herramienta in inventario.items():
        if herramienta["cantidad"] < limite:
            herramientas_bajo_stock.append({
                "codigo": codigo,
                "nombre": herramienta["nombre"],
                "cantidad": herramienta["cantidad"],
                "categoria": herramienta["categoria"]
            })
    
    if not herramientas_bajo_stock:
        print("No hay herramientas con stock bajo.")
        return
    
    # Ordenar por cantidad (menor a mayor)
    for i in range(len(herramientas_bajo_stock)):
        for j in range(i + 1, len(herramientas_bajo_stock)):
            if herramientas_bajo_stock[i]["cantidad"] > herramientas_bajo_stock[j]["cantidad"]:
                temp = herramientas_bajo_stock[i]
                herramientas_bajo_stock[i] = herramientas_bajo_stock[j]
                herramientas_bajo_stock[j] = temp
    
    print("Codigo      Nombre                   Cantidad    Categoria")
    print("-" * 69)
    
    for h in herramientas_bajo_stock:
        codigo = h['codigo']
        nombre = h['nombre']
        cantidad = str(h['cantidad'])
        categoria = h['categoria']
        print(codigo.ljust(12) + nombre.ljust(25) + cantidad.ljust(12) + categoria)
    
    print("-" * 69)
    print("\nTotal de herramientas con stock bajo: " + str(len(herramientas_bajo_stock)))


def reporte_prestamos_activos(prestamos, herramientas, usuarios):
    """Genera reporte de prestamos activos"""
    print("\n" + "="*80)
    print("REPORTE: PRESTAMOS ACTIVOS")
    print("="*80 + "\n")
    
    prestamos_activos = []
    
    for id_prestamo, prestamo in prestamos.items():
        if prestamo["estado"] == "activo":
            if prestamo["usuario"] in usuarios:
                nombre_usuario = usuarios[prestamo["usuario"]]["nombre"] + " " + usuarios[prestamo["usuario"]]["apellido"]
            else:
                nombre_usuario = "Desconocido"
            
            if prestamo["herramienta"] in herramientas:
                nombre_herramienta = herramientas[prestamo["herramienta"]]["nombre"]
            else:
                nombre_herramienta = "Desconocida"
            
            prestamos_activos.append({
                "id": id_prestamo,
                "usuario": nombre_usuario,
                "herramienta": nombre_herramienta,
                "cantidad": prestamo["cantidad"],
                "fecha_inicio": prestamo["fecha_inicio"],
                "fecha_devolucion": prestamo["fecha_devolucion"]
            })
    
    if not prestamos_activos:
        print("No hay prestamos activos.")
        return
    
    print("ID Prestamo    Usuario                  Herramienta         Cant.   F. Inicio      F. Devolucion")
    print("-" * 98)
    
    for p in prestamos_activos:
        print(p['id'].ljust(15) + p['usuario'].ljust(25) + p['herramienta'].ljust(20) + 
              str(p['cantidad']).ljust(8) + p['fecha_inicio'].ljust(15) + p['fecha_devolucion'])
    
    print("-" * 98)
    print("\nTotal de prestamos activos: " + str(len(prestamos_activos)))


def reporte_prestamos_vencidos(prestamos, herramientas, usuarios):
    """Genera reporte de prestamos vencidos"""
    print("\n" + "="*80)
    print("REPORTE: PRESTAMOS VENCIDOS")
    print("="*80 + "\n")
    
    prestamos_vencidos = []
    
    for id_prestamo, prestamo in prestamos.items():
        if prestamo["estado"] == "activo":
            # Comparar fechas manualmente (formato YYYY-MM-DD)
            fecha_dev = prestamo["fecha_devolucion"]
            # Simular fecha de hoy como 2026-02-17 (puedes cambiar esto)
            fecha_hoy = "2026-02-17"
            
            if fecha_dev < fecha_hoy:  # Comparación de strings en formato ISO funciona
                if prestamo["usuario"] in usuarios:
                    nombre_usuario = usuarios[prestamo["usuario"]]["nombre"] + " " + usuarios[prestamo["usuario"]]["apellido"]
                else:
                    nombre_usuario = "Desconocido"
                
                if prestamo["herramienta"] in herramientas:
                    nombre_herramienta = herramientas[prestamo["herramienta"]]["nombre"]
                else:
                    nombre_herramienta = "Desconocida"
                
                prestamos_vencidos.append({
                    "id": id_prestamo,
                    "usuario": nombre_usuario,
                    "herramienta": nombre_herramienta,
                    "fecha_devolucion": prestamo["fecha_devolucion"]
                })
    
    if not prestamos_vencidos:
        print("No hay prestamos vencidos.")
        return
    
    print("ID Prestamo    Usuario                  Herramienta         F. Devolucion")
    print("-" * 78)
    
    for p in prestamos_vencidos:
        print(p['id'].ljust(15) + p['usuario'].ljust(25) + p['herramienta'].ljust(20) + p['fecha_devolucion'])
    
    print("-" * 78)
    print("\nTotal de prestamos vencidos: " + str(len(prestamos_vencidos)))


def historial_prestamos_usuario(prestamos, herramientas, usuarios, id_usuario):
    """Muestra el historial completo de prestamos de un usuario"""
    print("\n" + "="*80)
    print("HISTORIAL DE PRESTAMOS - Usuario: " + id_usuario)
    print("="*80 + "\n")
    
    if id_usuario not in usuarios:
        print("Error: Usuario no encontrado.")
        return
    
    usuario = usuarios[id_usuario]
    print("Nombre: " + usuario['nombre'] + " " + usuario['apellido'])
    print("Tipo: " + usuario['tipo'] + "\n")
    
    prestamos_usuario = []
    
    for id_prestamo, prestamo in prestamos.items():
        if prestamo["usuario"] == id_usuario:
            if prestamo["herramienta"] in herramientas:
                nombre_herramienta = herramientas[prestamo["herramienta"]]["nombre"]
            else:
                nombre_herramienta = "Desconocida"
            
            prestamos_usuario.append({
                "id": id_prestamo,
                "herramienta": nombre_herramienta,
                "cantidad": prestamo["cantidad"],
                "fecha_inicio": prestamo["fecha_inicio"],
                "fecha_devolucion": prestamo["fecha_devolucion"],
                "estado": prestamo["estado"]
            })
    
    if not prestamos_usuario:
        print("Este usuario no tiene prestamos registrados.")
        return
    
    print("ID Prestamo    Herramienta              Cantidad    F. Inicio      F. Devolucion     Estado")
    print("-" * 97)
    
    for p in prestamos_usuario:
        print(p['id'].ljust(15) + p['herramienta'].ljust(25) + str(p['cantidad']).ljust(12) + 
              p['fecha_inicio'].ljust(15) + p['fecha_devolucion'].ljust(18) + p['estado'])
    
    print("-" * 97)
    print("\nTotal de prestamos: " + str(len(prestamos_usuario)))
    
    activos = 0
    devueltos = 0
    for p in prestamos_usuario:
        if p["estado"] == "activo":
            activos = activos + 1
        elif p["estado"] == "devuelto":
            devueltos = devueltos + 1
    
    print("Activos: " + str(activos) + " | Devueltos: " + str(devueltos))


def herramientas_mas_solicitadas(prestamos, herramientas, top=5):
    """Muestra las herramientas mas solicitadas"""
    print("\n" + "="*60)
    print("TOP " + str(top) + " HERRAMIENTAS MAS SOLICITADAS")
    print("="*60 + "\n")
    
    # Contar solicitudes por herramienta
    contador = {}
    
    for prestamo in prestamos.values():
        id_herramienta = prestamo["herramienta"]
        if id_herramienta in contador:
            contador[id_herramienta] = contador[id_herramienta] + 1
        else:
            contador[id_herramienta] = 1
    
    if not contador:
        print("No hay datos de prestamos.")
        return
    
    # Convertir a lista y ordenar
    lista_herramientas = []
    for id_herr, cantidad in contador.items():
        lista_herramientas.append({"id": id_herr, "cantidad": cantidad})
    
    # Ordenar de mayor a menor
    for i in range(len(lista_herramientas)):
        for j in range(i + 1, len(lista_herramientas)):
            if lista_herramientas[i]["cantidad"] < lista_herramientas[j]["cantidad"]:
                temp = lista_herramientas[i]
                lista_herramientas[i] = lista_herramientas[j]
                lista_herramientas[j] = temp
    
    # Tomar solo top N
    if len(lista_herramientas) > top:
        lista_herramientas = lista_herramientas[:top]
    
    print("#    Codigo       Nombre                         Veces Solicitada")
    print("-" * 67)
    
    posicion = 1
    for item in lista_herramientas:
        id_herr = item["id"]
        if id_herr in herramientas:
            nombre = herramientas[id_herr]["nombre"]
        else:
            nombre = "Desconocida"
        cantidad = item["cantidad"]
        
        print(str(posicion).ljust(5) + id_herr.ljust(13) + nombre.ljust(31) + str(cantidad))
        posicion = posicion + 1
    
    print("-" * 67)


def usuarios_mas_activos(prestamos, usuarios, top=5):
    """Muestra los usuarios que mas herramientas han solicitado"""
    print("\n" + "="*70)
    print("TOP " + str(top) + " USUARIOS MAS ACTIVOS")
    print("="*70 + "\n")
    
    # Contar prestamos por usuario
    contador = {}
    
    for prestamo in prestamos.values():
        id_usuario = prestamo["usuario"]
        if id_usuario in contador:
            contador[id_usuario] = contador[id_usuario] + 1
        else:
            contador[id_usuario] = 1
    
    if not contador:
        print("No hay datos de prestamos.")
        return
    
    # Convertir a lista y ordenar
    lista_usuarios = []
    for id_usr, cantidad in contador.items():
        lista_usuarios.append({"id": id_usr, "cantidad": cantidad})
    
    # Ordenar de mayor a menor
    for i in range(len(lista_usuarios)):
        for j in range(i + 1, len(lista_usuarios)):
            if lista_usuarios[i]["cantidad"] < lista_usuarios[j]["cantidad"]:
                temp = lista_usuarios[i]
                lista_usuarios[i] = lista_usuarios[j]
                lista_usuarios[j] = temp
    
    # Tomar solo top N
    if len(lista_usuarios) > top:
        lista_usuarios = lista_usuarios[:top]
    
    print("#    ID Usuario   Nombre                         Prestamos Realizados")
    print("-" * 70)
    
    posicion = 1
    for item in lista_usuarios:
        id_usr = item["id"]
        if id_usr in usuarios:
            nombre = usuarios[id_usr]["nombre"] + " " + usuarios[id_usr]["apellido"]
        else:
            nombre = "Desconocido"
        cantidad = item["cantidad"]
        
        print(str(posicion).ljust(5) + id_usr.ljust(13) + nombre.ljust(31) + str(cantidad))
        posicion = posicion + 1
    
    print("-" * 70)


def menu_reportes():
    """Menu de reportes y consultas"""
    herramientas, usuarios, prestamos = cargar_datos()
    
    while True:
        print("\n" + "="*40)
        print("REPORTES Y CONSULTAS")
        print("="*40)
        print("1. Herramientas con stock bajo")
        print("2. Prestamos activos")
        print("3. Prestamos vencidos")
        print("4. Historial de prestamos de un usuario")
        print("5. Herramientas mas solicitadas")
        print("6. Usuarios mas activos")
        print("7. Volver")
        
        opcion = input("\nSeleccione una opcion: ")
        
        if opcion == "1":
            reporte_stock_bajo(herramientas)
        elif opcion == "2":
            reporte_prestamos_activos(prestamos, herramientas, usuarios)
        elif opcion == "3":
            reporte_prestamos_vencidos(prestamos, herramientas, usuarios)
        elif opcion == "4":
            id_usuario = input("\nIngrese ID del usuario: ")
            historial_prestamos_usuario(prestamos, herramientas, usuarios, id_usuario)
        elif opcion == "5":
            herramientas_mas_solicitadas(prestamos, herramientas)
        elif opcion == "6":
            usuarios_mas_activos(prestamos, usuarios)
        elif opcion == "7":
            break
        else:
            print("Opcion invalida.")