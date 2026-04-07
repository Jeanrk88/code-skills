# OWASP Top 10 — Referência Completa

## A01 — Broken Access Control (Controle de Acesso Quebrado)

### O que é

O sistema não verifica adequadamente se o usuário tem permissão para acessar recursos.

### Como identificar

```python
# ❌ VULNERÁVEL — não verifica se o usuário logado é dono do recurso
@app.route('/api/pedido/<int:pedido_id>')
def ver_pedido(pedido_id):
    pedido = Pedido.query.get(pedido_id)  # qualquer usuário acessa qualquer pedido!
    return jsonify(pedido.to_dict())

# ❌ VULNERÁVEL — rota admin sem verificação de role
@app.route('/admin/usuarios')
@login_required
def listar_usuarios():  # login_required mas não checa se é admin!
    return User.query.all()
```

### Correção

```python
# ✅ CORRIGIDO — verifica propriedade do recurso
@app.route('/api/pedido/<int:pedido_id>')
@login_required
def ver_pedido(pedido_id):
    pedido = Pedido.query.filter_by(id=pedido_id, user_id=current_user.id).first_or_404()
    return jsonify(pedido.to_dict())

# ✅ CORRIGIDO — decorator de role
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated
```

---

## A02 — Cryptographic Failures (Falhas Criptográficas)

### O que é

Dados sensíveis transmitidos ou armazenados sem criptografia adequada.

### Como identificar

```python
# ❌ MD5 ou SHA1 para senhas (quebráveis)
import hashlib
hash = hashlib.md5(password.encode()).hexdigest()
hash = hashlib.sha1(password.encode()).hexdigest()

# ❌ Dados sensíveis em texto puro no banco
user.cpf = cpf  # sem criptografia

# ❌ Chave secreta fraca ou hardcoded
app.secret_key = "abc123"
JWT_SECRET = "secret"
```

### Correção

```python
# ✅ bcrypt para senhas
from passlib.hash import bcrypt
hash = bcrypt.hash(password)
bcrypt.verify(password, hash)

# ✅ Criptografia de dados sensíveis
from cryptography.fernet import Fernet
key = os.environ.get('ENCRYPTION_KEY')
f = Fernet(key)
user.cpf = f.encrypt(cpf.encode()).decode()

# ✅ Chave forte via variável de ambiente
import secrets
# Gere uma vez: secrets.token_hex(32)
app.secret_key = os.environ.get('SECRET_KEY')
```

---

## A03 — Injection (Injeção)

### Tipos principais

**SQL Injection**

```python
# ❌ VULNERÁVEL
query = f"SELECT * FROM users WHERE user='{username}' AND pass='{password}'"
cursor.execute(query)

# Ataque: username = ' OR '1'='1
# Query resultante: SELECT * FROM users WHERE user='' OR '1'='1' AND pass=''
# Resultado: loga sem senha, acessa todos os registros

# ✅ CORRIGIDO
cursor.execute("SELECT * FROM users WHERE user=%s AND pass=%s", (username, password))
```

**Command Injection**

```python
# ❌ VULNERÁVEL
import os
os.system(f"convert {filename} output.jpg")  # filename pode ser "x; rm -rf /"

# ✅ CORRIGIDO
import subprocess
subprocess.run(['convert', filename, 'output.jpg'], check=True)
```

**Template Injection (SSTI)**

```python
# ❌ VULNERÁVEL (Flask/Jinja2)
return render_template_string(f"Olá {name}")  # name = "{{7*7}}" → retorna 49

# ✅ CORRIGIDO
from markupsafe import escape
return render_template_string("Olá {{ name }}", name=escape(name))
```

**LDAP Injection**

```python
# ❌ VULNERÁVEL
ldap_filter = f"(uid={username})"  # username = "*)(uid=*))(|(uid=*"

# ✅ CORRIGIDO — escape de caracteres especiais LDAP
import ldap
username_safe = ldap.filter.escape_filter_chars(username)
ldap_filter = f"(uid={username_safe})"
```

---

## A04 — Insecure Design (Design Inseguro)

### O que é

Ausência de controles de segurança na arquitetura, não apenas na implementação.

### Problemas comuns

- Sem limite de tentativas de login (força bruta ilimitada)
- Resposta diferente para "usuário não existe" vs "senha errada" (enumeração)
- Tokens de reset de senha sem expiração
- Sem confirmação de email em cadastro
- Lógica de negócio manipulável (ex: preço enviado pelo cliente)

### Correções de design

```python
# ✅ Mensagem genérica no login (sem enumeração)
if not user or not bcrypt.verify(password, user.password_hash):
    return {"error": "Credenciais inválidas"}, 401  # NÃO diga qual está errado

# ✅ Token de reset com expiração curta
import secrets
from datetime import datetime, timedelta

def gerar_token_reset(user_id):
    token = secrets.token_urlsafe(32)
    expira_em = datetime.utcnow() + timedelta(hours=1)  # 1 hora
    salvar_token_reset(user_id, token, expira_em)
    return token

# ✅ Nunca confie em preços do cliente
@app.route('/checkout', methods=['POST'])
def checkout():
    item_id = request.json['item_id']
    quantidade = request.json['quantidade']
    item = Item.query.get(item_id)
    total = item.preco * quantidade  # preço vem do banco, não do cliente
```

---

## A05 — Security Misconfiguration (Configuração Incorreta)

### Checklist de configuração

```python
# ❌ Nunca em produção
DEBUG = True
TESTING = True

# ❌ CORS permissivo demais
from flask_cors import CORS
CORS(app, origins="*")  # permite qualquer origem

# ✅ CORS restrito
CORS(app, origins=["https://meusite.com.br", "https://app.meusite.com.br"])

# ❌ Erros detalhados expostos ao cliente
@app.errorhandler(Exception)
def handle_error(e):
    return str(e), 500  # stack trace vaza para o usuário!

# ✅ Erros genéricos ao cliente, detalhes nos logs
import logging
@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"Erro interno: {e}", exc_info=True)
    return {"error": "Erro interno do servidor"}, 500

# ❌ Listagem de diretórios habilitada (nginx/apache)
# autoindex on;  ← remova isso

# ❌ Arquivos sensíveis acessíveis
# /backup.sql, /.env, /config.php, /phpinfo.php
```

---

## A06 — Vulnerable and Outdated Components

### Como verificar

```bash
# Python
pip install pip-audit
pip-audit  # lista CVEs conhecidos nas dependências

# Node.js
npm audit
npm audit fix  # corrige automaticamente quando possível

# Ver dependências desatualizadas
pip list --outdated
npm outdated
```

### Prioridades de update

1. **Crítico**: bibliotecas de autenticação (PyJWT, passport, etc.)
2. **Crítico**: bibliotecas de parsing (XML, YAML, JSON)
3. **Alta**: frameworks web (Flask, Django, Express)
4. **Média**: demais dependências diretas

---

## A07 — Authentication Failures

### Problemas comuns e correções

```python
# ❌ Sem limite de tentativas
@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)

# ✅ Com rate limiting e lockout
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute; 20 per hour")
def login():
    ...

# ❌ JWT sem expiração
token = jwt.encode({'user_id': user.id}, SECRET)

# ✅ JWT com expiração curta
from datetime import datetime, timedelta
token = jwt.encode({
    'user_id': user.id,
    'exp': datetime.utcnow() + timedelta(hours=1),
    'iat': datetime.utcnow(),
}, SECRET, algorithm='HS256')

# ❌ Lembrar sessão indefinidamente
session.permanent = True
app.permanent_session_lifetime = timedelta(days=365)

# ✅ Sessão com timeout razoável
app.permanent_session_lifetime = timedelta(hours=8)  # 8 horas de inatividade
```

---

## A08 — Software and Data Integrity Failures

### Verificação de integridade

```python
# ✅ Verificar hash de downloads
import hashlib

def verificar_arquivo(filepath, hash_esperado):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest() == hash_esperado

# ✅ Usar lockfiles (pip-compile, npm ci)
# requirements.txt gerado com pip-compile (versões fixas + hashes)
# package-lock.json (npm ci em vez de npm install)
```

---

## A09 — Security Logging and Monitoring Failures

### Implementação de logging

```python
import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

# Configurar logger de segurança
security_logger = logging.getLogger('security')
handler = RotatingFileHandler('logs/security.log', maxBytes=10*1024*1024, backupCount=5)
security_logger.addHandler(handler)
security_logger.setLevel(logging.INFO)

def log_evento_seguranca(evento, ip, usuario=None, detalhes=None):
    """Registra eventos de segurança em formato estruturado."""
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'evento': evento,
        'ip': ip,
        'usuario': usuario,
        'detalhes': detalhes
    }
    security_logger.info(json.dumps(entry))

# Exemplos de uso
log_evento_seguranca('LOGIN_FALHOU', ip=request.remote_addr, usuario=email)
log_evento_seguranca('LOGIN_SUCESSO', ip=request.remote_addr, usuario=user.id)
log_evento_seguranca('ACESSO_NEGADO', ip=request.remote_addr, usuario=current_user.id,
                     detalhes={'rota': request.path})
log_evento_seguranca('ATAQUE_DETECTADO', ip=request.remote_addr,
                     detalhes={'tipo': 'sql_injection', 'payload': request.url})

# ❌ NUNCA logar dados sensíveis
log.info(f"Login: {email} senha={password}")  # ERRADO!

# ✅ Logar apenas o necessário
log.info(f"Tentativa de login: {email}")  # CERTO
```

---

## A10 — Server-Side Request Forgery (SSRF)

### O que é

O servidor faz requisições para URLs fornecidas pelo usuário, podendo acessar serviços internos.

### Identificação e correção

```python
# ❌ VULNERÁVEL
import requests
@app.route('/preview')
def preview():
    url = request.args.get('url')
    return requests.get(url).text  # usuário pode passar http://localhost:6379, etc.

# ✅ CORRIGIDO — whitelist de domínios
from urllib.parse import urlparse

ALLOWED_DOMAINS = ['api.parceiro.com', 'cdn.parceiro.com']

@app.route('/preview')
def preview():
    url = request.args.get('url')
    parsed = urlparse(url)

    # Bloquear IPs privados e localhost
    if parsed.hostname in ('localhost', '127.0.0.1', '0.0.0.0'):
        abort(400)

    # Bloquear ranges de IP privado
    import ipaddress
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            abort(400)
    except ValueError:
        pass  # é um hostname, não IP

    # Verificar whitelist
    if parsed.hostname not in ALLOWED_DOMAINS:
        abort(400)

    return requests.get(url, timeout=5).text
```
