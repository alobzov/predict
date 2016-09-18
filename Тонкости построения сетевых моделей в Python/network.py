from predict import Activity

import xml.etree.ElementTree as ET

import sys

import timeit
from timeit import Timer


# вычисляем значение параметра задачи
def get_child(child, activity_field):
    text = child.find(activity_field).text
    if text is None:
        return None
    return int(text)


# строим модель с использованием метода пересчета
def build_model_by_method(filename):

    sys.setrecursionlimit(10000)

    f = open(filename,'r')
    tree = ET.parse(f)
    root = tree.getroot()
    schedule = {}
    next = {}
    for child in root.findall('Activity'):
        id = child.find('id').text
        start_date = get_child(child,'start_date')
        finish_date = get_child(child,'finish_date')
        duration = get_child(child,'duration')
        not_early_date = get_child(child,'not_early_date')
        a = Activity(id, start_date, finish_date, duration, not_early_date)
        schedule[id] = a
        next_activity = '' if child.find('next_activity').text is None else child.find('next_activity').text
        next[id] = next_activity
    for key in schedule:
        if next[key] != '':
            for next_id in next[key].split(';'):
                schedule[key].append_next(schedule[next_id])

    sys.setrecursionlimit(1000)


# строим модель без использования метода пересчета
def build_model_by_assignment(filename):
    f = open(filename,'r')
    tree = ET.parse(f)
    root = tree.getroot()
    schedule = {}
    next = {}
    for child in root.findall('Activity'):
        id = child.find('id').text
        start_date = get_child(child,'start_date')
        finish_date = get_child(child,'finish_date')
        duration = get_child(child,'duration')
        not_early_date = get_child(child,'not_early_date')
        a = Activity(id, start_date, finish_date, duration, not_early_date)
        schedule[id] = a
        next_activity = '' if child.find('next_activity').text is None else child.find('next_activity').text
        next[id] = next_activity
    for key in schedule:
        if next[key] != '':
            for next_id in next[key].split(';'):
                schedule[key].next_activity.append(schedule[next_id])


# считаем скорость построения модели
print('Test for 100 activities:')
t1 = Timer("build_model_by_method('data/activity_100.xml')", "from __main__ import build_model_by_method")
print("build_model_by_method", t1.timeit(number = 1000))
t2 = Timer("build_model_by_assignment('data/activity_100.xml')", "from __main__ import build_model_by_assignment")
print("build_model_by_assignment", t2.timeit(number = 1000))

print('Test for 1000 activities')
t3 = Timer("build_model_by_method('data/activity_1000.xml')", "from __main__ import build_model_by_method")
print("build_model_by_method", t3.timeit(number = 1000))
t4 = Timer("build_model_by_assignment('data/activity_1000.xml')", "from __main__ import build_model_by_assignment")
print("build_model_by_assignment", t4.timeit(number = 1000))

print('Test for 10000 activities')
t5 = Timer("build_model_by_method('data/activity_10000.xml')", "from __main__ import build_model_by_method")
print("build_model_by_method", t5.timeit(number = 1000))
t6 = Timer("build_model_by_assignment('data/activity_10000.xml')", "from __main__ import build_model_by_assignment")
print("build_model_by_assignment", t6.timeit(number = 1000))