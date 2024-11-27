import bcrypt
import mysql.connector

# Conexión a la base de datos
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            database="youtube_simulacion",
            user="root",
            password=""
            
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error conectando a la base de datos: {err}")
        return None

# Función para crear la cuenta
def crear_cuenta():
    conexion = conectar_db()
    if conexion is None:
        return
    cursor = conexion.cursor()

    # Pedimos los datos al usuario
    nombre = input("Introduce tu nombre: ")
    apellido = input("Introduce tu apellido: ")
    email = input("Introduce tu correo: ")
    contraseña = input("Introduce tu contraseña: ")

    # Verificamos si el email ya está registrado
    cursor.execute("SELECT * FROM Usuarios WHERE Correo = %s", (email,))
    usuario_existente = cursor.fetchone()

    if usuario_existente:
        print("El email ya está registrado. Intenta con otro.")
    else:
        # Hasheamos la contraseña
        contraseña_hash = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

        # Verificamos si el email es de dominio @example.com para ser admin
        if email.endswith("@example.com"):
            es_admin = True
            print("Este usuario será administrador.")
        else:
            es_admin = False
            print("Este usuario será un usuario normal.")

        # Insertamos el nuevo usuario en la base de datos
        try:
            cursor.execute(
                "INSERT INTO Usuarios (Nombre, Apellido, Email, Contraseña, es_admin) VALUES (%s, %s, %s, %s, %s)",
                (nombre, apellido, email, contraseña_hash.decode('utf-8'), es_admin)
            )
            conexion.commit()
            print("¡Cuenta creada exitosamente!")
        except mysql.connector.Error as err:
            print(f"Error al crear la cuenta: {err}")

    cursor.close()
    conexion.close()

# Función para iniciar sesión
def iniciar_sesion():
    conexion = conectar_db()
    if conexion is None:
        return
    cursor = conexion.cursor()

    correo = input("Introduce tu correo: ")
    contraseña = input("Introduce tu contraseña: ")

    try:
        # Seleccionamos la contraseña, el estado de admin, el ID y el nombre del usuario para el usuario con el correo proporcionado
        cursor.execute("SELECT id, nombre, Contraseña, es_admin FROM Usuarios WHERE Email = %s", (correo,))
        resultado = cursor.fetchone()

        if resultado:
            usuario_id = resultado[0]
            nombre = resultado[1]
            contraseña_hash = resultado[2]
            es_admin = resultado[3]

            # Verificamos la contraseña usando bcrypt
            if bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_hash.encode('utf-8')):
                print("Inicio de sesión exitoso.")
                
                # Si es administrador, mostramos el menú de administrador
                if es_admin:
                    print(f"Bienvenido Administrador {nombre}")
                    menu_administrador()
                else:
                    print(f"Bienvenido Usuario {nombre}")
                    menu_usuario(usuario_id, nombre)  # Aquí pasamos el usuario_id y el nombre
            else:
                print("Contraseña incorrecta.")
        else:
            print("Correo no encontrado.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conexion.close()


# Función para crear una lista de reproducción
def crear_lista_reproduccion(usuario_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    nombre_lista = input("Introduce el nombre de la lista de reproducción: ")
    tipo_lista = input("¿La lista será pública o privada? (pública/privada): ").lower()

    # Determinar si la lista es pública o privada
    es_publica = tipo_lista == 'pública'

    # Insertar la lista en la tabla Listas_Reproducciones
    cursor.execute("INSERT INTO Listas_Reproducciones (nombre, usuario_id, fecha_creacion) VALUES (%s, %s, NOW())", 
                   (nombre_lista, usuario_id))
    conexion.commit()
    print(f"¡Lista de reproducción '{nombre_lista}' creada exitosamente!")

    cursor.close()
    conexion.close()

# Función para añadir canción a una lista de reproducción
def agregar_cancion_a_lista(usuario_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    lista_id = input("Introduce el ID de la lista de reproducción: ")
    cancion_id = input("Introduce el ID de la canción que deseas agregar: ")

    # Insertar la canción en la lista
    cursor.execute("INSERT INTO Lista_Canciones (lista_id, cancion_id) VALUES (%s, %s)", (lista_id, cancion_id))
    conexion.commit()
    print("¡Canción añadida a la lista de reproducción!")

    cursor.close()
    conexion.close()

# Función para añadir canción a la biblioteca del usuario
def agregar_cancion_a_biblioteca(usuario_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cancion_id = input("Introduce el ID de la canción que deseas agregar a tu biblioteca: ")

    # Insertar la canción en la biblioteca del usuario
    cursor.execute("INSERT INTO Bibliotecas (usuario_id, cancion_id) VALUES (%s, %s)", (usuario_id, cancion_id))
    conexion.commit()
    print("¡Canción añadida a tu biblioteca!")

    cursor.close()
    conexion.close()

# Función para buscar canciones por nombre
def buscar_cancion_por_nombre():
    conexion = conectar_db()
    cursor = conexion.cursor()

    nombre_cancion = input("Introduce el nombre de la canción que deseas buscar: ")

    # Buscar canciones que coincidan con el nombre
    cursor.execute("SELECT * FROM Canciones WHERE titulo LIKE %s", ('%' + nombre_cancion + '%',))
    canciones = cursor.fetchall()

    if canciones:
        print("Canciones encontradas:")
        for cancion in canciones:
            print(f"ID: {cancion[0]}, Título: {cancion[1]}, Duración: {cancion[2]}")
    else:
        print("No se encontraron canciones con ese nombre.")

    cursor.close()
    conexion.close()
# Función para visualizar usuarios (lectura)
def visualizar_usuarios():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT id, nombre, email FROM Usuarios")
    usuarios = cursor.fetchall()

    print("\n===== Lista de Usuarios =====")
    if usuarios:
        for usuario in usuarios:
            print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Email: {usuario[2]}")
    else:
        print("No hay usuarios registrados.")
    
    cursor.close()
    conexion.close()

# Función para ver listas de reproducción de un usuario
def ver_listas_reproduccion(usuario_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT id, nombre FROM Listas_Reproduccion WHERE usuario_id = %s", (usuario_id,))
    listas = cursor.fetchall()

    print("\n===== Tus Listas de Reproducción =====")
    if listas:
        for lista in listas:
            print(f"ID: {lista[0]}, Nombre: {lista[1]}")
    else:
        print("No tienes listas de reproducción.")
    
    cursor.close()
    conexion.close()

# Función para ver canciones en una lista de reproducción
def ver_canciones_en_lista(usuario_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Primero, listar las listas disponibles del usuario
    ver_listas_reproduccion(usuario_id)
    lista_id = input("Introduce el ID de la lista de reproducción para ver sus canciones: ")

    # Obtener las canciones de esa lista
    cursor.execute("""
        SELECT c.id, c.titulo, c.artista, c.album, c.URL
        FROM Canciones c
        INNER JOIN Canciones_Listas cl ON c.id = cl.cancion_id
        WHERE cl.lista_id = %s
    """, (lista_id,))
    canciones = cursor.fetchall()

    print("\n===== Canciones en la Lista =====")
    if canciones:
        for cancion in canciones:
            print(f"ID: {cancion[0]}, Título: {cancion[1]}, Artista: {cancion[2]}, Álbum: {cancion[3]}, URL: {cancion[4]}")
    else:
        print("No hay canciones en esta lista.")

    cursor.close()
    conexion.close()

# Función para eliminar una lista de reproducción
def eliminar_lista_reproduccion(usuario_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Mostrar las listas del usuario
    ver_listas_reproduccion(usuario_id)
    lista_id = input("Introduce el ID de la lista de reproducción que deseas eliminar: ")

    # Eliminar las relaciones de canciones con esa lista primero
    cursor.execute("DELETE FROM Canciones_Listas WHERE lista_id = %s", (lista_id,))
    # Luego, eliminar la lista de reproducción
    cursor.execute("DELETE FROM Listas_Reproduccion WHERE id = %s AND usuario_id = %s", (lista_id, usuario_id))
    conexion.commit()

    print(f"¡Lista de reproducción con ID {lista_id} eliminada exitosamente!")
    
    cursor.close()
    conexion.close()

# Menú del administrador (extendido con CRUD de canciones)
def menu_administrador():
    while True:
        print("\n===== Menú de Administrador =====")
        print("1. Añadir canción")
        print("2. Ver canciones")
        print("3. Editar canción")
        print("4. Eliminar canción")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            añadir_cancion(None)  # Administrador no necesita usuario_id
        elif opcion == "2":
            listar_canciones()
        elif opcion == "3":
            editar_cancion(None)
        elif opcion == "4":
            eliminar_cancion(None)
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
        # Aquí puedes implementar las opciones del menú de administrador
# Función para añadir una canción
def añadir_cancion(usuario_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    titulo = input("Introduce el título de la canción: ")
    duracion = input("Introduce la duración de la canción (HH:MM:SS): ")
    artista = input("Introduce el nombre del artista: ")
    album = input("Introduce el nombre del álbum (opcional, presiona Enter para omitir): ")
    URL = input("Introduce el url de la canción: ")

    cursor.execute(
        "INSERT INTO Canciones (titulo, duracion, artista, album, URL) VALUES (%s, %s, %s, %s, %s)",
        (titulo, duracion, artista, album if album else None, URL)
    )
    conexion.commit()
    print(f"¡Canción '{titulo}' añadida exitosamente!")

    cursor.close()
    conexion.close()

# Función para listar canciones (lectura)
def listar_canciones():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Canciones")
    canciones = cursor.fetchall()

    if canciones:
        print("Lista de canciones disponibles:")
        for cancion in canciones:
            print(f"ID: {cancion[0]}, Título: {cancion[1]}, Duración: {cancion[2]}, Artista: {cancion[3]}, Álbum: {cancion[4]} , URL: {cancion[5]}")
    else:
        print("No hay canciones disponibles.")

    cursor.close()
    conexion.close()

# Función para editar una canción
def editar_cancion(usuario_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    listar_canciones()
    cancion_id = input("Introduce el ID de la canción que deseas editar: ")

    # Datos nuevos
    nuevo_titulo = input("Introduce el nuevo título (deja vacío para mantener actual): ")
    nueva_duracion = input("Introduce la nueva duración (HH:MM:SS, deja vacío para mantener actual): ")
    nuevo_artista = input("Introduce el nuevo artista (deja vacío para mantener actual): ")
    nuevo_album = input("Introduce el nuevo álbum (deja vacío para mantener actual): ")
    nueva_URL = input("Introduce la nueva urlde la cancion (deja vacío para mantener actual): ")

    # Construir consulta dinámica
    query = "UPDATE Canciones SET"
    valores = []
    if nuevo_titulo:
        query += " titulo = %s,"
        valores.append(nuevo_titulo)
    if nueva_duracion:
        query += " duracion = %s,"
        valores.append(nueva_duracion)
    if nuevo_artista:
        query += " artista = %s,"
        valores.append(nuevo_artista)
    if nuevo_album:
        query += " album = %s,"
        valores.append(nuevo_album)
    if nueva_URL:
        query += " URL = %s,"
        valores.append(nueva_URL)

    query = query.rstrip(",") + " WHERE id = %s"
    valores.append(cancion_id)

    cursor.execute(query, tuple(valores))
    conexion.commit()
    print("¡Canción actualizada exitosamente!")

    cursor.close()
    conexion.close()

# Función para eliminar una canción
def eliminar_cancion(usuario_id):
    conexion = conectar_db()
    cursor = conexion.cursor()

    listar_canciones()
    cancion_id = input("Introduce el ID de la canción que deseas eliminar: ")

    cursor.execute("DELETE FROM Canciones WHERE id = %s", (cancion_id,))
    conexion.commit()
    print("¡Canción eliminada exitosamente!")

    cursor.close()
    conexion.close()
# Menú del usuario
def menu_usuario(usuario_id, nombre):
    while True:
        print(f"\n===== Menú de Usuario =====")
        print(f"Bienvenido, {nombre}!")
        print("1. busca algun video")
        print("2. Añadir video a lista de reproducción")
        print("3. Añadir canción a biblioteca")
        print("4. Buscar canciones por nombre")
        print("5. Visualizar usuarios")  # Añadir opción para visualizar usuarios
        print("6. Ver listas de reproducción")  # Ver listas de reproducción del usuario
        print("7. Ver canciones en una lista de reproducción")  # Ver canciones específicas
        print("8. Eliminar lista de reproducción")  # Eliminar una lista específica
        print("9. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            crear_lista_reproduccion(usuario_id)
        elif opcion == "2":
            agregar_cancion_a_lista(usuario_id)
        elif opcion == "3":
            agregar_cancion_a_biblioteca(usuario_id)
        elif opcion == "4":
            buscar_cancion_por_nombre()
        elif opcion == "5":
            visualizar_usuarios()
        elif opcion == "6":
            ver_listas_reproduccion(usuario_id)
        elif opcion == "7":
            ver_canciones_en_lista(usuario_id)
        elif opcion == "8":
            eliminar_lista_reproduccion(usuario_id)
        elif opcion == "9":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
        # Aquí puedes implementar las opciones del menú de usuario

# Menú de principal de youtube terminal
def menu_principal():
    while True:
        print("\n===== YOUTUBE =====")  # Agregamos el título aquí
        print("1. Crear cuenta")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            crear_cuenta()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()
