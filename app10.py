from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Tabla intermedia para relación N-M
libro_genero = db.Table(
    "libro_genero",
    db.Column("libro_id", db.Integer, db.ForeignKey("libros.id"), primary_key=True),
    db.Column("genero_id", db.Integer, db.ForeignKey("generos.id"), primary_key=True)
)

class Autor(db.Model):
    __tablename__ = "autores"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    nacionalidad = db.Column(db.String(50), nullable=False)

    libros = db.relationship("Libro", back_populates="autor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Autor: {self.nombre} ({self.nacionalidad})>"

class Libro(db.Model):
    __tablename__ = "libros"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    anio = db.Column(db.Integer, nullable=False)

    autor_id = db.Column(db.Integer, db.ForeignKey("autores.id"), nullable=False)
    autor = db.relationship("Autor", back_populates="libros")

    generos = db.relationship("Genero", secondary=libro_genero, back_populates="libros")

    def __repr__(self):
        return f"<Libro: {self.titulo} ({self.anio})>"

class Genero(db.Model):
    __tablename__ = "generos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    libros = db.relationship("Libro", secondary=libro_genero, back_populates="generos")

    def __repr__(self):
        return f"<Genero: {self.nombre}>"

# Funciones CRUD
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada satisfactoriamente")

def insertar_datos():
    with app.app_context():
        # Autores
        a1 = Autor(nombre="Gabriel García Márquez", nacionalidad="Colombiana")
        a2 = Autor(nombre="Julio Cortázar", nacionalidad="Argentina")
        a3 = Autor(nombre="Isabel Allende", nacionalidad="Chilena")

        # Géneros
        g1 = Genero(nombre="Ficción")
        g2 = Genero(nombre="Historia")
        g3 = Genero(nombre="Lenguaje")
        g4 = Genero(nombre="Tecnología")

        # Libros
        l1 = Libro(titulo="Cien Años de Soledad", anio=1967, autor=a1, generos=[g1, g2])
        l2 = Libro(titulo="El Amor en los Tiempos del Cólera", anio=1985, autor=a1, generos=[g1])
        l3 = Libro(titulo="Rayuela", anio=1963, autor=a2, generos=[g1, g3])
        l4 = Libro(titulo="La Casa de los Espíritus", anio=1982, autor=a3, generos=[g1, g2])
        l5 = Libro(titulo="Paula", anio=1994, autor=a3, generos=[g2])

        db.session.add_all([a1, a2, a3, g1, g2, g3, g4, l1, l2, l3, l4, l5])
        db.session.commit()
        print("Datos insertados correctamente")

def consultar_datos():
    with app.app_context():
        print("\nAutores y sus libros:")
        autores = Autor.query.all()
        for a in autores:
            print(f"{a.nombre} ({a.nacionalidad})")
            for l in a.libros:
                print(f" - {l.titulo} ({l.anio})")

        print("\nGéneros y sus libros:")
        generos = Genero.query.all()
        for g in generos:
            print(f"{g.nombre}:")
            for l in g.libros:
                print(f" - {l.titulo}")

def actualizar_datos():
    with app.app_context():
        libro = Libro.query.filter_by(id=3).first()
        if libro:
            libro.titulo = "Rayuela (Edición Revisada)"
            db.session.commit()
            print("Libro actualizado:", libro)
        else:
            print("Libro no encontrado")

def eliminar_datos():
    with app.app_context():
        autor = Autor.query.filter_by(id=1).first()
        if autor:
            db.session.delete(autor)
            db.session.commit()
            print(f"Autor {autor.nombre} eliminado junto con sus libros")
        else:
            print("Autor no encontrado")

if __name__ == "__main__":
    init_db()
    insertar_datos()
    consultar_datos()
    actualizar_datos()
    consultar_datos()
    eliminar_datos()
    consultar_datos()
