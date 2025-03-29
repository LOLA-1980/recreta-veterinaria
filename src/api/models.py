from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    mascotas =relationship("Mascota", back_populates="propietario", cascade="all, delete-orphan")
    recetas = relationship("RecetaMedica", back_populates="usuario", cascade="all, delete-orphan") 

    def __repr__(self):
        return f'<User {self.email}>'


    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "mascota": [mascota.serialize() for mascota in self.mascotas],
            "recetas": [receta.serialize() for receta in self.recetas]
            # do not serialize the password, its a security breach
        }


class Veterinario(db.Model):
    __tablename__ = "veterinario"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)

    recetas = relationship('RecetaMedica', back_populates='veterinario', cascade="all, delete-orphan")  # Relación con recetas

    def __repr__(self):
        return f'<Veterinario {self.id}: {self.nombre}>'
    
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "recetas": [receta.serialize() for receta in self.recetas]  # Serializar recetas
        }
    

class Mascota(db.Model):
    __tablename__ = "mascota"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    especie: Mapped[str] = mapped_column(String(50), nullable=False)
    raza: Mapped[str] = mapped_column(String(50), nullable=True)
    edad: Mapped[int] = mapped_column(Integer, nullable=True)
    peso: Mapped[int] = mapped_column(Integer, nullable=True)
    sexo: Mapped[str] = mapped_column(String(2), nullable=True)
    propietario_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    propietario = relationship("User", back_populates="mascotas")


    def __repr__(self):
        return f'<Mascota {self.id}: {self.nombre}>'
    
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
            "raza": self.raza,
            "edad": self.edad,
            "peso": self.peso,
            "sexo": self.sexo,
            "propietario": {
                "id": self.propietario.id,
                "nombre": self.propietario.nombre,  # Accedemos al nombre del propietario desde User
                "email": self.propietario.email
            }
        }
    

class RecetaMedica(db.Model):
    __tablename__ = "recetas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    diagnostico: Mapped[str] = mapped_column(Text, nullable=False)
    tratamiento: Mapped[str] = mapped_column(Text, nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    id_veterinario: Mapped[int] = mapped_column(Integer, ForeignKey('veterinario.id'), nullable=False)
    id_mascota: Mapped[int] = mapped_column(Integer, ForeignKey('mascota.id'), nullable=False)

    usuario = relationship('User', back_populates='recetas', cascade="all, delete-orphan")
    veterinario = relationship('Veterinario', back_populates='recetas', cascade="all, delete-orphan")
    mascota = relationship('Mascota', back_populates='recetas', cascade="all, delete-orphan")

    #Método para serializar la receta
    def serialize(self):
        usuario = {"id": self.usuario.id, "nombre": self.usuario.nombre} if self.usuario else None
        veterinario = {"id": self.veterinario.id, "nombre": self.veterinario.nombre} if self.veterinario else None
        mascota = {"id": self.mascota.id, "nombre": self.mascota.nombre} if self.mascota else None

        return {
            "id": self.id,
            "fecha": self.fecha.strftime('%Y-%m-%d %H:%M:%S'),  # Formato legible
            "diagnostico": self.diagnostico,
            "tratamiento": self.tratamiento,
            "usuario": usuario,
            "veterinario": veterinario,
            "mascota": mascota
        }
