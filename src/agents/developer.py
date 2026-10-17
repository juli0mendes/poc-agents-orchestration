from langchain_ollama import ChatOllama

from src.models.implementation import Implementation
from src.tools.workspace import materialize_implementation
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
- Use Spring Boot 3.x.
- Follow the provided architecture.
- Apply Clean Architecture principles.
- Apply DDD where appropriate.
- Generate production-quality code.

MAVEN PROJECT REQUIREMENTS:

- Generate a complete Maven project.
- Always include a pom.xml file at the project root.
- The pom.xml must declare all required dependencies.
- Configure Maven to compile using Java 21.
- Follow the standard Maven directory structure.
- Generate unit tests using JUnit 5.
- Include the Spring Boot Maven plugin.
- The generated project must support execution with mvn test.

SOURCE CODE REQUIREMENTS:

- Every generated file must contain its complete content.
- Include all required classes, methods, imports and configuration files.
- Ensure package declarations match their directory paths.
- Ensure all referenced classes and methods exist.
- Use APIs compatible with Spring Boot 3.x and Spring Security 6.
- Do not omit code with placeholders such as "TODO", "...", or comments
  saying that implementation was omitted.
- Keep the implementation focused on the requirements.

FILE GENERATION RULES:

- Return all project files as a structured list.
- Each file must contain its relative path and complete content.
- The pom.xml path must be exactly "pom.xml".
- Java source files must be under src/main/java/.
- Java test files must be under src/test/java/.
- Configuration files must be under src/main/resources/.
- Each iteration must return the complete project, not only changed files.
- Do not generate Docker, Kubernetes, Terraform or cloud infrastructure yet.

If a previous QA report exists, fix all reported issues
in the new implementation.

Do not simply repeat the previous implementation.
The new implementation must incorporate the QA feedback.
"""

    implementation = structured_llm.invoke(prompt)

    materialize_implementation(implementation)

    generated_files = [file.path for file in implementation.files]

    print(f"[DEVELOPER] Generated {len(generated_files)} files")

    for path in generated_files:
        print(f"  - {path}")

    if "pom.xml" not in generated_files:
        print("[DEVELOPER] WARNING: pom.xml was not generated")

    return {
        "implementation": implementation,
        "iteration": next_iteration,
        "status": "DEVELOPER_COMPLETED",
    }