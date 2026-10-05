# Auditoria do app_vulneravel.py feita com ajuda de IA

| # | OWASP 2025 | Falha | Impacto | Correção |
|---|------------|-------|---------|----------|
| 1 | A05 Injection | SQL concatenado em `/api/usuarios/buscar` | Leitura e alteração de todo o banco | Query parametrizada: `LIKE %s` com `(f"%{nome}%",)` |
| 2 | A05 Injection | XSS refletido em `/perfil` | Execução de JS no navegador da vítima, roubo de sessão | `markupsafe.escape` e CSP `default-src 'self'` |
| 3 | A01 Broken Access Control (AUSÊNCIA) | `DELETE /api/usuarios/<id>` sem autenticação nem autorização | Qualquer pessoa apaga qualquer usuário | `X-API-Key` validada no banco, 401 sem credencial e 403 abaixo do nível 5 |
| 4 | A02 Security Misconfiguration (AUSÊNCIA) | Nenhum header de segurança | Clickjacking, MIME sniffing e XSS sem camada extra | CSP, `X-Content-Type-Options`, `X-Frame-Options` em `after_request` |
| 5 | A02 Security Misconfiguration | `debug=True` | Console Werkzeug permite execução remota de código e vaza código-fonte | Debug desligado fora do desenvolvimento |
| 6 | A02 Security Misconfiguration | `host="0.0.0.0"` | Serviço de laboratório exposto a toda a rede | Bind em `127.0.0.1`, ou proxy reverso com TLS |
| 7 | A10 Mishandling of Exceptional Conditions | Exceção sem tratamento em `/api/relatorio` | Traceback revela tabela, estrutura e caminhos | `errorhandler` global devolve `{"erro":"erro interno"}` |
| 8 | A04 Cryptographic Failures | `SELECT *` devolve a coluna `senha` | Vazamento de credenciais | Projetar só `id, nome`; guardar senha com hash (bcrypt/argon2) |
| 9 | A07 Authentication Failures | `SENHA_MESTRA` e `root/senha` no código | Quem lê o repositório controla o banco | Variáveis de ambiente e usuário de banco com privilégio mínimo |
| 10 | A09 Logging & Alerting Failures (AUSÊNCIA) | Nenhum log de remoções, negações ou erros | Ataque invisível, sem trilha para investigação | `logging` em DELETE, 401, 403 e exceções |
| 11 | A06 Insecure Design | Sem rate limiting nem validação de entrada | Enumeração e força bruta sem freio | Limite por IP (ver exercício 9) e validação de parâmetros |