from pydantic import BaseModel, Field

class Requirement(BaseModel):
    id: str = Field(description="Unique requirement identifier")
    description: str = Field(description="Requirement description")

class AcceptanceCriterion(BaseModel):
    id: str = Field(description="Unique acceptance criterion identifier")
    description: str = Field(description="Acceptance criterion")

class Requirements(BaseModel):
    summary: str
    functional_requirements: list[Requirement]
    acceptance_criteria: list[AcceptanceCriterion]
    non_functional_requirements: list[str]