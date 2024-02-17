#!/usr/bin/python3
""" new class for sqlAlchemy """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """ create tables in environmental"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary"""
        obj_dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                obj_dic[key] = elem
        else:
            objs = [State, City]
            for c in objs:
                query = self.__session.query(c)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    obj_dic[key] = elem
        return obj_dic

    def new(self, obj):
        """adds a new element
        """
        self.__session.add(obj)

    def save(self):
        """saves changes
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete element
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """configuration
        """
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()

    def close(self):
        "Calls remove"
        self.__session.remove()
