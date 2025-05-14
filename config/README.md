
### **5. `config/` (Configurações Globais)**  
**O que é?**  
Centraliza todas as configurações do sistema, desde variáveis de ambiente até políticas de segurança.  

---

#### **Arquivos Principais:**  
- **`settings.py`**  
  - **Variáveis de Ambiente:**  
    - `SQLITE_DB_PATH`: Caminho do banco de dados (substituído por SQLCipher na Fase 2).  
    - `JWT_SECRET_KEY`: Chave assinatura dos tokens (deve ser gerada via `openssl rand -hex 32`).  
    - `ARGON2_PARAMS`: Configurações de custo (time_cost, memory_cost).  

- **`security.py`** (Fase 2+)  
  - **Proteções HTTP:**  
    - CSP (Content Security Policy): Bloquear scripts inline.  
    - HSTS: Forçar HTTPS.  
  - **Criptografia:**  
    - Salt padrão para Argon2 (gerado uma vez e armazenado com segurança).  

- **`policies/`** (Fase 3)  
  - `admin.yaml`: Definir permissões de administrador (ex: `delete_user: true`).  
  - `user.yaml`: Permissões básicas (ex: `max_passwords: 100`).  
