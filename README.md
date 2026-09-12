# PoC - Agents Orchestration with GenAI

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Main CI](https://github.com/juli0mendes/poc-agents-orchestration/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/juli0mendes/poc-agents-orchestration/actions/workflows/main.yml)

## Sobre o projeto

Este repositório é uma PoC para aplicar e demonstrar conhecimento sobre GenAI e orchestration de agentes. A proposta é explorar como múltiplos agentes especializados podem cooperar para transformar uma solicitação de negócio em requisitos, arquitetura, implementação e validação, usando modelos de linguagem e fluxos estruturados.

A implementação atual usa. Python com LangChain e LangGraph para orquestrar agentes que desempenham papéis como Product Manager, Architect, Developer, QA e SRE. A execução usa um modelo local via Ollama, com saída estruturada em Pydantic.

## Status de CI

Este repositório inclui automações de validação e entrega contínua em GitHub Actions:

- `feature.yml`: executa build, testes e análise de cobertura em branches de feature; gera artefatos e cria/atualiza PR para `main`.
- `main.yml`: valida `main`, executa testes, calcula versionamento semântico e cria tag/release automática quando os commits seguem a convenção do Conventional Commits.

Essas pipelines ajudam a manter a qualidade do código, a publicar artefatos e a automatizar a revisão e o release do projeto.

## Arquitetura da solução

A arquitetura do workflow segue uma sequência simples e didática:

- PM: interpreta a tarefa e gera requisitos.
- Architect: define a arquitetura técnica proposta.
- Developer: produz a implementação em arquivos estruturados.
- QA: valida a implementação e aponta problemas.
- SRE: etapa final de operação/observabilidade (em evolução).

O estado do workflow é orquestrado com `StateGraph` e persistido em SQLite para registrar o estado de execução.

## Requisitos e execução rápida

### Requisitos

- Git
- Python 3.12+
- uv
- Ollama instalado e em execução

### 1) Instalando Python no macOS/Unix

Se você ainda não tiver Python 3.12+, o jeito mais simples no macOS é via Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Depois da instalação do Homebrew
brew update
brew install python@3.12
```

Verifique a instalação:

```bash
python3 --version
```

Se quiser, também pode usar `pyenv` para gerenciar múltiplas versões do Python:

```bash
brew install pyenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc

pyenv install 3.12.7
pyenv local 3.12.7
```

### 2) Instalando o Ollama no macOS/Unix

O Ollama pode ser instalado via script oficial ou via Homebrew:

```bash
brew install ollama
```

Ou, se preferir seguir a instalação oficial:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Após a instalação, inicie o serviço:

```bash
ollama serve
```

### 3) Instalando o modelo local qwen3:8b

```bash
ollama pull qwen3:8b
```

Verifique se ele foi baixado corretamente:

```bash
ollama list
```

### 4) Instalando o gerenciador de dependências uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Ou com Homebrew:

```bash
brew install uv
```

Confirme:

```bash
uv --version
```

### 5) Clonando o projeto

```bash
git clone https://github.com/<seu-usuario>/poc-agents-orchestration.git
cd poc-agents-orchestration
```

### 6) Instalando as dependências do projeto

No diretório do repositório:

```bash
uv sync
```

Se preferir instalar manualmente em um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

### 7) Executando o workflow

```bash
uv run python src/main.py
```

### 8) Verificando se tudo está pronto

```bash
ollama run qwen3:8b "Teste de conexão. Responda apenas com 'ok'."
```

Se a resposta for `ok`, o modelo local está funcionando corretamente e o projeto pode ser executado.

### Troubleshooting rápido

- Se `python3` não for encontrado: instale o Python 3.12+ com Homebrew ou `pyenv`.
- Se `uv` não for encontrado: confirme a instalação do shell profile e reinicie o terminal.
- Se `ollama serve` falhar: certifique-se de que o Ollama foi instalado corretamente e que o processo não está bloqueado por outra instância.
- Se o modelo `qwen3:8b` não existir localmente: rode `ollama pull qwen3:8b`.
- Se houver erro de importação do Python: confirme que você está no diretório correto e que o ambiente está ativo.

## Stack principal

- Python
- LangChain
- LangGraph
- Pydantic
- SQLite
- Ollama
- qwen3:8b

## Licença

Este projeto está licenciado sob a MIT License. O texto completo da licença está disponível no arquivo [LICENSE](LICENSE).

A licença permite uso, cópia, modificação, fusão, publicação, distribuição e venda do software, desde que o aviso de copyright e a permissão sejam mantidos em todas as cópias e trechos relevantes do código.

## Contribuição

Contribuições são bem-vindas por meio de issues e pull requests. Para manter o projeto consistente com a proposta de PoC, favoreça mudanças pequenas, focadas e bem documentadas, sem alterar a lógica central do workflow de agentes.

Antes de enviar mudanças, valide se a alteração:

- respeita o objetivo educacional e de demonstração do projeto;
- não introduz infraestrutura ou configuração desnecessária;
- mantém compatibilidade com Python, LangChain, LangGraph e Ollama;
- preserva a estrutura documental e o foco em GenAI e orchestration de agentes.

## Observações

- O projeto é experimental e está em construção.
- As instruções de agentes e a documentação foram pensadas para facilitar uso por LLMs e humanos.
- A lógica central não deve ser alterada sem necessidade, para preservar a natureza de prova de conceito.

