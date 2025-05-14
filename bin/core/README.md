
### **1. `core/` (Domínio e Regras de Negócio)**
**O que é?**  
O coração do sistema, onde ficam as regras de negócio e entidades fundamentais, **independentes de tecnologias** (como FastAPI ou SQLite).  

**Estrutura e Tarefas:**  
- **`entities/`**  
  - `user.py`: Definir atributos do usuário (ex: `id`, `master_password_hash`, `2FA_secret`).  
  - `password_entry.py`: Modelar como uma senha criptografada será representada (ex: `encrypted_data`, `iv`, `metadata_tags`).  

- **`use_cases/`**  
  - `generate_password.py`: Lógica para criar senhas aleatórias (comprimento, caracteres especiais).  
  - `password_strength.py`: Regras para validar força da senha (ex: zxcvbn).  
  - `encryption_flow.py`: Definir como a chave derivada da master password será usada para criptografar/descriptografar.  

- **`exceptions/`**  
  - `auth_exceptions.py`: Erros como `InvalidMasterPassword` ou `2FARequired`.  
  - `crypto_exceptions.py`: Erros como `DecryptionFailed` ou `WeakKeyDerivation`.  

