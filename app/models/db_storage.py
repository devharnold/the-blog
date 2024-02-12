#!/usr/bin/python3

"""
Define storage engine
"""
from os import getenv
from sqlalchemy import create_engine
from models.posts import Posts
from models.settings import Settings
from models.user import User
from models.base_model import BaseModel,Base
from models.file_storage import FileStorage
from sqlalchemy.orm import relationships, scoped_session, sessionmaker

class DBStorage:
    """Replicates a database storage engine
    
    Attributes:
        __engine(SQLAlchemy engine): The working SQLAlchemy engine
        __session(sqlalchemy.session): The working SQLAlchemy session
    """
    __engine = None
    __session = None

    def __init__(self):
        """initializes a new storage instance"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(getenv("THEBLOG_MYSQL_USER"),
                                                                           getenv("THEBLOG_MYSQL_PWD"),
                                                                           getenv("THELOG_MYSQL_HOST"),
                                                                           getenv("THEBLOG_MYSQL_DB"),
                                                                           pool_pre_ping = True))
        if getenv("HBLOG_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current db session of all objects on the given class
        if cls is none, queries all types pf objects
        Return: Dict ofqueried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            objs =self.__session.query(User).all()
            objs.extend(self.__session.query(Settings).all())
            objs.extend(self.__session.query(Posts).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            obj = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}
    
    def new(self, obj):
        """add obj to current db session"""
        self.__session.add(obj)

    def save(self):
        """commit the change to current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current db session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the db and initialize a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(session_factory)
        self.__session = session()

    def close(self):
        """close the active SQLAlchemy session"""
        self.__session.close()
