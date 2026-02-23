import json
from gestor_herramientas import cargar_herramientas, guardar_herramientas
from gestor_logs import registrar_evento

def cargar_mantenimento():
    try:
        with open("mantenimentos.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}

def guardar_mantenimiento(mantenimientos):
    with open("mantenimentos.json", "w") as archivo:
        json.dump(mantenimientos, archivo, indent=4)


def registrar_mantenimiento(usuario_actual=None):
    inventario = cargar_herramientas()
    listar_activas()
    
        

    codigo = input('Codigo de la herramienta: ').strip().upper()
    if codigo not in inventario:
        print('Herramienta no encontrada.')
        return
    fecha_inicio = input('Fecha inicio del mantenimiento (YYYY-MM-DD): ').strip()
    fecha_final = input('Fecha final del mantenimiento (YYYY-MM-DD): ').strip()
   
 
    descripcion = input('Descripcion del mantenimiento: ').strip()
    if not descripcion:
        print('Error: La descripcion no puede estar vacia.')
        return
    
  
    inventario[codigo]['estado'] = 'en reparacion'
   

    mantenimientos = []

    guardar_herramientas(inventario)
    guardar_mantenimiento(mantenimientos)
    print('Mantenimiento registrado correctamente.')
    listar_inactivas()
    registrar_evento('INFO', 'Mantenimiento en ' + codigo + ': ' + descripcion, usuario_actual)

def listar_inactivas():
    inventario = cargar_herramientas()
    print('\n=== HERRAMIENTAS EN REPARACION ===\n')
    encontrado = False
    for cod, h in inventario.items():
        if h['estado'] == 'en reparacion':
            print(cod + ' - ' + h['nombre'] + ' | Estado: ' + h['estado'])
            encontrado = True
    if not encontrado:
        print('Todas las herramientas estan activas.')

def listar_activas():
    inventario = cargar_herramientas()
    print('\n=== HERRAMIENTAS ACTIVAS ===\n')
    encontrado = False
    for cod, h in inventario.items():
        if h['estado'] == 'activa':
            print(cod + ' - ' + h['nombre'] + ' | Estado: ' + h['estado'])
            encontrado = True
    if not encontrado:
        print('Todas las herramientas estan en reparacion.')

if __name__=="__main__":
    registrar_mantenimiento()