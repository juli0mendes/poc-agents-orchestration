from pydantic import BaseModel


class SourceFile(BaseModel):
    path: str
    content: str


class Implementation(BaseModel):
    summary: str
    files: list[SourceFile]