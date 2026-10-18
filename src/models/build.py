from pydantic import BaseModel


class BuildResult(BaseModel):
    success: bool
    exit_code: int
    stdout: str
    stderr: str