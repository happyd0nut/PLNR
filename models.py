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
    tasks = relationship("Task", ) # stopped here 4/26/23

    def __init__(self, first_name, last_name, email, username, password): 
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password


class Enrollment (Base):
    __tablename__ = "enrollments"

    id = Column("id", INTEGER, primary_key=True)
    user_id = Column("user_id", INTEGER, ForeignKey("users.id"), nullable=False)
    class_id = Column("class_id", INTEGER, ForeignKey("classes.id"), nullable=False)

    def __init__(self, user_id, class_id): 
        self.user_id = user_id
        self.class_id = class_id


class Class (Base):
    __tablename__ = "classes"

    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    teacher = Column("teacher", TEXT)
    period = Column("period", TEXT)
    subject = Column("password", TEXT)

    def __init__(self, name, teacher, period, subject): 
        self.name = name
        self.teacher = teacher
        self.period = period
        self.subject = subject

class Task (Base):
    __tablename__ = "tasks"

    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    due_date = Column("due_date", INTEGER)
    notes = Column("period", TEXT)
    class_id = Column("class_id", INTEGER, nullable=False)
    user_id = Column("user_id", INTEGER, nullable=False)

    def __init__(self, name, due_date, notes, class_id, user_id): 
        self.name = name
        self.due_date = due_date
        self. notes = notes
        self.class_id = class_id
        self. user_id = user_id