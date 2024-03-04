from pydantic import BaseModel

class CategorySchema(BaseModel):
    id: int
    name: str

class ExpenseCreateSchema(BaseModel):
    name: str
    amount: float
    category_id: int
    year: int
    month: int

class ExpenseSchema(BaseModel):
    id: int
    name: str
    amount: float
    category_id: int

    class Config:
        from_attributes = True
