import pytest 
from werkzeug.exceptions import HTTPException
from app.models.crystal import Crystal


def test_get_all_crystals_returns_empty_list(client):
    pass
    #arrange
    #act
    response = client.get("/crystals")
    response_body = response.get_json() 
    #assert
    assert response.status_code == 200 #list 
    assert response_body == []
    

def test_read_crystal_by_id(client,make_two_crystals):
    response = client.get("/crystals/2")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "name": "garnet",
        "color": "red",  
        "powers": "Awesomeness + protection against disasters"  
        }

def test_create_crystal(client):
    response = client.post("/crystals", json = {
        "name": "tiger's eye",
        "color": "golden brown",
        "powers": "focus the mind, promoting mental clarity, assisting us to resolve problems objectively and unclouded by emotions."
    })

    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body ==  {'message': "tiger's eye was successfully added"}
