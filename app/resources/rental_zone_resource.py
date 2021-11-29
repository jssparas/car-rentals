import falcon
from cerberus import Validator
from falcon import (HTTPNotFound, HTTPBadRequest, before,
                    HTTPUnauthorized, HTTP_200, HTTP_201, HTTPInvalidParam)
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exists
from datetime import datetime

from app.utils import errors_to_desc
from app.models import RentalZone, City

from app.log import get_logger

LOG = get_logger()


def validate_rental_zone_data(req, resp, resource, params):
    doc = req.context.doc
    schema = {
        'name': {
            'required': True,
            'type': 'string',
            'empty': False
        },
        'city_id': {
            'required': True,
            'type': 'integer',
        }
    }

    error_message = {
        'name': 'Provide rental zone name',
        'city_id': 'Invalid city id',
    }
    # validate input
    try:
        v = Validator(schema)
        if not v.validate(doc):
            raise HTTPBadRequest(title='Some parameters are invalid',
                                 description=errors_to_desc(v.errors))
    except Exception as ex:
        if isinstance(ex, HTTPBadRequest):
            raise ex
        raise HTTPBadRequest(title='Bad request', description='Error validating request')


def validate_city(req, res, resource, params):
    session = req.context.session
    doc = req.context.doc
    if not session.query(exists().where(City.id == doc.get('city_id'))).scalar():
        raise falcon.HTTPBadRequest(title="Bad Request", description="Please provide valid city_id")


class RentalZoneListResource:
    def on_get(self, req, resp):
        session = req.context.session
        city_id = req.get_param_as_int('city_id')
        if not session.query(exists().where(City.id == city_id)).scalar():
            raise HTTPBadRequest(title="Bad Request", description="Please provide valid city_id")
        rental_zones = session.query(RentalZone).filter(RentalZone.city_id == city_id)
        result = []
        for rz in rental_zones:
            result.append(rz.todict())

        req.context.result = result

    @falcon.before(validate_rental_zone_data)
    @falcon.before(validate_city)
    def on_post(self, req, resp):
        session = req.context.session
        doc = req.context.doc

        try:
            rental_zone = RentalZone.add_rental_zone(**doc)
            session.add(rental_zone)
            session.commit()
        except Exception as ex:
            LOG.error("Error occurred while adding rental_zone: %s", ex)
            raise falcon.HTTPInternalServerError(title="Error Occurred", description="Team has been notified.")

        req.context.result = rental_zone.todict()


class RentalZoneResource:
    def on_get(self, req, resp, rz_id):
        session = req.context.session
        rental_zone = session.query(RentalZone).get(rz_id)
        if rental_zone:
            req.context.result = rental_zone.todict()
        else:
            raise HTTPBadRequest(title="Bad Request", description="Please provide valid rental_zone id")

    @falcon.before(validate_rental_zone_data)
    @falcon.before(validate_city)
    def on_patch(self, req, resp, rz_id):
        session = req.context.session
        doc = req.context.doc

        try:
            rental_zone = RentalZone.add_rental_zone(**doc)
            session.add(rental_zone)
            session.commit()
        except Exception as ex:
            LOG.error("Error occurred while adding rental_zone: %s", ex)
            raise falcon.HTTPInternalServerError(title="Error Occurred", description="Team has been notified.")

        req.context.result = rental_zone.todict()

