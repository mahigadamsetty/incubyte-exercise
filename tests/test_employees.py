def test_create_employee(client):
    response = client.post("/employees", json={
        "full_name": "Alice Smith",
        "job_title": "Engineer",
        "country": "India",
        "salary": 75000.0
    })
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Alice Smith"
    assert data["job_title"] == "Engineer"
    assert data["country"] == "India"
    assert data["salary"] == 75000.0
    assert "id" in data


def test_create_employee_missing_field(client):
    response = client.post("/employees", json={
        "full_name": "Bob Jones",
        "job_title": "Manager",
        "country": "India"
    })
    assert response.status_code == 422


def test_create_employee_invalid_salary(client):
    response = client.post("/employees", json={
        "full_name": "Carol White",
        "job_title": "Analyst",
        "country": "India",
        "salary": -1000.0
    })
    assert response.status_code == 422


def test_get_employee_by_id(client):
    created = client.post("/employees", json={
        "full_name": "Alice Smith",
        "job_title": "Engineer",
        "country": "India",
        "salary": 75000.0
    }).json()
    response = client.get(f"/employees/{created['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["full_name"] == "Alice Smith"


def test_get_employee_not_found(client):
    response = client.get("/employees/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_employees(client):
    client.post("/employees", json={"full_name": "Alice", "job_title": "Engineer", "country": "India", "salary": 50000.0})
    client.post("/employees", json={"full_name": "Bob", "job_title": "Manager", "country": "US", "salary": 80000.0})
    response = client.get("/employees")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_employees_empty(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json() == []


def test_update_employee(client):
    created = client.post("/employees", json={
        "full_name": "Alice Smith",
        "job_title": "Engineer",
        "country": "India",
        "salary": 75000.0
    }).json()
    response = client.put(f"/employees/{created['id']}", json={"salary": 90000.0, "job_title": "Senior Engineer"})
    assert response.status_code == 200
    data = response.json()
    assert data["salary"] == 90000.0
    assert data["job_title"] == "Senior Engineer"
    assert data["full_name"] == "Alice Smith"


def test_update_employee_not_found(client):
    response = client.put("/employees/9999", json={"salary": 90000.0})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
