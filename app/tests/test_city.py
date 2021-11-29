import json

from app.tests import constants


def test_get_cities(client, db):
    url = '/cities'
    response = client.simulate_get(url)

    assert response.status_code == 200
    # pre-seeded data
    assert len(response.json) == 2
    for city in response.json:
        assert city.get('name') is not None


def test_add_city(client, db):
    url = '/cities'
    payload = {
        "name": "wuhan"
    }
    response = client.simulate_post(url, headers=constants.APP_HEADERS, body=json.dumps(payload))

    print(response.json)
    assert response.status_code == 201
    assert response.get('name') == 'wuhan'
