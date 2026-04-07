# Codex Code Skills

> **Antes de um software escalar, ele precisa nascer com padrão.**

---

<div align="center">

## O que é Code Skills?

Um **pack operacional** de skills para Codex que eleva a barra de design, engenharia, QA e segurança.  
Instale uma vez. Trabalhe com mais consistência, profundidade e qualidade.

**Não é um monte de prompts soltos. É um padrão reusável.**

</div>

---

## Por que usar?

### Problema

- Interface genérica sem diferenciação
- Arquitetura frouxa e débito técnico
- QA superficial (só testa happy path)
- Segurança deixada para depois
- Decisões sem critério técnico claro
- Testes que não cobrem o importante

### Solução

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

## As 4 Skills

<table>
<tr>
<td width="25%" align="center">

### Frontend Design

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

### Software Engineer

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

### QA

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

### Security

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

## Fluxo Recomendado

```
Construir/iterar → Frontend Design → Software Engineer → QA → Security
      ↓                ↓                   ↓              ↓        ↓
   codifica       valida interface    audita código   testa flusos  hardening
```

### Regra Prática

| Situação                      | Use                 |
| ----------------------------- | ------------------- |
| Mudou interface               | `frontend-design`   |
| Mudou estrutura/lógica        | `software-engineer` |
| Feature nova                  | `qa`                |
| Vai expor para usuários reais | `security`          |

---

## Exemplos Reais

### Exemplo 1: Revisar Interface

**Você:**

```bash
/frontend-design
Revisar esta landing page.
Análise crítica de sofisticação, diferenciação e usabilidade.
```

**Codex:**

- Identifica problemas de hierarquia visual
- Aponta ausência de direção estética
- Sugere mudanças concretas (layout, tipografia, contraste, spacing)

### Exemplo 2: Auditoria Técnica

**Você:**

```bash
/software-engineer
Auditar este fluxo de autenticação.
Principais riscos de arquitetura, segurança e custo.
```

**Codex:**

- Encontra problemas de boundary
- Aponta riscos de auth
- Revisa fluxo de sessão/token
- Destaca gargalos técnicos

### Exemplo 3: Teste Completo

**Você:**

```bash
/qa
Validar este fluxo de cadastro do começo ao fim.
Incluir browser testing e mobile, console errors.
```

**Codex:**

- Roda testes existentes
- Mapeia gaps
- Testa a jornada
- Captura screenshots
- Aponta bugs reais

### Exemplo 4: Endurecimento de Segurança

**Você:**

```bash
/security
Revisar esta API.
Relatório com riscos importantes e fixes recomendados.
```

**Codex:**

- Detecta stack
- Encontra padrões inseguros
- Classifica severidade
- Organiza report acionável

---

## Estrutura do Repositório

```
├── .codex-plugin/
│   ├── plugin.json
└── examples/
    ├── marketplace.personal.json
    └── marketplace.repo.json
├── skills/
│   ├── frontend-design/
│   │   └── SKILL.md
│   ├── qa/
│   │   └── SKILL.md
│   ├── security/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── attack-patterns.md
│   │   │   ├── fix-templates.md
│   │   │   ├── owasp-top10.md
│   │   │   └── report-template.md
│   │   └── scripts/
│   │       ├── firewall_setup.py
│   │       ├── generate_report.py
│   │       ├── monitor_daemon.py
│   │       ├── secret_scanner.py
│   │       ├── security_scanner.py
│   │       ├── security_scanner.test.py
│   │       └── stack_detector.py
│   └── software-engineer/
│       └── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
```

---

## Instalação

### Pré-requisitos

- Git
- Codex (VS Code com extensão GitHub Copilot)
- PowerShell 5.1+ (Windows) ou Bash (macOS/Linux)
- Python 3.12+ (para skill de security)

### Instalação via PowerShell (Recomendado)

<details>
<summary><b>Método automático - Clique para expandir</b></summary>

Abra o **PowerShell** na IDE e execute:

```
git clone --filter=blob:none --no-checkout https://github.com/Jeanrk88/code-skills.git .\.agents; Set-Location .\.agents; git sparse-checkout init --no-cone; git sparse-checkout set skills; git checkout main; Set-Location ..; if (-not (Get-Command python -ErrorAction SilentlyContinue)) { $r = Read-Host "Python nao encontrado. Deseja instalar agora? (S/N)"; if ($r -eq 'S' -or $r -eq 's') { winget install Python.Python.3.12 } else { Write-Host "Python necessario para rodar a skill de security." -ForegroundColor Yellow } } else { Write-Host "Python OK: $((python --version))" -ForegroundColor Green }
```

**O script irá:**

- ✅ Clonar o repositório com otimização
- ✅ Baixar somente a pasta `skills`
- ✅ Verificar Python e instalar se necessário
- ✅ Configurar tudo automaticamente

</details>

### Instalação via IDE + Extensão Codex

<details>
<summary><b>Método IDE - Clique para expandir</b></summary>

1. **Abra o VS Code** com a extensão Copilot/Codex instalada
2. **Abra o Terminal Integrado** (Ctrl + ` ou View > Terminal)
3. **Cole e execute** o comando PowerShell acima
4. **Reinicie o VS Code** após conclusão
5. **Verifique a instalação:**
   - Vá para `Explorer` (Ctrl + Shift + E)
   - Procure pela pasta `.agents/skills`
   - Você deve ver 4 pastas: `frontend-design`, `software-engineer`, `qa`, `security`

**Pronto!** Agora você pode usar as skills digitando `/frontend-design`, `/software-engineer`, `/qa` ou `/security` no chat Copilot.

</details>

### Instalação Pessoal (manual)

<details>
<summary><b>Método manual - Clique para expandir</b></summary>

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

### Instalação por Projeto (manual)

<details>
<summary><b>Método por projeto - Clique para expandir</b></summary>

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

## Como Usar

### Chamar Skills com Barra

Use a **barra (/) antes do nome da skill**:

```bash
/frontend-design
/software-engineer
/qa
/security
```

### Uso Explícito (Recomendado)

Combine a skill com contexto claro:

```bash
/frontend-design
Revisar esta página. Sofisticação, diferenciação e usabilidade.

/software-engineer
Auditar esta feature. Riscos de arquitetura, segurança e performance.

/qa
Testar este fluxo completo. Mobile, console errors, browser testing.

/security
Revisar esta API. Vulnerabilidades, OWASP Top 10, relatório final.
```

### Uso por Intenção

Descreva a tarefa e deixe o agente escolher a skill:

```bash
Quero revisão profunda da interface, focando em sofisticação e usabilidade.
Audite código como engenheiro senior com foco nos riscos de produção.
Teste este fluxo no navegador, incluindo mobile, estados de erro e console.
Análise de segurança da app, priorizando riscos mais graves.
```

### Dica de Ouro

Quanto mais claro você for sobre:

- **Objetivo** da tarefa
- **Contexto** do projeto
- **Stack** usada
- **Ambiente** (dev/staging/prod)
- **Restrições** existentes
- **Resultado** esperado

Melhor será a qualidade da skill.

---

## Atualização

### Atualização via PowerShell (Recomendado)

<details>
<summary><b>Método automático - Clique para expandir</b></summary>

Abra o **PowerShell** na IDE e execute:

```
git clone --filter=blob:none --no-checkout https://github.com/Jeanrk88/code-skills.git .\.agents; Set-Location .\.agents; git sparse-checkout init --no-cone; git sparse-checkout set skills; git checkout main; Set-Location ..; if (-not (Get-Command python -ErrorAction SilentlyContinue)) { $r = Read-Host "Python nao encontrado. Deseja instalar agora? (S/N)"; if ($r -eq 'S' -or $r -eq 's') { winget install Python.Python.3.12 } else { Write-Host "Python necessario para rodar a skill de security." -ForegroundColor Yellow } } else { Write-Host "Python OK: $((python --version))" -ForegroundColor Green }
```

**O script irá:**

- ✅ Verificar se a pasta `.agents` existe
- ✅ Comparar versão local com remota
- ✅ Atualizar automaticamente se houver mudanças
- ✅ Exibir o hash dos commits (antes → depois)

</details>

### Atualização via IDE + Extensão Codex

<details>
<summary><b>Método IDE - Clique para expandir</b></summary>

1. **Abra o Terminal Integrado** no VS Code (Ctrl + `)
2. **Cole e execute** o comando PowerShell acima
3. **Verifique a atualização** olhando as cores de status:
   - 🟢 Verde = Já está atualizado
   - 🔵 Cyan = Atualização concluída com sucesso
   - 🔴 Vermelho = Erro (verifique o caminho)
4. **Reinicie o VS Code** se necessário

</details>

### Atualização Manual

<details>
<summary><b>Método manual - Clique para expandir</b></summary>

**Instalação Pessoal:**

```bash
cd ~/.codex/plugins/codex-code-skills
git pull
```

**Instalação por Projeto:**

```bash
cd ./plugins/codex-code-skills
git pull
```

**Depois reinicie o Codex.**

</details>

---

## Desinstalação

### Desinstalação via Terminal PowerShell (Recomendado)

<details>
<summary><b>Método automático - Clique para expandir</b></summary>

Abra o **PowerShell** na IDE e execute:

```
if (Test-Path ".\.agents") { Remove-Item ".\.agents" -Recurse -Force; Write-Host "Pasta .agents removida." -ForegroundColor Green } else { Write-Host "Pasta .agents nao encontrada." -ForegroundColor Yellow }

```

**O script irá:**

- ✅ Verificar se a pasta `.agents` existe
- ✅ Remover a pasta e todo seu conteúdo permanentemente
- ✅ Exibir mensagem de confirmação

⚠️ **Aviso:** Esta operação é irreversível. Certifique-se de fazer backup se necessário.

</details>

### Desinstalação via IDE + Extensão Codex

<details>
<summary><b>Método IDE - Clique para expandir</b></summary>

1. **Abra o Terminal Integrado** no VS Code (Ctrl + `)
2. **Cole e execute** o comando PowerShell acima
3. **Verifique a remoção:**
   - Vá para `Explorer` (Ctrl + Shift + E)
   - Confirme que a pasta `.agents` foi removida
   - 🟢 Se não aparecer mais, a desinstalação foi bem-sucedida
4. **Reinicie o VS Code**

</details>

### Desinstalação Manual

<details>
<summary><b>Método manual - Clique para expandir</b></summary>

**Instalação Pessoal:**

```bash
rm -rf ~/.codex/plugins/codex-code-skills
# Remove a entrada de ~/.agents/plugins/marketplace.json
```

**Instalação por Projeto:**

```bash
rm -rf ./plugins/codex-code-skills
# Remove a entrada de ./.agents/plugins/marketplace.json
```

</details>

---

## Roadmap

- Exemplos práticos por stack (React, Vue, Angular)
- Assets visuais do plugin
- Releases versionadas
- Documentação extra de contribuição
- Integração com mais plataformas
- Novas skills especializadas

---

## Filosofia

<div align="center">

### Software melhor não nasce por acidente.

Ele nasce quando:

| Item       | Descrição                             |
| ---------- | ------------------------------------- |
| Design     | O design deixa de ser genérico        |
| Engenharia | A engenharia deixa de ser improvisada |
| QA         | O QA deixa de ser superficial         |
| Segurança  | A segurança deixa de ser adiada       |

**Este repositório existe para tornar isso repetível.**

_Instale uma vez. Depois itere com mais consistência._

</div>

---

## Para Quem É Isso?

### Para você se...

- Usa Codex como multiplicador técnico
- Quer mais consistência no output
- Não quer depender de prompts improvisados
- Constrói software de verdade, não só demos
- Se importa com craft, robustez e clareza
- Quer um agente mais útil em design, engenharia, QA e segurança

### Não é para você se quer...

- Resposta superficial
- Frontend genérico
- "Passou no teste local, então está ótimo"
- Segurança deixada para depois
- Validação rasa só para "marcar check"

---

## Licença

MIT

---

<div align="center">

### Criado por **Jeanrk88**

[GitHub](https://github.com/Jeanrk88) • [Report Issues](https://github.com/Jeanrk88/code-skills/issues)

</div>
