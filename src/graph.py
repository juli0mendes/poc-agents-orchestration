from langgraph.graph import StateGraph, START, END

from src.agents.pm import pm_agent
from src.agents.architect import architect_agent
from src.agents.developer import developer_agent
from src.agents.qa import qa_agent

from src.state import AgentState


def sre_agent(state: AgentState):
    print("[SRE] Executando...")

    return {
        "status": "SRE_COMPLETED"
    }


MAX_ITERATIONS = 3


def qa_router(state: AgentState):
    iteration = state.get("iteration", 0)
    status = state.get("status")

    print(
        f"[ROUTER] QA status={status}, "
        f"iteration={iteration}/{MAX_ITERATIONS}"
    )

    if status == "QA_PASSED":
        return "sre"

    if iteration >= MAX_ITERATIONS:
        print("[ROUTER] Limite de iterações atingido.")
        return "sre"

    return "developer"


builder = StateGraph(AgentState)

builder.add_node("pm", pm_agent)
builder.add_node("architect", architect_agent)
builder.add_node("developer", developer_agent)
builder.add_node("qa", qa_agent)
builder.add_node("sre", sre_agent)

builder.add_edge(START, "pm")
builder.add_edge("pm", "architect")
builder.add_edge("architect", "developer")
builder.add_edge("developer", "qa")

builder.add_conditional_edges(
    "qa",
    qa_router,
    {
        "developer": "developer",
        "sre": "sre",
    }
)

builder.add_edge("sre", END)

graph = builder.compile()