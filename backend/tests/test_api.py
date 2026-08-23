"""End-to-End-Smoke-Tests über alle 6 Kern-Features (siehe Implementierungsplan)."""


def test_register_and_login(client):
    response = client.post("/auth/register", json={"username": "neu", "password": "supersicher123"})
    assert response.status_code == 201

    response = client.post("/auth/login", data={"username": "neu", "password": "supersicher123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_unauthenticated_request_is_rejected(client):
    response = client.get("/animals")
    assert response.status_code == 401


def test_category_browsing(client, auth_headers):
    response = client.get("/categories", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get("/animals?category=saeugetier", headers=auth_headers)
    assert response.status_code == 200
    assert all(a["category"] == "saeugetier" for a in response.json())


def test_seeing_animal_marks_it_seen_and_updates_progress(client, auth_headers):
    response = client.get("/animals", headers=auth_headers)
    animal_id = response.json()[0]["id"]

    response = client.post(f"/animals/{animal_id}/seen", headers=auth_headers)
    assert response.status_code == 204

    response = client.get("/progress", headers=auth_headers)
    assert response.json()["seen_count"] == 1

    response = client.get("/animals", headers=auth_headers)
    seen_flags = {a["id"]: a["seen"] for a in response.json()}
    assert seen_flags[animal_id] is True


def test_daily_animal_is_stable_across_calls(client, auth_headers):
    first = client.get("/daily-animal", headers=auth_headers).json()
    second = client.get("/daily-animal", headers=auth_headers).json()
    assert first["id"] == second["id"]


def test_discover_returns_an_animal(client, auth_headers):
    response = client.get("/discover/next", headers=auth_headers)
    assert response.status_code == 200
    assert "name_de" in response.json()


def test_quiz_flow_updates_spaced_repetition(client, auth_headers):
    question = client.get("/quiz/next", headers=auth_headers).json()
    animal_id = question["animal"]["id"]
    assert len(question["options"]) >= 2
    assert any(o["animal_id"] == animal_id for o in question["options"])

    response = client.post(
        "/quiz/answer",
        json={"animal_id": animal_id, "selected_animal_id": animal_id},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["correct"] is True
    assert body["repetitions"] == 1
    assert body["interval_days"] == 1

    response = client.post(
        "/quiz/answer",
        json={"animal_id": animal_id, "selected_animal_id": -1},
        headers=auth_headers,
    )
    body = response.json()
    assert body["correct"] is False
    assert body["repetitions"] == 0
