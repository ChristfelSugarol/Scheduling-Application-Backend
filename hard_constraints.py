from constants import *
from utils2 import *

def initial_valid_subject_col(matrix, data, row, source):
    subject_container = []
        
    for i in range(0, NUMBER_OF_PERIODS):
        cl_name = data.classrooms[source.classrooms[0]].name
        cl_day = return_day_name_of_row(row)
        
        if matrix[cl_name][cl_day][i] is not None:
            if matrix[cl_name][cl_day][i]["Subject"] in subject_container:
                continue
            else:
                subject_container.append(matrix[cl_name][cl_day][i]["Subject"])

    if source.subject in subject_container:
        return False
    
    return True

def print_day_sched(matrix, data, row, source):
    arr = []
    cl_name = data.classrooms[source.classrooms[0]].name
    cl_day = return_day_name_of_row(row)
        
    print(cl_name)
    print(cl_day)
    print(matrix[cl_name][cl_day])
    for i in range(0, NUMBER_OF_PERIODS): 
        print("___________-")  
        print("{}: {}".format(str(i), matrix[cl_name][cl_day][i] ))    
        print(type(matrix[cl_name][cl_day][i]))
        print(type(matrix[cl_name][cl_day][i]) == type(None))
        if matrix[cl_name][cl_day][i] != None:
            arr.append(matrix[cl_name][cl_day][i]["Subject"])
        else:
            arr.append("None")

    return arr

def initial_valid_subject_day(data, row, source):
    if data.subject_availability[source.subject][get_day_from_period(row)] == 0:
        return False
    
    return True

def initial_valid_teacher_day(data, row, source):
    if data.teacher_availability[source.teacher][get_day_from_period(row)] == 0:
        return False
    
    return True

    
"""def valid_subject_col(matrix, data, row, col, source, p=0):
    subject_container = []

    for i in return_day_range_of_row(row):
        if matrix[i][col] is not None:
            if (data.classes[matrix[i][col]].subject) in subject_container:
                continue
        
            else:
                subject_container.append((data.classes[matrix[i][col]].subject))
    
    if source in subject_container:
        return False
    
    return True"""

def valid_subject_col(matrix, data, row, col, source):
    subject_container = []

    for i in return_day_range_of_row(row):
        if matrix[i][col] is not None:
            if (data.classes[matrix[i][col]].subject) in subject_container:
                continue
        
            else:
                subject_container.append((data.classes[matrix[i][col]].subject))
    
    if source in subject_container:
        return False
    
    return True

def valid_teacher_day(data, row, source):
    if data.teacher_availability[source.teacher][get_day_from_period(row)] == 0:
        return False
    
    return True

def valid_subject_day(data, row, source):
    if data.subject_availability[source.subject][get_day_from_period(row)] == 0:
        return False
    
    return True

def valid_teacher_group_row(matrix, data, index_class, row):
    """
    Returns if the class can be in that row because of possible teacher or groups overlaps.
    """
    c1 = data.classes[index_class]
    for j in range(len(matrix[row])):
        if matrix[row][j] is not None:
            c2 = data.classes[matrix[row][j]]
            
            # check teacher
            if c1.teacher == c2.teacher:
                return False
            # check groups
            for g in c2.groups:
                if g in c1.groups:
                    return False
    return True