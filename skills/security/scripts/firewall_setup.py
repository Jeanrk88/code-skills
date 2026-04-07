relatorio_template = """
# Template de Relatório Final

## Estrutura do relatório em texto (para respostas no chat)

## Quando gerar o relatório final na conversa, use esta estrutura:

---

## 🔐 RELATÓRIO DE SEGURANÇA — [Nome do Projeto]
**Data:** [data atual]  
**Analisado por:** Security Skill v1.0

---

### 📊 SCORE DE SEGURANÇA

╔══════════════════════════════════════╗
║  ANTES         DEPOIS        GANHO   ║
║  [XX]/100  →  [XX]/100   +[XX] pts  ║
║  [grade]      [grade]               ║
╚══════════════════════════════════════╝

---

### 🚨 PROBLEMAS ENCONTRADOS

**Resumo:**

| Severidade | Encontrados | Corrigidos | Pendentes |
|------------|-------------|------------|-----------|
| 🔴 Críticos | X | X | X |
| 🟠 Altos    | X | X | X |
| 🟡 Médios   | X | X | X |
| 🟢 Baixos   | X | X | X |

---

### 🔴 CRÍTICOS (corrigir imediatamente)

**1. [Nome da vulnerabilidade]**
- **O que é:** [explicação em português simples]
- **Onde:** `arquivo.py`, linha X
- **Risco:** [o que pode acontecer em linguagem simples]
- **Correção aplicada:** [sim/não + o que foi feito]

---

### ✅ PROTEÇÕES APLICADAS

- [X] Headers de segurança HTTP configurados
- [X] Proteção CSRF ativada
- [X] Rate limiting em rotas de login (5/min por IP)
- [X] Hashing bcrypt para senhas
- [X] Sanitização de inputs
- [X] Secrets movidos para variáveis de ambiente
- [X] Firewall backend instalado
- [ ] Bloqueio por geolocalização (requer MaxMind)
- [ ] HTTPS configurado (configuração de servidor)

---

### 🎯 PRÓXIMOS PASSOS RECOMENDADOS

**Imediato (hoje):**
1. [ação concreta]

**Esta semana:**
1. [ação concreta]

**Este mês:**
1. [ação concreta]

---

### 📡 MONITORAMENTO ATIVADO

Daemon rodando: ✅
Varredura rápida: a cada 6 horas
Varredura completa: diariamente às 03:00
Relatório semanal: domingo à noite
Alertas em tempo real: ativado

---

"Segurança não é um produto, é um processo."

---

## Frases explicativas para usar com usuários não técnicos

### SQL Injection
"Imagine que alguém pode digitar na caixinha de login não só a senha deles, mas um comando que diz pro banco de dados revelar todas as senhas de todos os usuários — ou apagar tudo. Era exatamente isso que estava acontecendo no seu código."

### XSS
"Se um atacante consegue colocar um comentário malicioso no seu site, esse comentário pode roubar automaticamente os cookies de todos os usuários que virem aquela página — dando acesso à conta deles."

### CSRF
"Alguém poderia criar uma página maliciosa que, quando um usuário logado visita, automaticamente faz ações no seu site sem o usuário perceber — como mudar senha, fazer transferências, deletar dados."

### Secrets expostos
"Você deixou as chaves da sua casa na fechadura, do lado de fora, visível para qualquer pessoa que olhar para o seu repositório no GitHub."

### Força bruta
"Sem limite de tentativas, um robô pode tentar 10.000 senhas por minuto até encontrar a certa. Com o rate limiting que instalamos, ele só pode tentar 5 vezes por minuto — tornando um ataque de força bruta impraticável."

### Debug em produção
"Quando DEBUG=True está ativado, se alguém forçar um erro no seu site, ele mostra na tela todo o código interno, variáveis, estrutura do banco — como se você mostrasse o projeto arquitetônico da sua casa para um ladrão."

### MD5/SHA1 para senhas
"MD5 foi quebrado em 1996. Bancos de dados de hashes MD5 rodam em segundos em qualquer computador moderno. Migramos para bcrypt, que foi especificamente projetado para ser lento e resistente a ataques."
"""