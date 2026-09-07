from pydantic import BaseModel

class QAIssue(BaseModel):
    severity: str
    file: str
    description: str
    recommendation: str

class QAReport(BaseModel):
    status: str
    summary: str
    issues: list[QAIssue]