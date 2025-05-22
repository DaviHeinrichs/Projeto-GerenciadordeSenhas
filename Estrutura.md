``` 
├── core/                           # Domínio puro
│   ├── entities/                   # Entidades
│   │   ├── user.py                # User + Roles
│   │   └── password_vault.py      # Senhas criptografadas
│   │
│   ├── repositories/              # Interfaces
│   │   ├── user_repository.py     # Operações de usuário
│   │   ├── role_repository.py     # RBAC: Gerenciamento de roles
│   │   └── password_repository.py # Senhas
│   │
│   ├── use_cases/                  # Lógica de negócio
│   │   ├── auth/                  # Autenticação
│   │   │   ├── login.py          # Fluxo de login
│   │   │   └── register.py       # Registro com role padrão
│   │   │
│   │   └── rbac/                 # RBAC
│   │       ├── assign_role.py    # Atribuir role a usuário
│   │       ├── check_permission.py # Verificar permissões
│   │       └── create_policy.py  # Definir políticas
│   │
│   └── exceptions/
│       ├── auth_errors.py        # Erros de autenticação
│       └── rbac_errors.py        # Erros de permissão
│
├── infrastructure/
│   ├── db/
│   │   ├── models/               # Modelos SQLAlchemy
│   │   │   ├── user.py          # Tabela User (com roles)
│   │   │   ├── role.py          # Tabela Role
│   │   │   └── permission.py    # Tabela Permission
│   │   │
│   │   └── repositories/        # Implementações
│   │       ├── user_repository_impl.py
│   │       └── role_repository_impl.py
│   │
│   ├── auth/                     # Autenticação
│   │   ├── jwt.py               # Geração/validação de tokens (com claims RBAC)
│   │   └── password_hasher.py   # Argon2
│   │
│   └── rbac/                     # Implementação RBAC
│       ├── policy_loader.py     # Carrega políticas de acesso (ex: YAML/JSON)
│       └── permission_checker.py # Verifica permissões em tempo real
│
├── interfaces/
│   ├── web/                      # FastAPI
│   │   ├── routers/
│   │   │   ├── auth.py          # Rotas de login/registro
│   │   │   └── admin.py         # Rotas administrativas (RBAC)
│   │   │
│   │   └── schemas/
│   │       ├── auth.py          # Schemas de autenticação
│   │       └── rbac.py          # Schemas para roles/permissões
│   │
│   └── browser_extension/        # Frontend
│       ├── popup/
│       │   ├── auth/            # UI de login/registro
│       │   └── admin/           # UI para admin (gerenciar roles)
│       └── background/
│           └── rbac.js          # Verificação de permissões no cliente
│
├── application/
│   ├── services/
│   │   ├── auth_service.py      # Serviço de autenticação
│   │   └── rbac_service.py      # Serviço RBAC (atribuir roles, etc.)
│   │
│   └── dto/
│       ├── auth.py              # DTOs de autenticação
│       └── rbac.py             # DTOs para RBAC
│
├── config/
│   ├── rbac_policies/           # Definições de políticas
│   │   ├── admin.yaml          # Permissões de admin
│   │   └── user.yaml           # Permissões de usuário comum
│   │
│   └── security.py             # Configurações de RBAC (ex: role padrão)
│
└── tests/
    ├── rbac/                   # Testes de RBAC
    │   ├── test_roles.py
    │   └── test_permissions.py
    └── ...                     # Demais testes