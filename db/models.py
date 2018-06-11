from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func, UniqueConstraint

from db.base import Base, inverse_relationship, create_tables 

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    fullname = Column(String)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    
    show_id = Column(Integer)
    user_id = Column(Integer)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())



# class Movie(Base):
#     __tablename__ = 'movies'
#     id = Column(Integer, primary_key=True)

#     fullname = Column(String)
#     username = Column(String)
#     email = Column(String, unique=True)
#     password = Column(String)

#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())