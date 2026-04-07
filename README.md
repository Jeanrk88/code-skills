# 🚀 Codex Code Skills

> **Antes de um software escalar, ele precisa nascer com padrão.**

---

<div align="center">

## ✨ O que é Code Skills?

Um **pack operacional** de skills para Codex que eleva a barra de design, engenharia, QA e segurança.  
Instale uma vez. Trabalhe com mais consistência, profundidade e qualidade.

**Não é um monte de prompts soltos. É um padrão reusável.**

</div>

---

## 🎯 Por que usar?

### ❌ Problema

- 🎨 Interface genérica sem diferenciação
- 🏗️ Arquitetura frouxa e débito técnico
- ✅ QA superficial (só testa happy path)
- 🔒 Segurança deixada para depois
- 📋 Decisões sem critério técnico claro
- 🧪 Testes que não cobrem o importante

### ✅ Solução

Toda vez que você usa um agente, precisa falar a mesma coisa:

```bash
"revisa como engenheiro senior"
"olha a segurança também"
"não entrega frontend genérico"
"testa de verdade, não só happy path"
"quero algo pronto pra produção"
```

**Code Skills** transforma isso em padrões reutilizáveis. Instala uma vez, usa sempre.

---

## 🎓 As 4 Skills

<table>
<tr>
<td width="25%" align="center">

### 🎨 Frontend Design

Cria interfaces distintivas e production-grade.

**Use para:**

- Landing pages
- Dashboards
- Elevar nível visual
- Fugir de "AI slop"

**Foca em:**

- Craft visual
- Estética
- Usabilidade
- Diferenciação

</td>
<td width="25%" align="center">

### 🏗️ Software Engineer

Auditoria técnica em nível world-class.

**Use para:**

- Revisar arquitetura
- Checar segurança
- Validar performance
- Encontrar gargalos

**Foca em:**

- Estrutura
- Data flow
- Segurança
- Performance

</td>
<td width="25%" align="center">

### ✅ QA

Testa comportamento real end-to-end.

**Use para:**

- Rodar testes
- Achar gaps
- Browser testing
- Testar jornadas

**Foca em:**

- Cobertura
- Fluxos reais
- Screenshots
- Console errors

</td>
<td width="25%" align="center">

### 🔒 Security

Endurecimento de segurança operacional.

**Use para:**

- Revisar vulnerabilidades
- Escanear OWASP Top 10
- Detectar secrets
- Gerar relatórios

**Foca em:**

- Reconhecimento
- Varredura
- Pen testing
- Score final

</td>
</tr>
</table>

---

## 🔄 Fluxo Recomendado

```
Construir/iterar → Frontend Design → Software Engineer → QA → Security
      ↓                ↓                   ↓              ↓        ↓
   codifica       valida interface    audita código   testa flusos  hardening
```

### 📋 Regra Prática

| Situação                      | Use                 |
| ----------------------------- | ------------------- |
| Mudou interface               | `frontend-design`   |
| Mudou estrutura/lógica        | `software-engineer` |
| Feature nova                  | `qa`                |
| Vai expor para usuários reais | `security`          |

---

## 📚 Exemplos Reais

### 💡 Exemplo 1: Revisar Interface

**Você:**

```bash
Use a skill frontend-design pra revisar esta landing page.
Quero análise crítica de sofisticação, diferenciação e usabilidade.
Depois proponha uma direção visual mais forte.
```

**Codex:**

- ✓ Identifica problemas de hierarquia visual
- ✓ Aponta ausência de direção estética
- ✓ Sugere mudanças concretas (layout, tipografia, contraste, spacing)

### 💡 Exemplo 2: Auditoria Técnica

**Você:**

```bash
Use a skill software-engineer para auditar este fluxo de autenticação.
Principais riscos de arquitetura, segurança e custo.
```

**Codex:**

- ✓ Encontra problemas de boundary
- ✓ Aponta riscos de auth
- ✓ Revisa fluxo de sessão/token
- ✓ Destaca gargalos técnicos

### 💡 Exemplo 3: Teste Completo

**Você:**

```bash
Use a skill qa para validar este fluxo de cadastro.
Do começo ao fim, include browser testing e mobile.
```

**Codex:**

- ✓ Roda testes existentes
- ✓ Mapeia gaps
- ✓ Testa a jornada
- ✓ Captura screenshots
- ✓ Aponta bugs reais

### 💡 Exemplo 4: Endurecimento de Segurança

**Você:**

```bash
Use a skill security para revisar esta API.
Entrega um relatório com riscos importantes e fixes recomendados.
```

**Codex:**

- ✓ Detecta stack
- ✓ Encontra padrões inseguros
- ✓ Classifica severidade
- ✓ Organiza report acionável

---

## ⚙️ Estrutura do Repositório

```
.
├── 📄 README.md                    # Este arquivo
├── 📋 CHANGELOG.md
├── 📄 LICENSE
├── 📁 skills/
│   ├── 🎨 frontend-design/
│   │   └── SKILL.md
│   ├── 🏗️ software-engineer/
│   │   └── SKILL.md
│   ├── ✅ qa/
│   │   └── SKILL.md
│   └── 🔒 security/
│       ├── SKILL.md
│       ├── 📁 references/
│       │   ├── attack-patterns.md
│       │   ├── fix-templates.md
│       │   ├── owasp-top10.md
│       │   └── report-template.md
│       └── 📁 scripts/
│           ├── firewall_setup.py
│           ├── security_scanner.py
│           ├── secret_scanner.py
│           └── ...
└── 📁 examples/
    ├── marketplace.personal.json
    └── marketplace.repo.json
```

---

## 📦 Instalação

### Pré-requisitos

- ✅ Git
- ✅ Codex
- ✅ Acesso ao diretório de plugins

### 🏠 Instalação Pessoal

<details>
<summary><b>Clique para expandir</b></summary>

Clone no seu diretório de plugins:

```bash
git clone https://github.com/Jeanrk88/code-skills.git ~/.codex/plugins/codex-code-skills
mkdir -p ~/.agents/plugins
```

Crie o arquivo `~/.agents/plugins/marketplace.json`:

```json
{
  "name": "codex-marketplace",
  "plugins": [
    {
      "name": "codex-code-skills",
      "source": {
        "source": "local",
        "path": "./.codex/plugins/codex-code-skills"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity",
      "interface": {
        "displayName": "Codex Code Skills"
      }
    }
  ]
}
```

**Reinicie o Codex.**

</details>

### 📂 Instalação por Projeto

<details>
<summary><b>Clique para expandir</b></summary>

Clone dentro do seu repositório:

```bash
mkdir -p ./plugins
git clone https://github.com/Jeanrk88/code-skills.git ./plugins/codex-code-skills
mkdir -p ./.agents/plugins
```

Crie o arquivo `./.agents/plugins/marketplace.json`:

```json
{
  "name": "local-repo",
  "plugins": [
    {
      "name": "codex-code-skills",
      "source": {
        "source": "local",
        "path": "./plugins/codex-code-skills"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity",
      "interface": {
        "displayName": "Codex Code Skills"
      }
    }
  ]
}
```

**Reinicie o Codex.**

</details>

---

## 🎮 Como Usar

### 1️⃣ Uso Explícito (Recomendado)

Fale claramente qual skill usar:

```bash
✓ Use a skill frontend-design para revisar esta página.
✓ Use a skill software-engineer para auditar esta feature.
✓ Use a skill qa para testar este fluxo completo.
✓ Use a skill security para revisar esta API.
```

### 2️⃣ Uso por Intenção

Descreva a tarefa e deixe o agente escolher:

```bash
✓ Quero revisão profunda da interface, focando em sofisticação e usabilidade.
✓ Audite código como engenheiro senior com foco nos riscos de produção.
✓ Teste este fluxo no navegador, incluindo mobile, estados de erro e console.
✓ Análise de segurança da app, priorizando riscos mais graves.
```

### 💡 Dica de Ouro

Quanto mais claro você for sobre:

- 🎯 **Objetivo** da tarefa
- 📋 **Contexto** do projeto
- 🛠️ **Stack** usada
- 🌍 **Ambiente** (dev/staging/prod)
- 🚫 **Restrições** existentes
- 🎁 **Resultado** esperado

Melhor será a qualidade da skill.

---

## 🔄 Atualizações

### 🏠 Instalação Pessoal

```bash
cd ~/.codex/plugins/codex-code-skills
git pull
```

### 📂 Instalação por Projeto

```bash
cd ./plugins/codex-code-skills
git pull
```

**Depois reinicie o Codex.**

---

## 🗑️ Desinstalação

### 🏠 Instalação Pessoal

```bash
rm -rf ~/.codex/plugins/codex-code-skills
# Remove a entrada de ~/.agents/plugins/marketplace.json
```

### 📂 Instalação por Projeto

```bash
rm -rf ./plugins/codex-code-skills
# Remove a entrada de ./.agents/plugins/marketplace.json
```

---

## 🗓️ Roadmap

- [ ] 🎨 Exemplos práticos por stack (React, Vue, Angular)
- [ ] 📊 Assets visuais do plugin
- [ ] 🏷️ Releases versionadas
- [ ] 📖 Documentação extra de contribuição
- [ ] 🔌 Integração com mais plataformas
- [ ] 🧩 Novas skills especializadas

---

## 🧠 Filosofia

<div align="center">

### Software melhor não nasce por acidente.

Ele nasce quando:

| ✨  | Descrição                             |
| --- | ------------------------------------- |
| 🎨  | O design deixa de ser genérico        |
| 🏗️  | A engenharia deixa de ser improvisada |
| ✅  | O QA deixa de ser superficial         |
| 🔒  | A segurança deixa de ser adiada       |

**Este repositório existe para tornar isso repetível.**

_Instale uma vez. Depois itere com mais consistência._

</div>

---

## 👥 Para Quem É Isso?

### ✅ Para você se...

- Usa Codex como multiplicador técnico
- Quer mais consistência no output
- Não quer depender de prompts improvisados
- Constrói software de verdade, não só demos
- Se importa com craft, robustez e clareza
- Quer um agente mais útil em design, engenharia, QA e segurança

### ❌ Não é para você se quer...

- Resposta superficial
- Frontend genérico
- "Passou no teste local, então está ótimo"
- Segurança deixada para depois
- Validação rasa só para "marcar check"

---

## 📜 Licença

MIT

---

<div align="center">

### Criado com ❤️ por **Jeanrk88**

[GitHub](https://github.com/Jeanrk88) • [Report Issues](https://github.com/Jeanrk88/code-skills/issues)

</div>
