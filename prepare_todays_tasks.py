#!/mingw64/bin/python3

import json
import datetime
from get_coming_events import get_coming_events

new_tasks = []
with open("settings-private/settings.json") as settings_file:
    settings = json.load(settings_file)
    directory = settings["directory"]
    projects = settings["projects"]
    dow_label = settings["dow_label"]
    due_label = settings["due_label"]
    ttl_label = settings["ttl_label"]
    late_label = settings["late_label"]
    stays_label = settings["stays_label"]
    skola = directory + settings["skola"]
    today = directory + settings["today"]
    daily = directory + settings["daily"]
    noras = directory + settings["noras"]
    fusion = directory + settings["fusion"]
    stroth = directory + settings["stroth"]
    laguna = directory + settings["laguna"]
    booked = directory + settings["booked"]
    weekly = directory + settings["weekly"]
    shlist = directory + settings["shlist"]
    heading_label = settings["heading_label"]
    finadit = directory + settings["finadit"]
    incoming = directory + settings["incoming"]
    periodic = directory + settings["periodic"]
    coming_events = settings["coming_events_file"]
    counter_limit = int(settings["numof_project_tasks_to_include"])
    start_label = settings["start_label"]
    lunch_label = settings["lunch_label"]
    dinner_label = settings["dinner_label"]
    shopping_label = settings["shopping_label"]
    main_work_label = settings["main_work_label"]
    day_routine_label = settings["day_routine_label"]
    additional_work_label = settings["additional_work_label"]
    morning_routine_label = settings["morning_routine_label"]
    evening_routine_label = settings["evening_routine_label"]

weekdays = {
    0: "mon",
    1: "tue",
    2: "wed",
    3: "thu",
    4: "fri",
    5: "sat",
    6: "sun"
}

day = int(input("Preparing for day  : "))
month = int(input("Preparing for month: "))
year = int(input("Preparing for year : "))
date = datetime.date(year, month, day)
today_str = "{:%Y-%m-%d}".format(date)


def read_tasks_file(tasks_file):
    with open(tasks_file, "r") as f:
        tasks = f.readlines()
    return tasks


def add_daily_segment(tasks, segment):
    for t in tasks:
        if segment in t:
            new_tasks.append(t[:len(t)-1])


def add_project_tasks(project_tasks):
    counter = 0
    in_ttl = False
    for t in project_tasks:
        if t[:5] == ttl_label:
            in_ttl = True
        elif in_ttl and len(t) > 1 and t[:5] != ttl_label:
            if t[0] == heading_label:
                in_ttl = False
            elif counter < counter_limit:
                if len(project_tasks) >= counter_limit:
                    new_tasks.append(t[:len(t)-1])
                    counter += 1


daily_tasks = read_tasks_file(daily)
add_daily_segment(daily_tasks, start_label)
add_daily_segment(daily_tasks, morning_routine_label)

get_coming_events(year, month, day)
coming_events = read_tasks_file(coming_events)
for e in coming_events:
    new_tasks.append(due_label + e[:len(e)-1])

booked_tasks = read_tasks_file(booked)
for t in booked_tasks:
    if t[6:6+10] <= today_str:
        new_tasks.append(t[:len(t)-1])

add_daily_segment(daily_tasks, main_work_label)
add_daily_segment(daily_tasks, shopping_label)

add_project_tasks(read_tasks_file(shlist))

add_daily_segment(daily_tasks, lunch_label)
add_daily_segment(daily_tasks, day_routine_label)

late_tasks = read_tasks_file(today)
for i in late_tasks:
    if stays_label in i:
        task_string = i
        if late_label not in i:
            i = "- " + late_label + " " + i[2:len(i)-1]
        new_tasks.append(i[:len(i)-1])

add_daily_segment(daily_tasks, additional_work_label)

weekly_tasks = read_tasks_file(weekly)
for t in weekly_tasks:
    dow = t[t.find(dow_label)+4:t.find(dow_label)+4+3]
    if weekdays[date.weekday()] == dow:
        new_tasks.append(t[:len(t)-1])

periodic_tasks = read_tasks_file(periodic)
for t in periodic_tasks:
    if t[0] != 'x' and t[6:6+10] <= today_str:
        new_tasks.append(t[:len(t)-1])

add_project_tasks(read_tasks_file(laguna))
add_project_tasks(read_tasks_file(fusion))
add_project_tasks(read_tasks_file(noras))
add_project_tasks(read_tasks_file(finadit))
add_project_tasks(read_tasks_file(skola))

add_daily_segment(daily_tasks, dinner_label)
add_daily_segment(daily_tasks, evening_routine_label)

add_project_tasks(read_tasks_file(incoming))
add_project_tasks(read_tasks_file(stroth))

for t in new_tasks:
    with open(today, "w") as f:
        for t in new_tasks:
            print(t, file=f)
