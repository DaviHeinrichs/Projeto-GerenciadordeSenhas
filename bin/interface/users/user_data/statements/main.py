from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

db = create_engine("sqlite:///user_data.db")
Session = sessionmaker(bind=db)
session = Session()

base = declarative_base()

class User(base):
    __tablename__ = "users"
    
    user_id = Column("user_id", String(55), primary_key=True, nullable=False)
    user_salt = Column("user_salt", String(55), nullable=False)
    role_id = Column("role_id", Integer, nullable=False)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean, nullable=False)
    
    def __init__ (self, user_id, user_salt, role_id, email, senha, ativo=True):
        self.user_id = user_id
        self.user_salt = user_salt
        self.role_id = role_id
        self.email = email 
        self.senha = senha
        self.ativo = ativo

class Role(base):
    __tablename__ = "role"
    
    role_id = Column("role_id", Integer, primary_key=True)
    role_name = Column("role_name", String)
    
    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name= role_name



class Blocked_user(base):
    __tablename__ = "blocked_users"
    
    user_id = Column("user_id", String, ForeignKey("users.user_id"), primary_key=True)
    
    def __init__(self, user_id):
        self.user_id = user_id
    
base.metadata.create_all(bind=db)
    