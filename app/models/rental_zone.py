from app.models import Base, City
from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Boolean,
    func, event, BigInteger, exists, and_, ForeignKey, or_
)
from sqlalchemy.orm import relationship, backref, validates


class RentalZone(Base):
    __tablename__ = 'rental_zone'

    name = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    city = relationship(City, backref=backref('rental_zones', uselist=True, cascade='delete,all'))

    @validates('name',)
    def convert_upper(self, key, value):
        return value.upper()

    @classmethod
    def add_rental_zone(cls, **doc):
        rental_zone = cls(**doc)
        return rental_zone
