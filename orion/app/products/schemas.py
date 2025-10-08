from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    base_price: float
