# AGENTS.md

## Visão geral

Este repositório é uma PoC (proof of concept) para aplicar conhecimento sobre GenAI e orchestration de agentes. A ideia central é demonstrar um workflow de agentes de IA em Python, onde cada agente assume um papel específico no ciclo de desenvolvimento de software: Product Manager, Architect, Developer, QA e SRE.

O projeto usa LangChain + LangGraph para orquestrar chamadas estruturadas a um modelo local de LLM via Ollama. As saídas dos agentes são modeladas com Pydantic para manter contratos e facilitar a validação do que cada etapa produz.

## Licença

Este projeto é distribuído sob a MIT License. O texto completo da licença está em `LICENSE` e deve ser mantido junto ao código e à documentação do repositório.

## Arquitetura do projeto

A estrutura principal está em `src/`:

- `src/main.py`: ponto de entrada do workflow. Executa o estado inicial e imprime os artefatos gerados.
- `src/graph.py`: define o grafo de estados com `StateGraph` do LangGraph e as transições entre agentes.
- `src/state.py`: `AgentState`, estrutura de tipos do workflow.
- `src/agents/`: agentes especializados
  - `pm.py`: gera requisitos a partir da tarefa.
  - `architect.py`: define a arquitetura com base nos requisitos.
  - `developer.py`: produz implementação estruturada em arquivos.
  - `qa.py`: valida a implementação e identifica problemas.
  - `sre.py`: estágio de operação/observabilidade (atualmente placeholder).
- `src/models/`: modelos Pydantic de domínio do workflow
  - `requirements.py`: requisitos, critérios de aceitação e NFR.
  - `architecture.py`: componentes, endpoints, persistência e stack tecnológica.
  - `implementation.py`: arquivos gerados e conteúdo.
  - `qa.py`: relatório de qualidade.
- `src/persistence/sqlite.py`: persistência do estado em SQLite na pasta `data/`.
- `data/`: dados locais do projeto, incluindo banco SQLite do workflow.

Fluxo principal:

1. PM gera requisitos.
2. Architect projeta a solução.
3. Developer implementa.
4. QA valida o resultado e retorna feedback.
5. O router decide se continua para refinamento ou encerra no SRE.

## Linguagens e frameworks

- Python 3.12+
- Pydantic v2
- LangChain
- LangGraph
- LangChain Ollama
- SQLite (persistência de estado do workflow)
- uv como gerenciador de dependências/execução

Também há indicação de stack alvo para o software gerado pelos agentes:

- Java 21
- Spring Boot
- Clean Architecture
- DDD (quando apropriado)
- API REST

## LLM e modelos

A PoC usa um modelo local com Ollama e `ChatOllama`.

Modelo atual configurado no projeto:

- `qwen3:8b`

Local de uso:

- `src/agents/pm.py`
- `src/agents/architect.py`
- `src/agents/developer.py`
- `src/agents/qa.py`

Os agentes usam `with_structured_output(...)` para obter respostas em modelos Pydantic e manter estrutura de dados consistente.

## Como instalar SDKs e dependências

Pré-requisitos:

- Python 3.12+
- uv (`pip install uv` ou via Homebrew)
- Ollama instalado e em execução

Instalação:

```bash
cd /caminho/para/o/repo
uv sync
```

Se preferir um ambiente virtual manual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

Dependências explícitas do projeto:

```toml
langchain
langchain-ollama
langgraph
pydantic
python-dotenv
```

## Como listar, instalar, executar e invocar LLM localmente

### Verificar e listar modelos locais

```bash
ollama list
curl http://localhost:11434/api/tags
```

### Instalar um modelo local

```bash
ollama pull qwen3:8b
```

### Executar o modelo localmente no terminal

```bash
ollama run qwen3:8b
```

### Testar invocação direta via prompt

```bash
ollama run qwen3:8b "Explique em 3 frases o que é orchestration de agentes em GenAI."
```

### Iniciar o serviço Ollama

```bash
ollama serve
```

## Como executar o projeto

A execução principal do workflow:

```bash
cd /caminho/para/o/repo
uv run python src/main.py
```

Também é possível usar o entry point do pacote, se houver instalação local disponível:

```bash
uv run poc-agents-orchestration
```

## Padrão de código

- Preferir código Python tipado.
- Usar Pydantic para contratos e estruturas de saída de LLM.
- Manter nomes claros e autoexplicativos.
- Priorizar composição de agentes e workflows explícitos em vez de lógica acoplada.
- Escrever prompts em inglês, pois o projeto usa agentes LLM instruídos nesse idioma.
- O projeto tem exemplos em português em `task` e nos artefatos do workflow, mas os prompts de agentes e a modelagem de saídas devem manter clareza e consistência.

## Segurança e conformidade

- Nunca commitar segredos, tokens, chaves ou `API keys`.
- Usar `.env` para configurações locais quando necessário.
- Não armazenar dados sensíveis em `data/` ou em logs de execução.
- Validar saídas estruturadas com Pydantic antes de usar em etapas subsequentes.
- Evitar depender de APIs externas em ambientes de demonstração/local.

## Comandos úteis

### Build / empacotamento

```bash
uv build
```

### Compilação/validação de sintaxe

```bash
python3 -m compileall src
```

### Testes

Não há suíte de testes configurada no repositório neste momento. Se testes forem adicionados mais tarde, a convenção natural é:

```bash
uv run pytest
```

### Docker

Este repositório não possui Dockerfile, Compose ou infraestrutura definida. Não criar arquivos de CI ou de orquestração de container neste escopo.

## Observações para agentes de IA

- Mantenha mudanças focadas e minimamente invasivas.
- Não altere a lógica de orquestração sem necessidade.
- Sempre que modificar documentação ou prompts, preserve o objetivo da PoC: demonstrar orchestration de agentes com LLM local.
- Prefira ajustes em arquivos de documentação ou instruções em vez de reescrever a arquitetura existente.
- Caso seja necessário introduzir uma mudança de runtime, mantenha compatibilidade com `LangGraph`, `Pydantic` e `Ollama`.
