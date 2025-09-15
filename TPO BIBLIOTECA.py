#SISTEMA GESTION DE BIBLIOTECAS GRUPO 4 VIERNES TARDE

import os

# ---- Funciones ----

def limpiar_consola():
    """Limpia la consola; si no funciona, imprime líneas en blanco."""
    os.system('cls' if os.name == 'nt' else 'clear')
    #print("\n" * 50)

def mostrar_menu():
    print("\n--- Biblioteca ---")
    print("1. Mostrar libros")
    print("2. Registrar usuario")
    print("3. Mostrar usuarios")
    print("4. Listar préstamos")
    print("0. Salir")

def mostrar_libros(matriz_libros):
    print("\n               --- Lista de Libros --- \n ")
    print("ID | Título              | Autor             | Disponible    | Cantidad")
    for fila in matriz_libros:
        print(f"{fila[0]:<3}| {fila[1]:<20}| {fila[2]:<18}| {fila[3]}            |{fila[4]}")

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


# ---- Gestión de préstamos ----

def listar_prestamos(matriz_prestamos):
    print("\n                       --- Lista de prestamos --- \n ")
    print("|Usuario            | Libro               | Fecha de ingreso    | Fecha de devolución")
    for fila in matriz_prestamos:
        print(f"|{fila[0]:<3}               | {fila[1]:<20}| {fila[2]:<18}  | {fila[3]}")

def prestar_libro(libros, usuarios, prestamos):
    """Registra un préstamo si hay stock y el usuario existe."""
    
    pass

def devolver_libro(libros, prestamos):
    """Devuelve un libro prestado y actualiza el stock."""
    pass


# ---- Gestión de usuarios ----

def eliminar_usuario(usuarios, prestamos):
    """Elimina un usuario si no tiene préstamos activos."""
    pass

def editar_usuario(usuarios):
    """Permite modificar el nombre de un usuario."""
    pass


# ---- Reportes y menús auxiliares ----
def mostrar_menu_prestamos():
    """Muestra las opciones relacionadas con préstamos."""
    pass

# ---- Gestión de libros ----

def buscar_libro_por_titulo(libros):
    """Busca y muestra libros cuyo título contenga un texto."""
    pass

#Programa Principal

libros = [
    #ID, Titulo, Autor, Disponibilidad, Cantidad en stock
    [1, "El Quijote", "Cervantes", "Sí", "20"],
    [2, "Cien Años de Soledad", "G. García Márquez", "Sí", "2"],
    [3, "La Odisea", "Homero", "Sí", "13"]
]

usuarios = ["juan", "ricardo", "miguel"]       # lista de usuarios

prestamos = [
    # lista de préstamos (usuario, libro, fecha ingreso, fecha devolución)

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
    elif opcion == 0:
        print("Saliendo del sistema...")
    else:
        print("Opción inválida, intente nuevamente.")