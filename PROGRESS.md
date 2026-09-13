# PROGRESS — PoC Agents Orchestration

Última verificação: 2026-09-13T13:01:05.719-03:00

Resumo: verifiquei a implementação atual do repositório e atualizei o status de cada etapa do plano. Para cada etapa há: Estado (Não iniciado / Iniciado / Finalizado), evidência (arquivos relevantes) e próximos passos curtos quando aplicável.

| Etapa                              |       Estado | Evidência                                                     | Observações / Próximos passos                                                                                                                                                    |
|------------------------------------|-------------:|---------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. Preparar o ambiente             |   Finalizado | README.md, .venv (ambiente local de desenvolvimento presente) | Documentação de instalação pronta.                                                                                                                                               |
| 2. Python com uv                   |   Finalizado | pyproject.toml, uv.lock                                       | Projeto empacotado e entrypoint definido.                                                                                                                                        |
| 3. LLM local (Ollama + modelo)     |     Iniciado | src/agents/*.py (usa ChatOllama, modelo `qwen3:8b`)           | Código pronto; requer Ollama e o modelo local rodando (user action: `ollama pull qwen3:8b` e `ollama serve`).                                                                    |
| 4. Estado do workflow (SQLite)     |   Finalizado | src/persistence/sqlite.py, data/agent-state.db                | DB + funções de persistência existem; porém não há chamadas automáticas ao salvar estado no fluxo principal. Próximo passo: integrar chamadas a save_state()/init_db() no fluxo. |
| 5. Criar o Orchestrator            |   Finalizado | src/graph.py (StateGraph, roteamento QA → Developer/SRE)      | Grafo compilado e usado por src/main.py.                                                                                                                                         |
| 6. Criar o PM Agent                |   Finalizado | src/agents/pm.py (structured LLM → Requirements)              | Produz Requirements via Pydantic.                                                                                                                                                |
| 7. Architect Agent                 |   Finalizado | src/agents/architect.py (structured LLM → Architecture)       | Produz Architecture via Pydantic.                                                                                                                                                |
| 8. Developer Agent                 |   Finalizado | src/agents/developer.py (structured LLM → Implementation)     | Produz Implementation (arquivos) via Pydantic e controla iterações.                                                                                                              |
| 9. QA Agent                        |   Finalizado | src/agents/qa.py (structured LLM → QAReport)                  | Produz QAReport e define PASS/FAIL; router usa resultado.                                                                                                                        |
| 10. SRE Agent                      |     Iniciado | src/graph.py (sre_agent stub); src/agents/sre.py (vazio)      | SRE é placeholder — não gera Dockerfile/docker-compose/observability. Próximo passo: implementar geração de artefatos em src/agents/sre.py ou usar um utilitário.                |
| 11. Integração (workflow completo) |   Finalizado | src/main.py (invoca graph.invoke e imprime artefatos)         | Fluxo integrado localmente; cuidado: depende de Ollama e não persiste automaticamente no DB.                                                                                     |
| 12. Hardening / Demo final         | Não iniciado | (nenhum arquivo específico)                                   | Logging, tracing, human approval e limites finos não implementados. Priorizar logging e integração com persistence.                                                              |

---

Detalhamento por etapa

1) Preparar o ambiente — Finalizado
- Evidência: README.md detalha passos; existe .venv no repositório.
- Observação: ambiente de desenvolvimento presente; confirmar que `uv sync` e `uv run` funcionam no host.

2) Python com uv — Finalizado
- Evidência: pyproject.toml, uv.lock e entrypoint em [project.scripts].
- Observação: dependências declaradas (langchain, langgraph, pydantic, langchain-ollama).

3) LLM local — Iniciado
- Evidência: agentes usam ChatOllama(model="qwen3:8b").
- Observação: runtime externo necessário. Executar:
  - ollama pull qwen3:8b
  - ollama serve
  Teste rápido via README: `ollama run qwen3:8b "ok"`.

4) Estado do workflow (SQLite) — Finalizado (parcialmente integrado)
- Evidência: src/persistence/sqlite.py cria tabela e oferece save_state(). data/agent-state.db presente.
- Observação: nenhuma chamada automática ao init_db() ou save_state() no fluxo atual; recomenda-se integrar persistência no builder ou em src/main.py.

5) Orchestrator — Finalizado
- Evidência: src/graph.py implementa StateGraph, nós PM→Architect→Developer→QA→SRE e roteador QA.
- Observação: MAX_ITERATIONS=3 já aplicado no roteador.

6) PM Agent — Finalizado
- Evidência: src/agents/pm.py (usa with_structured_output(Requirements)).

7) Architect Agent — Finalizado
- Evidência: src/agents/architect.py (with_structured_output(Architecture)).

8) Developer Agent — Finalizado
- Evidência: src/agents/developer.py (with_structured_output(Implementation)).
- Observação: gera Implementation estruturada; não escreve arquivos no workspace automaticamente (é um artefato em memória retornado pelo LLM).

9) QA Agent — Finalizado
- Evidência: src/agents/qa.py (with_structured_output(QAReport)).
- Observação: QA retorna status e issues; router converte para QA_PASSED / QA_FAILED.

10) SRE Agent — Iniciado (placeholder)
- Evidência: grafos usam sre_agent em src/graph.py (retorna status simples). src/agents/sre.py está vazio.
- Próximo passo: implementar geração de Dockerfile/docker-compose.yml e um observability.md conforme plano.

11) Integração — Finalizado (condições)
- Evidência: src/main.py invoca graph.invoke(initial_state) e imprime Requirements/Architecture/Implementation.
- Observação: execução completa depende do LLM local; integração com persistence/logging ainda pendente.

12) Hardening / Demo final — Não iniciado
- Falta: logging, tracing (Langfuse), human-in-the-loop approval gate, limites e monitoramento.
- Prioridade recomendada: 1) adicionar logging centralizado (biblioteca logging), 2) salvar estados no SQLite em pontos-chave, 3) implementar SRE artifacts, 4) adicionar um prompt/manual approval antes do SRE.

Ações sugeridas (curto prazo)
- Integrar src/persistence/sqlite.init_db() no startup (src/main.py) e chamar save_state() após cada agente completar.
- Implementar src/agents/sre.py para gerar Dockerfile e docker-compose.yml minimal.
- Adicionar logging básico (Python logging) em cada agente e no router para facilitar debugging.
- Documentar no README os comandos exatos para baixar e iniciar o modelo Ollama (já parcialmente presente).
