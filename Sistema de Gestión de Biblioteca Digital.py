class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        # Usamos tuplas para almacenar atributos inmutables
        self.titulo_autor = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"Libro: {self.titulo_autor[0]} | Autor: {self.titulo_autor[1]} | Categoría: {self.categoria} | ISBN: {self.isbn}"


class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []  # Lista para libros prestados

    def __str__(self):
        return f"Usuario: {self.nombre} | ID: {self.id_usuario} | Libros prestados: {len(self.libros_prestados)}"


class Biblioteca:
    def __init__(self):
        self.libros_disponibles = {}  # Diccionario para libros (ISBN: Libro)
        self.usuarios_registrados = set()  # Conjunto para IDs de usuarios únicos
        self.usuarios = {}  # Diccionario para usuarios (ID: Usuario)

    def añadir_libro(self, libro):
        if libro.isbn not in self.libros_disponibles:
            self.libros_disponibles[libro.isbn] = libro
            print(f"Libro '{libro.titulo_autor[0]}' añadido.")
        else:
            print(f"El libro con ISBN {libro.isbn} ya existe.")

    def quitar_libro(self, isbn):
        if isbn in self.libros_disponibles:
            libro = self.libros_disponibles.pop(isbn)
            print(f"Libro '{libro.titulo_autor[0]}' eliminado.")
        else:
            print(f"No se encontró un libro con ISBN {isbn}.")

    def registrar_usuario(self, usuario):
        if usuario.id_usuario not in self.usuarios_registrados:
            self.usuarios_registrados.add(usuario.id_usuario)
            self.usuarios[usuario.id_usuario] = usuario
            print(f"Usuario '{usuario.nombre}' registrado.")
        else:
            print(f"El ID de usuario {usuario.id_usuario} ya está registrado.")

    def dar_de_baja_usuario(self, id_usuario):
        if id_usuario in self.usuarios_registrados:
            self.usuarios_registrados.remove(id_usuario)
            self.usuarios.pop(id_usuario)
            print(f"Usuario con ID {id_usuario} dado de baja.")
        else:
            print(f"No se encontró un usuario con ID {id_usuario}.")

    def prestar_libro(self, id_usuario, isbn):
        if id_usuario not in self.usuarios_registrados:
            print(f"Usuario con ID {id_usuario} no registrado.")
            return
        if isbn not in self.libros_disponibles:
            print(f"Libro con ISBN {isbn} no disponible.")
            return

        libro = self.libros_disponibles[isbn]
        usuario = self.usuarios[id_usuario]
        usuario.libros_prestados.append(libro)
        self.libros_disponibles.pop(isbn)
        print(f"Libro '{libro.titulo_autor[0]}' prestado a {usuario.nombre}.")

    def devolver_libro(self, id_usuario, isbn):
        if id_usuario not in self.usuarios_registrados:
            print(f"Usuario con ID {id_usuario} no registrado.")
            return

        usuario = self.usuarios[id_usuario]
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                usuario.libros_prestados.remove(libro)
                self.libros_disponibles[isbn] = libro
                print(f"Libro '{libro.titulo_autor[0]}' devuelto por {usuario.nombre}.")
                return
        print(f"El usuario {usuario.nombre} no tiene prestado el libro con ISBN {isbn}.")

    def buscar_libros(self, criterio, valor):
        resultados = []
        for libro in self.libros_disponibles.values():
            if criterio == "titulo" and valor.lower() in libro.titulo_autor[0].lower():
                resultados.append(libro)
            elif criterio == "autor" and valor.lower() in libro.titulo_autor[1].lower():
                resultados.append(libro)
            elif criterio == "categoria" and valor.lower() == libro.categoria.lower():
                resultados.append(libro)
        return resultados

    def listar_libros_prestados(self, id_usuario):
        if id_usuario not in self.usuarios_registrados:
            print(f"Usuario con ID {id_usuario} no registrado.")
            return

        usuario = self.usuarios[id_usuario]
        if not usuario.libros_prestados:
            print(f"{usuario.nombre} no tiene libros prestados.")
        else:
            print(f"Libros prestados a {usuario.nombre}:")
            for libro in usuario.libros_prestados:
                print(f"- {libro.titulo_autor[0]} ({libro.isbn})")


# Ejemplo de uso
biblioteca = Biblioteca()

# Añadir libros
libro1 = Libro("Cien años de soledad", "Gabriel García Márquez", "Novela", "9788437604947")
libro2 = Libro("1984", "George Orwell", "Ciencia Ficción", "9780451524935")
biblioteca.añadir_libro(libro1)
biblioteca.añadir_libro(libro2)

# Registrar usuarios
usuario1 = Usuario("Juan Pérez", "001")
biblioteca.registrar_usuario(usuario1)

# Prestar libros
biblioteca.prestar_libro("001", "9788437604947")

# Buscar libros por autor
resultados = biblioteca.buscar_libros("autor", "George Orwell")
for libro in resultados:
    print(libro)

# Listar libros prestados
biblioteca.listar_libros_prestados("001")

# Devolver libro
biblioteca.devolver_libro("001", "9788437604947")