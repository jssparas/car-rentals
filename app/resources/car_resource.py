from falcon import HTTPBadRequest, before, HTTPInternalServerError
from sqlalchemy import exists, or_, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from cerberus import Validator
from app.models import Car, RentalZone, City,CarBooking
from app.log import get_logger
from app.utils import errors_to_desc
from datetime import date, timedelta

LOG = get_logger()


class BookingDatesValidator(Validator):
    def _validate_depends_on_col(self, col_name, field, value):
        """
         Custom dependencies tests
        """
        if col_name == 'from_date':
            if self.document.get(col_name) > value:
                self._error(field, f"`{field}` must be greater than or equal to `{col_name}`")


def validate_car_data(req, resp, resource, params):
    doc = req.context.doc
    schema = {
        'name': {
            'required': True,
            'type': 'string',
            'empty': False
        },
        'rental_zone_id': {
            'required': True,
            'type': 'integer',
        },
        'registration_no': {
            'required': True,
            'type': 'string',
            'empty': False
        },
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


def validate_rental_zone(req, res, resource, params):
    session = req.context.session
    doc = req.context.doc
    if not session.query(exists().where(RentalZone.id == doc.get('rental_zone_id'))).scalar():
        raise HTTPBadRequest(title="Bad Request", description="Please provide valid rental_zone_id")


def validate_car(req, res, resource, params):
    session = req.context.session
    doc = req.context.doc
    if not session.query(exists().where(Car.id == doc.get('car_id'))).scalar():
        raise HTTPBadRequest(title="Bad Request", description="Please provide valid car_id")


def validate_carbooking_data(req, resp, resource, params):
    doc = req.context.doc
    schema = {
        'car_id': {
            'required': True,
            'type': 'integer',
        },
        'from_date': {
            'required': True,
            'type': 'date',
            'min': date.today(),
            'max': date.today() + timedelta(days=59)
        },
        'to_date': {
            'required': True,
            'type': 'date',
            'min': date.today(),
            'max': date.today() + timedelta(days=59),
            'depends_on_col': 'from_date'
        },
    }

    # validate input
    try:
        v = BookingDatesValidator(schema)
        if not v.validate(doc):
            raise HTTPBadRequest(title='Some parameters are invalid',
                                 description=errors_to_desc(v.errors))
    except Exception as ex:
        if isinstance(ex, HTTPBadRequest):
            raise ex
        raise HTTPBadRequest(title='Bad request', description='Error validating request')


def validate_against_exiting_bookings(req, resp, resource, params):
    session = req.context.session
    doc = req.context.doc
    from_date = doc.get('from_date')
    to_date = doc.get('to_date')
    if session.query(exists().where(CarBooking.car_id == doc.get('car_id')).where(
            or_(and_(CarBooking.from_date >= from_date, CarBooking.from_date <= to_date),
                and_(CarBooking.to_date >= from_date, CarBooking.to_date <= to_date)))).scalar():
        raise HTTPBadRequest(title="Bad Request", description="Booking already done for this period.")


class CarListResource:
    def on_get(self, req, resp):
        session = req.context.session
        # TODO: add available filter
        available_date = req.get_param_as_date('available_date')
        city_id = req.get_param_as_int('city_id')
        cars = session.query(Car).\
            options(joinedload('rental_zone').joinedload('city')).\
            join(RentalZone, RentalZone.id == Car.rental_zone_id).\
            join(City, City.id == RentalZone.city_id).\
            filter(City.id == city_id)

        result = []
        for car in cars:
            result.append(car.todict())
        req.context.result = result

    @before(validate_car_data)
    @before(validate_rental_zone)
    def on_post(self, req, resp):
        session = req.context.session
        doc = req.context.doc

        try:
            car = Car.add_car(**doc)
            session.add(car)
            session.commit()
        except IntegrityError as ie:
            LOG.error("Error occurred while adding car: %s", ie)
            raise HTTPBadRequest(title="Error Occurred", description="Model number already exists")
        except Exception as ex:
            LOG.error("Error occurred while adding rental_zone: %s", ex)
            raise HTTPInternalServerError(title="Error Occurred", description="Team has been notified.")

        req.context.result = car.todict()


class CarBookingListResource:
    def on_get(self, req, resp):
        session = req.context.session
        city_id = req.get_param_as_int('city_id')
        car_bookings = session.query(CarBooking). \
            options(joinedload('car')). \
            join(Car, Car.id == CarBooking.car_id). \
            join(RentalZone, RentalZone.id == Car.rental_zone_id). \
            join(City, City.id == RentalZone.city_id).\
            filter(City.id == city_id)

        result = []
        for car_b in car_bookings:
            car_b_data = car_b.todict()
            car_b_data.pop('car_id')
            car_b_data['car'] = car_b.car.todict()
            result.append(car_b_data)
        req.context.result = result

    @before(validate_carbooking_data)
    @before(validate_car)
    @before(validate_against_exiting_bookings)
    def on_post(self, req, resp):
        session = req.context.session
        doc = req.context.doc

        try:
            car_b = CarBooking.add_car_booking(**doc)
            session.add(car_b)
            session.commit()
        except IntegrityError as ie:
            LOG.error("Error occurred while adding car: %s", ie)
            raise HTTPBadRequest(title="Error Occurred", description="Model number already exists")
        except Exception as ex:
            LOG.error("Error occurred while adding rental_zone: %s", ex)
            raise HTTPInternalServerError(title="Error Occurred", description="Team has been notified.")

        req.context.result = car_b.todict()
