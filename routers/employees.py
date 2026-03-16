from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from database import get_db
from models import Employee

router = APIRouter(prefix="/employees", tags=["employees"])


class EmployeeCreate(BaseModel):
    full_name: str
    job_title: str
    country: str
    salary: float

    @field_validator("salary")
    @classmethod
    def salary_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("salary must be a positive number")
        return v


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    country: Optional[str] = None
    salary: Optional[float] = None

    @field_validator("salary")
    @classmethod
    def salary_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("salary must be a positive number")
        return v


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    job_title: str
    country: str
    salary: float


@router.get("", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")
    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, updates: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee


@router.post("", response_model=EmployeeResponse, status_code=201)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(
        full_name=employee.full_name,
        job_title=employee.job_title,
        country=employee.country,
        salary=employee.salary,
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
