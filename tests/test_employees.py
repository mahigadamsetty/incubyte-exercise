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
