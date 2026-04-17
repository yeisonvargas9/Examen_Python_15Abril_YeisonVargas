import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ARCHIVO_INVENTARIO = os.path.join(BASE_DIR, "data", "inventario.json")
ARCHIVO_HISTORIAL = os.path.join(BASE_DIR, "data", "historial.json")

def asegurarCarpeta():
    ruta = os.path.join(BASE_DIR, "data")
    if not os.path.exists(ruta):
        os.makedirs(ruta)
asegurarCarpeta()

def cargarDatos():
    if os.path.exists(ARCHIVO_INVENTARIO):
        with open(ARCHIVO_INVENTARIO, "r") as f:
            return json.load(f)
    return []

def guardarDatos(datos):
    with open(ARCHIVO_INVENTARIO, "w") as f:
        json.dump(datos, f, indent=4)

def cargarHistorial():
    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "r") as f:
            return json.load(f)
    return []

def guardarHistorial(historial):
    with open(ARCHIVO_HISTORIAL, "w") as f:
        json.dump(historial, f, indent=4)

def buscarProducto(datos, codigo):
    for producto in datos:
        if producto["codigo"] == codigo:
            return producto
    return None

def fecha():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def registrarProducto(datos):
    codigo = input("Código: ")

    if buscarProducto(datos, codigo):
        print("Ya existe")
        return

    nombre = input("Nombre: ")
    proveedor = input("Proveedor: ")

    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "proveedor": proveedor,
        "bodegas": {"norte": 0, "centro": 0, "oriente": 0}
    }

    datos.append(producto)
    guardarDatos(datos)
    print("Producto registrado")

def ingresarProducto(datos):
    codigo = input("Código: ")
    producto = buscarProducto(datos, codigo)

    if not producto:
        print("No existe")
        return

    bodega = input("Bodega: ").lower()

    if bodega not in ["norte", "centro", "oriente"]:
        print("Bodega inválida")
        return

    cantidad = input("Cantidad: ")

    if not cantidad.isdigit():
        print("Cantidad inválida")
        return

    cantidad = int(cantidad)
    descripcion = input("Descripción: ")

    producto["bodegas"][bodega] += cantidad
    guardarDatos(datos)

    movimiento = {
        "codigo": codigo,
        "tipo": "entrada",
        "bodega": bodega,
        "cantidad": cantidad,
        "descripcion": descripcion,
        "fecha": fecha()
    }

    historial = cargarHistorial()
    historial.append(movimiento)
    guardarHistorial(historial)

    print("Ingreso realizado")

def sacarProducto(datos):
    codigo = input("Código: ")
    producto = buscarProducto(datos, codigo)

    if not producto:
        print("No existe")
        return

    bodega = input("Bodega: ").lower()

    if bodega not in ["norte", "centro", "oriente"]:
        print("Bodega inválida")
        return

    cantidad = input("Cantidad: ")

    if not cantidad.isdigit():
        print("Cantidad inválida")
        return

    cantidad = int(cantidad)

    if producto["bodegas"][bodega] < cantidad:
        print("No hay suficiente")
        return

    descripcion = input("Descripción: ")

    producto["bodegas"][bodega] -= cantidad
    guardarDatos(datos)

    movimiento = {
        "codigo": codigo,
        "tipo": "salida",
        "bodega": bodega,
        "cantidad": cantidad,
        "descripcion": descripcion,
        "fecha": fecha()
    }

    historial = cargarHistorial()
    historial.append(movimiento)
    guardarHistorial(historial)

    print("Salida realizada")

def buscar(datos):
    codigo = input("Código: ")
    producto = buscarProducto(datos, codigo)

    if not producto:
        print("No existe")
        return

    print("Nombre:", producto["nombre"])
    print("Proveedor:", producto["proveedor"])
    print("Bodegas:", producto["bodegas"])
    

def historial(datos):
    codigo = input("Código: ")

    lista_historial = cargarHistorial()

    for movimiento in lista_historial:
        if movimiento["codigo"] == codigo:
            print("=================")

            for clave,valor in movimiento.items():
                print(clave,":",valor)


def transferir(datos):

    codigoProducto = input("Código: ")
    producto = buscar(datos)

    if codigoProducto != producto:
        print("No existe")
        return

    bodegaOrigen = input("Bodega de origen: ").lower()

    if bodegaOrigen not in ["norte", "centro", "oriente"]:
        print("Bodega inválida")
        return
    

    bodegaDestino = input("Bodega de destino: ")
    if bodegaDestino not in ["norte", "centro", "oriente"]:
        print("Bodega inválida")
        return

    
    cantidad = input("cantidad: ")

    if not cantidad.isdigit():
        print("Cantidad inválida")
        return

    cantidad = int(cantidad)

    if producto["bodegas"][bodegaOrigen] < cantidad:
        print("No hay suficiente Stock en la bodega de origen")
        return
    
    descripcion = input("Descripción: ")
    
    producto["bodegas"][bodegaOrigen] -= cantidad
    guardarDatos(datos)


    transferencia = {
        "codigo": codigoProducto,
        "tipo": "transferido",
        "bodega": bodegaOrigen,
        "cantidad": cantidad,
        "descripcion": descripcion,
        "fecha": fecha()
    }
    historial = cargarHistorial()
    historial.append(transferencia)
    guardarHistorial(historial)

    print("Transferencia realizada")


def reporte(datos):
    for producto in datos:
        total = sum(producto["bodegas"].values())
        print(producto["nombre"], "-", total)

    guardar = input("¿Guardar reporte? (si/no): ")

    if guardar.lower() == "si":
        with open("reporte.txt", "w") as f:
            for producto in datos:
                total = sum(producto["bodegas"].values())
                f.write(f"{producto['nombre']} - Total: {total}\n")


