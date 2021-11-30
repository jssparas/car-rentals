import json

from app.tests import constants


def test_get_rental_zones(client, db):
    url = '/rental-zones'

    # search without city should raise 400
    response = client.simulate_get(url)
    assert response.status_code == 400
    assert "Please provide valid city_id" in response.json.get('description')

    # pre-seeded data
    url = '/rental-zones?city_id=2'
    response = client.simulate_get(url)
    assert len(response.json) == 2
    for rz in response.json:
        assert rz.get('name') is not None
        assert rz.get('city') is not None


def test_add_rental_zone(client, db):
    url = '/rental-zones'
    # valid case
    payload = {
        "city_id": 2,
        "name": "RZ5"
    }
    response = client.simulate_post(url, headers=constants.APP_HEADERS, body=json.dumps(payload))
    assert response.status_code == 201
    assert response.json.get('name') == 'RZ5'
    assert response.json.get('city').get('id') == 2

    # invalid city
    payload = {
        "city_id": 3,
        "name": "RZ5"
    }
    response = client.simulate_post(url, headers=constants.APP_HEADERS, body=json.dumps(payload))
    assert response.status_code == 400
    assert "Please provide valid city_id" in response.json.get('description')

    # duplicate rental_zone name
    payload = {
        "city_id": 2,
        "name": "RZ5"
    }
    response = client.simulate_post(url, headers=constants.APP_HEADERS, body=json.dumps(payload))
    assert response.status_code == 400
    assert "Rental zone with this name already exists" in response.json.get('description')
