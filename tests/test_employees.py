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
        # salary missing
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
