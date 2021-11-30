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
    from_date_str = (date.today() + timedelta(days=4)).strftime("%Y-%m-%d")
    to_date_str = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
    book_car(client, car1_id, from_date_str, to_date_str)

    # search in a city on booked dates
    url = f'/cars?city_id=1&available_date={from_date_str}'
    response = client.simulate_get(url)
    assert len(response.json) == 1

    url = f'/cars?city_id=1&available_date={to_date_str}'
    response = client.simulate_get(url)
    assert len(response.json) == 1

    # try searching on some other date 2021-12-13
    url = f'/cars?city_id=1&available_date={(date.today() + timedelta(days=6)).strftime("%Y-%m-%d")}'
    response = client.simulate_get(url)
    assert len(response.json) == 2


def test_car_booking(client, db):
    payload = {
        "name": "creta",
        "rental_zone_id": 1,
        "registration_no": "R1"
    }
    car_resp = add_car(client, payload)
    car_id = car_resp.json.get('id')
    from_date_str = (date.today() + timedelta(days=4)).strftime("%Y-%m-%d")
    to_date_str = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
    book_resp = book_car(client, car_id, from_date_str, to_date_str)
    assert book_resp.status_code == 201
    assert book_resp.json.get('from_date') == from_date_str
    assert book_resp.json.get('to_date') == to_date_str

    # try booking the same car on booked dates
    book_resp = book_car(client, car_id, from_date_str, from_date_str)
    # print(book_resp.json)
    assert book_resp.status_code == 400
    assert "Booking already done for this period" in book_resp.json.get('description')

    # try booking invalid car
    book_resp = book_car(client, 10, from_date_str, from_date_str)
    # print(book_resp.json)
    assert book_resp.status_code == 400
    assert "Please provide valid car_id" in book_resp.json.get('description')
