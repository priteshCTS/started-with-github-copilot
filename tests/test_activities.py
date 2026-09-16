from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def reset_activities():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
    activities["Basketball Team"]["participants"] = []
    activities["Track and Field"]["participants"] = []
    activities["Art Club"]["participants"] = []
    activities["Drama Club"]["participants"] = []
    activities["Debate Club"]["participants"] = []
    activities["Science Club"]["participants"] = []


def test_get_activities_returns_activity_list():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload
    assert "Gym Class" in payload


def test_signup_for_activity_adds_participant():
    # Arrange
    reset_activities()
    email = "student@example.edu"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


def test_signup_for_activity_rejects_duplicate_registration():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    reset_activities()
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == f"Removed {email} from Chess Club"


def test_unregister_missing_participant_returns_404():
    # Arrange
    reset_activities()
    email = "notregistered@example.edu"

    # Act
    response = client.delete(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_signup_for_unknown_activity_returns_404():
    # Arrange
    reset_activities()
    email = "student@example.edu"

    # Act
    response = client.post("/activities/Unknown Activity/signup?email=student@example.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
