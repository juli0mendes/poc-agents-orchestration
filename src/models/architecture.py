from pydantic import BaseModel, Field


class Component(BaseModel):
    name: str
    responsibility: str


class ApiEndpoint(BaseModel):
    method: str
    path: str
    description: str


class Architecture(BaseModel):
    overview: str
    components: list[Component]
    api_endpoints: list[ApiEndpoint]
    persistence: str
    security: str
    technology_stack: list[str]