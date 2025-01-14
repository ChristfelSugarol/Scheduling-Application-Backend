import json
import random
from costs import check_hard_constraints, subjects_order_cost, empty_space_groups_cost, empty_space_teachers_cost, \
    free_hour
from model import Class, Classroom, Data
from constants import *

def get_type(a):
    return type(a).__name__

def load_data(file_path, teachers_empty_space, groups_empty_space, subjects_order):
    """
    Loads and processes input data, initialises helper structures.
    :param file_path: path to file with input data
    :param teachers_empty_space: dictionary where key = name of the teacher, values = list of rows where it is in
    :param groups_empty_space: dictionary where key = group index, values = list of rows where it is in
    :param subjects_order: dictionary where key = (name of the subject, index of the group), value = [int, int, int]
    where ints represent start times (row in matrix) for types of classes P, V and L respectively. If start time is -1
    it means that that subject does not have that type of class.
    :return: Data(groups, teachers, classes, classrooms)
    """

    data = data = json.loads(json.loads(file_path))
    print(get_type(file_path))

    # classes: dictionary where key = index of a class, value = class
    classes = {}
    # classrooms: dictionary where key = index, value = classroom name
    classrooms = {}
    # teachers: dictionary where key = teachers' name, value = index
    teachers = {}
    # groups: dictionary where key = name of the group, value = index
    groups = {}
    class_list = []

    for cl in data['Casovi']:
        new_group = cl['Grupe']
        new_teacher = cl['Nastavnik']

        # initialise for empty space of teachers
        if new_teacher not in teachers_empty_space:
            teachers_empty_space[new_teacher] = []


        new = Class(new_group, new_teacher, cl['Predmet'], cl['Tip'], cl['Trajanje'], cl['Ucionica'], cl['Definite'], cl['Laboratory'], cl['Break'], cl["MathSci"])

        # add groups
        for group in new_group:
            if group not in groups:
                groups[group] = len(groups)
                # initialise for empty space of groups
                groups_empty_space[groups[group]] = []

        # add teacher
        if new_teacher not in teachers:
            teachers[new_teacher] = len(teachers)
        class_list.append(new)

    # shuffle mostly because of teachers
    random.shuffle(class_list)
    # add classrooms
    for cl in class_list:
        classes[len(classes)] = cl

    # every class is assigned a list of classrooms he can be in as indexes (later columns of matrix)
    for type in data['Ucionice']:
        for name in data['Ucionice'][type]:
            new = Classroom(name, type)
            classrooms[len(classrooms)] = new

    # every class has a list of groups marked by its index, same for classrooms
    for i in classes:
        cl = classes[i]

        classroom = cl.classrooms
        index_classrooms = []
        # add classrooms
        for index, c in classrooms.items():

            if c.type == classroom:
                index_classrooms.append(index)
        cl.classrooms = index_classrooms

        class_groups = cl.groups
        index_groups = []
        for name, index in groups.items():
            if name in class_groups:
                # initialise order of subjects
                if (cl.subject, index) not in subjects_order:
                    subjects_order[(cl.subject, index)] = [-1, -1, -1]
                index_groups.append(index)
        cl.groups = index_groups

    teacher_availability = {}
    
    for teacher in data['Teacher_Availability']:
        teacher_availability[teacher["Name"]] = [teacher["Mon"], teacher["Tue"], teacher["Wed"], teacher["Thu"], teacher["Fri"]]

    subject_availability = {}
    
    for subject in data['Subject_Availability']:
        subject_availability[subject["Name"]] = [subject["Mon"], subject["Tue"], subject["Wed"], subject["Thu"], subject["Fri"]]

    return Data(groups, teachers, classes, classrooms, teacher_availability, subject_availability)

def set_up(num_of_columns):
    """
    Sets up the timetable matrix and dictionary that stores free fields from matrix.
    :param num_of_columns: number of classrooms
    :return: matrix, free
    """
    total_periods = 5*NUMBER_OF_PERIODS

    w, h = num_of_columns, total_periods                                       # 5 (workdays) * 12 (work hours) = 60
    matrix = [[None for x in range(w)] for y in range(h)]
    free = []

    # initialise free dict as all the fields from matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            free.append((i, j))
    return matrix, free


def show_timetable(matrix, data):
    """
    Prints timetable matrix.
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

    # print heading for classrooms
    for i in range(len(matrix[0])):
        if i == 0:
            print('{:17s} C{:6s}'.format('', '0'), end='')
        else:
            print('C{:6s}'.format(str(i)), end='')
    print()

    d_cnt = 0
    h_cnt = 0
    for i in range(len(matrix)):
        day = days[d_cnt]
        hour = hours[h_cnt]
        print('{:10s} {:2d} ->  '.format(day, hour), end='')
        for j in range(len(matrix[i])):
            # print('{:6s} '.format(str(matrix[i][j])), end='')

            if matrix[i][j] is not None:
                print('{:6s} '.format(str(data.classes[matrix[i][j]].subject) + str(matrix[i][j])), end='')
            else:
                print('{:6s} '.format(str(matrix[i][j])), end='')

        print()
        h_cnt += 1
        if h_cnt == NUMBER_OF_PERIODS:
            h_cnt = 0
            d_cnt += 1
            print()

def show_statistics(matrix, data, subjects_order, groups_empty_space, teachers_empty_space, filled):
    """
    Prints statistics.
    """
    cost_hard = check_hard_constraints(matrix, data, filled)
    if cost_hard == 0:
        print('Hard constraints satisfied: 100.00 %')
    else:
        print('Hard constraints NOT satisfied, cost: {}'.format(cost_hard))
    print('Soft constraints satisfied: {:.02f} %\n'.format(subjects_order_cost(subjects_order)))

    empty_groups, max_empty_group, average_empty_groups = empty_space_groups_cost(groups_empty_space)
    print('TOTAL empty space for all GROUPS and all days: ', empty_groups)
    print('MAX empty space for GROUP in day: ', max_empty_group)
    print('AVERAGE empty space for GROUPS per week: {:.02f}\n'.format(average_empty_groups))

    empty_teachers, max_empty_teacher, average_empty_teachers = empty_space_teachers_cost(teachers_empty_space)
    print('TOTAL empty space for all TEACHERS and all days: ', empty_teachers)
    print('MAX empty space for TEACHER in day: ', max_empty_teacher)
    print('AVERAGE empty space for TEACHERS per week: {:.02f}\n'.format(average_empty_teachers))

    f_hour = free_hour(matrix)
    if f_hour != -1:
        print('Free term ->', f_hour)
    else:
        print('NO hours without classes.')
