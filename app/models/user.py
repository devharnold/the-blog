#!/usr/bin/python3
"""Defines the User class"""
from flask import Flask
from models.basemodel import Base
from models.basemodel import BaseModel
from sqlalchemy import Column, String, ForeignKey
import sqlalchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)

class User(BaseModel, Base):
    """Represents a MySQL db for User
    Inherits from sqlalchemy base and links to the User MySQL table
    Attributes: 
        __tablename__(str): The name of the MySQL table to store users
        email(sqlalchemy string): The user's email address
        password(sqlalchemy string): User's password
        full_name(sqlalchemy string): User's fullname
        Posts(sqlalchemy relationship): User-Post relationship
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    full_name = Column(String(128), nullable=False)
    posts = relationship("Posts", backref="user", cascade="delete")
    settings = relationship("Settings", backref="user", cascade="delete")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)