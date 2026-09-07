from langchain_ollama import ChatOllama

from src.models.qa import QAReport
from src.state import AgentState


llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)

structured_llm = llm.with_structured_output(QAReport)


def qa_agent(state: AgentState):
    requirements = state["requirements"]
    architecture = state["architecture"]
    implementation = state["implementation"]

    iteration = state.get("iteration", 0)

    prompt = f"""
You are a Senior QA Engineer.

Review the implementation below against the software requirements
and architecture.

REQUIREMENTS:

{requirements.model_dump_json(indent=2)}

ARCHITECTURE:

{architecture.model_dump_json(indent=2)}

IMPLEMENTATION:

{implementation.model_dump_json(indent=2)}

Your responsibility is to identify defects before the software
is considered ready.

Analyze:

- Compilation errors.
- Missing classes, methods or imports.
- Incorrect package references.
- Type inconsistencies.
- Broken dependencies between classes.
- Requirements that are not implemented.
- Acceptance criteria that are not satisfied.
- Missing or invalid tests.
- Obvious architectural violations.

Rules:

- Do not modify the implementation.
- Do not generate source code.
- Report concrete and actionable issues.
- If there are no relevant issues, return PASSED.
- If there is at least one blocking issue, return FAILED.
- Severity must be one of: CRITICAL, HIGH, MEDIUM, LOW.
- The file field must identify the affected file.
"""

    qa_report = structured_llm.invoke(prompt)

    print(
        f"[QA] {qa_report.status} "
        f"iteration={iteration} "
        f"issues={len(qa_report.issues)}"
    )

    return {
        "qa_report": qa_report,
        "status": "QA_PASSED"
        if qa_report.status == "PASSED"
        else "QA_FAILED",
    }