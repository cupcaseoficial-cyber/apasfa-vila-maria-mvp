# APASFA Vila Maria — MVP móvel

MVP acadêmico para a disciplina **Experiência Prática de Projeto de Software**, com foco em apoio aos cuidados de animais no abrigo APASFA (Vila Maria). O produto simula dois fluxos centrais: prontuários clínicos e controle de estoque de medicamentos/insumos.

## O que foi entregue

- API REST em Python, FastAPI, Pydantic e uvicorn.
- Autenticação demonstrativa com senha submetida apenas por HTTPS em produção, hash Argon2id e token Bearer JWT.
- Endpoints protegidos para listar/consultar/criar animais e listar/criar/ajustar estoque.
- Frontend Angular standalone com tela de entrada, painel de cuidados, alertas, prontuários e estoque.
- Layout mobile-first, foco visível, labels explícitos, `aria-label`, mensagens de erro com `role="alert"` e estados não dependentes somente de cor.
- `.gitignore`, testes básicos do backend e documentação de Git/GitHub.

## Estrutura

```text
apasfa-mvp/
├── backend/
│   ├── app/main.py       # aplicação FastAPI e rotas
│   ├── app/models.py     # contratos Pydantic
│   ├── app/security.py   # Argon2id, JWT e dependência de autenticação
│   ├── app/store.py      # dados simulados em memória
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/app/app.component.*
│   ├── src/app/core/api.service.ts
│   ├── package.json
│   └── angular.json
├── .gitignore
├── plan.md
└── TODO.md
```

## Pré-requisitos

- Python 3.11+ e `pip`.
- Node.js 20+ e npm.
- Angular CLI não precisa ser instalado globalmente: o script usa a dependência local do projeto.

## Executar o backend

```bash
cd backend
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env  # Windows: copy .env.example .env
# Edite .env e troque APASFA_SECRET_KEY/APASFA_DEMO_PASSWORD
uvicorn app.main:app --reload --port 8000
```

API e documentação: `http://127.0.0.1:8000/docs`; saúde: `http://127.0.0.1:8000/api/health`.

Em outro terminal:

```bash
cd frontend
npm install
npm start
```

Abra `http://localhost:4200`. Para o primeiro acesso, use o e-mail configurado em `APASFA_DEMO_EMAIL` e a senha definida em `APASFA_DEMO_PASSWORD`. O armazenamento é em memória: reiniciar a API restaura os dados de exemplo.

## Endpoints principais

| Método | Rota | Finalidade |
|---|---|---|
| GET | `/api/health` | Saúde da aplicação; público |
| POST | `/api/auth/login` | Login demonstrativo |
| GET | `/api/animals` | Lista de prontuários; Bearer obrigatório |
| GET | `/api/animals/{id}` | Detalha prontuário |
| POST | `/api/animals` | Cria animal com validação Pydantic |
| GET | `/api/stock` | Lista medicamentos/insumos |
| POST | `/api/stock` | Cadastra item |
| PATCH | `/api/stock/{id}/adjust` | Entrada/baixa de estoque |

Exemplo de ajuste:

```json
{"quantity_delta": -1, "reason": "Uso no curativo da Luna"}
```

## Segurança — especificação acadêmica

- Senhas nunca são armazenadas em texto limpo; o exemplo usa Argon2id via `argon2-cffi`.
- O segredo JWT deve ser longo, aleatório e injetado por secret manager/variável de ambiente; o valor padrão existe apenas para desenvolvimento.
- Em produção, habilite TLS, use access tokens curtos e refresh tokens revogáveis, rotação de chaves, sessões seguras, RBAC por função, auditoria, rate limiting, backup criptografado e política de retenção.
- CORS está restrito a `http://localhost:4200` no MVP. Não use `allow_origins=["*"]` com credenciais.
- Validação ocorre no servidor com Pydantic; erros não devem revelar stack traces ao usuário.
- Recomendações mapeiam OWASP Top 10: controle de acesso (A01), criptografia (A02), validação e configuração segura (A03/A05), dependências fixadas e atualizadas (A06), logs sem segredos e revisão de código (A09/A08).
- Este repositório não deve receber `.env`, tokens, chaves privadas ou dados pessoais/reais de animais.

## Acessibilidade — WCAG 2.2 AA

O frontend usa contraste de texto principal em nível AA, labels associados a inputs, foco visível, navegação sem depender de hover, `role="alert"` para falhas, linguagem clara, alvos de toque amplos e textos alternativos/`aria-hidden` apenas para ícones decorativos. Antes de uma entrega final, rode Lighthouse/axe, teste somente com teclado, zoom de 200%, leitor de tela e contraste real em dispositivos móveis.

## Sustentabilidade — ODS 15.9

O MVP apoia a meta 15.9 do ODS 15 ao incorporar valores de biodiversidade e proteção da vida terrestre em planejamento local: prontuários ajudam a manter continuidade clínica e o estoque reduz interrupções de tratamento. A próxima versão deve medir indicadores como tratamentos acompanhados, alertas resolvidos, perdas por vencimento e animais com vacinação/reavaliação em dia.

## Limitações e próximos passos

Os dados são simulados em memória e o login é deliberadamente demonstrativo. Para uso real: PostgreSQL com migrações, segregação por abrigo, perfis e permissões, trilha de auditoria, consentimento/privacidade, upload seguro de documentos, notificações, testes E2E, CI/CD e deploy com TLS.

## Testes

```bash
cd backend
source .venv/bin/activate
pytest
```

## Licença acadêmica

Código criado como base educacional. Confirme as regras de licenciamento e autorização de uso de dados/imagens com a APASFA antes de publicação.

## Guia Git e GitHub

### 1. Inicializar o Git localmente

No terminal, dentro da pasta do projeto:

```bash
cd caminho/para/apasfa-mvp
# opcional, se sua identidade ainda não estiver configurada
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@example.com"
git init -b main
git status
git add .
git diff --cached --stat
```

Antes de commitar, confirme que `.env`, `.venv` e `node_modules` não aparecem no staged. Se algum segredo entrou no Git, remova-o do índice e troque o segredo imediatamente; apagar o arquivo depois não remove o histórico.

### 2. Fazer o primeiro commit semântico

O padrão de Conventional Commits usa `tipo(escopo): descrição`. Para este primeiro estado:

```bash
git commit -m "feat: cria MVP móvel da APASFA Vila Maria"
git log --oneline -1
```

Outros exemplos: `fix(api): valida baixa de estoque`, `docs: atualiza guia de instalação`, `test(api): cobre rota de saúde`.

### 3. Criar um repositório público no GitHub

Opção pela interface web:

1. Acesse `https://github.com/new` e entre na sua conta.
2. Em **Repository name**, use `apasfa-vila-maria-mvp`.
3. Escolha **Public**.
4. Não marque “Add a README”, `.gitignore` ou licença, pois estes arquivos já existem localmente.
5. Clique em **Create repository** e copie a URL HTTPS exibida.

### 4. Conectar e subir o código

Substitua `SEU_USUARIO` pelo seu usuário do GitHub:

```bash
git remote add origin https://github.com/SEU_USUARIO/apasfa-vila-maria-mvp.git
git remote -v
git push -u origin main
```

O GitHub pode abrir autenticação pelo navegador ou pedir um token pessoal em vez de senha. Nunca coloque o token na URL nem no README. Depois do push, abra:

```text
https://github.com/SEU_USUARIO/apasfa-vila-maria-mvp
```

Esse é o link que você pode entregar na plataforma da faculdade.

### 5. Conferência final antes da entrega

```bash
git status
git log --oneline --decorate -5
```

Confira no GitHub se aparecem `backend/`, `frontend/`, `README.md`, `.gitignore`, `plan.md` e `TODO.md`, e se não há `.env`, senhas, tokens ou dados reais. Se o professor pedir uma URL exata, copie a URL do navegador do repositório, não a URL do comando local.

## Entrega acadêmica

Projeto desenvolvido para a disciplina Experiência Prática de Projeto de Software.

