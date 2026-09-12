# Agents overview

This project contains agent implementations under `src/agents/` coordinated by the orchestration PoC.

Key points related to CI:
- Agents code is NOT modified by CI; CI only runs build/tests and may open PRs.
- Tests for agents (if present) run in `feature-unit-tests` and `main` pipelines.
- The CI may push a README update (coverage badge) back to the triggering feature branch so the badge appears in the PR.

Local run quickstart:
- python -m venv .venv && source .venv/bin/activate
- python -m pip install -e .
- pytest -q

Files of interest:
- src/agents/*.py
- src/graph.py (wiring of agents)
- src/state.py (AgentState)
