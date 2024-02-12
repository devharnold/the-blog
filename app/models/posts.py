#!/usr/bin/python3
"""
Defines the Posts class
"""
import models
from models.base_model import BaseModel
from models.base_model import Base
from os import getenv
import sqlalchemy
from sqlalchemy import ForeignKey, Column, String, Table, Integer, Float
from sqlalchemy.orm import relationship


if models.storage_t == 'db':
    post_user = Table('post_user', Base.metadata, Column('place_id', String(60),
                                                         ForeignKey('post.id', onupdate='CASCADE', ondelete='CASCADE'),
                                                         primary_key=True))

class Posts(BaseModel, Base):
    """Represents a MySQL database for Posts
    Inherits from SQLAlchemy Base and links to th MySQL table posts
    Attributes:
    __tablename__: The MySQL table name to store posts
    name (SQLAlchemy String): The name of the post
    blog_id: (sqlalchemy string): The blog_id of the post
    """
    __tablename__ = "posts"
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    post_id = Column(String(128), ForeignKey("post.id"), nullable=False)
    user = relationship("User", backref="Posts", cascade="delete")
    settings = relationship("Settings", backref="posts", cascade="delete")