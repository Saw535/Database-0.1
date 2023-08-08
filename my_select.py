from models import Student, Group, Teacher, Subject, Grade, session
from sqlalchemy import func, desc

def select_1():
    return session.query(Student.name, func.avg(Grade.grade).label('average_grade')) \
        .join(Grade, Student.id == Grade.student_id) \
        .group_by(Student.name) \
        .order_by(desc('average_grade')) \
        .limit(5) \
        .all()

def select_2(subject_name):
    return session.query(Student.name, func.avg(Grade.grade).label('average_grade')) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subject_name == Subject.name) \
        .filter(Subject.name == subject_name) \
        .group_by(Student.name) \
        .order_by(desc('average_grade')) \
        .first()

def select_3(subject_name):
    subject = session.query(Subject).filter_by(name=subject_name).first()

    if subject is None:
        return "Subject not found."

    average_grades = (
        session.query(Group.name.label("group_name"), func.avg(Grade.grade).label("average_grade"))
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Subject.name == Grade.subject_name)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .all()
    )

    result = "\n".join([f"Group: {group_name}, Average Grade: {average:.2f}" for group_name, average in average_grades])
    return result

def select_4():
    return session.query(func.avg(Grade.grade).label('average_grade')) \
        .scalar()

def select_5(teacher_name):
    teacher = session.query(Teacher).filter_by(name=teacher_name).first()

    if teacher is None:
        return "Teacher not found."

    courses = teacher.subjects
    course_names = [course.name for course in courses]
    return course_names

def select_6(group_name):
    group = session.query(Group).filter_by(name=group_name).first()

    if group is None:
        return "Group not found."

    students_in_group = (
        session.query(Student.name)
        .join(Group, Group.id == Student.group_id)
        .filter(Group.name == group_name)
        .all()
    )

    if not students_in_group:
        return f"No students found in {group_name} group."

    student_names = [student.name for student in students_in_group]
    return ", ".join(student_names)

def select_7(group_name, subject_name):
    group = session.query(Group).filter_by(name=group_name).first()

    if group is None:
        return "Group not found."

    subject = session.query(Subject).filter_by(name=subject_name).first()

    if subject is None:
        return "Subject not found."

    grades_in_group = (
        session.query(Grade)
        .join(Student, Student.id == Grade.student_id)
        .join(Group, Group.id == Student.group_id)
        .join(Subject, Subject.name == Grade.subject_name)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )

    if not grades_in_group:
        return f"No grades found in {group_name} group for {subject_name}."

    grades = [grade.grade for grade in grades_in_group]
    average_grade = sum(grades) / len(grades)
    return f"Average grade in {group_name} group for {subject_name}: {average_grade:.2f}"

def select_8(teacher_name):
    teacher = session.query(Teacher).filter_by(name=teacher_name).first()

    if teacher is None:
        return "Teacher not found."

    grades_given_by_teacher = (
        session.query(Grade)
        .join(Subject, Subject.name == Grade.subject_name)
        .filter(Subject.teacher_id == teacher.id)
        .all()
    )

    if not grades_given_by_teacher:
        return f"No grades given by {teacher_name}."

    grades = [grade.grade for grade in grades_given_by_teacher]
    average_grade = sum(grades) / len(grades)
    return f"Average grade given by {teacher_name}: {average_grade:.2f}"

def select_9(student_name):
    student = session.query(Student).filter_by(name=student_name).first()

    if student is None:
        return "Student not found."

    courses_attended = (
        session.query(Subject.name)
        .join(Grade, Grade.subject_name == Subject.name)
        .filter(Grade.student_id == student.id)
        .distinct()
        .all()
    )

    if not courses_attended:
        return f"{student_name} has not attended any courses."

    course_list = [course[0] for course in courses_attended]
    return f"Courses attended by {student_name}: {', '.join(course_list)}"

def select_10(student_name, teacher_name):
    student = session.query(Student).filter_by(name=student_name).first()

    if student is None:
        return "Student not found."

    teacher = session.query(Teacher).filter_by(name=teacher_name).first()

    if teacher is None:
        return "Teacher not found."

    courses_by_teacher = (
        session.query(Subject.name)
        .join(Grade, Grade.subject_name == Subject.name)
        .filter(Grade.student_id == student.id, Subject.teacher_id == teacher.id)
        .distinct()
        .all()
    )

    if not courses_by_teacher:
        return f"{student_name} is not taking any courses from {teacher_name}."

    course_list = [course[0] for course in courses_by_teacher]
    return f"Courses taken by {student_name} from {teacher_name}: {', '.join(course_list)}"

def main():
    while True:
        print("Select a function:")
        print("1. Find 5 students with the highest average grade")
        print("2. Find the student with the highest average grade in a subject")
        print("3. Find average grades in groups for a subject")
        print("4. Find the overall average grade")
        print("5. Find courses taught by a teacher")
        print("6. Find students in a specific group")
        print("7. Find grades of students in a specific group for a subject")
        print("8. Find the average grade given by a specific teacher")
        print("9. Find courses attended by a specific student")
        print("10. Find courses taught by a specific teacher for a specific student")
        print("0. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '0':
            break
        elif choice == '1':
            result = select_1()
        elif choice == '2':
            subject_name = input("Enter subject name: ")
            result = select_2(subject_name)
        elif choice == '3':
            subject_name = input("Enter subject name: ")
            result = select_3(subject_name)
        elif choice == '4':
            result = select_4()
        elif choice == '5':
            teacher_name = input("Enter teacher name: ")
            result = select_5(teacher_name)
        elif choice == '6':
            group_name = input("Enter group name: ")
            result = select_6(group_name)
        elif choice == '7':
            group_name = input("Enter group name: ")
            subject_name = input("Enter subject name: ")
            result = select_7(group_name, subject_name)
        elif choice == '8':
            teacher_name = input("Enter teacher name: ")
            result = select_8(teacher_name)
        elif choice == '9':
            student_name = input("Enter student name: ")
            result = select_9(student_name)
        elif choice == '10':
            student_name = input("Enter student name: ")
            teacher_name = input("Enter teacher name: ")
            result = select_10(student_name, teacher_name)
        else:
            print("Invalid choice. Please enter a valid option.")

        print("Result:")
        print(result)
        print()

if __name__ == "__main__":
    main()