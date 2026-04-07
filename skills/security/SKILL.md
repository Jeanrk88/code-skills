---
name: security
description: >
  Use esta skill SEMPRE que o usuário mencionar segurança de aplicação, auditoria de código, vulnerabilidades,
  OWASP, SQL Injection, XSS, CSRF, proteção de API, hashing de senhas, headers HTTP, firewall, pen test,
  varredura de segurança, secrets expostos, monitoramento de segurança, score de segurança, ou qualquer
  pedido relacionado a proteger, auditar ou corrigir código. Também dispare quando o usuário perguntar
  "meu código está seguro?", "como proteger minha aplicação?", "como bloquear ataques?", "análise de
  segurança", "revisão de segurança" ou colar código pedindo para "verificar" ou "melhorar". Esta skill
  transforma código vulnerável em aplicação segura automaticamente, com explicações em português simples.
  Não espere o usuário usar a palavra exata "segurança" — qualquer pedido de proteção, auditoria ou
  análise de risco em código deve disparar esta skill.
---

# 🔐 Security Skill — Aplicação Blindada em Português

Esta skill transforma seu projeto em uma aplicação segura e monitorada sem você precisar entender
segurança. Cole o código, ela faz o resto.

---

## Fluxo de trabalho principal

Siga sempre nesta ordem. Não pule etapas.

```
1. RECONHECIMENTO → detectar stack
2. VARREDURA      → identificar falhas (OWASP Top 10)
3. PEN TEST       → simular ataques reais
4. CORREÇÃO       → aplicar fixes automáticos
5. PROTEÇÕES      → headers, CSRF, sanitização, hashing
6. FIREWALL       → bloquear força bruta, IPs, bots, geo
7. MONITORAMENTO  → daemon contínuo + alertas
8. RELATÓRIO      → score 0-100 + antes/depois
```

---

## ETAPA 1 — Reconhecimento automático da stack

Execute `scripts/stack_detector.py` passando o diretório do projeto:

```bash
python scripts/stack_detector.py /caminho/do/projeto
```

O script retorna JSON com:

- `backend`: python|node|php|ruby|java|go|unknown
- `frontend`: html|react|vue|angular|none
- `database`: sqlite|postgres|mysql|mongodb|none
- `auth`: jwt|session|oauth|basic|none
- `hosting`: vps|heroku|railway|vercel|docker|unknown
- `frameworks`: lista de frameworks detectados
- `entry_points`: arquivos principais encontrados

**Se o usuário colar o código diretamente na conversa**, analise manualmente:

- Imports/requires → identifica linguagem e frameworks
- Padrões de rota → Flask/FastAPI/Express/etc
- Consultas SQL → ORM ou raw queries
- Variáveis de ambiente → `os.environ`, `process.env`, `dotenv`
- Tokens/chaves → procure por `api_key`, `secret`, `password`, `token`

---

## ETAPA 2 — Varredura OWASP Top 10

Execute o scanner:

```bash
python scripts/security_scanner.py /caminho/do/projeto --output /tmp/scan_results.json
```

Para código colado na conversa, aplique a checklist de `references/owasp-top10.md`.

### Checklist rápida (aplique mentalmente a cada arquivo):

| #   | Vulnerabilidade           | O que procurar                                                         |
| --- | ------------------------- | ---------------------------------------------------------------------- |
| A01 | Broken Access Control     | rotas sem autenticação, IDOR, acesso direto a objetos                  |
| A02 | Cryptographic Failures    | MD5/SHA1 em senhas, dados sensíveis sem criptografia, HTTP sem TLS     |
| A03 | Injection                 | queries SQL concatenadas, eval(), exec(), shell=True                   |
| A04 | Insecure Design           | sem rate limiting, sem validação de negócio                            |
| A05 | Security Misconfiguration | DEBUG=True, CORS \*, headers ausentes, erros expostos                  |
| A06 | Vulnerable Components     | bibliotecas desatualizadas (verifique requirements.txt / package.json) |
| A07 | Auth Failures             | senhas fracas, sem MFA, tokens sem expiração, sessão sem invalidação   |
| A08 | Software Integrity        | sem verificação de integridade em atualizações                         |
| A09 | Logging Failures          | sem logs de acesso, falhas silenciosas, dados sensíveis em logs        |
| A10 | SSRF                      | requests para URLs controladas pelo usuário                            |

### Formato de reporte de cada falha:

```
🔴 CRÍTICA | A03 — SQL Injection
📁 Localização: auth/login.py, linha 47
💥 Impacto: Atacante pode extrair todos os dados do banco
🔍 Código vulnerável:
   query = f"SELECT * FROM users WHERE email='{email}'"
✅ Correção: Usar parâmetros preparados (ver Etapa 4)
```

Severidade: 🔴 CRÍTICA | 🟠 ALTA | 🟡 MÉDIA | 🟢 BAIXA

---

## ETAPA 3 — Pen Test Simulado

Leia `references/attack-patterns.md` para os vetores completos.

Execute os ataques simulados mentalmente (ou via script) contra o código:

### Vetores obrigatórios a testar:

**SQL Injection**

```python
# Tente: ' OR '1'='1' --
# Tente: '; DROP TABLE users; --
# Tente: ' UNION SELECT username,password FROM users --
```

**XSS (Cross-Site Scripting)**

```html
<script>
  alert("XSS");
</script>
<img src="x" onerror="alert(1)" />
javascript:alert(document.cookie)
```

**CSRF**

- Verifique se formulários têm token CSRF
- Verifique se API aceita requests de outras origens

**Força Bruta / Rate Limiting**

- Tente 100 logins em 10 segundos — o sistema bloqueia?
- Tente enumerar usuários via respostas diferentes ("email não existe" vs "senha errada")

**IDOR (Insecure Direct Object Reference)**

```
GET /api/user/1/dados → troca para /api/user/2/dados sem ser o user 2
```

**JWT Attacks**

- Token com `alg: none`
- Secret fraco (tente brute force com `jwt_tool`)
- Token sem expiração

**Path Traversal**

```
/download?file=../../etc/passwd
/download?file=..%2F..%2Fetc%2Fpasswd
```

**SSRF**

```
url=http://169.254.169.254/latest/meta-data/  (AWS metadata)
url=http://localhost:6379  (Redis interno)
```

Reporte cada vetor como: ✅ Protegido | ❌ Vulnerável | ⚠️ Parcialmente protegido

---

## ETAPA 4 — Correção automática

Use os templates de `references/fix-templates.md` para cada categoria.

### Guia rápido de correções:

#### SQL Injection → Parâmetros preparados

```python
# ❌ VULNERÁVEL
cursor.execute(f"SELECT * FROM users WHERE email='{email}'")

# ✅ CORRIGIDO
cursor.execute("SELECT * FROM users WHERE email=%s", (email,))

# ✅ Com SQLAlchemy ORM
user = User.query.filter_by(email=email).first()
```

#### XSS → Sanitização de saída

```python
# ❌ VULNERÁVEL
return f"<p>Olá {name}</p>"

# ✅ CORRIGIDO (Flask)
from markupsafe import escape
return f"<p>Olá {escape(name)}</p>"

# ✅ CORRIGIDO (frontend)
element.textContent = name  # em vez de innerHTML
```

#### Hashing seguro de senhas

```python
# ❌ VULNERÁVEL
import hashlib
senha_hash = hashlib.md5(senha.encode()).hexdigest()

# ✅ CORRIGIDO
from passlib.hash import bcrypt
senha_hash = bcrypt.hash(senha)  # hash
bcrypt.verify(senha, senha_hash)  # verificar
```

#### Headers de segurança HTTP

```python
# Flask
from flask import Flask
app = Flask(__name__)

@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=()'
    return response
```

#### Proteção CSRF (Flask-WTF)

```python
# Instalação
pip install flask-wtf

# Configuração
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Template HTML
<form method="POST">
  {{ csrf_token() }}
  ...
</form>
```

#### Variáveis de ambiente (nunca hardcode secrets)

```python
# ❌ VULNERÁVEL
DB_PASSWORD = "minha_senha_123"
API_KEY = "sk-abc123..."

# ✅ CORRIGIDO
import os
from dotenv import load_dotenv
load_dotenv()

DB_PASSWORD = os.environ.get('DB_PASSWORD')
API_KEY = os.environ.get('API_KEY')
```

**Adicione ao .gitignore:**

```
.env
*.env
.env.local
config/secrets.py
```

---

## ETAPA 5 — Proteções essenciais

Execute o setup de proteções:

```bash
python scripts/firewall_setup.py --mode full --project /caminho/do/projeto
```

### Rate Limiting (Flask + Flask-Limiter)

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # máx 5 tentativas/minuto por IP
def login():
    ...

@app.route('/api/', methods=['GET', 'POST'])
@limiter.limit("100 per hour")
def api():
    ...
```

### Validação de inputs

```python
# Com Pydantic (recomendado)
from pydantic import BaseModel, EmailStr, constr

class LoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)

# Com WTForms
from wtforms import StringField, validators
class LoginForm(Form):
    email = StringField('Email', [validators.Email()])
    password = StringField('Senha', [validators.Length(min=8)])
```

---

## ETAPA 6 — Firewall no backend

O script `scripts/firewall_setup.py` instala:

```bash
# Instalação completa
python scripts/firewall_setup.py --install --project /caminho/do/projeto

# Isso configura:
# 1. Middleware de bloqueio de IPs maliciosos
# 2. Rate limiting por IP
# 3. Detecção de user-agents suspeitos (bots, scanners)
# 4. Bloqueio por geolocalização (opcional, requer MaxMind)
# 5. Logging de tentativas de ataque
```

### Middleware de firewall (Python/Flask):

```python
# firewall.py — adicione ao seu projeto
import re
import time
from collections import defaultdict
from flask import request, abort, g
from functools import wraps

# Configurações
BLOCKED_IPS = set()
RATE_LIMIT_WINDOW = 60  # segundos
RATE_LIMIT_MAX = 100    # requests por janela
request_counts = defaultdict(list)

MALICIOUS_PATTERNS = [
    r'(union|select|insert|update|delete|drop|;|--)',  # SQLi
    r'(<script|javascript:|onerror=|onload=)',          # XSS
    r'(\.\./|\.\.\\|%2e%2e)',                          # Path traversal
    r'(eval\(|exec\(|system\(|passthru\()',            # Code injection
]

SUSPICIOUS_UA = [
    'sqlmap', 'nikto', 'nmap', 'masscan', 'dirbuster',
    'burpsuite', 'zgrab', 'scrapy', 'python-requests/2.2',
]

def firewall_middleware(app):
    @app.before_request
    def check_request():
        ip = request.remote_addr

        # 1. IP bloqueado
        if ip in BLOCKED_IPS:
            abort(403)

        # 2. Rate limiting
        now = time.time()
        request_counts[ip] = [t for t in request_counts[ip] if now - t < RATE_LIMIT_WINDOW]
        request_counts[ip].append(now)
        if len(request_counts[ip]) > RATE_LIMIT_MAX:
            BLOCKED_IPS.add(ip)
            abort(429)

        # 3. User-Agent suspeito
        ua = request.headers.get('User-Agent', '').lower()
        if any(s in ua for s in SUSPICIOUS_UA):
            abort(403)

        # 4. Padrões maliciosos na URL/body
        check_target = request.url + str(request.get_data(as_text=True))
        for pattern in MALICIOUS_PATTERNS:
            if re.search(pattern, check_target, re.IGNORECASE):
                app.logger.warning(f"ATTACK BLOCKED: {ip} — {pattern} — {request.url}")
                abort(400)
```

### Bloqueio por geolocalização (MaxMind GeoIP2):

```bash
pip install geoip2
# Baixe o banco: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
```

```python
import geoip2.database

BLOCKED_COUNTRIES = ['CN', 'RU', 'KP', 'IR']  # customizável

reader = geoip2.database.Reader('GeoLite2-Country.mmdb')

@app.before_request
def check_geo():
    try:
        response = reader.country(request.remote_addr)
        if response.country.iso_code in BLOCKED_COUNTRIES:
            abort(403)
    except:
        pass  # IP local ou não encontrado
```

---

## ETAPA 7 — Detecção de secrets expostos

```bash
python scripts/secret_scanner.py /caminho/do/projeto
```

O scanner procura por:

- API keys (OpenAI, AWS, Stripe, SendGrid, Twilio, etc.)
- Tokens JWT hardcoded
- Senhas em strings
- Connection strings de banco de dados
- Chaves privadas (RSA, PEM)
- Credenciais OAuth

### Padrões de detecção:

```python
SECRET_PATTERNS = {
    'OpenAI API Key':      r'sk-[a-zA-Z0-9]{48}',
    'AWS Access Key':      r'AKIA[0-9A-Z]{16}',
    'AWS Secret Key':      r'[0-9a-zA-Z/+]{40}',
    'Stripe Secret Key':   r'sk_live_[0-9a-zA-Z]{24}',
    'Generic Password':    r'(password|senha|pass|pwd)\s*=\s*["\'][^"\']{4,}["\']',
    'Generic API Key':     r'(api_key|apikey|api-key)\s*=\s*["\'][^"\']{8,}["\']',
    'JWT Token':           r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}',
    'Private Key':         r'-----BEGIN (RSA |EC )?PRIVATE KEY-----',
    'Database URL':        r'(postgres|mysql|mongodb):\/\/[^\s"\']+:[^\s"\']+@',
    'GitHub Token':        r'ghp_[a-zA-Z0-9]{36}',
    'Slack Token':         r'xox[baprs]-[0-9a-zA-Z-]{10,}',
}
```

---

## ETAPA 8 — Scanner contínuo + monitoramento

```bash
# Iniciar o daemon de monitoramento
python scripts/monitor_daemon.py --project /caminho/do/projeto --daemonize

# Verificar status
python scripts/monitor_daemon.py --status

# Ver logs
tail -f /var/log/security_monitor.log
```

### Agendamento automático:

```
# Crontab gerado automaticamente pelo setup
*/6 * * * *     python scripts/security_scanner.py --quick --project $PROJECT
0   3 * * *     python scripts/security_scanner.py --full  --project $PROJECT
0   3 * * 0     python scripts/security_scanner.py --full  --project $PROJECT --report weekly
```

### O que o monitoramento faz:

- **A cada 6h**: varredura rápida de secrets e padrões críticos
- **Diariamente às 03h**: scan completo OWASP + Bandit + Semgrep
- **Semanalmente**: relatório completo com diff de segurança
- **Em tempo real**: inotify/watchdog nos arquivos .py/.js/.env
  - Se código mudar → rescan automático em 30 segundos
  - Se secret aparecer → alerta imediato por email/webhook

---

## ETAPA 9 — Relatório final

```bash
python scripts/generate_report.py --project /caminho/do/projeto --output relatorio_seguranca.html
```

O relatório inclui:

- **Score de segurança**: 0 a 100 (com breakdown por categoria)
- **Comparativo antes/depois**: vulnerabilidades encontradas vs corrigidas
- **Gráfico de evolução**: histórico de scores ao longo do tempo
- **Checklist de proteções**: ✅/❌ para cada item aplicado
- **Próximos passos**: o que ainda pode ser melhorado

### Tabela de pontuação:

| Categoria                  | Peso     | Pontos possíveis |
| -------------------------- | -------- | ---------------- |
| Injection (SQL, XSS, etc.) | 20%      | 20               |
| Autenticação segura        | 20%      | 20               |
| Secrets protegidos         | 15%      | 15               |
| Headers HTTP               | 10%      | 10               |
| Rate limiting / Firewall   | 10%      | 10               |
| Criptografia               | 10%      | 10               |
| Logging e monitoramento    | 10%      | 10               |
| Configuração segura        | 5%       | 5                |
| **TOTAL**                  | **100%** | **100**          |

### Escala de score:

- 🔴 0–39: Crítico — aplicação em risco imediato
- 🟠 40–59: Ruim — múltiplas falhas sérias
- 🟡 60–79: Regular — melhorias necessárias
- 🟢 80–89: Bom — proteções básicas aplicadas
- 💎 90–100: Excelente — aplicação blindada

---

## Arquivos de referência

Leia conforme necessário durante a análise:

- `references/owasp-top10.md` — Checklist detalhada OWASP Top 10 com exemplos
- `references/attack-patterns.md` — Todos os vetores de ataque com payloads reais
- `references/fix-templates.md` — Templates de correção por linguagem (Python, Node.js, PHP)
- `references/report-template.md` — Template HTML do relatório final

## Scripts disponíveis

| Script                        | Função                                  |
| ----------------------------- | --------------------------------------- |
| `scripts/stack_detector.py`   | Detecta stack automaticamente           |
| `scripts/security_scanner.py` | Varredura OWASP + Bandit + Semgrep      |
| `scripts/secret_scanner.py`   | Encontra secrets e credenciais expostas |
| `scripts/firewall_setup.py`   | Instala middleware de firewall          |
| `scripts/monitor_daemon.py`   | Daemon de monitoramento contínuo        |
| `scripts/generate_report.py`  | Gera relatório HTML com score           |

---

## Comunicação com o usuário

Explique SEMPRE em português simples, sem jargão técnico desnecessário.

**Boas explicações:**

- ✅ "Seu código mistura dados do usuário diretamente na consulta ao banco — isso permite que um atacante roube todos os dados."
- ❌ "Detected unsanitized input in parameterized query construction."

**Estrutura padrão de resposta:**

1. **Resumo executivo** (3-4 linhas em linguagem simples)
2. **Score atual** (antes das correções)
3. **Lista de problemas** (do mais grave ao menos grave)
4. **Correções aplicadas** (com diff de código)
5. **Score final** (depois das correções)
6. **O que fazer agora** (próximos passos concretos)

---

## Instalação de dependências

```bash
# Python
pip install bandit semgrep passlib flask-wtf flask-limiter pydantic python-dotenv geoip2 watchdog

# Node.js
npm install helmet csurf express-rate-limit bcryptjs joi dotenv

# Verificação de bibliotecas desatualizadas
pip install pip-audit && pip-audit
npm audit
```
