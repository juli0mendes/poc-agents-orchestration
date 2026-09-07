from langchain_ollama import ChatOllama

from src.models.architecture import Architecture
from src.state import AgentState


llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)

structured_llm = llm.with_structured_output(Architecture)


def architect_agent(state: AgentState):
    requirements = state["requirements"]

    prompt = f"""
You are a Senior Software Architect.

Design a technical architecture based on the software requirements below.

Requirements:

{requirements.model_dump_json(indent=2)}

Rules:

- Use Java 21 and Spring Boot.
- Follow Clean Architecture principles.
- Apply DDD where appropriate.
- Design a REST API.
- Define the main application components.
- Define the API endpoints.
- Define the persistence strategy.
- Define the security approach.
- Keep the architecture pragmatic.
- Do not write source code.
"""

    architecture = structured_llm.invoke(prompt)

    print("[ARCHITECT] Architecture generated.")

    return {
        "architecture": architecture,
        "status": "ARCHITECT_COMPLETED",
    }