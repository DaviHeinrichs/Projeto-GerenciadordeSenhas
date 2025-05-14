
### **6. `tests/` (Testes Automatizados)**  
**O que é?**  
Garante que cada componente funcione conforme o esperado, especialmente **fluxos críticos de segurança**.  

---

#### **Estrutura e Prioridades:**  
- **`unit/`**  
  - `test_password_generation.py`:  
    - Verificar se senhas geradas atendem aos critérios (ex: 12 caracteres, pelo menos 1 símbolo).  
  - `test_encryption.py`:  
    - Garantir que AES-256 + Argon2 funcionem corretamente (ex: `decrypt(encrypt(data)) == data`).  

- **`integration/`**  
  - `test_auth_flow.py`:  
    - Simular login completo (master password → JWT → acesso a endpoint protegido).  
  - `test_api_endpoints.py`:  
    - Validar respostas da API (ex: `GET /passwords` retorna 403 sem token).  

- **Fase 2+:**  
  - Testes de performance para Argon2 (ex: derivação deve levar ≥ 500ms).  
  - Testes de segurança (ex: SQL injection nos endpoints).  

---

**Próximos Passos:**  
1. Criar testes unitários para geração de senhas e criptografia.  
2. Testar autenticação com tokens JWT.  
