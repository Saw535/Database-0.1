from faker import Faker
from models import Student, Group, Teacher, Subject, Grade, session, Base
from sqlalchemy import inspect

def seed_data():
    fake = Faker()

    inspector = inspect(session.get_bind())

    if not inspector.has_table('students'):
        print("Creating database tables...")
        Base.metadata.create_all(session.get_bind())
        print("Database tables created successfully.")
    else:
        print("Database tables already exist.")

    groups = [Group(name=f"Group-{i}") for i in range(1, 4)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(name=fake.name()) for _ in range(1, 6)]
    session.add_all(teachers)
    session.commit()

    subjects = [Subject(name=f"Subject-{i}", teacher=teachers[i % len(teachers)]) for i in range(1, 9)]
    session.add_all(subjects)
    session.commit()

    students = [Student(name=fake.name(), group=groups[i % len(groups)]) for i in range(1, 51)]
    session.add_all(students)
    session.commit()

    for student in students:
        for subject in subjects:
            teacher_name = subject.teacher.name
            grade = fake.random_int(min=1, max=12)
            grade = Grade(student=student, subject_name=subject.name, teacher_name=teacher_name, grade=grade)
            session.add(grade)
            session.commit()

if __name__ == "__main__":
    seed_data()