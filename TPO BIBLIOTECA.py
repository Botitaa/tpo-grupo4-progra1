#SISTEMA GESTION DE BIBLIOTECAS GRUPO 4 VIERNES TARDE

import os
from datetime import date, timedelta

# ---- Utilidades ----

def limpiar_consola():
    """Limpia la consola; si no funciona, imprime líneas en blanco."""
    print("\n" * 50) # Alternativa simple
    os.system('cls' if os.name == 'nt' else 'clear')

# ---- Gestión de libros ----
def matriz_transpuesta(matriz_libros):
    transpuesta = []
    for i in range(len(matriz_libros[0])):
        fila_transpuesta = []
        for j in range(len(matriz_libros)):
            fila_transpuesta.append(matriz_libros[j][i])
        transpuesta.append(fila_transpuesta)
    return transpuesta

def mostrar_libros(matriz_libros):
    print("\n               --- Lista de Libros --- \n ")
    print("ID | Título              | Autor             | Disponible    | Cantidad")
    for fila in matriz_libros:
        print(f"{fila[0]:<3}| {fila[1]:<20}| {fila[2]:<18}| {fila[3]}            |{fila[4]}")

def buscar_libro_parcial(libros):
    """Busca y muestra libros por parte del txto del titulo o del autor."""
    print('\n----Busqueda de libros---')    
    print('1. Busqueda por titulo')    
    print('2. Busqueda por autor')    
    print('0. Volver')
    opcion = input('\nSeleccione una opcion por favor: ').strip()
    if opcion == '0':
        print('Volviendo...')
        return
    if opcion == '1':
        busqueda = input("Ingrese el título del libro a buscar: ").strip().lower()  # ingreso por teclado en minúsculas
        columna = 1
    if opcion == '2':
        busqueda = input("Ingrese el autor del libro a buscar: ").strip().lower()  # ingreso por teclado en minúsculas
        columna = 2
    else:
        print('Opcion invalida.')
        return []
       
    encontrados = [] 
    for fila in libros:
        if busqueda in fila[columna].lower():
            encontrados.append(fila)
            
    if len(encontrados) == 0:
        print('No se encontro ningun libro con ese texto')
        return []
    
    print('\nLibros encotrados:')
    mostrar_libros(encontrados)
    return encontrados

def agregar_libro(libros):
    """Agrega un nuevo libro a la matriz de libros."""
    print('\n--- Agregar Libro ---\n')
    if len(libros)> 0:
        nuevo_id = libros[-1][0] + 1
    else:
        nuevo_id = 1
        
    titulo = input('Ingrese el titulo del libro por favor: ').strip()
    autor = input('Ingrese el autor por favor: ').strip()
    
    duplicado = False

    for fila in libros:
        if fila[1].lower() == titulo.lower():
            duplicado = True
    if duplicado == True:
        print('Ese libro ya existe en la biblioteca.')
        return
    
    cantidad = -1

    while cantidad < 0:
        cantidad_str = input('Ingrese la cantidad en stock: ')
        if cantidad_str.isdigit():
            cantidad = int(cantidad_str)
            if cantidad<0:
                print('La cantidad no puede ser negativa.')
        else:
            print('Ingrese un numero entero valido.')
    
    if cantidad>0:
        disponibilidad = True
    else:
        disponibilidad = False
        
    libros.append([nuevo_id,titulo,autor,disponibilidad,cantidad])
    print(f'Libro "{titulo}" agregado con exito.')

def eliminar_libro(libros):
    """Elimina un libro de la matriz de libros por ID."""
    print("\n--- Eliminar Libro ---\n")
    mostrar_libros(libros)
    criterio = input("\nIngrese el ID del libro a eliminar: ").strip()
    
    eliminado = False
    
    if criterio.isdigit():
        criterio_num = int(criterio)
        for fila in libros:
            if fila[0] == criterio_num:
                mostrar_libros([fila])
                confirmacion = input( '\nEsta seguro que quiere eliminar este libro? (S/N): ').lower().strip()
                if confirmacion == 's':
                    titulo_eliminado = fila[1]
                    libros.remove(fila)
                    print(f"\nLibro: {titulo_eliminado}  (ID: {criterio_num}) eliminado con éxito.")
                    eliminado = True
                else:#queda vacante el ID 
                    print('\nOperacion cancelada, no se elimino el libro.')
                break    
            else:
                print('Ingrese un ID valido por favor')
                
    if eliminado == False:
        print("No se encontró el libro.")
    else:
        reordenar_ids(libros)

def reordenar_ids(libros):
    '''Reasigna los id de los libros consecutivamente desde 1'''
    for i in range(len(libros)):
        libros[i][0] = i + 1
# ---- Gestión de usuarios ----

def registrar_usuario(usuarios):

    # Asegurar estructura mínima de 5 listas (por si acaso)
    while len(usuarios) < 5:
        usuarios.append([])

    print("\n--- Registro de Usuario ---\n")

    # ------- Nombre -------
    validado = False
    while not validado:
        nombre = input("Ingrese nombre del usuario: ")

        if not nombre.strip():
            print("El nombre no puede estar vacío. Intente nuevamente.")
            continue
        elif not (3 <= len(nombre) <= 25):
            print("El nombre debe tener entre 3 y 25 caracteres.")
            continue
        elif not nombre.replace(" ", "").isalpha():
            print("El nombre solo debe contener letras y espacios.")
            continue
        elif nombre in usuarios[0]:
            print("El usuario ya existe. Intente con otro nombre.")
            continue
        else:
            validado = True

    usuarios[0].append(nombre)

    # ------- DNI -------
    validado = False
    dnis_existentes = set(map(str, usuarios[1]))
    while not validado:
        documento = input("Ingrese el DNI del usuario: ")

        if not documento.strip():
            print("El documento no puede estar vacío.")
            continue
        elif not documento.isdigit():
            print("El documento solo debe contener números.")
            continue
        elif not (7 <= len(documento) <= 9):
            print("El documento debe tener entre 7 y 9 dígitos.")
            continue
        elif documento in dnis_existentes:
            print("El documento ya está registrado.")
            continue

        validado = True

    usuarios[1].append(int(documento))

    # ------- Teléfono (10 dígitos y empieza con 11) -------
    validado = False
    tels_existentes = set(map(str, usuarios[2]))
    while not validado:
        telefono = input("Ingrese el teléfono (10 dígitos, debe iniciar con 11): ")

        if not telefono.strip():
            print("El teléfono no puede estar vacío.")
            continue
        elif not telefono.isdigit():
            print("El teléfono solo debe contener números.")
            continue
        elif len(telefono) != 10:
            print("El teléfono debe tener exactamente 10 dígitos.")
            continue
        elif not telefono.startswith("11"):
            print("El teléfono debe iniciar con '11'.")
            continue
        elif telefono in tels_existentes:
            print("Ese teléfono ya está registrado.")
            continue

        validado = True

    usuarios[2].append(int(telefono))

    # ------- Email (debe tener @ y un . después) -------
    validado = False
    emails_existentes = set(e.lower() for e in usuarios[3])
    while not validado:
        email = input("Ingrese el email: ").strip().lower()

        if not email:
            print("El email no puede estar vacío.")
            continue
        elif "@" not in email:
            print("El email debe contener '@'.")
            continue

        local, sep, dominio = email.partition("@")
        if not local or "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
            print("Formato de email inválido. Ej: usuario@dominio.com")
            continue
        elif email in emails_existentes:
            print("Ese email ya está registrado.")
            continue

        validado = True

    usuarios[3].append(email)

    # ------- Dirección (debe tener letras y números) -------
    validado = False
    while not validado:
        direccion = input("Ingrese la dirección: ").strip()

        if not direccion:
            print("La dirección no puede estar vacía.")
            continue
        
        tiene_letras = any(c.isalpha() for c in direccion)
        tiene_numeros = any(c.isdigit() for c in direccion)
        
        if not (tiene_letras and tiene_numeros):
            print("La dirección debe contener letras y números (ej: 'Calle Falsa 123').")
            continue

        validado = True

    usuarios[4].append(direccion)

    print(f"\n✅ {nombre} (DNI {documento}) registrado con éxito.\n")
    return usuarios

def mostrar_usuarios(usuarios):
    print("\n--- Lista de Usuarios ---\n")

    # Encabezados con formato tipo tabla
    encabezados = ["Nombre", "DNI", "Teléfono", "Email", "Dirección", "Estado"]
    print(f"| {encabezados[0]:<12} | {encabezados[1]:<10} | {encabezados[2]:<12} | {encabezados[3]:<30} | {encabezados[4]:<40} | {encabezados[5]:<12} |")
    print("-" * 136)

    # Cantidad de usuarios (filas)
    cant_usuarios = len(usuarios[0])

    # Recorrer cada usuario
    for i in range(cant_usuarios):
        nombre = str(usuarios[0][i])
        dni = str(usuarios[1][i])
        telefono = str(usuarios[2][i])
        email = str(usuarios[3][i])
        direccion = str(usuarios[4][i])
        bloqueado = usuarios[5][i]

        estado = "(Bloqueado)" if bloqueado else "Sin faltas"

        print(f"| {nombre:<12} | {dni:<10} | {telefono:<12} | {email:<30} | {direccion:<40} | {estado:<12} |")


def eliminar_usuario(usuarios):
    """Elimina un usuario """

    nombre = str(input("Ingrese el nombre del usuario a eliminar: "))

    if nombre not in usuarios[0]:
        print("El usuario no existe.")
        return

    intento = input("Ingrese la contraseña de administrador para confirmar: ")

    if intento != contrasenia:
        print("Contraseña incorrecta. Operación cancelada.")
        return
    
    if contrasenia == intento:
        indice = usuarios[0].index(nombre)
        for u in usuarios:
            u.pop(indice)
    
    print(f"Usuario '{nombre}' eliminado con éxito.")
    


def editar_usuario(usuarios):
    """Permite modificar el nombre de un usuario."""
    
    nombre = str(input("Ingrese el nombre del usuario a editar: ")).lower

    if nombre not in usuarios[0]:
        print("El usuario no existe.")
        return
    
    indice = usuarios[0].index(nombre)
    
    intento = input("Ingrese la contraseña de administrador para confirmar: ")

    if intento != contrasenia:
        print("Contraseña incorrecta. Operación cancelada.")
        return
    
    
    confirmado = False
    while not confirmado:

        print("1. Nombre")
        print("2. Dni")
        print("3. Telefono")
        print("4. Email")
        print("5. Direccion")
        print("6. Estado")
        print("0. volver")

        opcion = int(input("Elija un campo para editar: "))

        if opcion == 0:
            confirmado = True
            return
        elif opcion == 1:
            #editar nombre
            nuevo_nombre = input("Ingrese el nuevo nombre del usuario: ")
        
            if nuevo_nombre in usuarios[0]:
                print("El usuario ya existe. Intente con otro nombre.")
            elif not nuevo_nombre.strip():
                print("El nombre no puede estar vacío. Intente nuevamente.")
            elif len(nuevo_nombre) < 3 or len(nuevo_nombre) > 25:
                print("El nombre debe tener al menos 3 caracteres y menos de 25 caracteres. Intente nuevamente.")
            elif not nuevo_nombre.replace(" ", "").isalpha():
                print("El nombre solo debe contener letras y espacios. Intente nuevamente.")
            else:            
                usuarios[0][indice] = nuevo_nombre
                print("Usuario editado con éxito.")
                print(nombre,"cambio a:", nuevo_nombre)
                nombre = nuevo_nombre
        elif opcion == 2:
            #editar dni
            nuevo_dni = input("Ingrese el nuevo DNI del usuario: ")

            if not nuevo_dni.strip():
                print("El documento no puede estar vacío.")
            elif not nuevo_dni.isdigit():
                print("El documento solo debe contener números.")
            elif not (7 <= len(nuevo_dni) <= 9):
                print("El documento debe tener entre 7 y 9 dígitos.")
            elif int(nuevo_dni) in usuarios[1]:
                print("El documento ya está registrado.")
            else:
                usuarios[1][indice] = int(nuevo_dni)
                print("DNI editado con éxito.")
        elif opcion == 3:
            #editar telefono
            nuevo_telefono = input("Ingrese el nuevo teléfono (10 dígitos, debe iniciar con 11): ")

            if not nuevo_telefono.strip():
                print("El teléfono no puede estar vacío.")
            elif not nuevo_telefono.isdigit():
                print("El teléfono solo debe contener números.")
            elif len(nuevo_telefono) != 10:
                print("El teléfono debe tener exactamente 10 dígitos.")
            elif not nuevo_telefono.startswith("11"):
                print("El teléfono debe iniciar con '11'.")
            elif int(nuevo_telefono) in usuarios[2]:
                print("Ese teléfono ya está registrado.")
            else:
                usuarios[2][indice] = int(nuevo_telefono)
                print("Teléfono editado con éxito.")
        elif opcion == 4:
            #editar email
            nuevo_email = input("Ingrese el nuevo email: ").strip().lower()

            if not nuevo_email:
                print("El email no puede estar vacío.")
            elif "@" not in nuevo_email:
                print("El email debe contener '@'.")
            else:
                usuarios[3][indice] = nuevo_email
                print("Email editado con éxito.")
        elif opcion == 5:
            #direccion
            nueva_direccion = input("Ingrese la nueva dirección: ").strip()

            if not nueva_direccion:
                print("La dirección no puede estar vacía.")
            else:
                    usuarios[4][indice] = nueva_direccion
                    print("Dirección editada con éxito.")
        elif opcion == 6:
            #estado
            usuarios[5][indice] = not usuarios[5][indice]
            estado = "bloqueado" if usuarios[5][indice] else "desbloqueado"
            print(f"Usuario {estado} con éxito.")
        else:
            print("Elija una opcion correcta: ")



# ---- Gestión de préstamos ----

def listar_prestamos(matriz_prestamos):
    print("\n--- Lista de Préstamos ---\n")
    print(f"{'Usuario':<15} | {'Libro':<25} | {'Fecha ingreso':<15} | {'Fecha límite':<15}")
    print("-" * 80)

    for fila in matriz_prestamos:
        print(f"{fila[0]:<15} | {fila[1]:<25} | {fila[2]:<15} | {fila[3]:<15}")


def prestar_libro(libros, usuarios, prestamos):
    """Registra un préstamo si hay stock y el usuario existe."""

    libro_prestar = input("Ingrese el título del libro a prestar: ")

    if libro_prestar not in [libro[1] for libro in libros]:
        print("El libro no existe en la biblioteca.")
        return
    elif libros[[libro[1] for libro in libros].index(libro_prestar)][4] <= 0:
        print("No hay stock disponible para este libro.")
        return

    usuario_prestar = input("Ingrese el nombre del usuario: ")

    while usuario_prestar not in usuarios[0]:
        print("El usuario no está registrado.")
        usuario_prestar = input("Ingrese un usuario válido: ")

    suma = 0

    for i in prestamos:
        if i[0] == usuario_prestar:
            suma += 1
        if suma >= 3:
            print("supero el maximo de 3 prestamos")
            return

    fecha_ingreso = date.today().strftime("%d/%m/%Y")
    fecha_limite = determinar_fecha_vencimiento(date.today())

    prestamos.append([usuario_prestar, libro_prestar, fecha_ingreso, fecha_limite])
    libros[[libro[1] for libro in libros].index(libro_prestar)][4] -= 1
    print("Préstamo registrado con éxito.", prestamos[-1])

def devolver_libro(libros, prestamos):
    """Devuelve un libro prestado y actualiza el stock."""
    
    usuario_devolver = input("Ingrese el nombre del usuario que devuelve el libro: ")
    libro_devolver = input("Ingrese el título del libro a devolver: ")

    for prestamo in prestamos:
        if prestamo[0] == usuario_devolver and prestamo[1] == libro_devolver:
            prestamos.remove(prestamo)
            libros[[libro[1] for libro in libros].index(libro_devolver)][4] += 1
            print("Libro devuelto con éxito.")
            return

    print("No se encontró un préstamo para este usuario y libro.")


def prestamos_vencidos(prestamos):
    """Muestra los préstamos que han vencido."""
    hoy = date.today()
    print("\n--- Préstamos Vencidos ---\n")
    print(f"{'Usuario':<15} | {'Libro':<25} | {'Fecha ingreso':<15} | {'Fecha límite':<15}")
    print("-" * 80)

    for fila in prestamos:
        partes = fila[3].split("/")   # ["27","07","2025"]
        dia = int(partes[0])
        mes = int(partes[1])
        anio = int(partes[2])
        fecha_limite = date(anio, mes, dia)

        if fecha_limite < hoy:
            print(f"{fila[0]:<15} | {fila[1]:<25} | {fila[2]:<15} | {fila[3]:<15}")


def determinar_fecha_vencimiento(fecha_hoy):
    print("1. 7 días")
    print("2. 15 días")
    print("3. 30 días")

    opcion = input("Seleccione el plazo de devolución: ")

    dias_a_sumar = 0
    if opcion == '1':
        dias_a_sumar = 7
    elif opcion == '2':
        dias_a_sumar = 15
    elif opcion == '3':
        dias_a_sumar = 30
    else:
        print("Opción inválida. Se asignarán 7 días por defecto.")
        dias_a_sumar = 7

    fecha_vencimiento = fecha_hoy + timedelta(days=dias_a_sumar)
    return fecha_vencimiento.strftime("%d/%m/%Y")

def renovacion_prestamos():

    pass

# ---- Gestión de menues ----

def menu_principal():

    print("\n--- Biblioteca ---")
    print("1. Gestión de Libros")
    print("2. Gestión de Usuarios")
    print("3. Gestión de Préstamos")
    print("0. Salir")

    opcion = input("Seleccione una opción: ")
    limpiar_consola()


    if opcion == '1':
        menu_libros()
    elif opcion == '2':
        menu_usuarios()
    elif opcion == '3':
        menu_prestamos()
    elif opcion == '0':
        print("Saliendo del sistema...")
        quit()
    else:
        print("Opción inválida, intente nuevamente.")


def menu_libros():


    print("\n--- Gestión de Libros ---")
    print("1. Mostrar libros")
    print("2. Buscar libro por título")
    print("3. Agregar libro")
    print("4. Eliminar libro")
    print("0. Volver al menú principal")

    opcion = input("Seleccione una opción: ")
    
    limpiar_consola()
    
    if opcion == '1':
        mostrar_libros(libros)
    elif opcion == '2':
        buscar_libro_parcial(libros)
    elif opcion == '3':
        agregar_libro(libros)
    elif opcion == '4':
        eliminar_libro(libros)
    elif opcion == '0':
        menu_principal()
    else:
        print("Opción inválida, intente nuevamente.")

def menu_usuarios():

    
    print("\n--- Gestión de Usuarios ---")
    print("1. Registrar usuario")
    print("2. Mostrar usuarios")
    print("3. Editar usuario")
    print("4. Eliminar usuario")
    print("0. Volver al menú principal")

    opcion = input("Seleccione una opción: ")
    
    limpiar_consola()

    if opcion == '1':
        registrar_usuario(usuarios)
    elif opcion == '2':
        mostrar_usuarios(usuarios)
    elif opcion == '3':
        editar_usuario(usuarios)
    elif opcion == '4':
        eliminar_usuario(usuarios)
    elif opcion == '0':
        menu_principal()    
    else:
        print("Opción inválida, intente nuevamente.")

def menu_prestamos():

    
    print("\n--- Gestión de Préstamos ---")
    print("1. Listar préstamos")
    print("2. Prestar libro")
    print("3. Devolver libro")
    print("4. Préstamos vencidos")
    print("5. Renovacion")
    print("0. Volver al menú principal")
    
    opcion = input("Seleccione una opción: ")

    limpiar_consola()

    if opcion == '1':
        listar_prestamos(prestamos)
    elif opcion == '2':
        prestar_libro(libros, usuarios, prestamos)
    elif opcion == '3':
        devolver_libro(libros, prestamos)
    elif opcion == '4':
        prestamos_vencidos(prestamos)
    elif opcion == "5":
        renovacion_prestamos()
    elif opcion == '0':
        menu_principal()
    else:
        print("Opción inválida, intente nuevamente.")

#Programa Principal

libros = [
    #ID, Titulo, Autor, Disponibilidad, Cantidad en stock
    [1, "El Quijote", "Cervantes", True, 20],
    [2, "Cien Años de Soledad", "G. García Márquez", True, 2],
    [3, "La Odisea", "Homero", False, 0]
]

usuarios = [       
    # lista de usuarios
    # nombre, DNI, tel, mail, direcciónx, bloqueado
    
    ['juan', 'maria', 'pedro'],
    [46962189, 12345678, 98765432],
    [1126030810, 1189077253, 1178540819],
    ['juanagarcia@hotmail.com', 'mariacrisler@gmail.com', 'pedrotrota@gmail.com'],
    ['Calle Falsa 123', 'Avenida Siempre Viva 742', 'Boulevard de los Sueños Rotos 456'],
    [True, False, False]  # bloqueado

]

prestamos = [
    # lista de préstamos (usuario, libro, fecha ingreso, fecha maxima de devolución)

    ["juan", "El Quijote", "01/07/2025", "27/07/2025"],
    ["juan", "El Quijote", "01/07/2025", "27/07/2025"],
    ["juan", "El Quijote", "01/07/2025", "27/07/2025"]
]

prestamos_morosos = [
    # lista de préstamos morosos (usuario, libro, fecha ingreso, fecha maxima de devolución)

    ["juan", "El Quijote", "01/07/2025", "27/07/2025"]
]

contrasenia = "admin1234"

while True: 

    menu_principal()


