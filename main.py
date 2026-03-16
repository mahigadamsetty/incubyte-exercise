from fastapi import FastAPI
from database import Base, engine
from routers import employees, salary

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Incubyte Salary Management API")

app.include_router(employees.router)
app.include_router(salary.router)
