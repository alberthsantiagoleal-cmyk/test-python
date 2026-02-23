import json
from gestor_herramientas import cargar_herramientas

def generar_inventario_csv():
    print("\n" + "="*50)
    print("EXPORTAR INVENTARIO DE HERRAMIENTAS A CSV")
    print("="*50)

    inventario = cargar_herramientas()

    if not inventario:
        print("No hay herramientas registradas. No se generara el archivo.")
        return

    nombre_archivo = "herramientas_inventario.csv"
    valor_total = 0

    with open(nombre_archivo, "w") as archivo:
        archivo.write("codigo,nombre,categoria,cantidad,estado,valor\n")
        for codigo, h in inventario.items():
            valor_total = valor_total + (h["valor"] * h["cantidad"])
            linea = (codigo + "," + h["nombre"] + "," + h["categoria"] + "," +
                     str(h["cantidad"]) + "," + h["estado"] + "," + str(h["valor"]) + "\n")
            archivo.write(linea)

    print("Total de herramientas registradas: " + str(len(inventario)))
    print("Valor total del inventario: $" + str(round(valor_total, 2)))
    print("\nSe ha generado el archivo: " + nombre_archivo)

if __name__ == "__main__":
    generar_inventario_csv()
