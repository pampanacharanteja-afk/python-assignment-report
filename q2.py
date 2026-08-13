grades = {
    "math": {"anna": 1.7, "ben": 2.3, "clara": 1.0},
    "physics": {"ben": 3.0, "clara": 1.3, "david": 2.0},
    "art": {"anna": 1.0, "david": 1.7},
}

##  all subjects a student takes
def subjects_of(student):
    subjects = set()

    for subject, students in grades.items():
        if student in students:
            subjects.add(subject)

    return subjects

##  students enrolled in every subject
def takes_all(grades):
    subject_sets = [set(students.keys()) for students in grades.values()]

    if not subject_sets:
        return set()

    return set.intersection(*subject_sets)

## average grade across the students subjects
def student_average(grades, student):
    student_grades = []

    for students in grades.values():
        if student in students:
            student_grades.append(students[student])

    if not student_grades:
        return 0.0

    return round(sum(student_grades) / len(student_grades), 2)

## alphabetically sorted list of students whose average is <= limit
def honor_roll(grades, limit=1.5):
    all_students = set()

    for students in grades.values():
        all_students.update(students.keys())

    honored = []

    for student in all_students:
        if student_average(grades, student) <= limit:
            honored.append(student)

    return sorted(honored)
    
print("Demo... ")

print("Subjects of anna:", subjects_of("anna"))
print("Subjects of ben:", subjects_of("ben"))

print("Students taking all subjects:", takes_all(grades))

print("Anna's average:", student_average(grades, "anna"))
print("Ben's average:", student_average(grades, "ben"))
print("Unknown student's average:", student_average(grades, "eva"))
print("Honor roll:", honor_roll(grades))
