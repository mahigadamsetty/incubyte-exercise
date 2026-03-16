def test_salary_calculation_employee_not_found(client):
    response = client.get("/employees/9999/salary")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_salary_calculation_other_country(client):
    employee = client.post("/employees", json={
        "full_name": "Hans Muller",
        "job_title": "Engineer",
        "country": "Germany",
        "salary": 100000.0
    }).json()
    response = client.get(f"/employees/{employee['id']}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000.0
    assert data["deductions"] == {}
    assert data["net_salary"] == 100000.0


def test_salary_calculation_united_states(client):
    employee = client.post("/employees", json={
        "full_name": "John Doe",
        "job_title": "Engineer",
        "country": "United States",
        "salary": 100000.0
    }).json()
    response = client.get(f"/employees/{employee['id']}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000.0
    assert data["deductions"]["tds"] == 12000.0
    assert data["net_salary"] == 88000.0


def test_salary_calculation_india(client):
    employee = client.post("/employees", json={
        "full_name": "Ravi Kumar",
        "job_title": "Engineer",
        "country": "India",
        "salary": 100000.0
    }).json()
    response = client.get(f"/employees/{employee['id']}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000.0
    assert data["deductions"]["tds"] == 10000.0
    assert data["net_salary"] == 90000.0
