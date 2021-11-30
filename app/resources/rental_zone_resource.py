from cerberus import Validator
from falcon import HTTPBadRequest, before, HTTPInternalServerError, HTTP_201
from sqlalchemy import exists
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

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
        raise HTTPBadRequest(title="Bad Request", description="Please provide valid city_id")


class RentalZoneListResource:
    def on_get(self, req, resp):
        session = req.context.session
        city_id = req.get_param_as_int('city_id')
        if not session.query(exists().where(City.id == city_id)).scalar():
            raise HTTPBadRequest(title="Bad Request", description="Please provide valid city_id")
        rental_zones = session.query(RentalZone).options(joinedload('city')).filter(RentalZone.city_id == city_id)
        result = []
        for rz in rental_zones:
            rz_d = rz.todict()
            rz_d.pop('city_id')
            rz_d['city'] = rz.city.todict()
            result.append(rz_d)

        req.context.result = result

    @before(validate_rental_zone_data)
    @before(validate_city)
    def on_post(self, req, resp):
        session = req.context.session
        doc = req.context.doc

        try:
            rental_zone = RentalZone.add_rental_zone(**doc)
            session.add(rental_zone)
            session.commit()
        except IntegrityError as ie:
            LOG.error("Error occurred while adding rental_zone: %s", ie)
            raise HTTPBadRequest(title="Error Occurred", description="Rental zone with this name already exists")
        except Exception as ex:
            LOG.error("Error occurred while adding rental_zone: %s", ex)
            raise HTTPInternalServerError(title="Error Occurred", description="Team has been notified.")

        rz_d = rental_zone.todict()
        rz_d.pop('city_id')
        rz_d['city'] = rental_zone.city.todict()
        req.context.result = rz_d
        resp.status = HTTP_201


class RentalZoneResource:
    def on_get(self, req, resp, rz_id):
        session = req.context.session
        rental_zone = session.query(RentalZone).get(rz_id)
        if rental_zone:
            rz_d = rental_zone.todict()
            rz_d.pop('city_id')
            rz_d['city'] = rental_zone.city.todict()
            req.context.result = rz_d.todict()
        else:
            raise HTTPBadRequest(title="Bad Request", description="Please provide valid rental_zone id")

    @before(validate_rental_zone_data)
    @before(validate_city)
    def on_patch(self, req, resp, rz_id):
        session = req.context.session
        doc = req.context.doc

        try:
            rental_zone = RentalZone.add_rental_zone(**doc)
            session.add(rental_zone)
            session.commit()
        except Exception as ex:
            LOG.error("Error occurred while adding rental_zone: %s", ex)
            raise HTTPInternalServerError(title="Error Occurred", description="Team has been notified.")

        rz_d = rental_zone.todict()
        rz_d.pop('city_id')
        rz_d['city'] = rental_zone.city.todict()
        req.context.result = rz_d

