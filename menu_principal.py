# ==============================
# MENU PRINCIPAL
# Sistema de Gestion de Herramientas Comunitarias
# ==============================

from gestor_herramientas import (
    registrar_herramienta, listar_herramientas, consultar_herramienta,
    actualizar_herramienta, inactivar_herramienta, herramientas_stock_bajo,
    cargar_herramientas
)
from gestor_usuarios import (
    cargar_usuarios, registrar_usuario, listar_usuarios,
    consultar_usuario, actualizar_usuario, eliminar_usuario
)
from gestor_prestamos import (
    prestamo_herramienta_directo, devolver_herramienta, cargar_prestamos,
    solicitar_prestamo, listar_solicitudes_pendientes, aprobar_solicitud,
    rechazar_solicitud, mis_prestamos, cargar_solicitudes
)
from gestor_reportes import menu_reportes
from gestor_permisos import login, registrar_credencial, cambiar_password
from gestor_logs import ver_logs_recientes, ver_logs_por_tipo, ver_logs_por_usuario

# Cargar datos globales
prestamos = cargar_prestamos()
solicitudes = cargar_solicitudes()
inventario = cargar_herramientas()
usuarios = cargar_usuarios()

# Variables de sesion
usuario_logueado = None
tipo_usuario = None


def menu_principal():
    """Menu principal del sistema con login"""
    global usuario_logueado, tipo_usuario
    
    # Login
    usuario_logueado, tipo_usuario = login()
    
    if not usuario_logueado:
        print("No se pudo iniciar sesion. Saliendo...")
        return
    
    # Menu segun tipo de usuario
    if tipo_usuario == "administrador":
        menu_administrador()
    else:
        menu_residente()


def menu_administrador():
    """Menu para administradores con acceso completo"""
    while True:
        print("\n" + "="*50)
        print("MENU ADMINISTRADOR - " + usuario_logueado)
        print("="*50)
        print("1. Gestion de herramientas")
        print("2. Gestion de usuarios")
        print("3. Gestion de prestamos (directo)")
        print("4. Gestion de solicitudes")
        print("5. Reportes y consultas")
        print("6. Registro de eventos (logs)")
        print("7. Gestion de credenciales")
        print("8. Cambiar contrasena")
        print("9. Salir")

        opcion = input("\nSeleccione una opcion: ")

        if opcion == "1":
            submenu_herramientas_admin()
        elif opcion == "2":
            submenu_usuarios_admin()
        elif opcion == "3":
            submenu_prestamos_admin()
        elif opcion == "4":
            submenu_solicitudes_admin()
        elif opcion == "5":
            menu_reportes()
        elif opcion == "6":
            submenu_logs()
        elif opcion == "7":
            registrar_credencial(usuarios)
        elif opcion == "8":
            cambiar_password(usuario_logueado)
        elif opcion == "9":
            print("\nCerrando sesion...")
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opcion invalida.")


def menu_residente():
    """Menu para residentes con acceso limitado"""
    while True:
        print("\n" + "="*50)
        print("MENU USUARIO - " + usuario_logueado)
        print("="*50)
        print("1. Ver herramientas disponibles")
        print("2. Buscar herramienta")
        print("3. Solicitar prestamo")
        print("4. Devolver herramienta")
        print("5. Mis prestamos")
        print("6. Cambiar contrasena")
        print("7. Salir")

        opcion = input("\nSeleccione una opcion: ")

        if opcion == "1":
            listar_herramientas(inventario)
        elif opcion == "2":
            consultar_herramienta(inventario)
        elif opcion == "3":
            solicitar_prestamo(solicitudes, usuarios, inventario, usuario_logueado)
        elif opcion == "4":
            devolver_herramienta(prestamos, inventario, usuario_logueado)
        elif opcion == "5":
            mis_prestamos(prestamos, inventario, usuario_logueado)
        elif opcion == "6":
            cambiar_password(usuario_logueado)
        elif opcion == "7":
            print("\nCerrando sesion...")
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opcion invalida.")


def submenu_herramientas_admin():
    """Submenu de herramientas para administradores"""
    while True:
        print("\n=== GESTION DE HERRAMIENTAS ===")
        print("1. Registrar herramienta")
        print("2. Listar herramientas")
        print("3. Buscar herramienta")
        print("4. Actualizar herramienta")
        print("5. Inactivar herramienta")
        print("6. Ver herramientas con stock bajo")
        print("7. Volver")

        opcion = input("\nSeleccione una opcion: ")

        if opcion == "1":
            registrar_herramienta(inventario, usuario_logueado)
        elif opcion == "2":
            listar_herramientas(inventario)
        elif opcion == "3":
            consultar_herramienta(inventario)
        elif opcion == "4":
            actualizar_herramienta(inventario, usuario_logueado)
        elif opcion == "5":
            inactivar_herramienta(inventario, usuario_logueado)
        elif opcion == "6":
            herramientas_stock_bajo(inventario)
        elif opcion == "7":
            break
        else:
            print("Opcion invalida.")


def submenu_usuarios_admin():
    """Submenu de usuarios para administradores"""
    while True:
        print("\n=== GESTION DE USUARIOS ===")
        print("1. Registrar usuario")
        print("2. Listar usuarios")
        print("3. Buscar usuario")
        print("4. Actualizar usuario")
        print("5. Eliminar usuario")
        print("6. Volver")

        opcion = input("\nSeleccione una opcion: ")

        if opcion == "1":
            registrar_usuario(usuarios, usuario_logueado)
        elif opcion == "2":
            listar_usuarios(usuarios)
        elif opcion == "3":
            consultar_usuario(usuarios)
        elif opcion == "4":
            actualizar_usuario(usuarios, usuario_logueado)
        elif opcion == "5":
            eliminar_usuario(usuarios, usuario_logueado)
        elif opcion == "6":
            break
        else:
            print("Opcion invalida.")


def submenu_prestamos_admin():
    """Submenu de prestamos directos para administradores"""
    while True:
        print("\n=== GESTION DE PRESTAMOS (DIRECTO) ===")
        print("1. Crear prestamo directo")
        print("2. Devolver herramienta")
        print("3. Volver")

        opcion = input("\nSeleccione una opcion: ")

        if opcion == "1":
            prestamo_herramienta_directo(prestamos, usuarios, inventario, usuario_logueado)
        elif opcion == "2":
            devolver_herramienta(prestamos, inventario, usuario_logueado)
        elif opcion == "3":
            break
        else:
            print("Opcion invalida.")


def submenu_solicitudes_admin():
    """Submenu de gestion de solicitudes para administradores"""
    while True:
        print("\n=== GESTION DE SOLICITUDES ===")
        print("1. Ver solicitudes pendientes")
        print("2. Aprobar solicitud")
        print("3. Rechazar solicitud")
        print("4. Volver")

        opcion = input("\nSeleccione una opcion: ")

        if opcion == "1":
            listar_solicitudes_pendientes(solicitudes, inventario, usuarios)
        elif opcion == "2":
            aprobar_solicitud(solicitudes, prestamos, inventario, usuario_logueado)
        elif opcion == "3":
            rechazar_solicitud(solicitudes, usuario_logueado)
        elif opcion == "4":
            break
        else:
            print("Opcion invalida.")


def submenu_logs():
    """Submenu de logs para administradores"""
    while True:
        print("\n=== REGISTRO DE EVENTOS (LOGS) ===")
        print("1. Ver eventos recientes")
        print("2. Filtrar por tipo de evento")
        print("3. Filtrar por usuario")
        print("4. Volver")

        opcion = input("\nSeleccione una opcion: ")

        if opcion == "1":
            try:
                cantidad_str = input("Cuantos eventos mostrar? (default 10): ")
                if cantidad_str:
                    cantidad = int(cantidad_str)
                else:
                    cantidad = 10
                ver_logs_recientes(cantidad)
            except ValueError:
                print("Cantidad invalida. Mostrando 10 eventos.")
                ver_logs_recientes(10)
        elif opcion == "2":
            print("\nTipos disponibles: INFO, ERROR, WARNING, PRESTAMO, DEVOLUCION")
            tipo = input("Tipo de evento: ").upper()
            ver_logs_por_tipo(tipo)
        elif opcion == "3":
            id_usuario = input("ID del usuario: ")
            ver_logs_por_usuario(id_usuario)
        elif opcion == "4":
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    menu_principal()