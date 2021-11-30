from falcon import HTTPInternalServerError, HTTPBadRequest, HTTP_201
from sqlalchemy.exc import IntegrityError

from app.models import City
from app.log import get_logger

LOG = get_logger()


class CityListResource:
    def on_get(self, req, resp):
        session = req.context.session
        cities = session.query(City).all()
        result = []
        for city in cities:
            result.append(city.todict())

        req.context.result = result

    def on_post(self, req, resp):
        session = req.context.session
        doc = req.context.doc

        try:
            city = City.add_city(**doc)
            session.add(city)
            session.commit()
        except IntegrityError as ie:
            LOG.error("Error occurred while adding city: %s", ie)
            raise HTTPBadRequest(title="Bad Request", description="City already exists")
        except Exception as ex:
            LOG.error("Error occurred while adding rental_zone: %s", ex)
            raise HTTPInternalServerError(title="Error Occurred", description="Team has been notified.")

        req.context.result = city.todict()
        resp.status = HTTP_201
