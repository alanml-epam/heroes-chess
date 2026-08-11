"""SQLAlchemy models for the chess training platform domain."""
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    teacher = relationship("Teacher", back_populates="user", uselist=False)
    student = relationship("Student", back_populates="user", uselist=False)


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    user = relationship("User", back_populates="teacher")
    classes = relationship("Class", back_populates="teacher")
    puzzle_sets = relationship("PuzzleSet", back_populates="teacher")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    user = relationship("User", back_populates="student")
    enrollments = relationship("ClassEnrollment", back_populates="student")
    attempts = relationship("Attempt", back_populates="student")


class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    teacher = relationship("Teacher", back_populates="classes")
    enrollments = relationship("ClassEnrollment", back_populates="class_")
    assignments = relationship("Assignment", back_populates="class_")


class ClassEnrollment(Base):
    __tablename__ = "class_enrollments"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    class_ = relationship("Class", back_populates="enrollments")
    student = relationship("Student", back_populates="enrollments")


class PuzzleSet(Base):
    __tablename__ = "puzzle_sets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    teacher = relationship("Teacher", back_populates="puzzle_sets")
    puzzles = relationship("Puzzle", back_populates="puzzle_set")
    assignments = relationship("Assignment", back_populates="puzzle_set")


class Puzzle(Base):
    __tablename__ = "puzzles"
    id = Column(Integer, primary_key=True, index=True)
    puzzle_set_id = Column(Integer, ForeignKey("puzzle_sets.id"), nullable=False)
    fen = Column(String, nullable=False)
    solution = Column(JSON, nullable=False)  # ordered list of UCI/SAN moves
    difficulty = Column(String, nullable=True)
    motif = Column(String, nullable=True)

    puzzle_set = relationship("PuzzleSet", back_populates="puzzles")
    attempts = relationship("Attempt", back_populates="puzzle")


class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    puzzle_set_id = Column(Integer, ForeignKey("puzzle_sets.id"), nullable=False)

    class_ = relationship("Class", back_populates="assignments")
    puzzle_set = relationship("PuzzleSet", back_populates="assignments")
    attempts = relationship("Attempt", back_populates="assignment")


class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    puzzle_id = Column(Integer, ForeignKey("puzzles.id"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=True)
    moves_played = Column(JSON, nullable=True)
    success = Column(Boolean, nullable=False, default=False)
    solve_time = Column(Float, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="attempts")
    puzzle = relationship("Puzzle", back_populates="attempts")
    assignment = relationship("Assignment", back_populates="attempts")
