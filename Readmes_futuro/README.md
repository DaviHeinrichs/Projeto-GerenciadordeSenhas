
### **2. `backend/` (Implementações Técnicas)**
**O que é?**  
Camada que implementa as tecnologias concretas (banco de dados, criptografia, autenticação), **dependente de bibliotecas específicas** (SQLCipher, FastAPI, Argon2).  

---

#### **Subpastas e Tarefas:**  

#### **A. `db/` (Banco de Dados)**
- **`sqlcipher/`**  
  - `models.py`:  
    - Definir tabelas com SQLAlchemy (ex: `User`, `PasswordEntry`).  
    - **Segurança:** Campos sensíveis devem ser anotados para criptografia (ex: `__encrypted_fields__`).  
  - `repositories.py`:  
    - Implementar operações CRUD **com criptografia transparente** (ex: `save_password()` descriptografa antes de salvar).  
    - **MVP:** Usar SQLite3 simples; migrar para SQLCipher na Fase 2.  

- **`migrations/`** (Fase 3)  
  - Configurar Alembic para versionar esquema do banco.  
  - Garantir que migrações preservem dados criptografados.  

---

#### **B. `auth/` (Autenticação)**
- **`argon2.py`**  
  - Implementar derivação de chave da master password usando Argon2 (salt + iterações).  
  - **Segurança:** Parâmetros devem ser ajustáveis (ex: `time_cost=3`, `memory_cost=65536`).  

- **`jwt.py`**  
  - Gerar/validar tokens JWT com claims mínimas (ex: `user_id`, `expiry`).  
  - **MVP:** Sem RBAC; adicionar roles na Fase 3.  

- **`totp.py`** (Fase 3)  
  - Gerar códigos TOTP para 2FA usando `pyotp`.  
  - Vincular a dispositivos do usuário.  

---

#### **C. `encryption/` (Criptografia)**
- **`aes.py`**  
  - Implementar `encrypt()`/`decrypt()` com AES-256-GCM (autenticação + confidencialidade).  
  - **Chave:** Receber a chave derivada (Argon2) do `auth/`.  

- **`wasm/`** (Fase 2)  
  - Compilar Argon2 para WebAssembly (evitar enviar master password ao backend).  
  - Gerar bindings JavaScript para uso na extensão.  

---

#### **D. `api/` (FastAPI)**
- **`middleware/`**  
  - `rate_limiter.py`: Limitar tentativas de login (ex: 5 tentativas/minuto).  
  - `https_enforcer.py`: Redirecionar HTTP → HTTPS (Fase 2). 
