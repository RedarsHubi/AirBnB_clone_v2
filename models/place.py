#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) == "db":
        reviews = relationship("Review", backref="place", cascade="delete")
    else:
        @property
        def reviews(self):
            """Get a list of Reviews linked to Place"""
            reviews_list = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    reviews_list.append(review)
            return reviews_list
