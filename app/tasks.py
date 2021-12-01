from datetime import date, timedelta

from app.celery import wdb_session, celery_app, DBTask
from app.models import Car
from app.utils import chunks
from app.log import get_logger

LOG = get_logger()


@celery_app.task(base=DBTask)
def update_available_dates():
    # get all cars
    cars = wdb_session.query(Car.id)

    # for chunks of 10 cars, call update available date
    args = (r.id for r in cars)
    for car_ids in chunks(args, 10):
        update_available_dates_for_a_car.delay(car_ids)


@celery_app.task(base=DBTask)
def update_available_dates_for_a_car(car_ids=[]):
    for car_id in car_ids:
        try:
            car = wdb_session.query(Car).get(car_id)
            available_dates = sorted(car.availability_for_60_days)
            if available_dates[0] < date.today():
                # need to remove yesterday's available date
                available_dates.pop(0)

            # add next available dates after 59th day
            available_dates.append(date.today() + timedelta(days=59))
            car.availability_for_60_days = available_dates
            wdb_session.commit()
        except Exception as ex:
            LOG.error("Error occurred while updating available dates: ", ex)
            wdb_session.rollback()
