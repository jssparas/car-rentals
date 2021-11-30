import json

from app.tests import constants


def add_car(client, payload):
    url = '/cars'
    return client.simulate_post(url, headers=constants.APP_HEADERS, body=json.dumps(payload))


def setup_car_data(client):
    # add car 1
    payload = {
        "name": "creta",
        "rental_zone_id": 1,
        "registration_no": "R1"
    }
    car1_res = add_car(client, payload)

    # add car 2
    payload = {
        "name": "creta",
        "rental_zone_id": 2,
        "registration_no": "R2"
    }
    car2_res = add_car(client, payload)

    return car1_res.json.get('id'), car2_res.json.get('id')


def book_car(client, car_id, from_date_str, to_date_str):
    payload = {
        "car_id": car_id,
        "from_date": from_date_str,
        "to_date": to_date_str
    }
    url = "/car-bookings"
    response = client.simulate_post(url, headers=constants.APP_HEADERS, body=json.dumps(payload))
    return response
