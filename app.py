from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    
    def __repr__(self):
        return f"<User(name='{self.name}',email='{self.email}')>"

    
# Función para inicializar la base de datos
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada satisfactoriamente")
        
# Operaciones CRUD
def insert_users():
    with app.app_context():
        # Instanciación de objetos de tipo User
        user1 = User(name="Vidal", email="vidal@gmail.com")
        user2 = User(name="Jaime", email="jaime@gmail.com")
        user3 = User(name="Calle", email="calle@gmail.com")
        
        # Adición de objetos (registros en la tabla)
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        # Consolida los cambios en la base de datos
        db.session.commit()
        print("Usuarios insertados")

# Consultas a la base de datos
def query_users():
    with app.app_context():
        # Consultar todos los registros de una tabla
        print("Listado de usuarios")
        users = User.query.all()
        for item in users:
            print(item)
            
        # Consultas que cumplan cierta condición
        print("Listado de registros filtrados")
        filtrados = User.query.filter(User.id >= 2).all()
        for item in filtrados:
            print(item)
        
        # Consulta de un solo usuario
        print("Obtener un solo registro")
        user = User.query.filter_by(id = 100).first()
        if user:
            print(user)
        else:
            print("Usuario no encontrado")
            
def update_user():
    with app.app_context():
        print("\nActualización de un registro")
        user = User.query.filter_by(id = 1).first()
        if user:
            user.name = "Arroz con Leche"
            user.email = "arrozconleche@gmail.com"
            # Consolida los cambios en la base de datos
            db.session.commit()
            print("Usuario actualizado", user)
        else:
            print("Usuario no encontrado")
            
def delete_user():
    with app.app_context():
        print("\nEliminación de registro")
        user = User.query.filter_by(id = 3).first()
        if user:
            db.session.delete(user)
            # Consolida los cambios en la base de datos
            db.session.commit()
            print("Usuario satisfactoriamente")
        else:
            print("Usuario no encontrado")
            
            

if __name__ == "__main__":

    query_users()