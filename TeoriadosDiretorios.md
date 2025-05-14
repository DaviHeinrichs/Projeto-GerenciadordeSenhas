<div align="">
  <pre>

password-manager/
│
├── core/                           # Domínio e regras de negócio
│   ├── entities/                   # Entidades principais
│   │   ├── user.py                # Usuário + Master Password
│   │   └── password_entry.py      # Senha criptografada + metadados
│   │
│   ├── use_cases/                 # Lógica de negócio
│   │   ├── generate_password.py   # Geração de senhas (secrets)
│   │   ├── password_strength.py   # Validação de complexidade
│   │   └── encryption_flow.py     # Fluxo de criptografia (AES-256)
│   │
│   └── exceptions/
│       ├── auth_exceptions.py     # Erros de autenticação
│       └── crypto_exceptions.py  # Erros de criptografia
│
├── infrastructure/                # Implementações concretas
│   ├── db/
│   │   ├── sqlcipher/            # Config SQLCipher
│   │   │   ├── models.py        # Modelos SQLAlchemy
│   │   │   └── repositories.py  # Operações criptografadas
│   │   │
│   │   └── migrations/          # Alembic (Fase 3)
│   │
│   ├── auth/
│   │   ├── argon2.py            # Derivação de chaves
│   │   ├── jwt.py               # Autenticação JWT
│   │   └── totp.py              # 2FA (Fase 3)
│   │
│   └── encryption/
│       ├── aes.py               # AES-256 (cryptography)
│       └── wasm/                # Bindings WebAssembly (Fase 2)
│
├── interfaces/
│   ├── web/                      # FastAPI
│   │   ├── routers/
│   │   │   ├── auth.py         # Autenticação
│   │   │   ├── passwords.py    # CRUD de senhas
│   │   │   └── admin.py        # Rotas administrativas (Fase 3)
│   │   │
│   │   ├── schemas/            # Validação Pydantic
│   │   │   ├── passwords.py
│   │   │   └── auth.py
│   │   │
│   │   └── middleware/         # Segurança
│   │       ├── rate_limiter.py # slowapi
│   │       └── https_enforcer.py
│   │
│   └── browser_extension/       # Frontend Chrome
│       ├── popup/               # UI MVP
│       │   ├── ui/
│       │   │   ├── index.html   # HTML/CSS vanilla
│       │   │   └── main.js     # Lógica básica
│       │   │
│       │   └── api/
│       │       ├── auth.js      # Comunicação JWT
│       │       └── crypto.js   # WASM (Fase 2)
│       │
│       ├── background/          # Service Worker
│       │   └── api_handler.js  # Gerencia chamadas HTTPS
│       │
│       └── content_script/     # Auto-preenchimento (Fase 3)
│
├── application/                 # Serviços de aplicação
│   ├── services/
│   │   ├── password_service.py # Gerencia senhas + criptografia
│   │   └── auth_service.py    # Lógica de autenticação
│   │
│   └── dto/                    # Objetos de transferência
│       ├── password_dto.py
│       └── auth_dto.py
│
├── config/
│   ├── settings.py             # Variáveis de ambiente
│   ├── security.py            # CSP/HSTS (Fase 3)
│   └── policies/              # RBAC (Fase 3)
│
├── tests/
│   ├── unit/
│   │   ├── test_password_generation.py
│   │   └── test_encryption.py
│   │
│   └── integration/
│       ├── test_auth_flow.py
│       └── test_api_endpoints.py
│
├── scripts/                    # Utilitários
│   ├── deploy/                # Configuração HTTPS (Fase 2)
│   ├── backup/               # Backups criptografados (Fase 3)
│   └── wasm_build.sh        # Compilação WASM (Fase 2)
│
├── Dockerfile                 # Containerização (Fase Final)
├── docker-compose.yml        # Nginx + Prometheus (Fase Final)
└── README.md                # Documentação do projeto
    </pre>
</div>
