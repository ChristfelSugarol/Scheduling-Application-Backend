from constants import *
from utils2 import *

def no_consecutive_class(data, filled):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    teacher_list = {}
        
    # Initialize Periods per day
    daily_slots = {}
    
    for i in range(NUMBER_OF_PERIODS):
        daily_slots[i] = None
    
    
    #Create a dictionary for every teacher
    #Create a dictionary for every day
    #Assign daily slots to day
    for teacher in data.teacher_availability.keys():
        teacher_list[teacher] = {}
        
        for day in days:
            teacher_list[teacher][day] = daily_slots
        
    for class_index, times in filled.items():
        c = data.classes[class_index]
        room = str(data.classrooms[times[0][1]])
                
        for time in times:
            teacher_list[c.teacher][days[times[0][0] // NUMBER_OF_PERIODS]][time[0] % NUMBER_OF_PERIODS] = {
                "Subject": c.subject,
                "Classroom": room[:room.rfind('-')]
            }
            
    cost = 0

    for teacher_timetable in teacher_list:
        for day in teacher_timetable:
            c1 = 0 # if c1 = 3, cost starts to go up
            c2 = 0 # 0.5 cost per c2
            
            for i in range(len(day)):
                if day[i] is not None:
                    c1 += 1
                    c2 += 1
                else:
                    if c1 >= 3:
                        cost += c2*NO_CONSECUTIVE_CLASS_COST_MULTIPLIER
                        
                    c1 = 0
                    c2 = 0
                    
    return cost

def separate_laboratory(data, matrix):
    cost = 0

    #Check row of each column
    #If classes with laboratories are in the same row then cost is added
    for row in matrix:
        laboratory_list = []
        
        for col in row:
            if col is not None:
                if data.classes[col].laboratory is not None:
                    if data.classes[col].laboratory in laboratory_list:
                        cost += 1*NO_OVERLAPING_LABORATORY_CLASSES_MULTIPLIER
                    else:
                        laboratory_list.append(data.classes[col].laboratory)

    return cost

def mathsci_before_lunch(data, matrix):
    cost = 0

    section_sched = []
    final_day_sched = []
    
    for i in range(len(matrix[0])):
        section_sched.append([]) 
        final_day_sched.append("")    
        
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
    
    for section in final_day_sched:
        lunchfound = False
        for day in section:
                for subject in day:
                    if subject is not None:
                        
                        if lunchfound == False:
                            if subject.typeBreak == "Lunch":
                                lunchfound = True
                                
                        else:
                            if subject.isMathSci == True:
                                cost += 1*NO_MATH_SCIENCE_AFTER_LUNCH_MULTIPLIER
                        

    return cost