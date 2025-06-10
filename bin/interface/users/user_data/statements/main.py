from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

import os
from pathlib import Path


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_directory = Path(base_dir)
db_directory.mkdir(parents=True, exist_ok=True)

db_file_path = db_directory / "users_base.db"




db = create_engine(f"sqlite:///{db_file_path}")
Session = sessionmaker(bind=db)
session = Session()

base = declarative_base()

class User(base):
    __tablename__ = "users"
    
    user_id = Column("user_id", Integer, primary_key=True, nullable=False)
    user_salt = Column("user_salt", String(55), nullable=False)
    role_id = Column("role_id", Integer, nullable=False)
    nome = Column("nome", String, nullable=False)
    sobrenome = Column("sobrenome", String, nullable=False)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean, nullable=False)
    
    def __init__ (self, user_id, user_salt, role_id, nome, sobrenome, email, senha, ativo):
        self.user_id = user_id
        self.user_salt = user_salt
        self.role_id = role_id
        self.nome = nome
        self.sobrenome = sobrenome
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
    
    user_id = Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True)
    
    def __init__(self, user_id):
        self.user_id = user_id
        
def criar_user(user_nome,user_sobrenome,user_email,user_senha):
    import secrets
    from interface.users.user_data.statements.user_gen.gen_id import gerar_id
    user_id_gen = gerar_id()
    user_salt_binary = secrets.token_bytes(16)
    user_salt_hex = user_salt_binary.hex()
    
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    criar = User(
        user_id = user_id_gen,
        user_salt = user_salt_hex,
        role_id = 1,
        nome = user_nome,
        sobrenome = user_sobrenome, 
        email = user_email, 
        senha = user_senha, 
        ativo = True
    )
    session.add(criar)
    session.commit()

def check_user(used_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    usere = session.query(User).filter_by(email=used_email).first()
    if usere == None:
        return True    
    elif usere != None:        
        return False

def check_login(used_email, used_senha):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    checar_email = session.query(User).filter_by(email=used_email).first()
    checar_senha = session.query(User).filter_by(senha=used_senha).first()
    
    try:
        if (checar_email.email == used_email) and (checar_senha.senha == used_senha):
            return True
    except:
        return False    
base.metadata.create_all(bind=db)
    