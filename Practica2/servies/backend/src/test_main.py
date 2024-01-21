from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_team():
    response = client.post("/teams", json={"name": "Real Madrid", "country": "Spain", "description": "Nada"})
    assert response.status_code == 200
    assert response.json() == {"name": "Real Madrid", "country": "Spain", "description": "Nada", "id": 3}


def test_get_team():
    response = client.get("/team/Real%20Madrid")
    assert response.status_code == 200
    assert response.json() == {"name": "Real Madrid", "country": "Spain", "description": "Nada", "id": 3}


def test_put_team_act():
    response = client.put("/teams/Real%20Madrid",
                          json={"name": "Real Madrid", "country": "Spain", "description": "Ganador 14 Champions"})
    assert response.status_code == 200
    assert response.json() == {"name": "Real Madrid", "country": "Spain", "description": "Ganador 14 Champions",
                               "id": 3}


def test_delete_team():
    response = client.delete("/teams/Real%20Madrid")
    assert response.status_code == 200
    assert response.json() == {"name": "Real Madrid", "country": "Spain", "description": "Ganador 14 Champions",
                               "id": 3}


def test_add_competicio():
    response = client.post("/competitions", json={"name": "Test League",
                                                  "category": "Senior",
                                                  "sport": "Football",
                                                  "teams": [
                                                      {
                                                          "id": 2,
                                                          "name": "FCBarcelona",
                                                          "country": "Spain",
                                                          "description": "Millor equip del mon i de Barcelona"
                                                      }
                                                  ]})

    assert response.status_code == 200
    assert response.json() == {"name": "Test League", "category": "Senior", "sport": "Football",
                               "teams": [{"id": 2, "name": "FCBarcelona", "country": "Spain",
                                          "description": "Millor equip del "
                                                         "mon i de "
                                                         "Barcelona"}],
                               "id": 4}


def test_put_competicio():
    response = client.put("/competitions/4", json={"name": "Test League",
                                                   "category": "Junior",
                                                   "sport": "Football",
                                                   "teams": [
                                                       {
                                                           "id": 2,
                                                           "name": "FCBarcelona",
                                                           "country": "Spain",
                                                           "description": "Millor equip del mon i de "
                                                                          "Barcelona"
                                                       }
                                                   ], "id": 4})
    assert response.status_code == 200
    assert response.json() == {"name": "Test League",
                               "category": "Junior",
                               "sport": "Football",
                               "teams": [
                                   {
                                       "id": 2,
                                       "name": "FCBarcelona",
                                       "country": "Spain",
                                       "description": "Millor equip del mon i de Barcelona"
                                   }
                               ], "id": 4}

    def test_put_competicio():
        response = client.put("/competitions/4", json={"name": "Test League",
                                                       "category": "Junior",
                                                       "sport": "Football",
                                                       "teams": [
                                                           {
                                                               "id": 2,
                                                               "name": "FCBarcelona",
                                                               "country": "Spain",
                                                               "description": "Millor equip del mon i de "
                                                                              "Barcelona"
                                                           }
                                                       ], "id": 4})
        assert response.status_code == 200
        assert response.json() == {"name": "Test League",
                                   "category": "Junior",
                                   "sport": "Football",
                                   "teams": [
                                       {
                                           "id": 2,
                                           "name": "FCBarcelona",
                                           "country": "Spain",
                                           "description": "Millor equip del mon i de Barcelona"
                                       }
                                   ], "id": 4}


def test_delete_competicio():
    response = client.delete("/competitions/4")
    assert response.status_code == 200
    assert response.json() == {"name": "Test League",
                               "category": "Junior",
                               "sport": "Football",
                               "teams": [
                                   {
                                       "id": 2,
                                       "name": "FCBarcelona",
                                       "country": "Spain",
                                       "description": "Millor equip del mon i de Barcelona"
                                   }
                               ], "id": 4}
