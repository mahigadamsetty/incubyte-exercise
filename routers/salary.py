from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Employee
from services.salary_service import calculate_salary

router = APIRouter(tags=["salary"])


@router.get("/employees/{employee_id}/salary")
def get_employee_salary(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")
    return calculate_salary(employee)
