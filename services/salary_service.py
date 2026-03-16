def calculate_salary(employee):
    gross = employee.salary
    deductions = {}

    if employee.country == "India":
        deductions["tds"] = round(gross * 0.10, 2)
    elif employee.country == "United States":
        deductions["tds"] = round(gross * 0.12, 2)

    total_deductions = sum(deductions.values())
    net_salary = gross - total_deductions

    return {
        "gross_salary": gross,
        "deductions": deductions,
        "net_salary": net_salary,
    }


def get_metrics(employees):
    if not employees:
        return None
    salaries = [e.salary for e in employees]
    return {
        "min_salary": min(salaries),
        "max_salary": max(salaries),
        "average_salary": sum(salaries) / len(salaries),
    }
