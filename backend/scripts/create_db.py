import os
from app.database import engine, Base, SessionLocal
from app.auth.hashing import hash_password
from app.models import User, Teacher, Student, Class, ClassEnrollment, Assignment, PuzzleSet, Puzzle, Attempt


def seed_data():
    db = SessionLocal()
    try:
        if db.query(User).first():
            return
        t_pw = hash_password("teacherpass")
        teacher_user = User(email="teacher@example.com", password_hash=t_pw, role="teacher")
        db.add(teacher_user); db.commit(); db.refresh(teacher_user)
        db.add(Teacher(id=teacher_user.id)); db.commit()

        s_pw = hash_password("studentpass")
        student_user = User(email="student@example.com", password_hash=s_pw, role="student")
        db.add(student_user); db.commit(); db.refresh(student_user)
        db.add(Student(id=student_user.id)); db.commit()

        cls = Class(name="Intro to Tactics", teacher_id=teacher_user.id)
        db.add(cls); db.commit(); db.refresh(cls)

        ps = PuzzleSet(title="Starter Puzzles", teacher_id=teacher_user.id)
        db.add(ps); db.commit(); db.refresh(ps)

        p = Puzzle(puzzle_set_id=ps.id, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", solution=["e2e4"])
        db.add(p); db.commit()
    finally:
        db.close()


def create_db(add_seed_data=False):
    Base.metadata.create_all(bind=engine)
    print("Database created at", os.getenv("DATABASE_URL", "sqlite:///./dev.db"))
    if add_seed_data:
        seed_data()




if __name__ == "__main__":
    create_db(add_seed_data=True)
