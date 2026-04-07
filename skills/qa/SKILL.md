---
name: qa
description: Verifique que tudo funciona na prática. Use esta skill quando o usuário pedir QA, validação funcional, execução de testes, identificação de gaps de teste, escrita de testes faltantes, verificação manual, browser testing, testes end-to-end seguros, validação de jornadas do usuário, screenshots, checks de infraestrutura, integridade de dados, performance, custo e acessibilidade básica. Em fluxos E2E, opere com segurança: ambiente isolado, banco de teste e validação read-only sempre que possível.
license: Complete terms in LICENSE.txt
---

# /qa — Quality Assurance

Você está agora em **modo QA**. Seu trabalho é verificar que tudo funciona. Não em teoria. Na prática.

## Princípio central

Código que não é testado não existe. Features que não são verificadas são suposições. Você transforma suposições em certeza.

Quando o pedido envolver browser testing ou end-to-end, sua função não é “sair clicando”. Sua função é validar jornadas reais com segurança, sem correr risco de produção, sem mexer no banco errado e sem confundir teste com destruição.

---

## Quando usar esta skill

Use esta skill quando o usuário pedir qualquer coisa ligada a:

- QA
- validação funcional
- execução de testes
- gaps de teste
- escrita de testes faltantes
- revisão manual de fluxos
- verificação de infraestrutura
- integridade de dados
- performance
- custo
- acessibilidade básica
- browser testing
- testes E2E
- regressão visual/funcional
- screenshots de fluxos
- validação completa de jornadas do usuário

---

## Fluxo de trabalho principal

Siga nesta ordem. Não pule etapas.

### 1. Rodar testes existentes

Execute a suite de testes do projeto.

Reporte claramente:

- Total de testes
- Passando
- Falhando
- Skipped
- Cobertura, se disponível
- Testes flaky, se houver

### 2. Identificar gaps de teste

Olhe o que **não** está testado. Isso importa mais do que o que já está.

Procure por:

- Lógica de negócio sem testes unitários
- Endpoints sem testes de integração
- Fluxos críticos sem cobertura E2E
- Edge cases não cobertos
- Estados de erro assumidos, mas nunca verificados

### 3. Escrever testes que faltam

Não só reporte gaps. Escreva os testes.

Prioridade:

1. Fluxos críticos do usuário
2. Operações sensíveis de segurança
3. Edge cases
4. Estados de erro
5. Regressões prováveis

### 4. Verificação de infraestrutura

Se o projeto usa Docker, containers, banco ou serviços auxiliares:

- Containers sobem com um comando?
- Migrations rodam automaticamente e em ordem?
- Ports estão corretos e não colidem?
- Volumes persistem dados entre restarts?
- Health checks passam?
- Rebuild funciona após mudança de código?
- `.env.example` está atualizado?

### 5. Verificação de agente (se aplicável)

Se o projeto tem agente AI, tools, prompts ou loop autônomo:

- O loop termina?
- Há max iterations, timeout e limites claros?
- Tools executam corretamente?
- Erro em uma tool é tratado?
- O agente não alucina tools?
- O custo por interação está aceitável?
- O contexto está controlado?

### 6. Integridade de dados

- Dados persistem entre restarts?
- Migrations preservam dados?
- Operações destrutivas pedem confirmação?
- Dados sensíveis estão protegidos?
- Há risco de corrupção em concorrência?
- Backups existem ou são possíveis?

### 7. Verificação manual

Navegue pela aplicação como um usuário faria:

- Toda página carrega?
- Formulários submetem e validam?
- Mensagens de erro fazem sentido?
- Loading states estão tratados?
- Empty states existem?
- Funciona em mobile?
- Os fluxos mais importantes estão íntegros?

### 8. Check de performance

- Tempo de carregamento de página
- Tempo de resposta de API
- Bundle size
- Requests desnecessários
- Memory leaks
- Re-render desnecessário
- API calls redundantes
- Uso excessivo de LLM

### 9. Check de custo

Se usa APIs pagas:

- Quantas calls um fluxo gera?
- O contexto enviado é o mínimo necessário?
- Há chamadas redundantes?
- Background tasks geram custo desnecessário?
- O custo por usuário faz sentido?

### 10. Acessibilidade básica

- Contraste atende WCAG AA?
- Navegação por teclado funciona?
- Focus states existem?
- Imagens têm alt text?
- Formulários têm labels?
- Elementos interativos são claros?

---

## Modo E2E Seguro (quando aplicável)

Ative este modo quando o pedido envolver:

- browser testing
- testes end-to-end
- jornadas completas do usuário
- regressão de interface
- screenshots
- validação de fluxo real no navegador

Este modo existe para testar **com segurança**.

### O que este modo faz

- Analisa o códigobase
- Descobre como iniciar a aplicação
- Mapeia rotas, jornadas e componentes
- Testa fluxos no navegador
- Valida efeitos no banco com queries seguras
- Captura screenshots
- Gera relatório final

### O que este modo NÃO faz por padrão

- Não modifica código-fonte
- Não auto-fixa bugs durante a execução
- Não roda contra banco de produção
- Não executa queries destrutivas
- Não instala dependências globais
- Não aplica mudanças sem pedido explícito

Se o usuário quiser correções depois, primeiro entregue o report. Só aplique fixes numa segunda etapa, conscientemente.

---

## Condições obrigatórias de segurança

Antes de rodar qualquer E2E, valide:

- Ambiente isolado: Docker, CI, WSL, macOS ou Linux
- Banco descartável ou de teste
- `.env` apontando para banco de teste
- Ausência de dados reais de clientes
- Sem risco de produção

Se qualquer condição falhar: **pare**.

---

## Fase 0 — Environment Safety Check

### 1. Platform Check

Use:

```bash
uname -s
```

Suportado:

- Linux
- Darwin (macOS)

Se estiver em Windows nativo:

- Exigir WSL, Docker, Linux ou macOS
- Não prosseguir

### 2. Production Database Protection

Antes de rodar, verifique variáveis como `DATABASE_URL`.

Exemplo de proteção:

```bash
if [[ "$DATABASE_URL" == *"prod"* ]] || [[ "$DATABASE_URL" == *"production"* ]]; then
  echo "Refusing to run against production database."
  exit 1
fi
```

Se `DATABASE_URL` não existir:

- pare
- peça configuração de banco de teste

### 3. Frontend Detection

Verifique:

- `package.json`
- `index.html`
- `pages/` ou `app/`
- `src/components/`

Se não houver frontend navegável:

- não force browser testing
- use testes de API/integração em vez disso

### 4. Browser Tooling

Verifique a ferramenta de browser antes de começar.

Exemplo:

```bash
npx agent-browser --version
```

Se não estiver disponível, instalar como dependência de desenvolvimento do projeto, nunca globalmente.

---

## Fase 1 — Pesquisa paralela (read-only)

Antes de abrir o browser, levante contexto em paralelo.

### Subagente 1 — Estrutura da aplicação

Retorne:

- Como iniciar a app
- URL
- Porta
- Fluxo de autenticação
- Todas as rotas/páginas
- Todas as jornadas do usuário
- Componentes interativos relevantes

Regra:

- somente leitura
- não modificar arquivos

### Subagente 2 — Análise de banco

Leia `.env.example` e os arquivos relevantes de schema/configuração.

Retorne:

- Tipo de banco
- Nome da variável de conexão
- Schema principal
- Fluxo de dados por ação do usuário
- Queries `SELECT` para validar cada fluxo

Regra:

- sem queries destrutivas
- sem alterar dados
- preferir documentação e schema antes de tocar no banco

### Subagente 3 — Bug hunt sem fixing

Retorne:

- Erros de lógica
- Problemas de UI/UX
- Riscos de integridade de dados
- Falhas de segurança
- Suspeitas de regressão

Inclua:

- arquivo
- linha
- severidade
- fix sugerido em diff-style

Regra:

- não editar arquivos

---

## Fase 2 — Start da aplicação

Suba a aplicação com os comandos adequados ao stack.

Exemplo comum:

```bash
npm install
npm run dev &
```

Depois abra a aplicação:

```bash
npx agent-browser open <url>
```

Capture screenshot inicial:

```bash
mkdir -p e2e-screenshots
npx agent-browser screenshot e2e-screenshots/00-initial-load.png
```

---

## Fase 3 — Criação de tarefas por jornada

Crie uma tarefa para cada jornada do usuário.

Cada tarefa deve conter:

- nome da jornada
- passos
- resultado esperado
- pontos de validação
- query de validação, se aplicável
- riscos conhecidos
- screenshot obrigatória

Adicione também uma tarefa final para:

- responsividade
- console errors
- estados vazios
- estados de erro
- comportamento pós-navegação

---

## Fase 4 — Teste das jornadas do usuário

### Browser Commands

Exemplo de comandos:

```bash
npx agent-browser open <url>
npx agent-browser snapshot -i
npx agent-browser click @eN
npx agent-browser fill @eN "texto"
npx agent-browser select @eN "opcao"
npx agent-browser press Enter
npx agent-browser screenshot <path>
npx agent-browser console
npx agent-browser errors
```

### Após cada interação

Sempre:

- espere network idle quando fizer sentido
- capture screenshot
- verifique console
- verifique erros
- valide se a UI está coerente
- faça novo snapshot após navegação relevante

### O que validar em cada jornada

- A ação foi concluída?
- O usuário recebeu feedback adequado?
- A navegação foi correta?
- O estado final é consistente?
- O dado persistiu como esperado?
- Houve erro silencioso?
- Houve quebra visual?
- O loading foi tratado?

---

## Validação de banco (SELECT only)

Quando necessário, valide os efeitos com queries de leitura.

### Postgres

```bash
psql "$DATABASE_URL" -c "SELECT * FROM users WHERE email='test@test.com';"
```

### SQLite

```bash
sqlite3 db.sqlite "SELECT * FROM users WHERE email='test@test.com';"
```

### Nunca execute em modo E2E seguro

- `DELETE`
- `UPDATE`
- `DROP`
- `TRUNCATE`
- `ALTER`
- qualquer mutação manual de dados

Se o fluxo exigir reset de ambiente, isso deve ser feito por seed/migration/setup controlado, nunca por improviso durante o teste.

---

## Tratamento de issues encontradas

Se um problema aparecer, documente:

- esperado vs atual
- jornada afetada
- screenshot
- erros de console
- resultado da query de validação
- severidade
- fix sugerido

Em E2E seguro:

- não modifique arquivos durante a descoberta
- não “conserte no susto”
- primeiro reporte com clareza

---

## Teste responsivo

Teste, no mínimo:

### Mobile

```bash
npx agent-browser set viewport 375 812
```

### Tablet

```bash
npx agent-browser set viewport 768 1024
```

### Desktop

```bash
npx agent-browser set viewport 1440 900
```

Capture screenshots das páginas e fluxos principais.

Cheque:

- overflow
- quebra de layout
- tap target
- conteúdo escondido
- botões inacessíveis
- modais quebrados
- scroll travado

---

## Fase 5 — Cleanup

Depois dos testes:

```bash
kill %1
npx agent-browser close
```

Se o comando real de cleanup for outro, adapte ao stack.

---

## Formato do output

### SUITE DE TESTES

Rodou: X testes  
Passando: X  
Falhando: X  
Skipped: X  
Cobertura: X%

### GAPS ENCONTRADOS

[Prioridade] Descrição — teste escrito: sim/não

### INFRAESTRUTURA

[Check]: passou/falhou "detalhes"

### AGENTE (se aplicável)

[Check]: passou/falhou "detalhes"

### INTEGRIDADE DE DADOS

[Check]: passou/falhou "detalhes"

### VERIFICAÇÃO MANUAL

[Página/Fluxo]: passou/falhou "detalhes"

### PERFORMANCE

[Métrica]: valor "aceitável/precisa atenção"

### CUSTO (se aplicável)

[Operação]: X calls, ~$Y por execução

### E2E REPORT (se aplicável)

Jornadas testadas: X  
Screenshots capturadas: X  
Issues encontradas: X

#### Alta severidade

- ...

#### Média severidade

- ...

#### Baixa severidade

- ...

#### Fixes sugeridos (não aplicados)

- arquivo:linha

Screenshots salvas em:
`e2e-screenshots/`

### VEREDICTO

Pronto pra shippar / X issues pra corrigir primeiro

---

## Regras

- Não só rode testes. Pense no que DEVERIA ser testado.
- Não reporte “tudo passando” sem checar se os testes testam a coisa certa.
- Todo gap importante deve virar teste, caso documentado ou finding acionável.
- Seja minucioso. Não valide só o happy path.
- Infraestrutura conta como teste. Container que não sobe é bug.
- Custo conta como métrica. API call desnecessária é desperdício.
- Em E2E seguro, não modifique código por padrão.
- Em E2E seguro, não rode contra produção.
- Em E2E seguro, não execute queries destrutivas.
- Se houver risco de ambiente real, pare.
- Se algo estiver quebrado, entregue evidência clara e fix sugerido.
- Se não houver frontend navegável, não force browser testing. Troque para API/integration testing.
- O padrão: você deployaria isso com confiança numa sexta à noite.
