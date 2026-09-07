from langchain_ollama import ChatOllama

from src.models.requirements import Requirements
from src.state import AgentState

llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)

structured_llm = llm.with_structured_output(Requirements)

def pm_agent(state: AgentState):

    task = state["task"]

    prompt = f"""
You are a Senior Product Manager.

Analyze the software request below and transform it into
clear and testable software requirements.

Software request:

{task}

Rules:
- Do not write source code.
- Identify functional requirements.
- Define acceptance criteria.
- Identify relevant non-functional requirements.
- Keep requirements objective and testable.
- Assume the implementation will use Java 21 and Spring Boot.
"""

    requirements = structured_llm.invoke(prompt)

    print("[PM] Requirements generated.")

    return {
        "requirements": requirements,
        "status": "PM_COMPLETED",
    }