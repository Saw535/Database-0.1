from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    
    group = relationship('Group', back_populates='students')
    grades = relationship('Grade', back_populates='student')

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    students = relationship('Student', back_populates='group')

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    subjects = relationship('Subject', back_populates='teacher')

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    teacher = relationship('Teacher', back_populates='subjects')

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    subject_name = Column(String, ForeignKey('subjects.name'), nullable=False)
    teacher_name = Column(String, ForeignKey('teachers.name'), nullable=False)
    grade = Column(Integer, nullable=False)
    date = Column(DateTime, default=func.now())

    student = relationship('Student', back_populates='grades')

engine = create_engine('sqlite:///project.db')
Session = sessionmaker(bind=engine)
session = Session()