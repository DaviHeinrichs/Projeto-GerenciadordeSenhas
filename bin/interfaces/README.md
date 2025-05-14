
### **3. `interfaces/` (Camada de Comunicação)**
**O que é?**  
Tudo que interage com o mundo externo: **API REST (FastAPI)** e **Extensão de Navegador**. Foca em receber/validar inputs e entregar respostas seguras.  

---

#### **A. `web/` (Backend - FastAPI)**  
- **`routers/`**  
  - `auth.py`:  
    - **`POST /login`**: Validar master password + gerar JWT.  
    - **`POST /register`**: Criar usuário com hash da master password (usar Argon2).  
  - `passwords.py`:  
    - **`POST /generate-password`**: Retornar senha aleatória (usar `core/use_cases/generate_password.py`).  
    - **`GET /passwords`**: Listar senhas **criptografadas** (só descriptografar no frontend).  
  - **Validação:** Todos os endpoints devem usar schemas Pydantic para evitar injeção de dados malformados.  

- **`schemas/`**  
  - `auth.py`: Definir `LoginRequest` (ex: `master_password: str` com validação de mínimo 12 caracteres).  
  - `passwords.py`: Criar `PasswordCreateRequest` (ex: `service_name: str`, `tags: List[str]`).  

- **`middleware/`**  
  - **Fase 2:** Adicionar verificação de HTTPS e headers de segurança (CSP, HSTS).  

---

#### **B. `browser_extension/` (Frontend - Chrome Extension)**  
- **`popup/`** (UI MVP)  
  - `ui/index.html`:  
    - Formulário básico: campo para master password + botão de login.  
    - **Segurança:** Desabilitar autocomplete (`autocomplete="off"`).  
  - `ui/main.js`:  
    - Chamar `auth.js` para login e armazenar JWT no `chrome.storage.local`.  
  - `api/auth.js`:  
    - Enviar master password para derivação de chave (WASM na Fase 2).  
    - Gerenciar JWT (enviar em todas as requisições via `Authorization` header).  

- **`background/`**  
  - `api_handler.js`:  
    - Interceptar chamadas HTTP para adicionar JWT + tratar erros (ex: token expirado).  

- **`content_script/`** (Fase 3)  
  - Auto-preenchimento: Identificar campos de senha em páginas e sugerir preenchimento seguro.  

---

**Próximos Passos:**  
1. Criar endpoints básicos no FastAPI (`/login`, `/generate-password`).  
2. Implementar popup HTML/CSS vanilla com comunicação `fetch()` para a API.  
3. Validar todos os inputs com Pydantic (ex: regex para evitar XSS).  
