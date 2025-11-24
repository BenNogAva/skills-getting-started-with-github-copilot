from pathlib import Path
import sys

# Ensure src is importable
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Basic sanity checks
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_unregister():
    activity = "Chess Club"
    test_email = "tester@example.com"

    # Ensure clean state: remove test_email if already present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    if test_email in participants:
        client.delete(f"/activities/{activity}/participants?email={test_email}")

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert test_email in client.get("/activities").json()[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{activity}/participants?email={test_email}")
    assert resp.status_code == 200
    assert test_email not in client.get("/activities").json()[activity]["participants"]
