class Class:

    def __init__(self, groups, teacher, subject, type, duration, classrooms, definite, laboratory, typeBreak, isMathSci):
        self.groups = groups
        self.teacher = teacher
        self.subject = subject
        self.type = type
        self.duration = duration
        self.classrooms = classrooms
        self.definite = definite
        self.laboratory = laboratory
        self.typeBreak = typeBreak
        self.isMathSci = isMathSci



class Classroom:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return "{}: {}".format(type(self), self.name)

    def __repr__(self):
        return str(self)


class Data:

    def __init__(self, groups, teachers, classes, classrooms, teacher_availability, subject_availability):
        self.groups = groups
        self.teachers = teachers
        self.classes = classes
        self.classrooms = classrooms
        self.teacher_availability = teacher_availability
        self.subject_availability = subject_availability
