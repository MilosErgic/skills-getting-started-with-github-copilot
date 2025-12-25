from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

client = TestClient(app)

def test_root_redirects_to_static():
    resp = client.get("/")
    assert resp.status_code in (200, 307, 308)

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.parametrize("activity_name,email", [
    ("Chess Club", "newstudent@mergington.edu"),
])
def test_signup_and_unregister(activity_name, email):
    # Ensure clean state: remove if exists
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity_name]["participants"]

    # Signing up again should fail
    resp2 = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp2.status_code == 400

    # Unregister
    resp3 = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert resp3.status_code == 200
    assert email not in activities[activity_name]["participants"]

    # Unregistering again should return 404
    resp4 = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert resp4.status_code == 404
