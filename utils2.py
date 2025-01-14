from constants import *
import math
from new_constraints import *

def dict_to_clean_string(d):
    return ' '.join(str(d).split())

def return_day_range_of_row(row):
    if row < (1*NUMBER_OF_PERIODS):
        return range(0, NUMBER_OF_PERIODS-1)
    elif row < (2*NUMBER_OF_PERIODS):
        return range(NUMBER_OF_PERIODS, 2*NUMBER_OF_PERIODS-1)
    elif row < (3*NUMBER_OF_PERIODS):
        return range(2*NUMBER_OF_PERIODS, 3*NUMBER_OF_PERIODS-1)
    elif row < (4*NUMBER_OF_PERIODS):
        return range(3*NUMBER_OF_PERIODS, 4*NUMBER_OF_PERIODS-1)
    else:
        return range(4*NUMBER_OF_PERIODS, 5*NUMBER_OF_PERIODS-1)
    
def return_day_name_of_row(row):
    if row < (1*NUMBER_OF_PERIODS):
        return DAYS[0]
    elif row < (2*NUMBER_OF_PERIODS):
        return DAYS[1]
    elif row < (3*NUMBER_OF_PERIODS):
        return DAYS[2]
    elif row < (4*NUMBER_OF_PERIODS):
        return DAYS[3]
    else:
        return DAYS[4]
    
def get_day_from_period(period):
    return math.floor(period/NUMBER_OF_PERIODS)

def dict_to_array(dict):
    list = []
    for key in dict.keys():
        list.append(key)
        
    return list

def dict_value_to_array(dict):
    list = []
    for key in dict.keys():
        list.append(dict[key])
    
    return list

def intialize_matrix(names, dict):
    for i in range(len(names)):
        teacher = names[i]
        
        dict_teacher = {}
        
        for j in range(NUMBER_OF_DAYS):
            day = DAYS[j]
            
            dict_day = {}
            
            for k in range(NUMBER_OF_PERIODS):
                dict_day[k] = None
                
            dict_teacher[day] = dict_day
    
        dict[teacher] = dict_teacher
    
    return dict

def debug_check(data, matrix, filled):
    section_sched = []
    final_day_sched = {}
    
    for i in range(len(matrix[0])):
        section_sched.append([]) 
 
        
    #Check row of each column
    #If classes with laboratories are in the same row then cost is added
    for row in matrix:
        it = 0
        for col in row:
            if col is not None:
                section_sched[it].append(data.classes[col])
            else:
                section_sched[it].append(None)
            it += 1

    for section_it in range(len(section_sched)):
        section_slot = []
        for i in range(NUMBER_OF_DAYS):
            slot = []
            for j in range((i)*NUMBER_OF_PERIODS, NUMBER_OF_PERIODS*(i+1)):
                if section_sched[section_it][j] is not None:
                    slot.append(section_sched[section_it][j])
                else:
                    slot.append(None)
                
                
            
            section_slot.append(slot)
    
        final_day_sched[section_it] = (section_slot)
    
    section_names = []
    
    #parse section names from data input
    for it in data.classrooms:
        section_names.append(data.classrooms[it].name)
        
    teacher_names = dict_to_array(data.teacher_availability)
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    final_teacher_sched = {}
    
    # Initialize teacher timetable output
    for i in range(len(teacher_names)):
        teacher = teacher_names[i]
        
        dict_teacher = {}
        
        for j in range(NUMBER_OF_DAYS):
            day = days[j]
            
            dict_day = {}
            
            for k in range(NUMBER_OF_PERIODS):
                slot = k
                
                dict_day[k] = None
                
            dict_teacher[day] = dict_day
    
        final_teacher_sched[teacher] = dict_teacher
     
    # Convert Section timetable from rows -> columns
    # Assign values to teacher timetable output   
    dict_output = {}
    for i in range(len(final_day_sched)):
        section = final_day_sched[i]
        
        final_day_sched[section_names[i]] = {}
        
        for j in range(len(section)):
            day = section[j]

            dict_day = {}
            
            final_day_sched[section_names[i]][days[j]] = {}
            for k in range(len(day)):
                subject = day[k]
                
                if subject is not None:
                    final_day_sched[section_names[i]][days[j]][k] = {
                            "Subject": subject.subject,
                            "Teacher": subject.teacher
                        }
                    
                    final_teacher_sched[subject.teacher][str(days[j])][k] = {
                        "Section": str(section_names[i]),
                        "Subject": subject.subject
                    }

                else:
                    final_day_sched[section_names[i]][days[j]][k] = None
                        
    
    # Main Output
    
    
    new_cost_teacher_consecutive = no_consecutive_class(data, filled)
    new_cost_separate_laboratory = separate_laboratory(data, matrix)
    new_cost_mathsci_after_lunch = mathsci_before_lunch(data, matrix)
    
    print("No Consecutive: {}".format(new_cost_teacher_consecutive))
    print("Separate laboratory: {}".format(new_cost_separate_laboratory))
    print("No MathSci: {}".format(new_cost_mathsci_after_lunch))
    

    #Fix bug from algorithmm
    
    for i in range(len(section_names)):
        del final_day_sched[i]
    
    # OUTPUT OF PROGRAM. DO NOT REMOVE
    print(dict_to_clean_string(final_day_sched))
    print(dict_to_clean_string(final_teacher_sched))
    