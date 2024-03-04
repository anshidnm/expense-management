from database import Base
import sqlalchemy as sa

class Category(Base):
    __tablename__ = "category"
    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    name = sa.Column(sa.String(60), unique=True)

class Expense(Base):
    __tablename__ = "expense"
    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    name = sa.Column(sa.String(60))
    amount = sa.Column(sa.Float)
    category_id = sa.Column(sa.ForeignKey("category.id"))
    year = sa.Column(sa.Integer, default=2024, nullable=True)
    month = sa.Column(sa.Integer, default=3, nullable=True)

