from sqlalchemy import *
from sqlalchemy.orm import relationship

from config import db


class Region(db.Model):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class CarTax(db.Model):
    __tablename__ = 'car_tax'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    from_hp_car = Column(Integer, nullable=False)
    to_hp_car = Column(Integer, nullable=False)
    from_production_year_car = Column(Integer, nullable=False)
    to_production_year_car = Column(Integer, nullable=False)
    rate = Column(Numeric, nullable=False)
    region = relationship('Region', backref='car_tax')


class PropertyTax(db.Model):
    __tablename__ = 'property_tax'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    rate = Column(Numeric, nullable=False)
    region = relationship('Region', backref='property_tax')
