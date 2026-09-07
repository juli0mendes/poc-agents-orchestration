from typing import TypedDict

from src.models.requirements import Requirements
from src.models.architecture import Architecture
from src.models.implementation import Implementation
from src.models.qa import QAReport


class AgentState(TypedDict, total=False):
    task: str
    requirements: Requirements
    architecture: Architecture
    implementation: Implementation
    qa_report: QAReport
    sre_report: dict
    iteration: int
    status: str