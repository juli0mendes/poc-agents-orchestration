# PoC Agents Orchestration

Projeto em Python que orquestra agentes (PM, Architect, Developer, QA, SRE) usando LangGraph e LangChain com integração local ao Ollama.

## Linguagem

- Python >= 3.12

## Bibliotecas principais

As dependências estão declaradas em pyproject.toml (versões mínimas):

- langchain >= 1.3.18
- langchain-ollama >= 1.1.0
- langgraph >= 1.2.11
- pydantic >= 2.13.5
- python-dotenv >= 1.2.3

(Ver `pyproject.toml` para referência.)

## Como instalar dependências

1. Criar e ativar um ambiente virtual:

   - macOS / Linux:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

2. Atualizar pip e instalar o pacote localmente:

   ```bash
   python -m pip install --upgrade pip
   pip install -e .
   ```

Isso instalará as dependências listadas em `pyproject.toml`.

## Como rodar local

- Executar o fluxo principal:

  ```bash
  python src/main.py
  ```

  O script inicializa um fluxo de orquestração (graph) e imprime requirements, arquitetura e implementação gerados pelos agentes.

## Uso da LLM local (Ollama)

O projeto usa `langchain-ollama` para conectar-se a um servidor Ollama executando localmente.

Passos mínimos:

1. Instalar Ollama (https://ollama.com):
   - macOS (Homebrew): `brew install ollama`
   - Linux / outras plataformas: seguir instruções oficiais em https://ollama.com

2. Baixar o modelo usado pelo projeto (exemplo):

   ```bash
   ollama pull qwen3:8b
   ```

3. Garantir que o daemon do Ollama esteja disponível. Verificar com:

   ```bash
   ollama ls
   ```

4. O cliente `langchain-ollama` conecta ao daemon local no endpoint padrão (http://localhost:11434). Se o Ollama estiver em outro host/porta, exporte uma variável de ambiente apontando para a API do Ollama antes de rodar o script (exemplo):

   ```bash
   export OLLAMA_API_BASE=http://host:11434
   ```

Observação: o código já referencia o modelo `qwen3:8b` nas instâncias de ChatOllama dentro de `src/agents/`.

## Comandos úteis

- Instalar dependências:
  - `pip install -e .`
- Executar o programa:
  - `python src/main.py`
- Trabalhar com Ollama:
  - `ollama pull qwen3:8b`  # baixar modelo
  - `ollama ls`            # listar modelos disponíveis
- Empacotar / instalar (opcional):
  - `python -m pip install .`

## Docker (exemplo)

Não há Dockerfile no repositório por padrão. Exemplo mínimo para containerizar a aplicação:

1. Dockerfile (exemplo):

```
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
COPY src ./src
RUN python -m pip install --upgrade pip && pip install -e .
CMD ["python", "src/main.py"]
```

2. Build e run:

```bash
docker build -t poc-agents-orchestration:latest .
```

Para que o container acesse um daemon Ollama rodando no host local, uma opção (mac/linux) é usar `host.docker.internal` como host do Ollama e expor a porta 11434. Ao executar o container, passe a variável de ambiente apontando para o endpoint do Ollama:

```bash
docker run --rm -e OLLAMA_API_BASE=http://host.docker.internal:11434 poc-agents-orchestration:latest
```

Ou executar Ollama também em container e ligar via rede Docker.

## Estrutura principal

- src/
  - agents/  -> agentes (pm, architect, developer, qa, sre)
  - models/  -> modelos Pydantic para saída estruturada
  - persistence/ -> persistência SQLite (se aplicável)
  - graph.py -> orquestrador de estados (LangGraph)
  - main.py -> ponto de entrada de exemplo

## Observações

- O projeto assume que os agentes irão gerar código Java 21 / Spring Boot (veja prompts em `src/agents/developer.py`).
- Ajustar configurações do Ollama e do modelo conforme necessário (nome do modelo, memória, etc.).
