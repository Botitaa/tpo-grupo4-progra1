#SISTEMA GESTION DE BIBLIOTECAS GRUPO 4 VIERNES TARDE

import os
import time
from datetime import datetime, date, timedelta
from colorama import Fore, Style, init


# ---- Utilidades ----

def limpiar_consola():
    "Limpia la consola; si no funciona, imprime líneas en blanco."
    print("\n" * 50)
    os.system('cls' if os.name == 'nt' else 'clear')

def abrir_archivo_seguro(ruta, modo="r"):
    "Abre un archivo intentando UTF-8 y luego Latin-1 si falla."
    try:
        return open(ruta, modo, encoding="utf-8")
    except UnicodeDecodeError:
        return open(ruta, modo, encoding="latin-1")

def registrar_log(evento, detalle):
    "Registra eventos del sistema en log.txt"
    try:
        tiempo = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        linea = f"{tiempo} [{evento}] {detalle}\n"
        with abrir_archivo_seguro("log.txt", "a") as archivo:

            archivo.write(linea)
    except Exception as e:
        print(f"Error al registrar en log: {e}")

def cambiar_contrasenia():
    "Permite cambiar la contraseña del administrador."

    global contrasenia

    intento = input("Ingrese la contraseña actual: ").strip()
    if intento != contrasenia:
        print(Fore.RED + "❌ Contraseña incorrecta.")
        return

    nueva = input("Ingrese la nueva contraseña: ").strip()
    confirmar = input("Confirme la nueva contraseña: ").strip()

    if nueva != confirmar:
        print(Fore.RED + "❌ Las contraseñas no coinciden.")
        return

    if len(nueva) < 4:
        print(Fore.YELLOW + "⚠ La contraseña debe tener al menos 4 caracteres.")
        return

    contrasenia = nueva

    try:
        with abrir_archivo_seguro("admin_pass.txt", "w") as archivo:
            archivo.write(contrasenia)
        print(Fore.GREEN + "✅ Contraseña cambiada y guardada correctamente.")
        registrar_log("CAMBIO DE CONTRASEÑA", "exitoso")
    except Exception as e:
        print(Fore.RED + f"⚠ Error al guardar la nueva contraseña: {e}")

def hacer_backup():
    "Crea copias de seguridad de los archivos importantes y registra el evento."
    try:
        # Crear carpeta backup si no existe
        if not os.path.exists("backup"):
            os.makedirs("backup")
            registrar_log("BACKUP", "Carpeta 'backup' creada automáticamente.")

        # --- Copia de LIBROS ---
        with abrir_archivo_seguro("libros.txt", "r") as origen:
            lineas = origen.readlines()
        with abrir_archivo_seguro("backup/libros_backup.txt", "w") as destino:
            destino.writelines(lineas)

        # --- Copia de USUARIOS ---
        with abrir_archivo_seguro("usuarios.txt", "r") as origen:
            lineas = origen.readlines()
        with abrir_archivo_seguro("backup/usuarios_backup.txt", "w") as destino:
            destino.writelines(lineas)

        # --- Copia de PRÉSTAMOS ---
        with abrir_archivo_seguro("prestamos.txt", "r") as origen:
            lineas = origen.readlines()
        with abrir_archivo_seguro("backup/prestamos_backup.txt", "w") as destino:
            destino.writelines(lineas)

        print(Fore.GREEN + "✅ Backup automático realizado correctamente (en carpeta 'backup').")
        registrar_log("BACKUP", "Backup automático completado correctamente.")

    except FileNotFoundError as e:
        mensaje = f"No se encontró uno de los archivos originales: {e.filename}"
        print(Fore.YELLOW + f"⚠ {mensaje}")
        registrar_log("BACKUP_ERROR", mensaje)

    except Exception as e:
        mensaje = f"Error al realizar el backup: {e}"
        print(Fore.RED + f"⚠ {mensaje}")
        registrar_log("BACKUP_ERROR", mensaje)

def ver_logs():
    "Muestra los últimos registros del archivo log.txt"
    ruta = "log.txt"
    if not os.path.exists(ruta):
        print(Fore.YELLOW + "⚠ No hay registros disponibles.")
        return

    print(Fore.CYAN + "\n📄 Últimos registros del sistema:\n" + Style.RESET_ALL)
    try:
        with abrir_archivo_seguro(ruta, "r") as archivo:
            lineas = archivo.readlines()[-30:]
            for linea in lineas:
                print(linea.strip())
    except Exception as e:
        print(Fore.RED + f"⚠ Error al leer logs: {e}")


# ---- Gestión de libros ----


def mostrar_libros(matriz_libros):
    print("\n" + Fore.CYAN + "--- Lista de Libros ---\n" + Style.RESET_ALL)

    # Encabezado
    print(Fore.YELLOW + f"{'ID':<5}{'Título':<30}{'Autor':<25}{'Disponible':<15}{'Cantidad':<10}")
    print(Fore.CYAN + "-" * 90 + Style.RESET_ALL)

    for fila in matriz_libros:
        id_libro = fila[0]
        titulo = str(fila[1])[:28]
        autor = str(fila[2])[:23]
        cantidad = fila[4]

        # Color para la disponibilidad
        if fila[3]:
            disponible = Fore.GREEN + "Sí" + Style.RESET_ALL
        else:
            disponible = Fore.RED + "No" + Style.RESET_ALL

        # Imprimir cada campo con formato fijo
        print(f"{id_libro:<5}{titulo:<30}{autor:<25}{disponible:<22}  {cantidad:<10}")

    print(Fore.CYAN + "-" * 90 + Style.RESET_ALL)

def buscar_libro_parcial(libros):
    "Busca y muestra libros por parte del txto del titulo o del autor."

    print('\n----Busqueda de libros---')    
    print('1. Busqueda por titulo')    
    print('2. Busqueda por autor')    
    print('0. Volver')

    opcion = input('\nSeleccione una opcion: ').strip()

    if opcion == '0':
        print('Volviendo...')
        return 
    elif opcion == '1':
        busqueda = input("Ingrese el título del libro a buscar (0 para volver): ").strip().lower()  # ingreso por teclado en minúsculas
        if busqueda == '0':
            print('Volviendo...')
            return 
        columna = 1
    elif opcion == '2':
        busqueda = input("Ingrese el autor del libro a buscar (0 para volver): ").strip().lower()  # ingreso por teclado en minúsculas
        if busqueda == '0':
            print('Volviendo...')
            return 
        columna = 2
    else:
        print(Fore.RED + 'Opcion invalida.')
        return []
       
    encontrados = [] 
    for fila in libros:
        if busqueda in fila[columna].lower():
            encontrados.append(fila)
            
    if len(encontrados) == 0:
        print(Fore.RED + 'No se encontro ningun libro con ese texto')
        return 
    
    limpiar_consola()
    
    print(Fore.YELLOW + f"Busqueda realizada: {busqueda} \nLibros encotrados: ")
    mostrar_libros(encontrados)
    return encontrados

def editar_libro(libros):
    print(Fore.YELLOW + "\n--- Editar libro ---")
    if not libros:
        print(Fore.RED + "No hay libros cargados.")
        return

    try:
        mostrar_libros(libros)
        entrada = input("\nIngrese el ID del libro a editar (o 0/salir para cancelar): ").strip().lower()
        if entrada in ("0", "salir"):
            print(Fore.RED + "Operación cancelada.")
            registrar_log("CANCELADO", "Edición de libro cancelada por usuario")
            return

        id_libro = int(entrada)
        libro_encontrado = None
        for libro in libros:
            if libro[0] == id_libro:
                libro_encontrado = libro
                break

        if not libro_encontrado:
            print(Fore.RED + "No se encontró el libro con ese ID.")
            return

        print(Fore.YELLOW + "\nLibro seleccionado:")
        mostrar_libros([libro_encontrado])

        print("\nCampos que puede modificar:")
        print("1 - Título")
        print("2 - Autor")
        print("3 - Cantidad")
        print("4 - Disponibilidad")
        print("0 - Salir")

        while True:
            opcion = input("\nSeleccione campo a modificar: ").strip().lower()
            if opcion in ("0", "salir"):
                print(Fore.GREEN + "Edición finalizada.")
                registrar_log("CANCELADO", f"Edición libro ID {id_libro} finalizada por usuario")
                break

            if opcion == "1":
                nuevo = input("Nuevo título: ").strip()
                if nuevo in ("0", "salir"):
                    print(Fore.RED + "CANCELADO.")
                    registrar_log("CANCELADO", "Cambio de título cancelado")
                    break
                if nuevo in [l[1] for l in libros if l != libro_encontrado]:
                    print(Fore.RED + "Ya existe un libro con ese título.")
                    continue
                conf = input("¿Confirmar cambio? (s/n): ").lower()
                if conf != "s":
                    print(Fore.GREEN + "Cambio cancelado.")
                    continue
                libro_encontrado[1] = nuevo
                registrar_log("cambio", f"Libro ID {id_libro} título -> '{nuevo}'")
                print(Fore.GREEN + "Título actualizado.")

            elif opcion == "2":
                nuevo = input("Nuevo autor: ").strip()
                if nuevo in ("0", "salir"):
                    break
                libro_encontrado[2] = nuevo
                registrar_log("CAMBIO", f"Libro ID {id_libro} autor -> '{nuevo}'")
                print(Fore.GREEN + "Autor actualizado.")

            elif opcion == "3":
                nuevo = input("Nueva cantidad: ").strip()
                if not nuevo.isdigit():
                    print(Fore.YELLOW + "Debe ser un número.")
                    continue
                libro_encontrado[4] = int(nuevo)
                libro_encontrado[3] = True if libro_encontrado[4] > 0 else False
                registrar_log("CAMBIO", f"Libro ID {id_libro} cantidad -> {nuevo}, disponible={libro_encontrado[3]}")
                print(Fore.GREEN + "Cantidad actualizada.")

            elif opcion == "4":
                nuevo = input("¿Disponible? (si/no): ").strip().lower()
                libro_encontrado[3] = True if nuevo in ("si", "s") else False
                registrar_log("CAMBIO", f"Libro ID {id_libro} disponibilidad -> {libro_encontrado[3]}")
                print(Fore.GREEN + "Disponibilidad modificada.")

            else:
                print(Fore.RED + "Opción inválida.")

        guardar_libros(ruta_libros, libros)
        registrar_log("GUARDAR", f"Datos guardados tras edición de libro ID {id_libro}")
        print(Fore.GREEN + "Cambios guardados correctamente.")

    except Exception as e:
        print(Fore.RED + "Error al editar libro:", e)
        registrar_log("ERROR", f"Fallo al editar libro: {e}")


def agregar_libro(libros):
    "Agrega un nuevo libro a la matriz de libros."
    print('\n--- Agregar Libro ---\n')
    if len(libros)> 0:
        nuevo_id = libros[-1][0] + 1
    else:
        nuevo_id = 1
        
    titulo = input('Ingrese el titulo del libro (0 para volver): ').strip()
    if titulo == '0':
        print('Volviendo...')
        return 
    autor = input('Ingrese el autor (0 para volve): ').strip()
    if autor == '0':
        print('Volviendo...')
        return
    duplicado = False

    for fila in libros:
        if fila[1].lower() == titulo.lower():
            duplicado = True
    if duplicado == True:
        print(Fore.YELLOW + 'Ese libro ya existe en la biblioteca.')
        return
    
    cantidad = -1

    while cantidad < 0:
        cantidad_str = input('Ingrese la cantidad en stock: ')
        if cantidad_str == '0':
            print('Volviendo...')
            return 
        if cantidad_str.isdigit():
            cantidad = int(cantidad_str)
            if cantidad<0:
                print(Fore.YELLOW + 'La cantidad no puede ser negativa.')
        else:
            print(Fore.YELLOW + 'Ingrese un numero entero valido.')
    
    if cantidad>0:
        disponibilidad = True
    else:
        disponibilidad = False
        
    libros.append([nuevo_id,titulo,autor,disponibilidad,cantidad])
    registrar_log("AGREGADO", f"titulo: {titulo}, autor: '{autor}', cantidad en stock {cantidad}")
    print(f'Libro "{titulo}" agregado con exito.')

def eliminar_libro(libros):
    print("\n--- Eliminar Libro ---\n")
    mostrar_libros(libros)

    criterio = input("\nIngrese el ID del libro a eliminar (0 para volver): ").strip()
    if criterio == '0':
        print('Volviendo...')
        return

    if not criterio.isdigit():
        print(Fore.YELLOW + 'Ingrese un ID numérico válido')
        return

    criterio_num = int(criterio)
    eliminado = False

    for fila in libros:
        if fila[0] == criterio_num:
            mostrar_libros([fila])
            confirmacion = input('\n¿Está seguro que quiere eliminar este libro? (S/N): ').lower().strip()
            if confirmacion == 's':
                titulo_eliminado = fila[1]
                libros.remove(fila)

                reordenar_ids(libros)
                guardar_libros(ruta_libros, libros)

                print(Fore.GREEN + f"\nLibro: {titulo_eliminado} (ID: {criterio_num}) eliminado con éxito.")
                registrar_log("ELIMINACION", f"Libro '{titulo_eliminado}' eliminado y IDs reordenados.")
                eliminado = True
            else:
                print(Fore.RED + '\nOperación cancelada, no se eliminó el libro.')
            break

    if not eliminado:
        print(Fore.RED + "No se encontró el libro.")

def reordenar_ids(libros, i=0):
    "Reasigna los IDs de los libros de forma recursiva desde 1."
    if i >= len(libros):
        return
    libros[i][0] = i + 1
    reordenar_ids(libros, i + 1)
    
def reporte_stock_bajo(libros):
    "Muestra un reporte de libros cuyo stock es menor a un umbral ingresado por el usuario."
    print("\n--- Reporte de stock bajo ---")
    try:    
        minimo_stock = input(int("Ingrese el mínimo de stock: "))
    except ValueError:
        print(Fore.YELLOW + "⚠ Ingrese un número entero válido.")
        return

    print("\n" + Fore.CYAN + f"--- Libros con stock menor a {minimo_stock} ---\n" + Style.RESET_ALL)
    print(Fore.YELLOW + f"{'ID':<5}{'Título':<35}{'Autor':<25}{'Stock':<10}" + Style.RESET_ALL)
    print(Fore.CYAN + "-" * 75 + Style.RESET_ALL)

    encontrados = False

    for libro in libros:
        if libro[4] < minimo_stock:
            encontrados = True
            color_stock = Fore.RED if libro[4] == 0 else Fore.YELLOW
            print(f"{libro[0]:<5}{libro[1]:<35}{libro[2]:<25}{color_stock}{libro[4]:<10}{Style.RESET_ALL}")

    if not encontrados:
        print(Fore.GREEN + "✅ No hay libros con stock menor al mínimo ingresado." + Style.RESET_ALL)

    print(Fore.CYAN + "-" * 75 + Style.RESET_ALL)


def exportar_libros_sin_stock(libros):
    try:
        with abrir_archivo_seguro("libros_sin_stock.txt", "w") as archivo:
            for libro in libros:
                if libro[4] == 0:
                    archivo.write(f"{libro[0]},{libro[1]},{libro[2]}\n")
        print(Fore.GREEN + "💾Libros sin stock exportados correctamente")
    except Exception as error:
        print(Fore.RED + "⚠ Error al exportar librossin stock:", error)



# ---- Gestión de usuarios ----

def registrar_usuario(usuarios):

    # Asegurar estructura mínima de 6 listas (por si acaso)
    while len(usuarios) < 6:
        usuarios.append([])

    print("\n--- Registro de Usuario ---\n")

    # ------- Nombre -------
    validado = False
    while not validado:
        nombre = input("Ingrese nombre del usuario (0 para volver): ")
        if nombre == '0':
            print('Volviendo...')
            return 
        if not nombre.strip():
            print(Fore.YELLOW + "El nombre no puede estar vacío. Intente nuevamente.")
            continue
        elif not (3 <= len(nombre) <= 25):
            print(Fore.YELLOW + "El nombre debe tener entre 3 y 25 caracteres.")
            continue
        elif not nombre.replace(" ", "").isalpha():
            print(Fore.YELLOW + "El nombre solo debe contener letras y espacios.")
            continue
        elif nombre in usuarios[0]:
            print(Fore.YELLOW + "El usuario ya existe. Intente con otro nombre.")
            continue
        else:
            validado = True

   

    # ------- DNI -------
    validado = False
    dnis_existentes = set(map(str, usuarios[1]))
    while not validado:
        documento = input("Ingrese el DNI del usuario: ")
        if documento == '0':
            print('Volviendo...')
            return

        if not documento.strip():
            print(Fore.YELLOW + "El documento no puede estar vacío.")
            continue
        elif not documento.isdigit():
            print(Fore.YELLOW + "El documento solo debe contener números.")
            continue
        elif not (7 <= len(documento) <= 9):
            print(Fore.YELLOW + "El documento debe tener entre 7 y 9 dígitos.")
            continue
        elif documento in dnis_existentes:
            print(Fore.GREEN + "El documento ya está registrado.")
            continue

        validado = True

    

    # ------- Teléfono (10 dígitos y empieza con 11) -------
    validado = False
    tels_existentes = set(map(str, usuarios[2]))
    while not validado:
        telefono = input("Ingrese el teléfono (10 dígitos, debe iniciar con 11): ")
        if telefono == '0':
            print('Volviendo...')
            return 
        if not telefono.strip():
            print(Fore.YELLOW + "El teléfono no puede estar vacío.")
            continue
        elif not telefono.isdigit():
            print(Fore.YELLOW + "El teléfono solo debe contener números.")
            continue
        elif len(telefono) != 10:
            print(Fore.YELLOW + "El teléfono debe tener exactamente 10 dígitos.")
            continue
        elif not telefono.startswith("11"):
            print(Fore.YELLOW + "El teléfono debe iniciar con '11'.")
            continue
        elif telefono in tels_existentes:
            print(Fore.YELLOW + "Ese teléfono ya está registrado.")
            continue

        validado = True

    

    # ------- Email (debe tener @ y un . después) -------
    validado = False
    emails_existentes = set(e.lower() for e in usuarios[3])
    while not validado:
        email = input("Ingrese el email (0 para volver): ").strip().lower()
        if email == '0':
            print('Volviendo...')
            return []
        if not email:
            print(Fore.YELLOW + "El email no puede estar vacío.")
            continue
        elif "@" not in email:
            print(Fore.YELLOW + "El email debe contener '@'.")
            continue

        local, sep, dominio = email.partition("@")
        if not local or "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
            print(Fore.RED + "Formato de email inválido. Ej: usuario@dominio.com")
            continue
        elif email in emails_existentes:
            print(Fore.YELLOW + "Ese email ya está registrado.")
            continue

        validado = True

    # ------- Dirección (debe tener letras y números) -------
    validado = False
    while not validado:
        direccion = input("Ingrese la dirección: ").strip()
        if direccion == '0':
            print('Volviendo...')
            return
        if not direccion:
            print(Fore.YELLOW + "La dirección no puede estar vacía.")
            continue
        
        tiene_letras = any(c.isalpha() for c in direccion)
        tiene_numeros = any(c.isdigit() for c in direccion)
        
        if not (tiene_letras and tiene_numeros):
            print(Fore.YELLOW + "La dirección debe contener letras y números (ej: 'Calle Falsa 123').")
            continue

        validado = True

    usuarios[0].append(nombre)
    usuarios[1].append(int(documento))
    usuarios[2].append(int(telefono))
    usuarios[3].append(email)
    usuarios[4].append(direccion)
    usuarios[5].append(False)

    print(Fore.GREEN + f"\n✅ {nombre} (DNI {documento}) registrado con éxito.\n")
    registrar_log("USUARIO", f"{nombre} (DNI {documento}) registrado con éxito.'")
    return usuarios

def mostrar_usuarios(usuarios):
    print("\n" + Fore.CYAN + "--- Lista de Usuarios ---\n" + Style.RESET_ALL)

    encabezados = ["Nombre", "DNI", "Teléfono", "Email", "Dirección", "Estado"]
    print(Fore.YELLOW + f"| {encabezados[0]:<15} | {encabezados[1]:<10} | {encabezados[2]:<12} | {encabezados[3]:<30} | {encabezados[4]:<35} | {encabezados[5]:<12} |")
    print(Fore.CYAN + "-" * 130 + Style.RESET_ALL)

    cant_usuarios = len(usuarios[0])

    for i in range(cant_usuarios):
        nombre = str(usuarios[0][i])[:15]
        dni = str(usuarios[1][i])
        telefono = str(usuarios[2][i])
        email = str(usuarios[3][i])[:30]
        direccion = str(usuarios[4][i])[:35]
        bloqueado = usuarios[5][i]

        if bloqueado:
            estado = Fore.RED + "Bloqueado" + Style.RESET_ALL
        else:
            estado = Fore.GREEN + "Sin faltas" + Style.RESET_ALL

        print(f"| {nombre:<15} | {dni:<10} | {telefono:<12} | {email:<30} | {direccion:<35} | {estado:<12} |")

    print(Fore.CYAN + "-" * 130 + Style.RESET_ALL)


def eliminar_usuario(usuarios):
    "Eliminar un usuario "

    intento = input("Ingrese la contraseña de administrador para confirmar (0 para volver): ")
    if intento == '0':
        print('Volviendo...')
        return []
    if intento != contrasenia:
        print("Contraseña incorrecta. Operación cancelada.")
        return

    mostrar_usuarios(usuarios)

    dni = input("Ingrese el DNI del usuario a eliminar: ").strip()

    if not dni.isdigit():
        print("El DNI debe contener solo números.")
        return

    dni = int(dni)

    if dni not in usuarios[1]:
        print(Fore.RED + "No existe ningún usuario con ese DNI.")
        return
    else:
        confirmacion = input( '\nEsta seguro que quiere eliminar este usuario? (S/N): ').lower().strip()
        if confirmacion == 's':
            indice = usuarios[1].index(dni)
            for u in usuarios:
                u.pop(indice)

    print(Fore.GREEN + f"Usuario con DNI {dni} eliminado con éxito.")
    registrar_log("USUARIO", f"Usuario con DNI {dni} eliminado con éxito.")

def editar_usuario(usuarios):
    "Permite modificar el nombre de un usuario."
    
    intento = input("Ingrese la contraseña de administrador para confirmar (0 para volver): ")
    if intento == '0':
        print('Volviendo...')
        return 
    if intento != contrasenia:
        print(Fore.RED + "Contraseña incorrecta. Operación cancelada.")
        return

    dni_str = input("Ingrese el DNI del usuario a editar: ").strip()

    if not dni_str.isdigit():
        print(Fore.YELLOW + "El DNI debe contener solo números.")
        return

    dni = int(dni_str)

    if dni not in usuarios[1]:
        print(Fore.RED + "El usuario no existe.")
        return

    indice = usuarios[1].index(dni)
    
    confirmado = False
    while not confirmado:

        print("1. Nombre")
        print("2. Dni")
        print("3. Telefono")
        print("4. Email")
        print("5. Direccion")
        print("6. Estado")
        print("0. volver")

        try:
            opcion = int(input("Elija un campo para editar: "))
        except ValueError:
            print(Fore.YELLOW + "Debe ingresar un número.")
            continue

        if opcion == 0:
            confirmado = True
            return
        elif opcion == 1:
            #editar nombre
            nuevo_nombre = input("Ingrese el nuevo nombre del usuario (0 para volver): ")
            if nuevo_nombre == '0':
                print('Volviendo...')
                return
        
            if nuevo_nombre in usuarios[0]:
                print(Fore.YELLOW + "El usuario ya existe. Intente con otro nombre.")
            elif not nuevo_nombre.strip():
                print(Fore.YELLOW + "El nombre no puede estar vacío. Intente nuevamente.")
            elif len(nuevo_nombre) < 3 or len(nuevo_nombre) > 25:
                print(Fore.YELLOW + "El nombre debe tener al menos 3 caracteres y menos de 25 caracteres. Intente nuevamente.")
            elif not nuevo_nombre.replace(" ", "").isalpha():
                print(Fore.YELLOW + "El nombre solo debe contener letras y espacios. Intente nuevamente.")
            else:            
                nombre_viejo = usuarios[0][indice]
                usuarios[0][indice] = nuevo_nombre
                print(Fore.GREEN + "Usuario editado con éxito.")
                print(Fore.GREEN + nombre_viejo, "cambió a:", nuevo_nombre)
                registrar_log("USUARIO", f"{nombre_viejo}, cambió a:, {nuevo_nombre}")
        elif opcion == 2:
            #editar dni
            nuevo_dni = input("Ingrese el nuevo DNI del usuario (0 para volver): ")
            if nuevo_dni == '0':
                print('Volviendo...')
                return 
            if not nuevo_dni.strip():
                print(Fore.YELLOW + "El documento no puede estar vacío.")
            elif not nuevo_dni.isdigit():
                print(Fore.YELLOW + "El documento solo debe contener números.")
            elif not (7 <= len(nuevo_dni) <= 9):
                print(Fore.YELLOW + "El documento debe tener entre 7 y 9 dígitos.")
            elif int(nuevo_dni) in usuarios[1]:
                print(Fore.GREEN + "El documento ya está registrado.")
            else:
                usuarios[1][indice] = int(nuevo_dni)
                print(Fore.GREEN + "DNI editado con éxito.")
                registrar_log("USUARIO", f"DNI:{usuarios}cambió a: {nuevo_dni}")
        elif opcion == 3:
            #editar telefono
            nuevo_telefono = input("Ingrese el nuevo teléfono (10 dígitos, debe iniciar con 11) o '0' para volver: ")
            if nuevo_telefono == '0':
                print('Volviendo...')
                return

            if not nuevo_telefono.strip():
                print(Fore.YELLOW + "El teléfono no puede estar vacío.")
            elif not nuevo_telefono.isdigit():
                print(Fore.YELLOW + "El teléfono solo debe contener números.")
            elif len(nuevo_telefono) != 10:
                print(Fore.YELLOW + "El teléfono debe tener exactamente 10 dígitos.")
            elif not nuevo_telefono.startswith("11"):
                print(Fore.YELLOW + "El teléfono debe iniciar con '11'.")
            elif int(nuevo_telefono) in usuarios[2]:
                print(Fore.YELLOW + "Ese teléfono ya está registrado.")
            else:
                usuarios[2][indice] = int(nuevo_telefono)
                print(Fore.GREEN + "Teléfono editado con éxito.")
                registrar_log("USUARIO", f"{dni_str}, cambió a:, {nuevo_telefono}")
        elif opcion == 4:
            #editar email
            nuevo_email = input("Ingrese el nuevo email (0 para volver): ").strip().lower()
            if nuevo_email == '0':
                print('Volviendo...')
                return 
            
            if not nuevo_email:
                print(Fore.YELLOW + "El email no puede estar vacío.")
            elif "@" not in nuevo_email:
                print(Fore.YELLOW + "El email debe contener '@'.")
            else:
                usuarios[3][indice] = nuevo_email
                print(Fore.YELLOW + "Email editado con éxito.")
                registrar_log("USUARIO", f"{dni_str}, cambió a:, {nuevo_email}")
        elif opcion == 5:
            #direccion
            nueva_direccion = input("Ingrese la nueva dirección: ").strip()

            if not nueva_direccion:
                print(Fore.YELLOW + "La dirección no puede estar vacía.")
            else:
                    usuarios[4][indice] = nueva_direccion
                    print(Fore.GREEN + "Dirección editada con éxito.")
                    registrar_log("USUARIO", f"{dni_str}, cambió a:, {nueva_direccion}")
        elif opcion == 6:
            #estado
            usuarios[5][indice] = not usuarios[5][indice]
            estado = "bloqueado" if usuarios[5][indice] else "desbloqueado"
            print(Fore.GREEN + f"Usuario {estado} con éxito.")
            registrar_log("USUARIO", f"{dni_str}, cambió a:, {estado}")
        else:
            print(Fore.YELLOW + "Elija una opcion correcta: ")

def buscar_usuario_por_dni_dicc(diccionario):
    "Consulta para buscar un unico usuario"

    try:
        dni = int(input("Ingrese el DNI a buscar: "))
        if dni in diccionario:
            datos = diccionario[dni]
            print(f"\nUsuario encontrado:")
            print(f"Nombre: {datos['nombre']}")
            print(f"Teléfono: {datos['telefono']}")
            print(f"Email: {datos['email']}")
            print(f"Dirección: {datos['direccion']}")
            print(f"Estado: {'Bloqueado' if datos['bloqueado'] else 'Activo'}\n")
        else:
            print(Fore.RED + "No se encontró un usuario con ese DNI.")
    except ValueError:
        print(Fore.YELLOW + "DNI inválido. Ingrese solo números.")

# ---- Gestión de préstamos ----

def listar_prestamos(matriz_prestamos):
    print("\n" + Fore.CYAN + "--- Lista de Préstamos ---\n" + Style.RESET_ALL)

    print(
        Fore.YELLOW
        + f"{'Usuario':<20}{'Libro':<30}{'Fecha ingreso':<20}{'Fecha límite':<20}"
        + Style.RESET_ALL
    )
    print(Fore.CYAN + "-" * 90 + Style.RESET_ALL)

    for fila in matriz_prestamos:
        usuario = str(fila[0])[:18]
        libro = str(fila[1])[:28]
        fecha_ingreso = str(fila[2])
        fecha_limite = str(fila[3])

        print(f"{usuario:<20}{libro:<30}{fecha_ingreso:<20}{fecha_limite:<20}")

    print(Fore.CYAN + "-" * 90 + Style.RESET_ALL)



def prestar_libro(libros, usuarios, prestamos):
    "Registra un préstamo si hay stock y el usuario existe."

    resultados = buscar_libro_parcial(libros)
    if not resultados:
        print(Fore.RED + "No se encontró ningún libro con ese nombre.")
        registrar_log("ERROR", "Intento de préstamo de libro inexistente")
        return

    libro_prestar = resultados[0]

    usuario_prestar = input("Ingrese el nombre del usuario (o 0/salir para cancelar): ").strip()
    if usuario_prestar.lower() in ("0", "salir"):
        print(Fore.RED + "Operación cancelada.")
        registrar_log("CANCELADO", "Préstamo cancelado por usuario")
        return

    while usuario_prestar not in usuarios[0]:
        print(Fore.RED + "El usuario no está registrado.")
        usuario_prestar = input("Ingrese un usuario válido (o 0/salir para cancelar): ").strip()
        if usuario_prestar.lower() in ("0", "salir"):
            print(Fore.RED + "Operación cancelada.")
            registrar_log("CANCELADO", "Préstamo cancelado por usuario")
            return

    indice_usuario = usuarios[0].index(usuario_prestar)

    if usuarios[5][indice_usuario]:
        print(Fore.RED + "❌ El usuario está bloqueado y no puede realizar préstamos.")
        registrar_log("BLOQUEO", f"Intento de préstamo por usuario bloqueado: {usuario_prestar}")
        return

    cantidad_prestamos = sum(1 for p in prestamos if p[0] == usuario_prestar)
    if cantidad_prestamos >= 3:
        print(Fore.RED + "❌ El usuario superó el máximo de 3 préstamos.")
        registrar_log("ERROR", f"{usuario_prestar} superó el máximo de préstamos (3)")
        return

    if libro_prestar[4] <= 0:
        print(Fore.RED + "❌ No hay ejemplares disponibles para préstamo.")
        registrar_log("ERROR", f"Intento de préstamo sin stock: {libro_prestar[1]}")
        return

    fecha_ingreso = date.today().strftime("%d/%m/%Y")
    fecha_limite = determinar_fecha_vencimiento(date.today())

    prestamos.append([usuario_prestar, libro_prestar[1], fecha_ingreso, fecha_limite])
    indice_libro = [libro[1] for libro in libros].index(libro_prestar[1])
    libros[indice_libro][4] -= 1

    libros[indice_libro][3] = True if libros[indice_libro][4] > 0 else False

    guardar_prestamos(ruta_prestamos, prestamos)
    guardar_libros(ruta_libros, libros)

    registrar_log("PRESTAMO", f"{usuario_prestar} tomó '{libro_prestar[1]}' (vence {fecha_limite})")

    print(Fore.GREEN + "✅ Préstamo registrado con éxito.")
    print(f"Usuario: {usuario_prestar}")
    print(f"Libro: {libro_prestar[1]}")
    print(f"Fecha límite: {fecha_limite}")


def devolver_libro(libros, prestamos):
    "Devuelve un libro prestado y actualiza el stock."
    
    usuario_devolver = input("Ingrese el nombre del usuario que devuelve el libro (0 para volver): ")
    if usuario_devolver == '0':
        print('Volviendo...')
        return
    libro_devolver = input("Ingrese el título del libro a devolver: ")
    if libro_devolver == '0':
        print('Volviendo...')
        return
    for prestamo in prestamos:
        if prestamo[0] == usuario_devolver and prestamo[1] == libro_devolver:
            prestamos.remove(prestamo)
            libros[[libro[1] for libro in libros].index(libro_devolver)][4] += 1
            print(Fore.GREEN + "✅Libro devuelto con éxito.")
            registrar_log("PRESTAMO", f"{usuario_devolver} devolvió '{libro_devolver}'")
            guardar_prestamos(ruta_prestamos, prestamos)
            guardar_libros(ruta_libros, libros)
            return

    print(Fore.RED + "❌No se encontró un préstamo para este usuario y libro.")


def prestamos_vencidos(prestamos):
    "Muestra los préstamos que han vencido."
    hoy = date.today()
    
    print("\n" + Fore.CYAN + "--- Préstamos Vencidos ---\n" + Style.RESET_ALL)
    print(Fore.YELLOW + f"{'Usuario':<18}{'Libro':<45}{'Fecha ingreso':<18}{'Fecha límite':<18}" + Style.RESET_ALL)
    print(Fore.CYAN + "-" * 95 + Style.RESET_ALL)

    vencidos = False

    for fila in prestamos:
        try:
            dia, mes, anio = map(int, fila[3].split("/"))
            fecha_limite = date(anio, mes, dia)
        except Exception:
            continue 
        
        if fecha_limite < hoy:
            vencidos = True
            usuario = str(fila[0])[:17]
            libro = str(fila[1])[:45]
            fecha_ingreso = str(fila[2])
            fecha_limite_str = str(fila[3])

            print(Fore.RED + f"{usuario:<18}{libro:<45}{fecha_ingreso:<18}{fecha_limite_str:<18}" + Style.RESET_ALL)
            registrar_log("VENCIMIENTO", f"{usuario:<18}{libro:<45}{fecha_ingreso:<18}{fecha_limite_str:<18}")

    if not vencidos:
        print(Fore.GREEN + "✅ No hay préstamos vencidos." + Style.RESET_ALL)

    print(Fore.CYAN + "-" * 95 + Style.RESET_ALL)

def determinar_fecha_vencimiento(fecha_hoy):
    print("1. 7 días")
    print("2. 15 días")
    print("3. 30 días")

    opcion = input("Seleccione una opcion para el plazo de devolución (1,2,3) o '0' para volver: ")
    if opcion == '0':
        print('Volviendo...')
        return

    dias_a_sumar = 0
    if opcion == '1':
        dias_a_sumar = 7
    elif opcion == '2':
        dias_a_sumar = 15
    elif opcion == '3':
        dias_a_sumar = 30
    else:
        print(Fore.RED + "❌Opción inválida. Se asignarán 7 días por defecto.")
        dias_a_sumar = 7

    fecha_vencimiento = fecha_hoy + timedelta(days=dias_a_sumar)
    return fecha_vencimiento.strftime("%d/%m/%Y")


def renovacion_prestamos(prestamos, usuarios, ruta_prestamos):
    print("\n" + Fore.CYAN + "--- Renovación de préstamos ---\n" + Style.RESET_ALL)

    if not prestamos:
        print(Fore.RED + "❌ No hay préstamos registrados.")
        return

    hoy = date.today()

    # Bloquear usuarios con mora >15 días
    for p in prestamos:
        try:
            dia, mes, anio = map(int, p[3].split("/"))
            venc = date(anio, mes, dia)
            if (hoy - venc).days > 15 and p[0] in usuarios[0]:
                idx = usuarios[0].index(p[0])
                if not usuarios[5][idx]:
                    usuarios[5][idx] = True
                    registrar_log("BLOQUEO", f"Usuario {p[0]} bloqueado por mora (+15 días)")
        except Exception as e:
            registrar_log("ERROR", f"Error bloqueando usuario por mora: {e}")

    # Elegir si usar búsqueda parcial o mostrar todos
    print("\n¿Desea buscar un préstamo específico o listar todos?")
    print("1 - Buscar por usuario o libro (búsqueda parcial)")
    print("2 - Mostrar todos los préstamos")
    print("0 - Cancelar")

    opcion_busqueda = input("\nSeleccione una opción: ").strip()

    if opcion_busqueda == "0":
        print(Fore.RED + "Operación cancelada.")
        registrar_log("CANCELADO", "Renovación cancelada por usuario")
        return

    prestamos_filtrados = prestamos.copy()

    if opcion_busqueda == "1":
        texto = input("Ingrese parte del nombre del usuario o del libro (0 para volver): ").strip().lower()
        if texto == '0':
            print('Volviendo...')
            return
        prestamos_filtrados = [
            p for p in prestamos if texto in p[0].lower() or texto in p[1].lower()
        ]
        if not prestamos_filtrados:
            print(Fore.YELLOW + "⚠ No se encontraron préstamos que coincidan con la búsqueda.")
            return

    # Mostrar préstamos activos filtrados
    print("\n" + Fore.YELLOW + f"{'N°':<4}{'Usuario':<20}{'Libro':<45}{'Fecha límite':<15}" + Style.RESET_ALL)
    print(Fore.CYAN + "-" * 75 + Style.RESET_ALL)

    for i, p in enumerate(prestamos_filtrados):
        print(f"{i:<4}{p[0]:<20}{p[1]:<45}{p[3]:<15}")

    print(Fore.CYAN + "-" * 75 + Style.RESET_ALL)

    eleccion = input("\nIngrese el número de préstamo a renovar (0/salir): ").strip().lower()
    if eleccion in ("0", "salir"):
        registrar_log("CANCELADO", "Renovación cancelada por usuario")
        return

    if not eleccion.isdigit() or int(eleccion) >= len(prestamos_filtrados):
        print(Fore.RED + "❌ Selección inválida.")
        return

    # Obtener préstamo seleccionado
    seleccionado = prestamos_filtrados[int(eleccion)]
    usuario, libro, f_ingreso, f_limite = seleccionado

    # Buscar índice real en la lista original
    idx_original = prestamos.index(seleccionado)

    #Verificar si está vencido
    dia, mes, anio = map(int, f_limite.split("/"))
    fecha_limite = date(anio, mes, dia)
    if fecha_limite < hoy:
        print(Fore.RED + "❌ El préstamo ya está vencido y no puede renovarse.")
        registrar_log("ERROR", f"Intento de renovar préstamo vencido: {usuario}-{libro}")
        return

    #Contar renovaciones previas
    renovaciones_previas = 0
    try:
        with abrir_archivo_seguro("log.txt", "r") as log:
            for linea in log:
                if "[RENEW]" in linea and usuario in linea and libro in linea:
                    renovaciones_previas += 1
    except Exception as e:
        registrar_log("ERROR", f"No se pudo leer log.txt: {e}")

    if renovaciones_previas >= 2:
        print(Fore.YELLOW + "⚠ Este préstamo ya fue renovado dos veces.")
        registrar_log("ERROR", f"Intento de renovar +2 veces: {usuario}-{libro}")
        return

    #Elegir días de renovación
    print("\nDuración de renovación:")
    print("1 - +7 días")
    print("2 - +15 días")
    print("3 - +30 días")

    opcion = input("Seleccione: ").strip()
    opciones = {"1": 7, "2": 15, "3": 30}
    dias = opciones.get(opcion)

    if not dias:
        print(Fore.RED + "❌ Opción inválida.")
        return

    # Actualizar fecha y guardar
    nueva_fecha = fecha_limite + timedelta(days=dias)
    prestamos[idx_original][3] = nueva_fecha.strftime("%d/%m/%Y")

    guardar_prestamos(ruta_prestamos, prestamos)
    registrar_log("RENEW", f"{usuario} renovó '{libro}' +{dias} días (nuevo límite: {prestamos[idx_original][3]})")
    print(Fore.GREEN + f"✅ Préstamo renovado. Nueva fecha: {prestamos[idx_original][3]}")
   
def usuarios_con_mas_prestamos(prestamos):
    print("\n--- Usuarios con más préstamos ---\n")

    nombres = []
    cantidades = []

    # Contar préstamos por usuario
    for fila in prestamos:
        usuario = fila[0]
        if usuario in nombres:
            posicion = nombres.index(usuario)
            cantidades[posicion] += 1
        else:
            nombres.append(usuario)
            cantidades.append(1)

    # Ordenar por cantidad (descendente)
    for i in range(len(cantidades)):
        for j in range(i + 1, len(cantidades)):
            if cantidades[i] < cantidades[j]:
                cantidades[i], cantidades[j] = cantidades[j], cantidades[i]
                nombres[i], nombres[j] = nombres[j], nombres[i]

    # Encabezado ordenado y prolijo
    print(f"{'N°':<4}{'Usuario':<20}{'Cantidad':<10}")
    print("-" * 34)

    # Mostrar hasta los 10 primeros
    for i in range(min(10, len(nombres))):
        print(f"{i+1:<4}{nombres[i]:<20}{cantidades[i]:<10}")

    print("-" * 34)


def libros_mas_prestados(prestamos):
    "Muestra los libros ordenados por la cantidad de veces que fueron prestados."

    print("\n--- Libros más prestados ---\n")
    titulos = []
    cantidades = []
    # Contar préstamos por libro
    for fila in prestamos:
        libro = fila[1]
        if libro in titulos:
            posicion = titulos.index(libro)
            cantidades[posicion] += 1
        else:
            titulos.append(libro)
            cantidades.append(1)
    # Ordenar por cantidad de préstamos (descendente)
    for i in range(len(cantidades)):
        for j in range(i + 1, len(cantidades)):
            if cantidades[i] < cantidades[j]:
                cantidades[i], cantidades[j] = cantidades[j], cantidades[i]
                titulos[i], titulos[j] = titulos[j], titulos[i]
    # Mostrar hasta los 10 primeros libros más prestados
    for i in range(min(10, len(titulos))):
        print(f"{titulos[i]} - Veces prestado: {cantidades[i]}")


def morosos(prestamos):
    "Muestra los usuarios morosos con la cantidad de días de atraso acumulados."

    print("\n" + Fore.CYAN + "--- Morosos ---\n" + Style.RESET_ALL)

    nombres = []
    atrasos = []
    hoy = date.today()

    for fila in prestamos:
        usuario = fila[0]
        fecha_limite_str = fila[3]
        partes = fecha_limite_str.split("/")
        dia = int(partes[0])
        mes = int(partes[1])
        anio = int(partes[2])
        fecha_limite = date(anio, mes, dia)
        dias_atraso = (hoy - fecha_limite).days

        if dias_atraso > 0:
            if usuario in nombres:
                posicion = nombres.index(usuario)
                atrasos[posicion] += dias_atraso
            else:
                nombres.append(usuario)
                atrasos.append(dias_atraso)

    if len(nombres) == 0:
        print(Fore.GREEN + "✅ No hay morosos." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + f"{'Usuario':<20}{'Días de atraso':<15}" + Style.RESET_ALL)
        print(Fore.CYAN + "-" * 35 + Style.RESET_ALL)
        for i in range(len(nombres)):
            print(f"{nombres[i]:<20}{atrasos[i]:<15}")
        print(Fore.CYAN + "-" * 35 + Style.RESET_ALL)


def exportar_morosos(prestamos):
    hoy = date.today()
    try:
        with abrir_archivo_seguro("morosos.txt", "w") as archivo:
            for fila in prestamos:
                partes = fila[3].split("/")
                dia = int(partes[0])
                mes = int(partes[1])
                anio= int(partes[2])
                fecha_limite = date(anio, mes, dia)
                dias_atraso = (hoy - fecha_limite).days
                if dias_atraso > 0:
                    archivo.write(f"{fila[0]},{fila[1]},{dias_atraso}\n")
        print(Fore.GREEN + "✅Morosos exportados correctamente")
    except Exception as error:
        print(Fore.RED + "⚠ Error al exportar morosos:", error)

# ---- Carga de Datos ---- Persistencia ---- #

# --- LIBROS ---

def cargar_libros(ruta):
    "Carga los libros desde un archivo de texto."
    libros = []
    try:
        with abrir_archivo_seguro(ruta, "r") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if len(datos) == 5:
                    id_libro = int(datos[0])
                    titulo = datos[1]
                    autor = datos[2]
                    disponible = datos[3].lower() == "true"
                    cantidad = int(datos[4])
                    libros.append([id_libro, titulo, autor, disponible, cantidad])
        print(Fore.GREEN + "✅ Libros cargados correctamente.")
    except FileNotFoundError:
        print(Fore.YELLOW + "⚠ No se encontró el archivo de libros. Se creará uno nuevo.")
    except Exception as error:
        print(Fore.RED + "⚠ Error al cargar los libros:", error)
    return libros


def guardar_libros(ruta, libros):
    "Guarda la matriz de libros en un archivo de texto."
    try:
        with abrir_archivo_seguro(ruta, "w") as archivo:
            for libro in libros:
                linea = ",".join(map(str, libro))
                archivo.write(linea + "\n")
        print(Fore.GREEN + "💾 Libros guardados correctamente.")
    except Exception as error:
        print(Fore.RED + "⚠ Error al guardar los libros:", error)


# --- USUARIOS ---

def cargar_usuarios(ruta):
    "Carga los usuarios desde un archivo de texto."
    usuarios = [[] for _ in range(6)]  # crear 6 listas vacías
    try:
        with abrir_archivo_seguro(ruta, "r") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if len(datos) == 6:
                    usuarios[0].append(datos[0])                  # nombre
                    usuarios[1].append(int(datos[1]))             # dni
                    usuarios[2].append(int(datos[2]))             # tel
                    usuarios[3].append(datos[3])                  # email
                    usuarios[4].append(datos[4])                  # dirección
                    usuarios[5].append(datos[5].lower() == "true")  # bloqueado
        print(Fore.GREEN + "✅ Usuarios cargados correctamente.")
    except FileNotFoundError:
        print(Fore.YELLOW + "⚠ No se encontró el archivo de usuarios. Se creará uno nuevo.")
    except Exception as error:
        print(Fore.RED + "⚠ Error al cargar los usuarios:", error)
    return usuarios


def guardar_usuarios(ruta, usuarios):
    "Guarda los usuarios en un archivo de texto."
    try:
        with abrir_archivo_seguro(ruta, "w") as archivo:
            for i in range(len(usuarios[0])):
                linea = f"{usuarios[0][i]},{usuarios[1][i]},{usuarios[2][i]},{usuarios[3][i]},{usuarios[4][i]},{usuarios[5][i]}"
                archivo.write(linea + "\n")
        print(Fore.GREEN + "💾 Usuarios guardados correctamente.")
    except Exception as error:
        print(Fore.RED + "⚠ Error al guardar los usuarios:", error)


def actualizar_diccionario_usuarios():
    usuarios_dict.clear()
    for i in range(len(usuarios[0])):
        usuarios_dict[usuarios[1][i]] = {
            "nombre": usuarios[0][i],
            "telefono": usuarios[2][i],
            "email": usuarios[3][i],
            "direccion": usuarios[4][i],
            "bloqueado": usuarios[5][i]
        }


# --- PRÉSTAMOS ---

def cargar_prestamos(ruta):
    "Carga los préstamos desde un archivo de texto."
    prestamos = []
    try:
        with abrir_archivo_seguro(ruta, "r") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if len(datos) == 4:
                    prestamos.append(datos)
        print(Fore.GREEN + "✅ Préstamos cargados correctamente.")
    except FileNotFoundError:
        print(Fore.YELLOW + "⚠ No se encontró el archivo de préstamos. Se creará uno nuevo.")
    except Exception as error:
        print(Fore.RED + "⚠ Error al cargar los préstamos:", error)
    return prestamos


def guardar_prestamos(ruta, prestamos):
    "Guarda los préstamos en un archivo de texto."
    try:
        with abrir_archivo_seguro(ruta, "w") as archivo:
            for prestamo in prestamos:
                linea = ",".join(map(str, prestamo))
                archivo.write(linea + "\n")
        print(Fore.GREEN + "💾 Préstamos guardados correctamente.")
    except Exception as error:
        print(Fore.RED + "⚠ Error al guardar los préstamos:", error)

# ---- Gestión de menues ----

def menu_principal():

    init(autoreset=True)

    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    print(Fore.CYAN + "=" * 35)
    print(Fore.GREEN + "        📚 MENÚ PRINCIPAL        ")
    print(Fore.CYAN + "=" * 35)
    print(Fore.YELLOW + f"🕒 Fecha y hora actual: {ahora}")
    print(Style.RESET_ALL)

    print("\n--- Biblioteca ---")
    print("1. Gestión de Libros")
    print("2. Gestión de Usuarios")
    print("3. Gestión de Préstamos")
    print("4. Gestion de Admin")
    print("0. Salir")

    try:
        opcion = input("Seleccione una opción: ").strip()
    except Exception as error:
        print(Fore.RED + "⚠ Error inesperado al leer la opción:", error)
        return

    limpiar_consola()

    try:
        if opcion == '1':
            menu_libros()
        elif opcion == '2':
            menu_usuarios()
        elif opcion == '3':
            menu_prestamos()
        elif opcion == '4':
            menu_admin()
        elif opcion == '0':
            print(Fore.YELLOW + "Saliendo del sistema...")
            quit()
        else:
            print(Fore.YELLOW + "Opción inválida, intente nuevamente.")
    except Exception as error:
        print(Fore.RED + "⚠ Se produjo un error al ejecutar la opción:", error)



def menu_libros():

    print("\n--- Gestión de Libros ---")
    print("1. Mostrar libros")
    print("2. Buscar libro")
    print("3. Editar libro")
    print("4. Agregar libro")
    print("5. Eliminar libro")
    print("6. Reporte de stock bajo")
    print("0. Volver al menú principal")

    try:
        opcion = input("Seleccione una opción: ").strip()
    except Exception as error:
        print(Fore.RED + "⚠ Error inesperado al leer la opción:", error)
        return
    
    limpiar_consola()

    try:
        if opcion == '1':
            mostrar_libros(libros)
        elif opcion == '2':
            buscar_libro_parcial(libros)
        elif opcion == '3':
            editar_libro(libros)
        elif opcion == '4':
            agregar_libro(libros)
        elif opcion == '5':
            eliminar_libro(libros)
        elif opcion == '6':
            reporte_stock_bajo(libros)
        elif opcion == '0':
            menu_principal()
        else:
            print(Fore.YELLOW + "⚠ Opción inválida, intente nuevamente.")
    except Exception as error:
        print(Fore.RED + "⚠ Se produjo un error al ejecutar la opción seleccionada:", error)


def menu_usuarios():

    #actulizamos porque si hay algun cambio dps no va a aparecer

    actualizar_diccionario_usuarios()

    print("\n--- Gestión de Usuarios ---")
    print("1. Registrar usuario")
    print("2. Mostrar usuarios")
    print("3. Editar usuario")
    print("4. Eliminar usuario")
    print("5. Buscar usuario por DNI")
    print("0. Volver al menú principal")

    try:
        opcion = input("Seleccione una opción: ").strip()
    except Exception as error:
        print(Fore.RED + "⚠ Error inesperado al leer la opción:", error)
        return

    limpiar_consola()

    try:
        if opcion == '1':
            registrar_usuario(usuarios)
        elif opcion == '2':
            mostrar_usuarios(usuarios)
        elif opcion == '3':
            editar_usuario(usuarios)
        elif opcion == '4':
            eliminar_usuario(usuarios)
        elif opcion == '5':
            buscar_usuario_por_dni_dicc(usuarios_dict)
        elif opcion == '0':
            menu_principal()
        else:
            print(Fore.YELLOW + "⚠ Opción inválida. Intente nuevamente.")
    except Exception as error:
        print(Fore.RED + "⚠ Se produjo un error al ejecutar la opción seleccionada:", error)


def menu_prestamos():

    print("\n--- Gestión de Préstamos ---")
    print("1. Listar préstamos")
    print("2. Prestar libro")
    print("3. Devolver libro")
    print("4. Préstamos vencidos")
    print("5. Renovación")
    print("6. Usuarios con más préstamos")
    print("7. Libros más prestados")
    print("8. Morosos")
    print("0. Volver al menú principal")
    
    try:
        opcion = input("Seleccione una opción: ").strip()
    except Exception as error:
        print(Fore.RED + "⚠ Error inesperado al leer la opción:", error)
        return

    limpiar_consola()

    try:
        if opcion == '1':
            listar_prestamos(prestamos)
        elif opcion == '2':
            prestar_libro(libros, usuarios, prestamos)
        elif opcion == '3':
            devolver_libro(libros, prestamos)
        elif opcion == '4':
            prestamos_vencidos(prestamos)
        elif opcion == '5':
            renovacion_prestamos(prestamos, usuarios, ruta_prestamos)
        elif opcion == '6':
            usuarios_con_mas_prestamos(prestamos)
        elif opcion == '7':
            libros_mas_prestados(prestamos)
        elif opcion == '8':
            morosos(prestamos)
        elif opcion == '0':
            menu_principal()
        else:
            print(Fore.YELLOW + "⚠ Opción inválida, intente nuevamente.")
    except Exception as error:
        print(Fore.RED + "⚠ Se produjo un error al ejecutar la opción seleccionada:", error)

def menu_admin():
    "Menú del administrador: ver logs o cambiar contraseña"

    print(Fore.CYAN + "\n" + "=" * 45)
    print(Fore.YELLOW + "       🔒 MENÚ DE ADMINISTRADOR 🔒")
    print(Fore.CYAN + "=" * 45 + Style.RESET_ALL)
    print("1. Ver logs del sistema")
    print("2. Cambiar contraseña de administrador")
    print("0. Volver al menú principal")
    print("=" * 45)

    opcion = input("Seleccione una opción: ").strip()

    limpiar_consola()

    if opcion == "1":
        ver_logs()
    elif opcion == "2":
        cambiar_contrasenia()
    elif opcion == "0":
        print(Fore.GREEN + "Volviendo al menú principal...")
        return
    else:
        print(Fore.RED + "❌ Opción inválida.")


    
# --- Programa Principal ---

# --- Rutas de archivos ---
ruta_libros = "libros.txt"
ruta_usuarios = "usuarios.txt"
ruta_prestamos = "prestamos.txt"
ruta_pass = "admin_pass.txt"

# --- Cargar datos al iniciar ---
print(Fore.YELLOW + "📚 Cargando datos del sistema de biblioteca...\n")

libros = cargar_libros(ruta_libros)
usuarios = cargar_usuarios(ruta_usuarios)
prestamos = cargar_prestamos(ruta_prestamos)

registrar_log("INICIO", "Sistema iniciado correctamente.")

#para que espere antes de iniciar
time.sleep(1)
limpiar_consola()

# --- Contraseña del administrador ---

if os.path.exists(ruta_pass):
    try:
        with abrir_archivo_seguro(ruta_pass, "r") as archivo:
            contrasenia = archivo.read().strip()
    except Exception as e:
        print(Fore.RED + f"⚠ Error al leer {ruta_pass}: {e}")
        contrasenia = "admin1234"
else:
    contrasenia = "admin1234"
    try:
        with abrir_archivo_seguro(ruta_pass, "w") as archivo:
            archivo.write(contrasenia)
    except Exception as e:
        print(Fore.RED + f"⚠ Error al crear {ruta_pass}: {e}")


# --- Diccionario de usuarios (estructura auxiliar para consultas rápidas) ---
usuarios_dict = {}

for i in range(len(usuarios[0])):
    usuarios_dict[usuarios[1][i]] = {
        "nombre": usuarios[0][i],
        "telefono": usuarios[2][i],
        "email": usuarios[3][i],
        "direccion": usuarios[4][i],
        "bloqueado": usuarios[5][i]
    }

# --- Bucle principal ---

try:
    while True:
        menu_principal()
except KeyboardInterrupt:
    print(Fore.RED + "\n⚠ Programa interrumpido manualmente.")
except Exception as error:
    print(Fore.RED + "⚠ Ocurrió un error inesperado:", error)
finally:
    hacer_backup()
    registrar_log("SALIDA", "Cierre del sistema y guardado automático.")
    # --- Guardar datos automáticamente al cerrar ---
    print(Fore.YELLOW + "\n💾 Guardando datos antes de salir...")
    guardar_libros(ruta_libros, libros)
    guardar_usuarios(ruta_usuarios, usuarios)
    guardar_prestamos(ruta_prestamos, prestamos)
    exportar_libros_sin_stock(libros)
    exportar_morosos(prestamos)
    print(Fore.GREEN + "✅ Datos guardados correctamente. ¡Hasta luego!")