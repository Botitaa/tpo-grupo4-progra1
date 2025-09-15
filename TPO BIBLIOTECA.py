#SISTEMA GESTION DE BIBLIOTECAS GRUPO 4 VIERNES TARDE

import os

# ---- Gestion de menues ----

def limpiar_consola():
    """Limpia la consola; si no funciona, imprime líneas en blanco."""
    print("\n" * 50) # Alternativa simple
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n--- Biblioteca ---")
    print("1. Mostrar libros")
    print("2. Registrar usuario")
    print("3. Mostrar usuarios")
    print("4. Listar préstamos")
    print("5. Eliminar usuario")
    print("6. Editar usuario")
    print("7. Prestar libro")
    print("8. Devolver libro")
    print("0. Salir")


# ---- Gestión de libros ----
def mostrar_libros(matriz_libros):
    print("\n               --- Lista de Libros --- \n ")
    print("ID | Título              | Autor             | Disponible    | Cantidad")
    for fila in matriz_libros:
        print(f"{fila[0]:<3}| {fila[1]:<20}| {fila[2]:<18}| {fila[3]}            |{fila[4]}")

def buscar_libro_por_titulo(libros):
    """Busca y muestra libros cuyo título contenga un texto."""
    pass

def agregar_libro(libros):
    """Agrega un nuevo libro a la matriz de libros."""
    pass

def eliminar_libro(libros):
    """Elimina un libro de la matriz de libros."""
    pass

def editar_libro(libros):
    """Permite modificar los datos de un libro."""
    pass



# ---- Gestión de usuarios ----
def registrar_usuario(usuarios):

    print("\n--- Registro de Usuario ---\n")

    nombre = input("Ingrese nombre del usuario: ")

    #verificaciones

    while nombre in usuarios:
        print("El usuario ya existe. Intente con otro nombre.")
        nombre = input("Ingrese nombre del usuario: ")
    while not nombre.strip():
        print("El nombre no puede estar vacío. Intente nuevamente.")
        nombre = input("Ingrese nombre del usuario: ")
    while len(nombre) < 3 or len(nombre) > 25:
        print("El nombre debe tener al menos 3 caracteres y menos de 25 caracteres. Intente nuevamente.")
        nombre = input("Ingrese nombre del usuario: ")
    while not nombre.replace(" ", "").isalpha():
        print("El nombre solo debe contener letras y espacios. Intente nuevamente.")
        nombre = input("Ingrese nombre del usuario: ")

    usuarios.append(nombre)
    print("Usuario registrado con éxito.")

def mostrar_usuarios(usuarios):
    print("\n--- Lista de Usuarios ---\n")
    if len(usuarios) == 0:
        print("No hay usuarios registrados.")
    else:
        for i, usuario in enumerate(usuarios):
            print(f"{i+1}. {usuario}")

def eliminar_usuario(usuarios):
    """Elimina un usuario """

    nombre = str(input("Ingrese el nombre del usuario a eliminar: "))

    if nombre not in usuarios:
        print("El usuario no existe.")
        return
    
    for nombres in usuarios:
        if nombres == nombre:
            usuarios.remove(nombres)
            print("Usuario eliminado con éxito.")
            return
    
def editar_usuario(usuarios):
    """Permite modificar el nombre de un usuario."""
    
    nombre = str(input("Ingrese el nombre del usuario a editar: "))

    if nombre not in usuarios:
        print("El usuario no existe.")
        return
    
    nuevo_nombre = input("Ingrese el nuevo nombre del usuario: ")
    
    for n in range(0,len(usuarios),1):
        if usuarios[n] == nombre:
            usuarios[n] = nuevo_nombre
            print("Usuario editado con éxito.")
            print(nombre,"cambio a:", nuevo_nombre)
            return


# ---- Gestión de préstamos ----

def listar_prestamos(matriz_prestamos):
    print("\n                       --- Lista de prestamos --- \n ")
    print("|Usuario            | Libro               | Fecha de ingreso    | Fecha limite de devolución")
    for fila in matriz_prestamos:
        print(f"|{fila[0]:<3}               | {fila[1]:<20}| {fila[2]:<18}  | {fila[3]}")

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

    if usuario_prestar not in usuarios:
        print("El usuario no está registrado.")
        return
    
    fecha_ingreso = input("Ingrese la fecha de ingreso (dd/mm/aaaa): ")

    fecha_limite = input("Ingrese la fecha límite de devolución (dd/mm/aaaa): ")

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



# ---- Reportes y menús auxiliares ----
def mostrar_menu_prestamos():
    """Muestra las opciones relacionadas con préstamos."""
    pass


#Programa Principal

libros = [
    #ID, Titulo, Autor, Disponibilidad, Cantidad en stock
    [1, "El Quijote", "Cervantes", True, 20],
    [2, "Cien Años de Soledad", "G. García Márquez", True, 2],
    [3, "La Odisea", "Homero", False, 0]
]

usuarios = ["juan", "ricardo", "miguel"]       # lista de usuarios

prestamos = [
    # lista de préstamos (usuario, libro, fecha ingreso, fecha maxima de devolución)

    ["juan", "El Quijote", "01/07/2025", "27/07/2025"]
]      

opcion = -1
while opcion != 0:
    mostrar_menu()
    opcion = int(input("Seleccione una opción: "))
    limpiar_consola()

    if opcion == 1:
        mostrar_libros(libros)
    elif opcion == 2:
        registrar_usuario(usuarios)
    elif opcion == 3:
        mostrar_usuarios(usuarios)
    elif opcion == 4:
        listar_prestamos(prestamos)
    elif opcion == 5:
        eliminar_usuario(usuarios)
    elif opcion == 6:
        editar_usuario(usuarios)
    elif opcion == 7:
        prestar_libro(libros, usuarios, prestamos)
    elif opcion == 8:
        devolver_libro(libros, prestamos)
    elif opcion == 0:
        print("Saliendo del sistema...")
    else:
        print("Opción inválida, intente nuevamente.")