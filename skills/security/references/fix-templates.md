# Templates de Correção por Linguagem

## Python / Flask

### Setup completo de segurança Flask

```python
# security_config.py — adicione ao seu projeto Flask
import os
import logging
from datetime import timedelta
from flask import Flask, request, abort
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from passlib.hash import bcrypt

def configure_security(app):
    """Aplica todas as configurações de segurança ao app Flask."""

    # 1. Configurações básicas
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY'),  # OBRIGATÓRIO no .env
        SESSION_COOKIE_SECURE=True,               # Apenas HTTPS
        SESSION_COOKIE_HTTPONLY=True,             # Sem acesso JS
        SESSION_COOKIE_SAMESITE='Lax',            # Proteção CSRF
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
        WTF_CSRF_TIME_LIMIT=3600,                 # CSRF token expira em 1h
    )

    # 2. CSRF Protection
    csrf = CSRFProtect(app)

    # 3. Rate Limiting
    limiter = Limiter(app, key_func=get_remote_address,
                      default_limits=["200 per day", "50 per hour"])

    # 4. Security Headers
    @app.after_request
    def security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "  # remova unsafe-inline se possível
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'"
        )
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        # Remover header que revela tecnologia
        response.headers.pop('Server', None)
        response.headers.pop('X-Powered-By', None)
        return response

    # 5. Error handlers seguros
    @app.errorhandler(400)
    def bad_request(e):
        return {"error": "Requisição inválida"}, 400

    @app.errorhandler(403)
    def forbidden(e):
        return {"error": "Acesso negado"}, 403

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Não encontrado"}, 404

    @app.errorhandler(429)
    def too_many(e):
        return {"error": "Muitas requisições. Tente novamente mais tarde."}, 429

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error(f"Erro interno: {e}", exc_info=True)
        return {"error": "Erro interno do servidor"}, 500

    return app, csrf, limiter
```

### Autenticação segura completa

```python
# auth.py — sistema de autenticação seguro
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import jwt
import secrets

class AuthService:

    @staticmethod
    def hash_password(password: str) -> str:
        """Cria hash seguro da senha com bcrypt."""
        return bcrypt.hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verifica senha contra hash bcrypt."""
        return bcrypt.verify(password, password_hash)

    @staticmethod
    def generate_jwt(user_id: int, role: str = 'user') -> str:
        """Gera JWT com expiração e claims de segurança."""
        payload = {
            'user_id': user_id,
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=1),
            'jti': secrets.token_urlsafe(16),  # JWT ID único (permite blacklist)
        }
        return jwt.encode(payload, os.environ.get('JWT_SECRET'), algorithm='HS256')

    @staticmethod
    def verify_jwt(token: str) -> dict:
        """Verifica e decodifica JWT."""
        return jwt.decode(
            token,
            os.environ.get('JWT_SECRET'),
            algorithms=['HS256'],  # SEMPRE especifique algoritmo!
            options={"require": ["exp", "iat", "user_id"]}
        )

    @staticmethod
    def generate_reset_token() -> tuple[str, datetime]:
        """Gera token de reset seguro com expiração."""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        return token, expires_at
```

---

## Node.js / Express

### Setup completo de segurança Express

```javascript
// security.js — middleware de segurança para Express
const helmet = require("helmet");
const rateLimit = require("express-rate-limit");
const csrf = require("csurf");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");

function configureSecurity(app) {
  // 1. Helmet — headers de segurança automáticos
  app.use(
    helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: ["'self'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          imgSrc: ["'self'", "data:", "https:"],
          frameAncestors: ["'none'"],
        },
      },
      hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true,
      },
    }),
  );

  // 2. Rate limiting global
  const globalLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutos
    max: 100,
    message: { error: "Muitas requisições. Tente novamente mais tarde." },
    standardHeaders: true,
    legacyHeaders: false,
  });
  app.use(globalLimiter);

  // 3. Rate limiting rigoroso para auth
  const authLimiter = rateLimit({
    windowMs: 60 * 1000, // 1 minuto
    max: 5,
    message: { error: "Muitas tentativas de login. Aguarde 1 minuto." },
    skipSuccessfulRequests: true,
  });
  app.use("/auth/login", authLimiter);
  app.use("/auth/register", authLimiter);

  // 4. Remover headers que revelam tecnologia
  app.disable("x-powered-by");

  return app;
}

// Autenticação segura
const AuthService = {
  async hashPassword(password) {
    const saltRounds = 12;
    return bcrypt.hash(password, saltRounds);
  },

  async verifyPassword(password, hash) {
    return bcrypt.compare(password, hash);
  },

  generateToken(userId, role = "user") {
    return jwt.sign(
      { userId, role, jti: require("crypto").randomBytes(16).toString("hex") },
      process.env.JWT_SECRET,
      { expiresIn: "1h", algorithm: "HS256" },
    );
  },

  verifyToken(token) {
    return jwt.verify(token, process.env.JWT_SECRET, { algorithms: ["HS256"] });
  },
};

// Middleware de autenticação
function requireAuth(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Não autenticado" });
  }
  try {
    req.user = AuthService.verifyToken(authHeader.slice(7));
    next();
  } catch {
    return res.status(401).json({ error: "Token inválido ou expirado" });
  }
}

// Validação de inputs com Joi
const Joi = require("joi");
const loginSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).max(128).required(),
});

function validateLogin(req, res, next) {
  const { error } = loginSchema.validate(req.body);
  if (error) return res.status(400).json({ error: error.details[0].message });
  next();
}

module.exports = { configureSecurity, AuthService, requireAuth, validateLogin };
```

---

## PHP

### Headers de segurança PHP

```php
<?php
// security_headers.php

function apply_security_headers() {
    // Remover headers que revelam tecnologia
    header_remove('X-Powered-By');
    header_remove('Server');

    // Headers de segurança
    header('X-Content-Type-Options: nosniff');
    header('X-Frame-Options: DENY');
    header('X-XSS-Protection: 1; mode=block');
    header('Strict-Transport-Security: max-age=31536000; includeSubDomains');
    header("Content-Security-Policy: default-src 'self'");
    header('Referrer-Policy: strict-origin-when-cross-origin');
}

// Hash seguro de senhas (PHP moderno)
function hash_password(string $password): string {
    return password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);
}

function verify_password(string $password, string $hash): bool {
    return password_verify($password, $hash);
}

// Proteção SQL Injection com PDO
function get_user_by_email(PDO $pdo, string $email): ?array {
    // ✅ Prepared statements
    $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
    $stmt->execute([$email]);
    return $stmt->fetch(PDO::FETCH_ASSOC) ?: null;
}

// Proteção XSS
function sanitize_output(string $data): string {
    return htmlspecialchars($data, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

// CSRF Token
function generate_csrf_token(): string {
    if (!isset($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

function verify_csrf_token(string $token): bool {
    return hash_equals($_SESSION['csrf_token'] ?? '', $token);
}
?>
```

---

## Configuração .env segura

```bash
# .env — NUNCA commitar este arquivo!
# Adicione .env ao .gitignore

# Chaves criptográficas (gere com: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=gere_uma_chave_aleatoria_de_64_caracteres_aqui
JWT_SECRET=gere_outra_chave_aleatoria_diferente_aqui
ENCRYPTION_KEY=gere_uma_fernet_key_com_Fernet.generate_key()

# Banco de dados
DB_HOST=localhost
DB_PORT=5432
DB_NAME=meu_banco
DB_USER=usuario_limitado
DB_PASSWORD=senha_forte_aqui

# Email
SMTP_HOST=smtp.gmail.com
SMTP_USER=app@empresa.com
SMTP_PASSWORD=app_password_aqui

# APIs externas
STRIPE_SECRET_KEY=sk_live_...
OPENAI_API_KEY=sk-...

# Configurações de produção
FLASK_ENV=production
DEBUG=False
ALLOWED_HOSTS=meusite.com.br,www.meusite.com.br
```

```bash
# .gitignore — adicione estas linhas
.env
.env.*
*.env
config/secrets.py
config/secrets.js
credentials.json
*_credentials.json
*.pem
*.key
*.p12
*.pfx
```

---

## Nginx — Configuração segura

```nginx
# nginx.conf — configurações de segurança
server {
    listen 443 ssl http2;
    server_name meusite.com.br;

    # SSL
    ssl_certificate /etc/ssl/certs/meusite.pem;
    ssl_certificate_key /etc/ssl/private/meusite.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Headers de segurança
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header Content-Security-Policy "default-src 'self'" always;

    # Ocultar versão do nginx
    server_tokens off;

    # Bloquear acesso a arquivos sensíveis
    location ~ /\. {
        deny all;  # bloqueia .env, .git, .htaccess etc
    }
    location ~ \.(sql|bak|backup|log)$ {
        deny all;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    location /login {
        limit_req zone=login burst=10 nodelay;
        proxy_pass http://app;
    }

    # Limite de tamanho de upload
    client_max_body_size 10M;
}

# Redirect HTTP → HTTPS
server {
    listen 80;
    return 301 https://$host$request_uri;
}
```
