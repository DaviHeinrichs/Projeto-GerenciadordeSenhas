from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import bcrypt
import base64





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
    key = Column("key", String, nullable=True)
    
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
    where_used1 = Column("where_used1", String)
    where_used2 = Column("where_used2", String)
    where_used3 = Column("where_used3", String)
    where_used4 = Column("where_used4", String)
    where_used5 = Column("where_used5", String)
    
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
    
    user = session.query(User).filter_by(email=used_email).first()
    senha = user.senha
    email = user.email 
    
    if (email == used_email) and (senha == used_senha):
        
        return True
    else:
        session.close()
        return False
    session.close()

def get_key_salt(id):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    info = session.query(Info).filter_by(user_id=id).first()
    key_salt = info.key_salt
    
    return key_salt

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

def encrypt_password(key, password):
    import secrets
    
    
    iv = secrets.token_bytes(12)
    
    # Cria o cifrador
    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    )
    
    # Criptografa
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(password.encode()) + encryptor.finalize()
    
    # Combina IV + ciphertext + tag
    encrypted_data = iv + ciphertext + encryptor.tag
    
    # Retorna como string base64
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_password(key, encrypted_password) -> str:
    
    encrypted_data = base64.b64decode(encrypted_password)
    
    
    iv = encrypted_data[:12]
    ciphertext = encrypted_data[12:-16]
    tag = encrypted_data[-16:]
    
    # Cria o cifrador
    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    )
    
    # Descriptografa
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
    
    return decrypted.decode('utf-8')

def criar_masterpassword(used_master, used_salt, used_id):
    from core.hash_gen.main import verification_hash_create, key_gen
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    key_salt = get_key_salt(used_id)
    
    new_key = key_gen(used_master, key_salt)
    new_hash = verification_hash_create(used_master, used_salt)
    
    alterar = session.query(Info).filter_by(user_id=used_id).first()
    alterar.hash_verify = new_hash
    alterar.key = new_key
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

def não_tem_senha1(user_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    id = get_id(user_email)
    checar = session.query(Password).filter_by(user_id=id).first()
    
    if checar.pass1 is None:
        session.close()
        return True
    else:
        session.close()
        return False


def não_tem_senha2(user_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    id = get_id(user_email)
    checar = session.query(Password).filter_by(user_id=id).first()
    if checar.pass2 is None:
        session.close()
        return True
    else:
        session.close()
        return False

def não_tem_senha3(user_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    id = get_id(user_email)
    checar = session.query(Password).filter_by(user_id=id).first()
    if checar.pass3 is None:
        session.close()
        return True
    else:
        session.close()
        return False

def não_tem_senha4(user_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    id = get_id(user_email)
    checar = session.query(Password).filter_by(user_id=id).first()
    if checar.pass4 is None:
        session.close()
        return True
    else:
        session.close()
        return False

def não_tem_senha5(user_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    id = get_id(user_email)
    checar = session.query(Password).filter_by(user_id=id).first()
    if checar.pass5 is None:
        session.close()
        return True
    else:
        session.close()
        return False


def get_senha(password_number, user_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    id = get_id(user_email)
    
    info = session.query(Info).filter_by(user_id=id).first()
    key = info.key
    
    if password_number == "pass1":
        user = session.query(Password).filter_by(user_id=id).first()
        encrypted = user.pass1
        where_used = user.where_used1
        decrypted_password = decrypt_password(key, encrypted)
        return decrypted_password, where_used
    
    elif password_number == "pass2":
        user = session.query(Password).filter_by(user_id=id).first()
        encrypted = user.pass2
        where_used = user.where_used2
        decrypted_password = decrypt_password(key, encrypted)
        return decrypted_password, where_used
    elif password_number == "pass3":
        user = session.query(Password).filter_by(user_id=id).first()
        encrypted = user.pass3
        where_used = user.where_used3
        decrypted_password = decrypt_password(key, encrypted)
        return decrypted_password, where_used
    
    elif password_number == "pass4":
        user = session.query(Password).filter_by(user_id=id).first()
        encrypted = user.pass4
        where_used = user.where_used4
        decrypted_password = decrypt_password(key, encrypted)
        return decrypted_password, where_used
    
    elif password_number == "pass5":
        user = session.query(Password).filter_by(user_id=id).first()
        encrypted = user.pass5
        where_used = user.where_used5
        decrypted_password = decrypt_password(key, encrypted)
        return decrypted_password, where_used
    session.close()
    
def verificar_master(password, user_email):
    from core.hash_gen.main import master_verify
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    user = session.query(User).filter_by(email=user_email).first()
    salt = user.user_salt
    id = user.user_id
    Info_user = session.query(Info).filter_by(user_id=id).first()
    stored_hash = Info_user.hash_verify
    
    verificar = master_verify(password,salt,stored_hash)
    
    return verificar
        
def criar_senha(password_number, user_email, nova_senha, novo_local):
    from core.hash_gen.main import verification_hash_create
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    id = get_id(user_email)
    
    info = session.query(Info).filter_by(user_id=id).first()
    key = info.key

    encrypted_password = encrypt_password(key, nova_senha)

    
    if password_number == "pass1":
        user_table= session.query(User).filter_by(user_id=id).first()
        salt = user_table.user_salt
        user = session.query(Password).filter_by(user_id=id).first()
        user.pass1 = encrypted_password
        user.where_used1 = novo_local
        user.hash_pass1 = verification_hash_create(nova_senha,salt)
    
    elif password_number == "pass2":
        user_table = session.query(User).filter_by(user_id=id).first()
        salt = user_table.user_salt
        user = session.query(Password).filter_by(user_id=id).first()
        user.pass2 = encrypted_password
        user.where_used2 = novo_local
        user.hash_pass2 = verification_hash_create(nova_senha,salt)
        
        
    elif password_number == "pass3":
        user_table = session.query(User).filter_by(user_id=id).first()
        salt = user_table.user_salt
        salt = user_table.user_salt
        user = session.query(Password).filter_by(user_id=id).first()
        user.pass3 = encrypted_password
        user.where_used3 = novo_local
        user.hash_pass3 = verification_hash_create(nova_senha,salt)
    
    elif password_number == "pass4":
        user_table = session.query(User).filter_by(user_id=id).first()
        salt = user_table.user_salt
        user = session.query(Password).filter_by(user_id=id).first()
        user.pass4 = encrypted_password
        user.where_used4 = novo_local
        user.hash_pass4 = verification_hash_create(nova_senha,salt)
    
    elif password_number == "pass5":
        user_table = session.query(User).filter_by(user_id=id).first()
        salt = user_table.user_salt
        user = session.query(Password).filter_by(user_id=id).first()
        user.pass5 = encrypted_password
        user.where_used5 = novo_local
        user.hash_pass5 = verification_hash_create(nova_senha,salt)
    
    session.commit()
    session.close()

def get_role_id(user_email):
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    
    user = session.query(User).filter_by(email=user_email).first()
    id = user.role_id
    return id

def load_user_table():
    db = create_engine(f"sqlite:///{db_file_path}")
    Session = sessionmaker(bind=db)
    session = Session()
    metadata = MetaData()
    metadata.reflect(bind=db)
    tabela = metadata.tables[User.__tablename__]
    
    data = session.query(tabela).all()
    session.close()
    return data , tabela

        
base.metadata.create_all(bind=db)
    