from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

import os, sys
from pathlib import Path


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_directory = Path(base_dir)
db_directory.mkdir(parents=True, exist_ok=True)

db_file_path = db_directory / "database.db"

db = create_engine(f"sqlite:///{db_file_path}")
Session = sessionmaker(bind=db)
session = Session()

base = declarative_base()

class User(base):
    __tablename__ = "users"
    
    user_id = Column("user_id", Integer, primary_key=True, nullable=False)
    user_salt = Column("user_salt", String, nullable=False)
    role_id = Column("role_id", Integer, nullable=False)
    nome = Column("nome", String, nullable=False)
    sobrenome = Column("sobrenome", String, nullable=False)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean, nullable=False)
    have_master = Column("have_master", Boolean, nullable=False)
    
    def __init__ (self, user_id, user_salt, role_id, nome, sobrenome, email, senha, ativo,have_master):
        self.user_id = user_id
        self.user_salt = user_salt
        self.role_id = role_id
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email 
        self.senha = senha
        self.ativo = ativo
        self.have_master = have_master
        
        
class Role(base):
    __tablename__ = "role"
    
    role_id = Column("role_id", Integer, primary_key=True)
    role_name = Column("role_name", String)
    
    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name= role_name

class Info(base):
    __tablename__ = "infos"
    
    user_id = Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    hash_verify = Column("hash_verify", String, nullable=True)
    key_salt = Column("key_salt", String, nullable=False)
    
    def __init__ (self, user_id, key_salt):
        self.user_id = user_id
        self.key_salt = key_salt

class Password(base):
    __tablename__ = "passwords"
    
    user_id = Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True)
    pass1 = Column("pass1", String, nullable=True)
    pass2 = Column("pass2", String, nullable=True)
    pass3 = Column("pass3", String, nullable=True)
    pass4 = Column("pass4", String, nullable=True)
    pass5 = Column("pass5", String, nullable=True)
    hash_pass1 = Column("hash_pass1", String, nullable=True)
    hash_pass2 = Column("hash_pass2", String, nullable=True)
    hash_pass3 = Column("hash_pass3", String, nullable=True)
    hash_pass4 = Column("hash_pass4", String, nullable=True)
    hash_pass5 = Column("hash_pass5", String, nullable=True)
    
    def __init__(self, user_id):
        self.user_id = user_id


class Blocked_user(base):
    __tablename__ = "blocked_users"
    
    user_id = Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True)
    
    def __init__(self, user_id):
        self.user_id = user_id
        
def criar_user(user_nome,user_sobrenome,user_email,user_senha):
    import secrets
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from interface.users.user_data.statements.user_gen.gen_id import gerar_id
    
    user_id_gen = gerar_id()
    
    user_salt_binary = secrets.token_bytes(16)
    user_salt_hex = user_salt_binary.hex()
    
    key_salt_binary = secrets.token_bytes(16)
    key_salt_hex = key_salt_binary.hex()
    
    
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
        ativo = True,
        have_master=False
    )
    Info_id = Info(
        user_id=user_id_gen,
        key_salt = key_salt_hex
    )
    pass_id = Password(
        user_id=user_id_gen
    )
    
    
    session.add(criar)
    session.add(Info_id)
    session.add(pass_id)
    session.commit()
    session.close()
    

def check_user(used_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    usere = session.query(User).filter_by(email=used_email).first()
    if usere == None:
        return True    
    elif usere != None:        
        return False
    session.close()

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
    session.close()

def get_salt(used_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    user = session.query(User).filter_by(email=used_email).first()
    salt = user.user_salt
    session.close()
    return salt

def get_id(used_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    user = session.query(User).filter_by(email=used_email).first()
    id = user.user_id
    session.close()
    return id

def turn_havemaster(used_id):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    alterar = session.query(User).filter_by(user_id=used_id).first()
    alterar.have_master = True
    session.add(alterar)
    session.commit()
    session.close()
    
def criar_masterpassword(used_master, used_salt, used_id):
    from core.hash_gen.main import verification_hash_create
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    new_hash = verification_hash_create(used_master, used_salt)
    
    alterar = session.query(Info).filter_by(user_id=used_id).first()
    alterar.hash_verify = new_hash
    session.add(alterar)
    session.commit()
    session.close()

def have_masterpassword(used_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    checar_master = session.query(User).filter_by(email=used_email).first()
    tem_master = checar_master.have_master
    session.close()
    return tem_master
    

    


        
base.metadata.create_all(bind=db)
    