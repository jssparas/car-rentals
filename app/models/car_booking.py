from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Date, Integer, ForeignKey

from app.models import Base, Car


class CarBooking(Base):
    __tablename__ = 'car_booking'

    car_id = Column(Integer, ForeignKey('car.id'))
    car = relationship(Car, backref=backref('cars', uselist=True, cascade='delete,all'))
    from_date = Column(Date)
    to_date = Column(Date)

    @classmethod
    def add_car_booking(cls, **doc):
        car_booking = cls(**doc)
        return car_booking
