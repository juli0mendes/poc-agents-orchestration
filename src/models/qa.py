from enum import Enum
from pydantic import BaseModel

class QAStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"

class QAIssue(BaseModel):
    severity: str
    file: str
    description: str
    recommendation: str

class QAReport(BaseModel):
    status: QAStatus
    summary: str
    issues: list[QAIssue]