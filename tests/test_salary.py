def test_salary_metrics_by_country(client):
    client.post("/employees", json={"full_name": "A", "job_title": "Engineer", "country": "India", "salary": 50000.0})
    client.post("/employees", json={"full_name": "B", "job_title": "Manager", "country": "India", "salary": 90000.0})
    client.post("/employees", json={"full_name": "C", "job_title": "Engineer", "country": "United States", "salary": 120000.0})
    response = client.get("/salary/metrics?country=India")
    assert response.status_code == 200
    data = response.json()
    assert data["min_salary"] == 50000.0
    assert data["max_salary"] == 90000.0
    assert data["average_salary"] == 70000.0


def test_salary_metrics_edge_case_no_employees_country(client):
    response = client.get("/salary/metrics?country=Antarctica")
    assert response.status_code == 404
    assert "no employees found" in response.json()["detail"].lower()


def test_salary_metrics_edge_case_no_employees_job_title(client):
    response = client.get("/salary/metrics?job_title=TimeTraveler")
    assert response.status_code == 404
    assert "no employees found" in response.json()["detail"].lower()


def test_salary_metrics_by_job_title(client):
    client.post("/employees", json={"full_name": "A", "job_title": "Engineer", "country": "India", "salary": 60000.0})
    client.post("/employees", json={"full_name": "B", "job_title": "Engineer", "country": "United States", "salary": 100000.0})
    client.post("/employees", json={"full_name": "C", "job_title": "Manager", "country": "India", "salary": 80000.0})
    response = client.get("/salary/metrics?job_title=Engineer")
    assert response.status_code == 200
    data = response.json()
    assert data["average_salary"] == 80000.0


def test_salary_metrics_job_title_not_found(client):
    response = client.get("/salary/metrics?job_title=Wizard")
    assert response.status_code == 404
    assert "no employees found" in response.json()["detail"].lower()


def test_salary_metrics_country_not_found(client):
    response = client.get("/salary/metrics?country=Narnia")
    assert response.status_code == 404
    assert "no employees found" in response.json()["detail"].lower()


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
