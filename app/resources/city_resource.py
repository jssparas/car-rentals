import falcon

from app.models import City


class CityListResource:
    def on_get(self, req, resp):
        session = req.context.session
        cities = session.query(City).all()
        result = []
        for city in cities:
            result.append(city.todict())

        req.context.result = result
