"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

class User (Base):
    __tablename__ = "users"

    id = Column("id", INTEGER, primary_key=True)
    first_name = Column("first_name", TEXT, nullable=False)
    last_name = Column("last_name", TEXT)
    email = Column("email", TEXT, nullable=False)
    username = Column("username", TEXT, nullable=False)
    password = Column("password", TEXT, nullable=False)
    
    subjects = relationship("Subject", back_populates="user")
    tasks = relationship("Task", back_populates="user")
   

    def __init__(self, first_name, last_name, email, username, password): 
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password


class Subject (Base):
    __tablename__ = "subjects"

    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    teacher = Column("teacher", TEXT)
    period = Column("period", TEXT)
    user_id = Column("user_id", INTEGER, ForeignKey("users.id"))

    user = relationship("User", back_populates="subjects")
    tasks = relationship("Task", back_populates="subject")

    def __init__(self, name, user_id, teacher="", period=""): 
        self.name = name
        self.teacher = teacher
        self.period = period
        self.user_id = user_id


class Task (Base):
    __tablename__ = "tasks"

    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    due_date = Column("due_date", INTEGER)
    notes = Column("notes", TEXT)
    subject_id = Column("subject_id", INTEGER, ForeignKey("subjects.id"), nullable=False)
    user_id = Column("user_id", INTEGER, ForeignKey("users.id"), nullable=False)

    subject = relationship("Subject", back_populates="tasks")
    user = relationship("User", back_populates="tasks")


    def __init__(self, name, subject_id, user_id, due_date="", notes=""): 
        self.name = name
        self.due_date = due_date
        self. notes = notes
        self.subject_id = subject_id
        self. user_id = user_id