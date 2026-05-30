"""
API tests for the Mergington High School app.
"""

from urllib.parse import quote


def test_get_activities_returns_activity_data(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "participants" in activities["Chess Club"]


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Drama Club"
    email = "testing@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_remove_participant_removes_the_user(client):
    # Arrange
    activity_name = "Art Studio"
    email = "removeuser@mergington.edu"
    signup_path = f"/activities/{quote(activity_name)}/signup"
    delete_path = f"/activities/{quote(activity_name)}/participants"
    client.post(signup_path, params={"email": email})

    # Act
    response = client.delete(delete_path, params={"email": email})

    # Assert
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Gym Class"
    email = "noone@mergington.edu"
    delete_path = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(delete_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
