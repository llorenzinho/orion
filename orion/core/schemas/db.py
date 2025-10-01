from pydantic import BaseModel


class DBConnectionTestResult(BaseModel):
    success: bool
    message: str = ""
