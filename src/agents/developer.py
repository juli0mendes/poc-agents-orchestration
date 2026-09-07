from langchain_ollama import ChatOllama

from src.models.implementation import Implementation
from src.state import AgentState


llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)

structured_llm = llm.with_structured_output(Implementation)


def developer_agent(state: AgentState):
    requirements = state["requirements"]
    architecture = state["architecture"]
    qa_report = state.get("qa_report")

    current_iteration = state.get("iteration", 0)
    next_iteration = current_iteration + 1

    prompt = f"""
You are a Senior Software Engineer.

Implement the software described by the requirements and architecture below.

REQUIREMENTS:

{requirements.model_dump_json(indent=2)}

ARCHITECTURE:

{architecture.model_dump_json(indent=2)}

PREVIOUS QA REPORT:

{
    qa_report.model_dump_json(indent=2)
    if qa_report
    else "No previous QA report. This is the first implementation."
}

Rules:

- Use Java 21.
- Use Spring Boot.
- Follow the provided architecture.
- Apply Clean Architecture principles.
- Apply DDD where appropriate.
- Generate production-quality code.
- Generate unit tests for the main business logic.
- Use Maven.
- Every generated file must contain its complete content.
- Do not omit code with placeholders such as "TODO", "...", or comments
  saying that implementation was omitted.
- Keep the implementation focused on the requirements.
- Do not generate Docker, Kubernetes, Terraform or cloud infrastructure yet.

Return the implementation as a structured list of files.

If a previous QA report exists, fix all reported issues
in the new implementation.

Do not simply repeat the previous implementation.
The new implementation must incorporate the QA feedback.
"""

    implementation = structured_llm.invoke(prompt)

    print(
        f"[DEVELOPER] Implementation generated. "
        f"iteration: {current_iteration} -> {next_iteration}"
    )

    return {
        "implementation": implementation,
        "iteration": next_iteration,
        "status": "DEVELOPER_COMPLETED",
    }