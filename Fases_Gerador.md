
### **🌱 Fase 1: Fundamentos em Python (Pré-MVP)**
1. **Manipulação de Strings e Segurança Básica**  
   - Gerar senhas aleatórias com o módulo `secrets` (não use `random`!).  
   - Validar força de senhas (ex: mínimo de caracteres, símbolos).  

2. **Estrutura de Projetos Python**  
   - Organizar código em funções e módulos (ex: `password_generator.py`, `validator.py`).  
   - Usar `__init__.py` e imports relativos.  

3. **Ambientes Virtuais e Dependências**  
   - Criar e ativar venv (`python -m venv venv`).  
   - Gerenciar pacotes com `pip` e `requirements.txt`.  

---

### **🚀 Fase 2: Backend Básico (MVP)**
4. **FastAPI Essentials**  
   - Criar rotas simples (`@app.get("/generate-password")`).  
   - Validar inputs com `Pydantic` (ex: tamanho mínimo da senha).  

5. **Autenticação Simples**  
   - Implementar login básico com senha mestra (sem JWT ainda).  
   - Usar `hashlib` para SHA-256 (provisório, substituirá por Argon2 depois).  

6. **Banco de Dados Inicial**  
   - SQLite3 com `sqlite3` padrão do Python.  
   - Operações CRUD: salvar senhas geradas em uma tabela.  

7. **RBAC**

8. **Variáveis de Ambiente**  
   - Usar `python-dotenv` para carregar `.env` (ex: `DB_PATH`, `SECRET_KEY`).  
   - **Por que?** Evitar hardcoding de dados sensíveis.  

---

### **🛡️ Fase 3: Segurança Intermediária (Pós-MVP)**
9. **Criptografia Básica**  
   - Criptografar senhas no banco com `cryptography` (AES-256).  
   - Gerenciar IVs (Initialization Vectors) e salting.  

10. **Autenticação Robustecida**  
   - Substituir SHA-256 por **Argon2** (`passlib`).  
   - Implementar JWT (`python-jose`).  

11. **HTTPS e Middlewares**  
    - Configurar certificado SSL local (para testes com `mkcert`).  
    - Adicionar middlewares no FastAPI (ex: verificar HTTPS).  

---

### **🔗 Fase 4: Integração Frontend (Extensão Chrome)**
12. **JavaScript Básico**  
    - Manipular DOM (ex: `document.getElementById()`).  
    - Fazer chamadas HTTP com `fetch()` para sua API.  

13. **Chrome API**  
    - Usar `chrome.storage.local` para armazenar tokens JWT.  
    - Criar popups com HTML/CSS vanilla.  

14. **Comunicação Segura**  
    - Enviar senhas criptografadas para o backend (usar AES do Python).  

---

### **⚙️ Fase 5: Tópicos Avançados**
15. **WebAssembly (Opcional)**  
    - Compilar Argon2 para WASM (melhorar segurança no cliente).  

16. **SQLCipher**  
    - Migrar de SQLite para SQLCipher (criptografia at-rest).  

17. **Deploy Seguro**  
    - Dockerizar o backend.  
    - Configurar Nginx como proxy reverso.  

---

### **📌 Ordem de Aprendizado Resumida**  
1. Python → FastAPI → SQLite → Variáveis de Ambiente  
2. Hashlib → Argon2 → JWT → AES-256  
3. JavaScript → Chrome API → WASM (opcional)  
4. Docker → Nginx → Monitoramento  


#Explicação:

### **🌱 Passo 1: Gerar Senhas Aleatórias com `secrets`**  
**O que fazer?**  
Criar uma função em Python que gere senhas aleatórias usando o módulo `secrets` (seguro para criptografia).  

**Por quê?**  
- `random` é previsível e inseguro para senhas.  
- `secrets` usa fontes criptográficas do sistema operacional.  

**O que aprender?**  
- Como usar: `secrets.token_hex()`, `secrets.choice()`.  
- Combinar caracteres (letras, números, símbolos).  
- Parâmetros: tamanho da senha, complexidade.  

**Exemplo mínimo:**  
```python
import secrets
import string

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(secrets.choice(chars) for _ in range(length))
```
 

---

### **🌱 Passo 2: Validar Força de Senhas**  
**O que fazer?**  
Implementar uma função que avalie a complexidade da senha (ex: mínimo 12 caracteres, 1 símbolo).  

**Por quê?**  
- Evitar senhas fracas mesmo que geradas aleatoriamente.  
- Atender a políticas de segurança.  

**O que aprender?**  
- Expressões regulares (regex) para verificar padrões.  
- Bibliotecas como `zxcvbn` (para análise avançada).  

**Exemplo mínimo:**  
```python
import re

def is_strong(password):
    return (len(password) >= 12 and 
            re.search(r"[!@#$%]", password) and 
            re.search(r"\d", password))
```

---

### **🌱 Passo 3: Organizar o Código em Módulos**  
**O que fazer?**  
Dividir o código em arquivos como `password_generator.py` e `validator.py`.  

**Por quê?**  
- Manter o código reutilizável e legível.  
- Evitar "spaghetti code".  

**O que aprender?**  
- Estrutura de pastas em Python.  
- Como usar `__init__.py` e imports (ex: `from .validator import is_strong`).  

**Exemplo de estrutura:**  
```
my_project/
├── utils/
│   ├── password_generator.py
│   └── validator.py
└── main.py
```

--- 

### **🚀 Passo 4: Introdução ao FastAPI (Backend Básico)**  
**Objetivo:** Transformar seu gerador/validador de senhas em uma **API web** que possa ser acessada por HTTP (útil para a extensão do navegador no futuro).  

---

#### **📌 O Que Você Vai Aprender/Aplicar:**  
1. **FastAPI Essentials**:  
   - Criar rotas (`@app.get`, `@app.post`).  
   - Usar `Pydantic` para validar dados de entrada.  

2. **Integração com Suas Funções**:  
   - Chamar `generate_password()` e `is_strong()` a partir de endpoints.  

3. **Testar a API Localmente**:  
   - Usar o Swagger UI automático (`/docs`) ou ferramentas como `curl`/Postman.  

---

#### **📝 Estrutura Básica do Código**  
1. **Arquivo `bin/interfaces/web/app.py`** (ponto de entrada da API):  
```python
from fastapi import FastAPI
from ..backend.password_functions.utils import generate_password, is_strong
from pydantic import BaseModel

app = FastAPI()

# Modelo Pydantic para validação
class PasswordRequest(BaseModel):
    length: int = 12

# Rota para gerar senha
@app.post("/generate-password")
async def generate_password_route(request: PasswordRequest):
    password = generate_password(length=request.length)
    return {
        "password": password,
        "is_strong": is_strong(password)
    }

# Rota para validar senha
@app.get("/validate-password")
async def validate_password_route(password: str):
    return {"is_strong": is_strong(password)}
```

2. **Instale as dependências**:  
```bash
pip install fastapi uvicorn
```

3. **Execute a API**:  
```bash
uvicorn bin.interfaces.web.app:app --reload
```

---

#### **🔍 Como Testar a API:**  
1. **Via Swagger UI (Recomendado para iniciantes)**:  
   - Acesse `http://localhost:8000/docs` no navegador.  
   - Teste os endpoints diretamente na interface interativa.  

2. **Via `curl` (Terminal)**:  
```bash
# Gerar senha:
curl -X POST "http://localhost:8000/generate-password" -H "Content-Type: application/json" -d '{"length": 16}'

# Validar senha:
curl "http://localhost:8000/validate-password?password=MinhaSenha@123"
```

---

#### **🌐 Próximos Passos (Quando Estiver Pronto):**  
1. **Adicionar Autenticação Básica**:  
   - Proteger a API com JWT (usando `auth/jwt.py` do seu projeto).  

2. **Conectar à Extensão de Navegador**:  
   - Modificar `popup/main.js` para chamar a API via `fetch()`.  

3. **Usar Variáveis de Ambiente**:  
   - Movar configurações (ex: porta da API) para `config/settings.py`.  

---

### **🔐 Passo 5: Autenticação com JWT (JSON Web Tokens)**  
**Objetivo:** Implementar login simples usando tokens JWT para proteger os endpoints da API.

---

#### **📌 O Que Você Vai Aprender/Aplicar:**  
1. **Bibliotecas Necessárias:**  
   - `python-jose` (para gerar/validar tokens JWT).  
   - `passlib` (para hash de senhas).  

2. **Fluxo de Autenticação:**  
   - Usuário envia `master_password` → API verifica → Retorna um token JWT.  
   - Token é usado em requisições subsequentes.  

3. **Proteção de Endpoints:**  
   - Criar um sistema de dependência (`Depends`) no FastAPI para validar tokens.  

---

#### **📝 Estrutura do Código**  
1. **Adicione em `bin/backend/auth/jwt.py`:**  
```python
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Configurações (em produção, use variáveis de ambiente!)
SECRET_KEY = "sua-chave-secreta"  # Gerada com: openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expires}, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

2. **Crie um novo endpoint de login em `bin/interfaces/web/routers/auth.py`:**  
```python
from fastapi import APIRouter, Depends, HTTPException
from ..backend.auth.jwt import create_access_token, verify_password

router = APIRouter()

@router.post("/login")
async def login(master_password: str):
    # Em um sistema real, você verificaria a senha no banco de dados
    if not verify_password(master_password, "hash_armazenado_no_banco"):
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    token = create_access_token({"sub": "user_id"})
    return {"access_token": token}
```

3. **Proteja os endpoints existentes em `bin/interfaces/web/app.py`:**  
```python
from fastapi import Depends, HTTPException
from .routers.auth import router as auth_router
from ..backend.auth.jwt import decode_token

app = FastAPI()
app.include_router(auth_router)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return decode_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.post("/generate-password")
async def generate_password_route(..., user: dict = Depends(get_current_user)):
    # Endpoint agora requer autenticação!
```

---

#### **🔍 Como Testar:**  
1. **Obtenha um token:**  
   ```bash
   curl -X POST "http://localhost:8000/login" -H "Content-Type: application/json" -d '{"master_password": "sua_senha"}'
   ```

2. **Use o token em endpoints protegidos:**  
   ```bash
   curl -X POST "http://localhost:8000/generate-password" -H "Authorization: Bearer SEU_TOKEN" -H "Content-Type: application/json" -d '{"length": 16}'
   ```

Você está absolutamente certo! Vamos corrigir essa lacuna e detalhar o **Passo 6** antes de prosseguir com o RBAC. Aqui está o que faltou, integrado ao fluxo original:

---

### **🔒 Passo 6: Armazenar Senhas no Banco de Dados (SQLite + SQLAlchemy)**  
**Objetivo:** Persistir usuários e senhas de forma segura, substituindo o armazenamento temporário em memória.

---

#### **📌 O Que Você Vai Aprender/Aplicar:**  
1. **Modelagem de Dados com SQLAlchemy:**  
   - Criar tabelas `User` e `PasswordEntry`.  
   - Relacionamentos (um usuário tem múltiplas senhas).  

2. **Hash de Senhas:**  
   - Usar `passlib` para hash da master password (nunca armazenar em texto puro).  

3. **Operações CRUD Seguras:**  
   - Inserir, consultar e deletar senhas criptografadas.  

---

#### **📝 Estrutura do Código**  
1. **Em `bin/backend/db/models.py`:**  
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    master_password_hash = Column(String(255))  # Hash usando Argon2
    passwords = relationship("PasswordEntry", back_populates="user")

class PasswordEntry(Base):
    __tablename__ = "passwords"
    id = Column(Integer, primary_key=True)
    service_name = Column(String(100))
    encrypted_password = Column(String(255))  # Criptografado com AES
    iv = Column(String(255))  # Vetor de inicialização
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="passwords")
```

2. **Em `bin/backend/db/repositories.py`:**  
```python
from sqlalchemy.orm import Session
from .models import User, PasswordEntry
from ..auth.jwt import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, email: str, master_password: str):
        hashed_password = get_password_hash(master_password)
        user = User(email=email, master_password_hash=hashed_password)
        self.db.add(user)
        self.db.commit()
        return user
```

3. **Em `bin/interfaces/web/routers/auth.py` (atualizado):**  
```python
from ..backend.db.repositories import UserRepository

@router.post("/register")
async def register(email: str, master_password: str, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.create_user(email, master_password)
    return {"user_id": user.id}
```

---

#### **🔍 Como Testar:**  
1. **Crie um usuário:**  
   ```bash
   curl -X POST "http://localhost:8000/register" -H "Content-Type: application/json" -d '{"email":"user@test.com","master_password":"senha_segura"}'
   ```

2. **Verifique o banco de dados:**  
   ```bash
   sqlite3 instance/database.db "SELECT * FROM users;"
   ```

---

Ótimo! Vamos adicionar o **Passo 7 (RBAC - Role-Based Access Control)** sem substituir os passos existentes. Este é um complemento avançado para controlar permissões de usuários (ex: admin vs. usuário comum).  

---

### **👑 Passo 7: Implementar RBAC (Role-Based Access Control)**  
**Objetivo:**  
Adicionar hierarquia de permissões (ex: `admin` pode acessar todas as senhas, `user` só as suas).  

---

#### **📌 O Que Você Vai Aprender/Aplicar:**  
1. **Novas Tabelas no Banco de Dados:**  
   - `roles` (ex: `admin`, `user`).  
   - `permissions` (ex: `read:all_passwords`, `delete:any_user`).  

2. **Modificações no JWT:**  
   - Adicionar `roles` e `permissions` ao token.  

3. **Middleware de Autorização:**  
   - Verificar permissões antes de acessar endpoints.  

---

#### **📝 Estrutura do Código**  
1. **Adicione modelos em `bin/backend/db/models.py`:**  
```python
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

# Tabela de associação (many-to-many entre roles e permissions)
role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id")),
    Column("permission_id", ForeignKey("permissions.id"))
)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    permissions = relationship("Permission", secondary=role_permission)

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)  # Ex: "read:all_passwords"
```

2. **Atualize `bin/backend/auth/jwt.py`:**  
```python
def create_access_token(data: dict, role: str = "user"):
    data.update({"role": role})  # Adiciona role ao token
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
```

3. **Crie um verificador de permissões em `bin/backend/auth/rbac.py`:**  
```python
from fastapi import HTTPException, Depends

def check_permission(required_permission: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    user_role = payload.get("role")
    
    # Consulta ao banco para verificar permissões da role
    if not db.query(Role).filter_by(name=user_role).first().permissions:
        raise HTTPException(status_code=403, detail="Acesso negado")
```

4. **Proteja endpoints específicos (ex: em `routers/admin.py`):**  
```python
from ..auth.rbac import check_permission

@router.get("/all-passwords")
async def list_all_passwords(_ = Depends(check_permission("read:all_passwords"))):
    # Lógica para listar todas as senhas (apenas para admin)
```

---

#### **🔍 Como Testar:**  
1. **Crie um usuário admin via terminal:**  
   ```python
   admin_role = Role(name="admin", permissions=[Permission(name="read:all_passwords")])
   db.add(admin_role)
   ```

2. **Gere um token com role `admin`:**  
   ```python
   token = create_access_token({"sub": "admin_id"}, role="admin")
   ```

3. **Acesse endpoints protegidos:**  
   ```bash
   curl -X GET "http://localhost:8000/all-passwords" -H "Authorization: Bearer TOKEN_ADMIN"
   ```

---

#### **✅ Checklist RBAC**  
- [ ] Criar tabelas `roles` e `permissions`.  
- [ ] Atualizar token JWT com `role`.  
- [ ] Implementar `check_permission()`.  
- [ ] Proteger endpoints críticos (ex: `/admin/*`).  

---

### **📌 Passo 8 (Detalhado): Variáveis de Ambiente**  
**Objetivo:**  
Armazenar configurações sensíveis (chaves JWT, credenciais de DB) fora do código, usando `.env`.  

#### **O Que Você Vai Aprender:**  
1. Usar `python-dotenv` para carregar variáveis.  
2. Criar um arquivo `config/settings.py` centralizado.  
3. Proteger dados como `SECRET_KEY` e `DB_URL`.  

#### **Implementação:**  
1. **Instale a dependência:**  
   ```bash
   pip install python-dotenv
   ```

2. **Crie `.env` na raiz:**  
   ```ini
   # .env
   SECRET_KEY="sua-chave-secreta-gerada-com-openssl-rand-hex-32"
   DB_URL="sqlite:///instance/database.db"
   ```

3. **Configure `config/settings.py`:**  
   ```python
   from pydantic import BaseSettings
   from pathlib import Path

   class Settings(BaseSettings):
       secret_key: str
       db_url: str

       class Config:
           env_file = Path(__file__).parent.parent / ".env"

   settings = Settings()
   ```

4. **Use no código (ex: `jwt.py`):**  
   ```python
   from config.settings import settings

   SECRET_KEY = settings.secret_key  # ← Agora seguro!
   ```

---

### **🔒 Passo 9: Criptografia Básica com AES-256**  
**Objetivo:** Implementar criptografia **no backend** para proteger as senhas antes de armazená-las no banco de dados.  

---

#### **📌 O Que Você Precisa Aprender/Fazer:**  
1. **Biblioteca `cryptography`**:  
   - Usar AES-256 em modo GCM (Galois/Counter Mode) para **confidencialidade + autenticação**.  
   - Gerar IVs (*Initialization Vectors*) únicos para cada operação.  

2. **Integração com o Banco de Dados**:  
   - Criptografar senhas antes de salvar no SQLite.  
   - Descriptografar apenas quando necessário (ex: quando o usuário solicitar).  

3. **Segurança**:  
   - A chave AES deve vir de variáveis de ambiente (Passo 8).  

---

#### **📝 Implementação Passo a Passo**  

1. **Instale a biblioteca**:  
   ```bash
   pip install cryptography
   ```

2. **Crie `bin/backend/encryption/aes.py`**:  
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from config.settings import settings  # Chave vem do .env

def encrypt_password(password: str, key: bytes) -> tuple[bytes, bytes, bytes]:
    # Gera um IV único (16 bytes)
    iv = os.urandom(16)
    # Configura o cifrador AES-256-GCM
    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(password.encode()) + encryptor.finalize()
    return (encrypted, iv, encryptor.tag)  # Tag para autenticação

def decrypt_password(encrypted: bytes, key: bytes, iv: bytes, tag: bytes) -> str:
    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    return (decryptor.update(encrypted) + decryptor.finalize()).decode()
```

3. **Modifique o repositório do banco (`bin/backend/db/repositories.py`)** para usar criptografia:  
```python
from ..encryption.aes import encrypt_password, decrypt_password

class PasswordRepository:
    def add_password(self, user_id: int, service: str, password: str):
        encrypted, iv, tag = encrypt_password(password, settings.AES_KEY)
        # Armazena IV + tag junto com os dados!
        db_entry = PasswordEntry(
            service=service,
            encrypted_password=encrypted,
            iv=iv,
            tag=tag,
            user_id=user_id
        )
        self.db.add(db_entry)
```

4. **Adicione a chave AES no `.env`**:  
   ```ini
   AES_KEY="sua-chave-aes-32-bytes"  # Gerada com: openssl rand -hex 32
   ```

---

#### **🔍 Como Testar:**  
1. **Criptografe uma senha manualmente**:  
   ```python
   from bin.backend.encryption.aes import encrypt_password, decrypt_password
   encrypted, iv, tag = encrypt_password("senha_secreta", settings.AES_KEY)
   print(decrypt_password(encrypted, settings.AES_KEY, iv, tag))  # Deve retornar "senha_secreta"
   ```

2. **Verifique no banco de dados**:  
   - As senhas devem aparecer como dados binários ilegíveis.  

---

#### **⚠️ Boas Práticas:**  
- **Nunca reuse IVs**: Sempre gere um novo IV para cada senha.  
- **Proteja a chave AES**: Armazene-a **apenas** em variáveis de ambiente.  

---

### **🔐 Passo 10: Autenticação Robustecida com Argon2 e JWT**  
**Objetivo:** Substituir o hash SHA-256 provisório por **Argon2** (padrão atual para senhas) e implementar autenticação stateless com JWT.

---

#### **📌 O Que Você Vai Implementar:**
1. **Argon2** (via `passlib`):
   - Derivação segura de chaves com salt automático
   - Proteção contra brute-force (parâmetros de custo ajustáveis)

2. **JWT** (JSON Web Tokens):
   - Tokens assinados com HS256
   - Claims básicas (sub, exp, role)

3. **Integração com FastAPI**:
   - Dependency Injection para rotas protegidas
   - Tratamento de erros personalizado

---

#### **📝 Implementação Detalhada**

1. **Instale as dependências**:
```bash
pip install python-jose[cryptography] passlib
```

2. **Configure o serviço de autenticação (`bin/backend/auth/service.py`)**:
```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config.settings import settings

# Configuração do Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)

def get_password_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)

# Configuração JWT
def create_access_token(user_id: str) -> str:
    expires = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {"sub": user_id, "exp": expires}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
```

3. **Atualize o endpoint de login (`bin/interfaces/web/routers/auth.py`)**:
```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login")
async def login(username: str, password: str):
    user = authenticate_user(username, password)  # Sua função existente
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
```

4. **Proteja suas rotas**:
```python
@router.get("/users/me")
async def read_user_me(current_user: str = Depends(get_current_user)):
    return {"user_id": current_user}
```

---

#### **🔍 Testando a Implementação**
1. **Gere um hash de senha**:
```python
print(get_password_hash("sua_senha")) 
# Exemplo: $argon2id$v=19$m=65536,t=3,p=4$B1O9sLUT9k/KFivQ$ND83...
```

2. **Teste o fluxo completo**:
```bash
curl -X POST "http://localhost:8000/login" \
-H "Content-Type: application/json" \
-d '{"username":"seu_user","password":"sua_senha"}'
```

3. **Acesse rota protegida**:
```bash
curl "http://localhost:8000/users/me" \
-H "Authorization: Bearer SEU_TOKEN_JWT"
```

---

#### **⚙️ Configurações Recomendadas no `.env`**
```ini
# Argon2 Parameters (opcional)
ARGON2_TIME_COST=3
ARGON2_MEMORY_COST=65536
ARGON2_PARALLELISM=4
ARGON2_HASH_LEN=32
ARGON2_SALT_LEN=16

# JWT Configuration
SECRET_KEY="sua-chave-secreta-32-bytes"  # openssl rand -hex 32
JWT_EXPIRE_MINUTES=30
```

---

### **🔒 Passo 11: Configurar HTTPS e Middlewares de Segurança**  
**Objetivo:** Garantir que todas as comunicações com sua API sejam criptografadas e adicionar proteções extras contra ataques comuns.

---

#### **📌 O Que Você Vai Implementar:**  
1. **HTTPS Local** (para desenvolvimento):  
   - Gerar certificado SSL com `mkcert`  
   - Configurar Uvicorn/FastAPI para usar HTTPS  

2. **Middlewares Essenciais:**  
   - `HSTS` (HTTP Strict Transport Security)  
   - `CSP` (Content Security Policy) básico  
   - `Rate Limiting` (proteção contra brute force)  

3. **Headers de Segurança:**  
   - Desativar sniffing de MIME type  
   - Prevenir clickjacking  

---

#### **📝 Implementação Passo a Passo**

### **1. HTTPS Local com mkcert**  
**Instale o mkcert** (uma única vez no seu sistema):  
```bash
# No Linux:
sudo apt install libnss3-tools mkcert  # Ou equivalente para seu distro

# No macOS:
brew install mkcert

# No Windows (PowerShell como Admin):
choco install mkcert
```

**Gere e instale certificados:**  
```bash
mkcert -install  # Instala a CA local
mkcert localhost 127.0.0.1 ::1  # Cria certificados para localhost
```

**Configure o FastAPI (`bin/interfaces/web/app.py`):**  
```python
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# ... (seus routers e lógica)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="./localhost-key.pem",
        ssl_certfile="./localhost.pem"
    )
```

---

### **2. Middlewares de Segurança**  
**Adicione em `bin/interfaces/web/middleware/security.py`:**  
```python
from fastapi import Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

def add_security_middlewares(app):
    # Middleware 1: Forçar HTTPS
    app.add_middleware(HTTPSRedirectMiddleware)

    # Middleware 2: Headers de segurança
    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response
```

**Registre os middlewares no `app.py`:**  
```python
from .middleware.security import add_security_middlewares

app = FastAPI()
add_security_middlewares(app)
```

---

### **3. Rate Limiting**  
**Instale a dependência:**  
```bash
pip install slowapi
```

**Configure em `bin/interfaces/web/middleware/rate_limiter.py`:**  
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
default_limits = ["5 per minute"]  # Limite padrão para todas as rotas

def init_rate_limiter(app):
    app.state.limiter = limiter
    app.add_exception_handler(429, lambda _, __: HTTPException(429, "Too Many Requests"))
```

**Proteja endpoints sensíveis:**  
```python
from ..middleware.rate_limiter import limiter

@router.post("/login")
@limiter.limit("3/minute")
async def login(request: Request, username: str, password: str):
    # ... sua lógica
```

---

#### **🔍 Como Testar:**  
1. **Verifique HTTPS:**  
   ```bash
   curl -k https://localhost:8000  # -k ignora verificação de cert (apenas para dev)
   ```

2. **Verifique headers:**  
   ```bash
   curl -I https://localhost:8000
   ```
   Deve retornar:  
   ```
   Strict-Transport-Security: max-age=63072000; includeSubDomains
   X-Content-Type-Options: nosniff
   ```

3. **Teste Rate Limiting:**  
   ```bash
   for i in {1..6}; do curl -s -o /dev/null -w "%{http_code}\n" https://localhost:8000/login; done
   ```
   - Os 5 primeiros retornam 200, o 6º deve retornar 429.

---

### **⚠️ Atenção para Produção**  
- Substitua os certificados auto-assinados por certificados reais (Let's Encrypt)  
- Ajuste os limites do rate limiting conforme seu uso real  

---

### **🔹 Passo 12: JavaScript Básico para Integração Frontend**  
**Objetivo:** Criar a comunicação básica entre a extensão Chrome e o backend FastAPI usando JavaScript puro, conforme definido na Fase 4.

---

#### **📌 Implementação de Acordo com o Roadmap:**
1. **Manipulação DOM**  
   - Criar elementos HTML dinâmicos para exibir senhas  
   - Capturar inputs do usuário  

2. **Chamadas HTTP com `fetch()`**  
   - Consumir os endpoints do FastAPI  
   - Tratar respostas/erros  

3. **Estrutura Mínima**  
   - Sem bibliotecas externas (vanilla JS)  
   - Foco apenas nos pontos listados no roadmap  

---

#### **📝 Código Essencial (Passo 12 - Fase 4)**

### **1. Estrutura de Arquivos**
```
extension/
├── popup/
│   ├── index.html      # → Manipulação DOM (Passo 12)
│   └── api.js         # → Chamadas fetch() (Passo 12)
```

### **2. HTML Básico (`popup/index.html`)**
```html
<!DOCTYPE html>
<html>
<body>
  <div id="app">
    <h1>Gerenciador de Senhas</h1>
    <div id="password-list"></div>
    <button id="load-btn">Carregar Senhas</button>
  </div>
  <script src="api.js"></script>
</body>
</html>
```

### **3. JavaScript Vanilla (`popup/api.js`)**
```javascript
// Endpoint do FastAPI (Passo 4)
const API_URL = "http://localhost:8000/passwords";

document.getElementById("load-btn").addEventListener("click", async () => {
  try {
    const response = await fetch(API_URL, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        // Token seria obtido via chrome.storage (Passo 13)
      }
    });

    if (!response.ok) throw new Error("Falha ao carregar senhas");

    const passwords = await response.json();
    renderPasswords(passwords);
  } catch (error) {
    console.error("Erro:", error);
  }
});

// Manipulação DOM (Passo 12)
function renderPasswords(passwords) {
  const container = document.getElementById("password-list");
  container.innerHTML = passwords.map(pwd => `
    <div class="password-item">
      <span>${pwd.service}:</span>
      <span>${"*".repeat(pwd.password.length)}</span>
    </div>
  `).join("");
}
```

---

#### **🔍 Testando o Passo 12:**
1. **No Frontend:**
   - O botão "Carregar Senhas" faz uma chamada GET para `/passwords`
   - Exibe os dados recebidos sem formatação complexa

2. **No Backend (FastAPI - Passo 4):**
   - Certifique-se de ter a rota:
     ```python
     @app.get("/passwords")
     def list_passwords():
         return [
             {"service": "Gmail", "password": "*****"},
             {"service": "GitHub", "password": "*****"}
         ]
     ```

---

### **🔹 Passo 13: Chrome API para Armazenamento Seguro**  
**Objetivo:** Implementar o armazenamento local seguro de tokens JWT usando a Chrome API, conforme definido na Fase 4 do roadmap.

---

#### **📌 Implementação Alinhada ao Roadmap:**  
1. **`chrome.storage.local`**  
   - Armazenar tokens JWT com expiração  
   - Isolamento por domínio (opcional)  

2. **Manifest V3**  
   - Atualizar permissões necessárias  

3. **Integração com o Frontend Existente**  
   - Acoplamento com o código do Passo 12  

---

#### **📝 Código Essencial (Passo 13 - Fase 4)**  

### **1. Atualize o Manifest (`manifest.json`)**
```json
{
  "manifest_version": 3,
  "permissions": [
    "storage"  // Necessário para chrome.storage.local
  ]
}
```

### **2. Modifique o JavaScript (`popup/api.js`)**
```javascript
// Armazena token após login
async function storeToken(token) {
  await chrome.storage.local.set({ 
    jwt: token,
    expires: Date.now() + 1800000 // 30 minutos
  });
}

// Recupera token válido
async function getValidToken() {
  const { jwt, expires } = await chrome.storage.local.get(["jwt", "expires"]);
  return (expires > Date.now()) ? jwt : null;
}

// Exemplo de uso no login
document.getElementById("login-btn").addEventListener("click", async () => {
  const token = await authenticateUser(); // Sua função do Passo 12
  await storeToken(token);
});
```

### **3. Atualize as Chamadas API**
```javascript
async function fetchPasswords() {
  const token = await getValidToken();
  if (!token) return;

  const response = await fetch(API_URL, {
    headers: {
      "Authorization": `Bearer ${token}`  // Passo 14 usará criptografia
    }
  });
  // ... resto do código
}
```

---

#### **🔍 Testando o Passo 13:**  
1. **Inspecione o Armazenamento:**  
   - Acesse `chrome://extensions`  
   - Clique em "Service Worker" na sua extensão  
   - Execute `chrome.storage.local.get(console.log)` no console  

2. **Fluxo Completo:**  
   - Login → Armazena token → Recupera token → Faz requisição autenticada  

---

#### **⚠️ Limitações (Serão Resolvidas nos Próximos Passos):**  
- **Sem Criptografia:** O token é armazenado em claro (será tratado no Passo 14)  
- **Sem RBAC:** Controle básico de acesso (será tratado no Passo 7 quando migrar para JWT)  

---

### **🔒 Passo 14: Comunicação Segura entre Frontend e Backend**  
**Objetivo:** Implementar criptografia AES-256 no frontend para proteger senhas antes de enviá-las ao backend, conforme previsto na Fase 4 do roadmap.

---

#### **📌 Implementação Alinhada ao Roadmap**  
1. **Criptografia no Cliente**  
   - Usar a mesma chave AES do backend (Passo 9)  
   - IVs únicos para cada operação  

2. **Integração com FastAPI**  
   - Manter compatibilidade com a descriptografia do backend  

3. **Sem Bibliotecas Externas**  
   - Usar Web Crypto API (nativa nos navegadores)  

---

#### **📝 Código Essencial (Passo 14 - Fase 4)**  

### **1. Frontend: Criptografia AES-GCM (`popup/crypto.js`)**
```javascript
// Configuração compatível com o Python (Passo 9)
async function encryptData(data, key) {
  const iv = crypto.getRandomValues(new Uint8Array(12)); // 96 bits
  const encoded = new TextEncoder().encode(data);
  
  const encrypted = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    encoded
  );

  return {
    ciphertext: Array.from(new Uint8Array(encrypted)),
    iv: Array.from(iv)
  };
}

// Chave deve ser a mesma do backend (Passo 9)
async function getEncryptionKey() {
  const key = await fetch('/api/encryption-key'); // Endpoint protegido
  return crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(key),
    { name: "AES-GCM" },
    false,
    ["encrypt", "decrypt"]
  );
}
```

### **2. Adaptação no Backend (`backend/routes.py`)**
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

@app.post("/store-password")
async def store_password(enc_data: schemas.EncryptedData):
    # Descriptografia compatível com frontend
    cipher = Cipher(
        algorithms.AES(settings.AES_KEY),
        modes.GCM(enc_data.iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    password = decryptor.update(enc_data.ciphertext) + decryptor.finalize()
    # ... armazene no banco
```

### **3. Chamada Segura do Frontend (`popup/api.js`)**
```javascript
document.getElementById("save-btn").addEventListener("click", async () => {
  const key = await getEncryptionKey();
  const encrypted = await encryptData("minhaSenha123", key);
  
  fetch("/store-password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(encrypted)
  });
});
```

---

#### **🔍 Testando a Implementação**  
1. **Verifique o Tráfego:**  
   - Use o DevTools (F12) → Network  
   - Confira se as senhas estão criptografadas nas requisições  

2. **Valide no Backend:**  
   - Debug a descriptografia no endpoint `/store-password`  

---

#### **⚠️ Limitações (Serão Resolvidas no Passo 15)**  
- **Chave Fixa:** Atualmente compartilhada em texto (será substituída por derivação via Argon2 no cliente)  
- **Performance:** WebAssembly será usado para operações pesadas  

---

### **⚙️ Passo 15: WebAssembly (WASM) para Derivação de Chaves no Cliente**  
**Objetivo:** Implementar derivação segura de chaves no frontend usando Argon2 via WASM, conforme previsto na Fase 5 do roadmap.

---

#### **📌 Implementação Alinhada ao Roadmap**  
1. **Argon2 no Cliente**  
   - Substitui a chave AES fixa do Passo 14  
   - Deriva chaves da senha mestra sem expô-la  

2. **Compilação para WASM**  
   - Uso do `argon2-wasm` (biblioteca pré-compilada)  

3. **Integração Segura**  
   - Chave derivada nunca deixa o navegador  

---

#### **📝 Código Essencial (Passo 15 - Fase 5)**  

### **1. Estrutura de Arquivos**
```
extension/
├── lib/
│   └── argon2.wasm    # Binário compilado
└── popup/
    ├── wasm-loader.js # Carregador WASM
    └── crypto.js      # Adaptado do Passo 14
```

### **2. Carregador WASM (`popup/wasm-loader.js`)**
```javascript
let argon2;
async function loadWASM() {
  const response = await fetch('../lib/argon2.wasm');
  const wasm = await WebAssembly.instantiateStreaming(response);
  argon2 = wasm.instance.exports;
}

// Deriva chave com os mesmos parâmetros do backend (Passo 10)
async function deriveKey(password, salt) {
  await loadWASM();
  const key = argon2.argon2_hash(
    password, 
    salt,
    3,    // iterations (time_cost)
    65536 // memory (memory_cost)
  );
  return new Uint8Array(key);
}
```

### **3. Adaptação da Criptografia (`popup/crypto.js`)**
```javascript
async function encryptPassword(password, masterPassword) {
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const keyMaterial = await deriveKey(masterPassword, salt);
  
  // Usa Web Crypto API como no Passo 14
  const key = await crypto.subtle.importKey(
    "raw", keyMaterial, 
    { name: "AES-GCM" }, false, ["encrypt"]
  );

  const encrypted = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv: salt.slice(0, 12) }, // 96 bits
    key,
    new TextEncoder().encode(password)
  );

  return {
    ciphertext: Array.from(new Uint8Array(encrypted)),
    salt: Array.from(salt)
  };
}
```

### **4. Backend Compatível (`backend/auth.py`)**
```python
# Verifica se o salt e hash coincidem
def verify_password(stored_salt: bytes, stored_hash: bytes, password: str):
    derived_key = argon2.hash(password, salt=stored_salt)
    return secrets.compare_digest(derived_key, stored_hash)
```

---

#### **🔍 Testando a Implementação**  
1. **Debug do WASM:**  
   ```javascript
   console.log(await deriveKey("senhaForte", new Uint8Array(16)));
   // Deve retornar 32 bytes (256 bits)
   ```

2. **Fluxo Completo:**  
   - Frontend: Deriva chave → Criptografa senha → Envia para backend  
   - Backend: Valida com mesma configuração Argon2  

---

#### **⚠️ Boas Práticas**  
- **Parâmetros Iguais:** Time/Memory cost devem ser idênticos no front/back  
- **Otimização:** Pré-carregar WASM no Service Worker  

---
### **🔐 Passo 16: Migrar para SQLCipher (Criptografia At-Rest)**  
**Objetivo:** Substituir o SQLite padrão por SQLCipher para criptografia completa do banco de dados, conforme previsto na Fase 5 do roadmap.

---

#### **📌 Implementação Alinhada ao Roadmap**  
1. **SQLCipher vs SQLite**  
   - Criptografia transparente AES-256 do arquivo completo  
   - Todos os dados (incluindo metadados) são protegidos  

2. **Configuração com SQLAlchemy**  
   - Uso do driver `pysqlcipher3`  
   - Chave de criptografia via variáveis de ambiente  

3. **Migração de Dados**  
   - Processo para converter bancos existentes  

---

#### **📝 Implementação Passo a Passo**  

### **1. Instalação das Dependências**
```bash
pip install pysqlcipher3-binary cryptography
```

### **2. Atualização do Ambiente (`config/settings.py`)**
```python
class Settings(BaseSettings):
    DB_KEY: str  # Chave de 32 bytes (armazenada no .env)
    DB_PATH: str = "instance/database.db"
    
    class Config:
        env_file = ".env"
```

### **3. Configuração do Banco (`backend/db/__init__.py`)**
```python
from sqlalchemy import create_engine
from config.settings import settings

# Formato: sqlite+pysqlcipher://:senha@/caminho/do/banco.db
engine = create_engine(
    f"sqlite+pysqlcipher://:{settings.DB_KEY}@/{settings.DB_PATH}",
    connect_args={
        "kdf_iter": 64000,  # Iterações para derivação de chave
        "cipher_page_size": 1024
    }
)
```

### **4. Migração de Dados Existente**
```bash
# 1. Exporte os dados do SQLite original
sqlite3 instance/database.db .dump > dump.sql

# 2. Crie novo banco com SQLCipher
sqlcipher instance/encrypted.db
> PRAGMA key='sua-chave-secreta';
> BEGIN;
> $(cat dump.sql)
> COMMIT;
```

### **5. Verificação da Criptografia**
```python
# Tente abrir sem a chave (deve falhar)
try:
    engine = create_engine("sqlite:///instance/encrypted.db")
    engine.connect()  # ← Isso deve gerar um erro
except Exception as e:
    print("✅ Banco corretamente criptografado")
```

---

#### **🔍 Testando a Implementação**  
1. **Verifique o Arquivo do Banco:**  
   - Tente abrir `encrypted.db` em um editor de texto  
   - Todos os dados devem aparecer como lixo binário  

2. **Teste de Performance:**  
   - Compare queries com/sem criptografia  
   - Ajuste `kdf_iter` conforme necessário  

---

#### **⚠️ Boas Práticas**  
- **Backup da Chave:** Armazene em um gerenciador de segredos (ex: HashiCorp Vault)  
- **Rotação de Chaves:** Planeje como migrar para novas chaves periodicamente  

---

### **🐳 Passo 17: Dockerizar o Backend e Configurar Nginx**  
**Objetivo:** Criar containers isolados para o backend FastAPI com Nginx como proxy reverso, conforme previsto na Fase 5 do roadmap.

---

#### **📌 Implementação Alinhada ao Roadmap**  
1. **Containerização**  
   - Imagem otimizada para Python + FastAPI  
   - Variáveis de ambiente seguras  

2. **Nginx como Proxy Reverso**  
   - Terminação SSL  
   - Balanceamento de carga (pronto para escala)  

3. **Segurança em Produção**  
   - Non-root containers  
   - Configurações CSP via Nginx  

---

#### **📝 Implementação Passo a Passo**  

### **1. Estrutura de Arquivos**
```
docker/
├── backend/
│   ├── Dockerfile      # Imagem do FastAPI
│   └── entrypoint.sh  # Script de inicialização
├── nginx/
│   ├── nginx.conf     # Configuração do proxy
│   └── ssl/           # Certificados (quando em produção)
docker-compose.yml     # Orquestração
```

### **2. Dockerfile do Backend (`docker/backend/Dockerfile`)**
```dockerfile
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim as runtime

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

# Configurações de segurança
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
```

### **3. Configuração do Nginx (`docker/nginx/nginx.conf`)**
```nginx
worker_processes auto;

events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Configurações de segurança
        add_header Content-Security-Policy "default-src 'self'";
        add_header X-Frame-Options DENY;
    }
}
```

### **4. Docker Compose (`docker-compose.yml`)**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/backend/Dockerfile
    environment:
      - DB_KEY=${DB_KEY}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./instance:/app/instance
    restart: unless-stopped

  nginx:
    image: nginx:1.23-alpine
    ports:
      - "80:80"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
```

### **5. Script de Inicialização (`docker/backend/entrypoint.sh`)**
```bash
#!/bin/sh

# Aguarda o banco estar pronto (se necessário)
while ! python -c "import sqlite3; sqlite3.connect('instance/database.db')" &>/dev/null; do
    sleep 1
done

exec uvicorn main:app --host 0.0.0.0 --port 8000
```

---

#### **🔍 Testando a Implementação**  
1. **Construa e Inicie os Containers**  
   ```bash
   docker-compose up --build
   ```

2. **Verifique o Log do Backend**  
   ```bash
   docker-compose logs backend
   ```

3. **Teste o Proxy**  
   ```bash
   curl http://localhost/api/passwords
   ```

---

#### **⚠️ Boas Práticas para Produção**  
1. **Certificado SSL**  
   - Adicione certificados Let's Encrypt no volume `nginx/ssl/`  
   - Atualize `nginx.conf` para porta 443  

2. **Monitoramento**  
   - Adicione Prometheus + Grafana (passo opcional)  

3. **Segurança**  
   - Utilize `--no-cache` no Docker build  
   - Revise permissões de volumes  

---

### **✅ Próximos Passos (Opcionais):**  
1. **Auto-Preenchimento:** Usar `content_script.js` para preencher senhas em sites.  
2. **Notificações:** Alertar o usuário sobre vazamentos de senhas (usando API como HaveIBeenPwned).  

