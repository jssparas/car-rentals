from sqlalchemy import Column, String
from sqlalchemy.orm import validates

from app.models import Base


class City(Base):
    __tablename__ = 'city'

    name = Column(String, unique=True)

    @validates('name',)
    def convert_upper(self, key, value):
        return value.lower()

    # for adding cities in future
    @classmethod
    def add_city(cls, name):
        city = cls(name=name.lower())
        return city
