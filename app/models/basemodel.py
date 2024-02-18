#!/usr/bin/python3
"""class BaseModel that defines all common attributes/methods for other classes"""

import os
import sys
import datetime
import models
import uuid
from os import getenv
from flask import app
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_type == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def save(self):
        """Updates the public instance attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_fs=None):
        """Returns a dictionary containing all keys/valus of `__dict__` of the instance
        by using self.__dict__, only instance attributes will be returned
        a key __class__ is added to this dictionary with the class name of the object
        created_at and updated_at is converted to string in ISO format
        """
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime("%Y-%m-%dT%H:%M:%S")
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime("%Y-%m-%dT%H:%M:%S")
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict
    
    def delete(self):
        """drops the current instance from storage"""
        models.storage.delete(self)
    
    def __str__(self):
        """Returns a string representation of the instance"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)