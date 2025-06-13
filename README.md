# Projeto Gerenciador de Senhas

  Projeto totalmente open-source que surge da Fatec São Caetano do Sul...
  Criadores: Davi Heinrichs, Gabriel Tagawa, Gerson Hermínio e Walter Neto.
  Objetivo de tornar mais comum o uso de gerenciadores de senha, até para pessoas que não possuem contato com Tecnologias.
  Todos estão convidados a testar e reportar bugs, mas lembre-se, estamos apenas começando...
  Estamos atrás de uma logo para nosso projeto, então se quiser contribuir nesse aspecto também está convidado 😊

  rode o Arquivo main.py presente em "projeto-gerenciadordesenhas/bin/interface/local_interface/" para ter acesso ao programa.

  utilizar o comando "pip install" para baixar:
  - Requests
  - SQLAlchemy
  - PyQt5
  - Cryptography
  
# Tecnologias que foram usadas (Até o momento)

    Backend: Python + SQLAlchemy + Cryptography.

    Segurança: PBKDF2/Argon2 + AES-256 + SHA-256

    Banco de Dados: Totalmente criado com SQLAlchemy, baseado em SQLite



# O que precisa ser feito? 

---

## 🔙 **Backend (FastAPI) - Primeira Fase (MVP)**

| Item | Descrição | Tecnologias/Implementação | Prioridade |
|------|-----------|--------------------------|------------|
| 1. **Rotas Básicas da API** | Endpoints essenciais para MVP. | `POST /generate-password`, `GET /passwords` | Crítica |
| 2. **Validação de Dados** | Schemas para inputs seguros. | Pydantic (`PasswordRequest`) | Crítica |
| 3. **Autenticação Básica** | Login e geração de tokens. | JWT (FastAPI `Depends`) | Crítica |
| 4. **Integração com SQLite3** | Armazenamento inicial (sem criptografia at-rest). | SQLAlchemy | Alta |
| 5. **Logger Simples** | Registro de atividades básicas. | `logging` padrão | Média |

---

## 🖥️ **Extensão de Navegador (MVP)**

| Item | Descrição | Tecnologias/Implementação | Prioridade |
|------|-----------|--------------------------|------------|
| 1. **Popup UI Básica** | Interface mínima para inserir master password. | HTML/CSS vanilla | Crítica |
| 2. **Comunicação com Backend** | Chamadas HTTPS para a API. | `fetch` + JWT | Crítica |
| 3. **Cache Local Simples** | Armazenamento temporário em `chrome.storage`. | Chrome API | Alta |

---

## 🔒 **Segurança (Fase 2 - Pós-MVP)**

| Item | Descrição | Tecnologias/Implementação | Prioridade |
|------|-----------|--------------------------|------------|
| 1. **HTTPS** | Configurar certificado SSL. | Let's Encrypt + Nginx | Crítica |
| 2. **SQLCipher** | Migrar para banco criptografado. | SQLAlchemy + SQLCipher | Crítica |
| 3. **Criptografia AES-256** | Implementar encrypt/decrypt no backend. | `cryptography` (Fernet) | Crítica |
| 4. **Derivação de Chaves** | Master password → chave segura. | Argon2 (`passlib`) | Alta |
| 5. **Rate Limiting** | Prevenir brute-force. | `slowapi` | Alta |

---

## 🖥️ **Extensão (Fase 2 - Melhorias)**

| Item | Descrição | Tecnologias/Implementação | Prioridade |
|------|-----------|--------------------------|------------|
| 1. **Criptografia no Cliente** | Derivação de chaves via WASM. | WebAssembly + Argon2 | Alta |
| 2. **UI Avançada** | Adicionar listagem de senhas. | Svelte/Preact | Média |
| 3. **Content Script** | Auto-preenchimento em formulários. | JavaScript | Baixa |

---

## 🗃️ **Banco de Dados (Fase 3 - Robustez)**

| Item | Descrição | Tecnologias/Implementação | Prioridade |
|------|-----------|--------------------------|------------|
| 1. **Migrations** | Controle de versão do esquema. | Alembic | Média |
| 2. **Backups Automatizados** | Cópias criptografadas. | Scripts Python + GPG | Média |

---

## 🔒 **Segurança Avançada (Fase 3)**

| Item | Descrição | Tecnologias/Implementação | Prioridade |
|------|-----------|--------------------------|------------|
| 1. **2FA (TOTP)** | Autenticação em dois fatores. | `pyotp` | Alta |
| 2. **Secure Headers** | Proteção contra XSS/CSRF. | CSP, HSTS | Alta |
| 3. **Auditoria** | Logs detalhados de acesso. | SQLAlchemy Events | Média |

---

## 🚀 **Deploy & Otimização (Fase Final)**

| Item | Descrição | Tecnologias/Implementação | Prioridade |
|------|-----------|--------------------------|------------|
| 1. **Containerização** | Empacotamento do backend. | Docker | Alta |
| 2. **Proxy Reverso** | Gerenciamento de tráfego. | Nginx | Alta |
| 3. **Monitoramento** | Métricas de performance. | Prometheus + Grafana | Baixa |

---

## ✅ **Checklist por Fases**

### **Fase 1 (MVP)**
- [ ] Backend: Rotas básicas + autenticação JWT + SQLite3.  
- [ ] Extensão: Popup UI + comunicação com API.  
- [ ] Segurança: Validação de dados com Pydantic.  

### **Fase 2 (Segurança e Melhorias)**
- [ ] Migrar para SQLCipher + HTTPS.  
- [ ] Implementar criptografia AES-256 + Argon2.  
- [ ] Extensão: Adicionar WASM para criptografia no cliente.  

### **Fase 3 (Robustez e Escala)**
- [ ] Implementar 2FA + backups automatizados.  
- [ ] Adicionar sistema de auditoria.  
- [ ] Containerizar aplicação com Docker.
  
---
