import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # Para el hash de contraseñas
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

# Definir la base de datos de SQLAlchemy
Base = declarative_base()

# Tabla de Usuarios (Login)
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones de favoritos
    favoritos_naves = relationship('FavoritoNave', back_populates='usuario', cascade="all, delete-orphan")
    favoritos_planetas = relationship('FavoritoPlaneta', back_populates='usuario', cascade="all, delete-orphan")
    favoritos_personajes = relationship('FavoritoPersonaje', back_populates='usuario', cascade="all, delete-orphan")

    # Método para setear la contraseña en forma de hash
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Método para verificar la contraseña
    def check_password(self, password):
        return check_password_hash(self.password, password)

# Tabla de Naves
class Nave(Base):
    __tablename__ = 'naves'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    fabricante = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con los favoritos
    usuarios_favoritos = relationship('FavoritoNave', back_populates='nave')

# Tabla de Planetas
class Planeta(Base):
    __tablename__ = 'planetas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    clima = Column(String(100))
    terreno = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con los favoritos
    usuarios_favoritos = relationship('FavoritoPlaneta', back_populates='planeta')

# Tabla de Personajes
class Personaje(Base):
    __tablename__ = 'personajes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    altura = Column(Integer)
    masa = Column(Integer)
    color_ojos = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con los favoritos
    usuarios_favoritos = relationship('FavoritoPersonaje', back_populates='personaje')

# Tabla de Favoritos de Naves
class FavoritoNave(Base):
    __tablename__ = 'favoritos_naves'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    nave_id = Column(Integer, ForeignKey('naves.id'), nullable=False)
    
    usuario = relationship('Usuario', back_populates='favoritos_naves')
    nave = relationship('Nave', back_populates='usuarios_favoritos')

# Tabla de Favoritos de Planetas
class FavoritoPlaneta(Base):
    __tablename__ = 'favoritos_planetas'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    planeta_id = Column(Integer, ForeignKey('planetas.id'), nullable=False)
    
    usuario = relationship('Usuario', back_populates='favoritos_planetas')
    planeta = relationship('Planeta', back_populates='usuarios_favoritos')

# Tabla de Favoritos de Personajes
class FavoritoPersonaje(Base):
    __tablename__ = 'favoritos_personajes'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    personaje_id = Column(Integer, ForeignKey('personajes.id'), nullable=False)
    
    usuario = relationship('Usuario', back_populates='favoritos_personajes')
    personaje = relationship('Personaje', back_populates='usuarios_favoritos')

# Crear el diagrama ER
render_er(Base, 'blog_starwars_diagram.png')

# Configuración de la base de datos (SQLite en este caso)
engine = create_engine('sqlite:///starwars_blog.db')
Base.metadata.create_all(engine)
