
### **4. `application/` (Camada de Serviços de Aplicação)**
**O que é?**  
Camada que **orquestra a lógica entre o domínio (`core/`) e as interfaces (`interfaces/`)**, transformando dados e gerenciando transações.  

---

#### **A. `services/`**  
- **`auth_service.py`**  
  - **Responsabilidades:**  
    - Chamar `argon2.py` para derivar a chave da master password.  
    - Usar `jwt.py` para gerar tokens após login válido.  
    - Gerenciar sessões (ex: invalidar tokens em caso de logout).  
  - **Segurança:**  
    - Implementar tempo de expiração curto para tokens (15-30 minutos).  
    - Logar tentativas falhas de login (para detectar brute force).  

- **`password_service.py`**  
  - **Responsabilidades:**  
    - Chamar `generate_password.py` (`core/`) para criar senhas aleatórias.  
    - Usar `aes.py` (`infrastructure/`) para criptografar/descriptografar senhas antes de salvar no banco.  
    - Validar permissões antes de operações (ex: usuário só acessa suas próprias senhas).  
  - **Fluxo Crítico (MVP):**  
    1. Receber senha descriptografada do frontend.  
    2. Criptografar com AES-256 + chave derivada (Argon2).  
    3. Salvar no banco via `db/repositories.py`.  

---

#### **B. `dto/` (Data Transfer Objects)**  
- **`auth_dto.py`**  
  - Definir objetos para transferência segura:  
    - `LoginDTO`: `{ master_password: str }` (nunca logar ou retornar isso em claro).  
    - `TokenDTO`: `{ access_token: str, expires_in: int }`.  

- **`password_dto.py`**  
  - `PasswordCreateDTO`: `{ service_name: str, encrypted_password: str, iv: str }` (dados já criptografados pelo frontend na Fase 2).  
  - **MVP:** Frontend envia senha em claro (criptografada pelo backend).  

---

**Próximos Passos:**  
1. Implementar `auth_service.py` para integrar Argon2 + JWT.  
2. Criar `PasswordService` com métodos `encrypt_password()` e `decrypt_password()`.  
3. Definir DTOs para garantir que nenhum dado sensível vaze em logs/respostas.  
