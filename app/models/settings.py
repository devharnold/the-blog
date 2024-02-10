#!/usr/bin/python3
"""Defines the Settings class"""
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, ForeignKey
from models.base_model import BaseModel, Base

class Settings(BaseModel, Base):
    """Replicates the MySQL table for Settings class
    inherits from SQLAlchemy base and links to the Profile MySQL table
    Attributes:
        __tablename__(str): The Settings table-name
        name(sqlalchemy String): The Settings name
        user_profile(sqlalchemy relationship): User-Settings Relationship
    """
    __tablename__ = "settings"
    name = Column(String(128), nullable=False)
    user_settings = relationship("User", secondary="user_settings", viewonly=False)
    post_settings = relationship("Post", secondary="post_settings", viewonly=False)