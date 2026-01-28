from pydantic import BaseModel
from typing import List, Dict

class EndpointInfo(BaseModel):
    method: str
    path: str
    description: str

class HealthResponse(BaseModel):
    status: str
    database: str
    hostname: str
    db_host: str

class RootResponse(BaseModel):
    message: str
    version: str
    hostname: str
    endpoints: List[EndpointInfo]
