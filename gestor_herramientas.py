# ==============================
# GESTION DE HERRAMIENTAS
# ==============================
import json 
from gestor_logs import registrar_evento

def cargar_herramientas():
    try:
        with open("herramientas.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}

def guardar_herramientas(inventario):
    with open("herramientas.json", "w") as archivo:
        json.dump(inventario, archivo, indent=4)


def registrar_herramienta(inventario, usuario_actual=None):
    print("\n1. Registrar herramienta\n")

    # Validar codigo
    codigo = input("Codigo de la herramienta: ").strip().upper()
    
    if not codigo:
        print("Error: El codigo no puede estar vacio.")
        return
    
    if len(codigo) < 3:
        print("Error: El codigo debe tener al menos 3 caracteres.")
        return
    
    # Verificar que el codigo no tenga espacios
    if " " in codigo:
        print("Error: El codigo no puede contener espacios.")
        return

    if codigo in inventario:
        print("Error: ya existe una herramienta con ese codigo.")
        registrar_evento("ERROR", "Intento de registrar herramienta con codigo duplicado: " + codigo, usuario_actual)
        return

    # Validar nombre
    nombre = input("Nombre: ").strip()
    
    if not nombre:
        print("Error: El nombre no puede estar vacio.")
        return
    
    if len(nombre) < 3:
        print("Error: El nombre debe tener al menos 3 caracteres.")
        return
    
    # Validar categoria
    categoria = input("Categoria (construccion, jardineria, electricidad, plomeria, etc.): ").strip().lower()
    
    if not categoria:
        print("Error: La categoria no puede estar vacia.")
        return
    
    if not categoria.replace(" ", "").isalpha():
        print("Error: La categoria debe contener solo letras.")
        return
    
    try:
        cantidad = int(input("Cantidad disponible: "))
        if cantidad < 0:
            print("Error: La cantidad no puede ser negativa.")
            return
    except ValueError:
        print("Error: Debe ingresar un numero valido.")
        return
    
    estados_validos = ["activa", "en reparacion", "fuera de servicio"]
    estado = input("Estado (activa, en reparacion, fuera de servicio): ").lower()
    
    if estado not in estados_validos:
        print("Error: Estado invalido. Opciones: activa, en reparacion, fuera de servicio")
        return
    
    try:
        valor = float(input("Valor estimado: "))
        if valor < 0:
            print("Error: El valor no puede ser negativo.")
            return
    except ValueError:
        print("Error: Debe ingresar un numero valido.")
        return

    inventario[codigo] = {
        "nombre": nombre,
        "categoria": categoria,
        "cantidad": cantidad,
        "estado": estado,
        "valor": valor
    }

    print("Herramienta registrada correctamente.")
    guardar_herramientas(inventario)
    registrar_evento("INFO", "Herramienta registrada: " + codigo + " - " + nombre, usuario_actual)


def listar_herramientas(inventario):
    print("\n2. Listar herramientas\n")

    if not inventario:
        print("No hay herramientas registradas.")
        return

    print("Codigo    Nombre              Categoria           Cantidad  Estado              Valor")
    print("-" * 90)

    for codigo, herramienta in inventario.items():
        print(codigo.ljust(10) + herramienta['nombre'].ljust(20) + herramienta['categoria'].ljust(20) + 
              str(herramienta['cantidad']).ljust(10) + herramienta['estado'].ljust(20) + str(herramienta['valor']))

    print("-" * 90)
    print("Total de herramientas: " + str(len(inventario)))


def consultar_herramienta(inventario):
    print("\n3. Buscar herramienta\n")

    codigo = input("Ingrese el codigo: ")

    if codigo not in inventario:
        print("Herramienta no encontrada.")
        return
    
    herramienta = inventario[codigo]

    print("\nInformacion de la herramienta:")
    print("Codigo: " + codigo)
    print("Nombre: " + herramienta['nombre'])
    print("Categoria: " + herramienta['categoria'])
    print("Cantidad disponible: " + str(herramienta['cantidad']))
    print("Estado: " + herramienta['estado'])
    print("Valor estimado: " + str(herramienta['valor']))


def actualizar_herramienta(inventario, usuario_actual=None):
    print("\n4. Actualizar herramienta\n")

    codigo = input("Ingrese el codigo: ")

    if codigo not in inventario:
        print("Herramienta no encontrada.")
        return

    herramienta = inventario[codigo]

    nuevo_nombre = input("Nuevo nombre (Enter para mantener): ")
    nueva_categoria = input("Nueva categoria (Enter para mantener): ")
    nueva_cantidad = input("Nueva cantidad (Enter para mantener): ")
    nuevo_estado = input("Nuevo estado (Enter para mantener): ").lower()
    nuevo_valor = input("Nuevo valor (Enter para mantener): ")

    if nuevo_nombre:
        herramienta["nombre"] = nuevo_nombre
    if nueva_categoria:
        herramienta["categoria"] = nueva_categoria
    if nueva_cantidad:
        try:
            cantidad = int(nueva_cantidad)
            if cantidad >= 0:
                herramienta["cantidad"] = cantidad
            else:
                print("Advertencia: Cantidad negativa ignorada.")
        except ValueError:
            print("Advertencia: Cantidad invalida ignorada.")
    if nuevo_estado:
        estados_validos = ["activa", "en reparacion", "fuera de servicio"]
        if nuevo_estado in estados_validos:
            herramienta["estado"] = nuevo_estado
        else:
            print("Advertencia: Estado invalido.")
    if nuevo_valor:
        try:
            valor = float(nuevo_valor)
            if valor >= 0:
                herramienta["valor"] = valor
            else:
                print("Advertencia: Valor negativo ignorado.")
        except ValueError:
            print("Advertencia: Valor invalido ignorado.")

    print("Herramienta actualizada correctamente.")
    guardar_herramientas(inventario)
    registrar_evento("INFO", "Herramienta " + codigo + " actualizada", usuario_actual)


def inactivar_herramienta(inventario, usuario_actual=None):
    print("\n5. Inactivar herramienta\n")

    codigo = input("Ingrese el codigo: ")

    if codigo not in inventario:
        print("Herramienta no encontrada.")
        return

    inventario[codigo]["estado"] = "fuera de servicio"
    print("Herramienta inactivada correctamente.")
    guardar_herramientas(inventario)
    registrar_evento("INFO", "Herramienta inactivada: " + codigo, usuario_actual)


def herramientas_stock_bajo(inventario, limite=3):
    print("\nHerramientas con stock bajo (< " + str(limite) + " unidades):\n")

    encontrado = False

    for codigo, herramienta in inventario.items():
        if herramienta["cantidad"] < limite:
            print(codigo + " - " + herramienta['nombre'] + " (Cantidad: " + str(herramienta['cantidad']) + ")")
            encontrado = True

    if not encontrado:
        print("No hay herramientas con stock bajo.")