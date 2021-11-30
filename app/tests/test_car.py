import json
from datetime import date, timedelta

from app.tests import constants
from app.tests.helpers import add_car, setup_car_data, book_car
from app.models import Car


def test_add_car(client, db):
    # valid case
    payload = {
        "name": "creta",
        "rental_zone_id": 1,
        "registration_no": "R1"
    }
    response = add_car(client, payload)
    assert response.status_code == 201
    assert response.json.get('name') == 'creta'
    assert len(response.json.get('availability_for_60_days')) == 60
    available_days = sorted(response.json.get('availability_for_60_days'))
    assert available_days[0] == date.today().strftime('%Y-%m-%d')
    assert available_days[-1] == (date.today() + timedelta(days=59)).strftime('%Y-%m-%d')
    assert response.json.get('rental_zone').get('id') == 1

    # invalid rental_zone_id
    payload = {
        "name": "breza",
        "rental_zone_id": 10,
        "registration_no": "R2"
    }
    response = add_car(client, payload)
    assert response.status_code == 400
    assert "Please provide valid rental_zone_id" in response.json.get('description')

    # duplicate registration no
    payload = {
        "name": "creta",
        "rental_zone_id": 1,
        "registration_no": "R1"
    }
    response = add_car(client, payload)
    assert response.status_code == 400
    assert "Registration number already exists" in response.json.get('description')


def test_search_car(client, db):
    car1_id, car2_id = setup_car_data(client)

    # search in a city
    url = '/cars?city_id=1'
    response = client.simulate_get(url)
    assert len(response.json) == 2

    # search in a city on available date
    url = '/cars?city_id=1&available_date=2021-12-12'
    response = client.simulate_get(url)
    assert len(response.json) == 2

    # try setting available dates of one car = []
    db.query(Car).filter(Car.id == car1_id).update({'availability_for_60_days': []})
    db.commit()
    response = client.simulate_get(url)
    assert len(response.json) == 1


def test_search_car_after_booking(client, db):
    car1_id, car2_id = setup_car_data(client)

    # book a car
    book_car(client, car1_id, "2021-12-12", "2021-12-13")
    # search in a city on available date
    url = '/cars?city_id=1&available_date=2021-12-12'
    response = client.simulate_get(url)
    assert len(response.json) == 1

    url = '/cars?city_id=1&available_date=2021-12-13'
    response = client.simulate_get(url)
    assert len(response.json) == 1

    # try searching on some other date 2021-12-13
    url = '/cars?city_id=1&available_date=2021-12-14'
    response = client.simulate_get(url)
    assert len(response.json) == 2
