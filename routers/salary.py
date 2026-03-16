from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Employee
from services.salary_service import calculate_salary, get_metrics

router = APIRouter(tags=["salary"])


@router.get("/employees/{employee_id}/salary")
def get_employee_salary(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")
    return calculate_salary(employee)


@router.get("/salary/metrics")
def salary_metrics(country: Optional[str] = None, job_title: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Employee)
    if country:
        query = query.filter(Employee.country == country)
    if job_title:
        query = query.filter(Employee.job_title == job_title)
    employees = query.all()
    metrics = get_metrics(employees)
    if metrics is None:
        filter_desc = country or job_title
        raise HTTPException(status_code=404, detail=f"No employees found for '{filter_desc}'")
    return metrics
