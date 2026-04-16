import funciones

datos = funciones.cargarDatos()

while True:

    print("==============================================")
    print("MENÚ")
    print("==============================================")
    print("1. REGISTRAR PRODUCTO AL INVENTARIO")
    print("2. INGRESAR PRODUCTO AL INVENTARIO")
    print("3. SACAR PRODUCTO DEL INVENTARIO")
    print("4. BUSCAR PRODUCTO EN EL INVENTARIO")
    print("5. HISTORIAL DEL PRODUCTO")
    print("6. TRANSFERIR PRODUCTO ENTRE BODEGAS")
    print("7. VER REPORTE")
    print("8. SALIR")
    print("==============================================")
    opcion = input("Opción: ")

    match opcion:

        case "1":
            funciones.registrarProducto(datos)
        case "2":
            funciones.ingresarProducto(datos)
        case "3":
            funciones.sacarProducto(datos)
        case "4":
            funciones.buscar(datos)
        case "5":
            funciones.historial(datos)
        case "6":
            funciones.transferir(datos)
        case "7":
            funciones.reporte(datos)
        case "8":
            print("Saliendo...")
            break
        case _:
            print("Opción inválida")
