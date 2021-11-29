from sqlalchemy import Column, DateTime, func, Integer
from sqlalchemy.ext.declarative import declarative_base


class BaseModel(object):
    """
    All models will inherit from this base model
    """
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=func.now())
    modified_on = Column(DateTime, default=func.now(), onupdate=func.now())

    def todict(self):
        """
        Utility to convert a row to a dict
        """
        # ref: https://stackoverflow.com/a/1960546
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


Base = declarative_base(cls=BaseModel)
