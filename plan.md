# Plano de implementação — APASFA Vila Maria

## Escopo
MVP acadêmico mobile-first para apoiar o abrigo APASFA (Vila Maria) no controle clínico de animais e estoque de medicamentos/insumos. O backend usa FastAPI com armazenamento em memória propositalmente simulado; o frontend usa Angular standalone com dados carregados por HTTP.

## Arquitetura
- `backend/`: API REST Python, validação Pydantic, autenticação demonstrativa com Bearer token e hash Argon2id para senhas.
- `frontend/`: Angular/TypeScript, componentes standalone, navegação por abas, layout responsivo e mensagens de estado.
- Comunicação local: Angular em `4200` chama FastAPI em `8000` por `/api`; durante o desenvolvimento, o proxy Angular redireciona para o backend.

## Design
- **Movimentos considerados:** Editorial de serviço público (0,04), Neo-humanista clínico (0,07), Painel utilitário acolhedor (0,05).
- **Escolha:** Painel utilitário acolhedor.
- **Princípios:** informação prioritária, leitura rápida em campo, linguagem humana e estados visuais claros.
- **Cores:** azul-petróleo para confiança, verde para cuidado e âmbar para alertas; contraste verificado para textos principais em WCAG AA.
- **Layout:** cabeçalho compacto, navegação inferior/por cartões e listas empilhadas para telas estreitas.
- **Assinaturas:** marca em formato de selo, chips de status e cartões com borda lateral de prioridade.
- **Interação:** ações explícitas, confirmação por texto e foco visível; sem depender apenas de cor.
- **Tipografia:** sistema sans-serif, títulos fortes e corpo com altura de linha confortável.
- **Voz:** direta, respeitosa e orientada ao cuidado. Ex.: “Cuidados de hoje” e “Repor antes de acabar”.
- **Essência:** uma visão operacional simples para transformar registros em cuidado contínuo; cuidadosa, prática e comunitária.

## Segurança e conformidade
A especificação documenta Argon2id, tokens Bearer, validação de entrada, CORS restrito, não exposição de segredos, logs sem credenciais, menor privilégio e recomendações alinhadas ao OWASP Top 10. O MVP não deve ser usado em produção sem banco persistente, TLS, gestão real de sessões, auditoria e revisão de privacidade.

## Sustentabilidade
A documentação relaciona o produto ao ODS 15, meta 15.9, ao apoiar diretamente o bem-estar e a proteção de animais terrestres por meio de prontuários, alertas clínicos e disponibilidade de insumos.
