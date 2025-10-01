from pydantic import BaseModel

from orion.core.schemas.db import DBConnectionTestResult


class TestResultSchema(BaseModel):
    db: DBConnectionTestResult
