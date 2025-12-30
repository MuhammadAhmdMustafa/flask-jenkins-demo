from app import app

def test_home_route():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert b"Hello from Flask + Jenkins!" in res.data

def test_health_route():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"
