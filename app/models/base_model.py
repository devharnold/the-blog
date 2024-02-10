#!/usr/bin/python3
"""class BaseModel that defines all common attributes/methods for other classes"""

import os
import sys
import datetime
import models
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String

Base = declarative_base()

class BaseModel:
    def __init__(self, *args, **kwargs):
        """
    id: string - assign with an uuid when an instance is created:
    you can use uuid.uuid4() to generate unique id but don’t forget to convert to a string
    the goal is to have unique id for each BaseModel
    created_at: datetime - assign with the current datetime when an instance is created
    updated_at: datetime - assign with the current datetime when an instance is created
    and it will be updated every time you change your object
        """
        self.id == str(uuid.uuid(4))
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, values in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def save(self):
        """Updates the public instance attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        """Returns a dictionary containing all keys/valus of `__dict__` of the instance
        by using self.__dict__, only instance attributes will be returned
        a key __class__ is added to this dictionary with the class name of the object
        created_at and updated_at is converted to string in ISO format
        """
        obj_dict = self.__dict__copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict
    
    def delete(self):
        """drops the current instance from storage"""
        models.storage.delete(self)
    
    def __str__(self):
        """Returns a string representation of the instance"""
        d = self.__dict__.cop
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)