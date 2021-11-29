from datetime import date, timedelta
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship, backref, validates
from sqlalchemy.dialects.postgresql import ARRAY
from app.models import Base, RentalZone


class Car(Base):
    __tablename__ = 'car'

    name = Column(String)
    registration_no = Column(String, unique=True, nullable=False)
    rental_zone_id = Column(Integer, ForeignKey('rental_zone.id'))
    rental_zone = relationship(RentalZone, backref=backref('cars', uselist=True, cascade='delete,all'))
    availability_for_60_days = Column(ARRAY(Date), default=[])

    @validates('registration_no',)
    def convert_upper(self, key, value):
        return value.upper()

    @classmethod
    def add_car(cls, **doc):
        car = cls(**doc)
        today_ = date.today()
        car.availability_for_60_days = [today_ + timedelta(days=x) for x in range(60)]
        return car
