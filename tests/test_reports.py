def test_hired_per_quarter(client):
    response = client.get("/report/hired-per-quarter")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_departments_above_average(client):
    response = client.get("/report/above-average-hiring")
    assert response.status_code == 200
    assert isinstance(response.json(), list)