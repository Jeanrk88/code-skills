# Codex Code Skills

Antes de um software escalar, ele precisa nascer com padrão.

**Codex Code Skills** é um pack público de skills para Codex criado para elevar a barra de **design**, **engenharia**, **QA** e **segurança** em projetos reais.  
Não é um monte de prompts soltos. É um padrão operacional empacotado uma vez para que o agente trabalhe com mais consistência, mais profundidade e mais qualidade.

Quando o projeto cresce, o problema não costuma ser “falta de código”.  
O problema costuma ser outro:

- interface genérica
- arquitetura frouxa
- QA superficial
- segurança deixada para depois
- decisões técnicas sem critério claro
- testes que não cobrem o que realmente importa

Esse repositório existe para corrigir isso.

---

## O problema

Toda vez que você abre um agente e pede ajuda, você precisa repetir a mesma coisa de novo:

- “revisa isso como engenheiro senior”
- “olha a segurança também”
- “não me entrega um frontend genérico”
- “testa de verdade, não só o happy path”
- “quero algo pronto para produção, não só funcionando no meu computador”

Sem um padrão fixo, a qualidade varia conforme o prompt, o contexto e a pressa do momento.

**Codex Code Skills** resolve isso transformando esses padrões em skills reutilizáveis.  
Em vez de explicar sua barra toda vez, você instala o pack uma vez e passa a operar com um conjunto de modos especializados.

---

## Como funciona

Este repositório usa duas camadas:

### 1. Plugin

O plugin é a unidade instalável no Codex.  
Ele aponta para a pasta `skills/` e disponibiliza este pack para uso pessoal ou por projeto.

### 2. Skills

Cada skill é um modo especializado de execução.

Elas não existem para “enfeitar” o fluxo.  
Elas existem para colocar o agente no mindset certo para um trabalho específico.

---

## Skills incluídas

### `frontend-design`

Cria e valida interfaces frontend distintivas, memoráveis e production-grade.

Use quando quiser:

- construir landing pages
- desenhar dashboards
- revisar UI
- elevar o nível visual de uma aplicação
- fugir de interface genérica e “AI slop”

O foco é:

- craft visual
- direção estética
- usabilidade
- experiência
- diferenciação
- implementação real

---

### `software-engineer`

Audita código em nível world-class em todas as camadas.

Use quando quiser:

- revisar arquitetura
- verificar segurança
- checar performance
- avaliar custo técnico
- encontrar gargalos antes de produção
- validar resiliência e escala

O foco é:

- estrutura
- boundaries
- data flow
- segurança
- performance
- custo
- confiabilidade
- qualidade de engenharia

---

### `qa`

Verifica que tudo funciona na prática.

Use quando quiser:

- rodar testes existentes
- achar gaps de cobertura
- escrever testes que faltam
- validar fluxos do usuário
- fazer browser testing
- testar jornadas end-to-end
- validar performance básica
- checar custo
- revisar acessibilidade básica

A `qa` já inclui **modo E2E seguro**, então você não precisa manter uma skill separada para `safe-e2e-test`.

Esse modo cobre:

- browser testing
- screenshots
- fluxos completos
- validação read-only no banco
- checagem de console/errors
- responsividade
- proteção contra ambiente de produção

---

### `security`

Transforma revisão de segurança em workflow operacional.

Use quando quiser:

- revisar vulnerabilidades
- escanear OWASP Top 10
- detectar secrets expostos
- validar headers
- revisar auth
- checar SQL injection / XSS / CSRF
- gerar relatório de segurança
- montar monitoramento básico

O foco é:

- reconhecimento de stack
- varredura
- pen test simulado
- correção guiada
- proteções
- firewall
- monitoramento
- score final

---

## O fluxo recomendado

Você não precisa usar as skills sempre na mesma ordem.  
Mas, para a maioria dos projetos, este fluxo funciona muito bem:

```text
[constrói ou itera no produto]
        ↓
frontend-design   → valida a interface e a experiência
software-engineer → valida estrutura, arquitetura, custo e robustez
qa                → verifica se funciona no uso real
security          → endurece o sistema antes de produção
```

Regra prática
Mudou interface → rode frontend-design
Mudou estrutura/lógica → rode software-engineer
Fez feature nova → rode qa
Vai expor para usuários reais → rode security
Exemplo de uso
Exemplo 1 — revisão de interface

Você:

Use a skill frontend-design para revisar esta landing page e me dizer por que ela ainda parece genérica.

Codex:

aponta problemas de hierarquia visual
identifica ausência de direção estética
sugere mudanças reais de layout, tipografia, contraste, spacing e microinterações
Exemplo 2 — auditoria técnica

Você:

Use a skill software-engineer para auditar este fluxo de autenticação e me dizer os principais riscos de arquitetura, segurança e custo.

Codex:

encontra problemas de boundary
aponta riscos de auth
revisa fluxo de sessão/token
avalia resiliência
destaca gargalos técnicos
Exemplo 3 — teste completo

Você:

Use a skill qa para validar este fluxo de cadastro do começo ao fim, incluindo browser testing e viewport mobile.

Codex:

roda testes existentes
mapeia gaps
testa a jornada
captura screenshots
valida erros e estados
verifica console
aponta bugs reais
Exemplo 4 — endurecimento de segurança

Você:

Use a skill security para revisar esta API e me entregar um relatório com os riscos mais importantes e os fixes recomendados.

Codex:

detecta stack
encontra padrões inseguros
classifica severidade
sugere correções
organiza um report acionável
Para quem é isso

Este pack é para quem:

usa Codex como multiplicador técnico
quer mais consistência no output
não quer depender de prompts improvisados
constrói software de verdade, não só demos
se importa com craft, robustez e clareza
quer um agente mais útil em design, engenharia, QA e segurança

Não é para quem quer:

resposta superficial
frontend genérico
“passou no teste local, então está ótimo”
segurança deixada para depois
validação rasa só para “marcar check”
Estrutura do repositório
.codex-plugin/plugin.json
skills/
frontend-design/SKILL.md
software-engineer/SKILL.md
qa/SKILL.md
security/
SKILL.md
scripts/
references/
examples/
marketplace.personal.json
marketplace.repo.json
README.md
CHANGELOG.md
LICENSE
.gitignore
Instalação
Requisitos
Git
Codex
acesso ao seu diretório de plugins local
Instalação pessoal

Clone este repositório no diretório local de plugins:

git clone https://github.com/Jeanrk88/code-skills.git ~/.codex/plugins/codex-code-skills
mkdir -p ~/.agents/plugins

Depois crie o arquivo:

~/.agents/plugins/marketplace.json

Com este conteúdo:

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

Reinicie o Codex.

Instalação por projeto

Se você quiser disponibilizar este pack dentro de um repositório específico:

mkdir -p ./plugins
git clone https://github.com/Jeanrk88/code-skills.git ./plugins/codex-code-skills
mkdir -p ./.agents/plugins

Depois crie:

./.agents/plugins/marketplace.json

Com este conteúdo:

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
}
]
}

Reinicie o Codex.

Como usar as skills

Você pode usar de duas formas:

1. Uso explícito

Fale claramente qual skill deve ser usada.

Exemplos:

Use a skill frontend-design para revisar esta página.
Use a skill software-engineer para auditar esta feature.
Use a skill qa para testar este fluxo completo.
Use a skill security para revisar esta API. 2. Uso orientado por intenção

Descreva a tarefa com clareza e deixe o agente selecionar a skill mais adequada.

Exemplos:

Quero uma revisão profunda desta interface, focando em sofisticação, diferenciação e usabilidade.
Audite este código como engenheiro senior e me diga os principais riscos de produção.
Teste este fluxo no navegador, incluindo mobile, estados de erro e console.
Faça uma análise de segurança desta aplicação e priorize os riscos mais graves.
Dica de uso

Quanto mais claro você for sobre:

objetivo
contexto
stack
ambiente
restrições
resultado esperado

melhor será o uso da skill.

Como usar cada skill na prática
frontend-design

Use quando quiser elevar a barra visual e de experiência.

Prompt exemplo:

Use a skill frontend-design para revisar esta tela de onboarding.
Quero uma análise crítica de sofisticação, diferenciação e usabilidade.
Depois proponha uma direção visual mais forte e me dê mudanças concretas.
software-engineer

Use quando quiser uma auditoria técnica séria.

Prompt exemplo:

Use a skill software-engineer para revisar esta feature.
Quero findings de arquitetura, segurança, performance, custo e resiliência.
Priorize o que bloqueia produção.
qa

Use quando quiser validar comportamento real.

Prompt exemplo:

Use a skill qa para validar este fluxo end-to-end.
Rode os testes existentes, encontre gaps, teste o fluxo no navegador,
capture screenshots e valide responsividade e console errors.
security

Use quando quiser endurecer o sistema.

Prompt exemplo:

Use a skill security para revisar esta aplicação.
Quero findings priorizados por severidade, possíveis impactos e fixes recomendados.
O que cada skill instala na prática
frontend-design
instruções de direção visual
framework de crítica de interface
critérios de diferenciação, craft e usabilidade
software-engineer
baseline de auditoria senior
critérios de arquitetura, segurança, performance e custo
padrão de findings acionáveis
qa
framework de validação funcional
critérios de teste, gap analysis e verificação manual
modo E2E seguro integrado
security
workflow de segurança
scripts de varredura
referências de ataque, correção e reporte
Atualização
Instalação pessoal
cd ~/.codex/plugins/codex-code-skills
git pull
Instalação por projeto
cd ./plugins/codex-code-skills
git pull

Depois reinicie o Codex.

Desinstalação
Instalação pessoal

Remova a pasta do plugin:

rm -rf ~/.codex/plugins/codex-code-skills

Depois remova a entrada correspondente de:

~/.agents/plugins/marketplace.json
Instalação por projeto

Remova a pasta:

rm -rf ./plugins/codex-code-skills

Depois remova a entrada correspondente de:

./.agents/plugins/marketplace.json
Roadmap
frontend-design
software-engineer
qa
security
modo E2E seguro integrado na qa
exemplos práticos por stack
assets visuais do plugin
releases versionadas
documentação extra de contribuição
Filosofia

Software melhor não nasce por acidente.

Ele nasce quando:

o design deixa de ser genérico
a engenharia deixa de ser improvisada
o QA deixa de ser superficial
a segurança deixa de ser adiada

Este repositório existe para tornar isso repetível.

Você instala uma vez.
Depois itera com mais consistência.

Licença

MIT

Autor

Criado por Jeanrk88.
