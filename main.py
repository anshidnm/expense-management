from fastapi import FastAPI, Depends, Body, HTTPException
from typing import List
from database import SessionLocal, Base, engine
from models import Category, Expense
from schemas import CategorySchema, ExpenseCreateSchema, ExpenseSchema
from sqlalchemy.orm import Session
from sqlalchemy import func

app = FastAPI(title="Expense management")

Base.metadata.create_all(bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

@app.post("/category", response_model=CategorySchema)
def create_category(
    name: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    try:
        category = Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except:
        raise HTTPException(
            detail="failure", 
            status_code=400
        )

@app.post("/expense", response_model=ExpenseSchema)
def create_expense(
    *,
    db: Session = Depends(get_db),
    data: ExpenseCreateSchema,
):
    creation_data = data.model_dump()
    exp = Expense(**creation_data)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

@app.get("/expenses", response_model=List[ExpenseSchema])
def list_expense(
    db: Session = Depends(get_db),     
):
    data = db.query(Expense).all()
    return data

@app.get("/expenses/month/{year}/{month}", response_model=List[ExpenseSchema])
def filter_expense(
    *,
    db: Session = Depends(get_db),
    year: int,
    month: int
):
    data = db.query(Expense).filter(
        Expense.month==month,
        Expense.year==year
    )
    return data

@app.get("/totals/")
def total_expense(
    *,
    db: Session = Depends(get_db),
):
    data = db.query(
        func.sum(Expense.amount).label("total")
    )
    total = 0
    if data.first():
        total = data.first()[0]
    return {"total": total}