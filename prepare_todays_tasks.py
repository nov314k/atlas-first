#!/mingw64/bin/python3

import json
import datetime
from schedule import schedule
from get_coming_events import get_coming_events


new_tasks = []
with open("credson/prepare-todays-tasks.json") as json_file:
    json_data = json.load(json_file)
    projects = json_data["projects"]
    skola_file = json_data["skola_file"]
    today_file = json_data["today_file"]
    daily_file = json_data["daily_file"]
    noras_file = json_data["noras_file"]
    fusion_file = json_data["fusion_file"]
    laguna_file = json_data["laguna_file"]
    booked_file = json_data["booked_file"]
    weekly_file = json_data["weekly_file"]
    shlist_file = json_data["shlist_file"]
    periodic_file = json_data["periodic_file"]
    coming_events_file = json_data["coming_events_file"]
weekdays = {
    0: "mon",
    1: "tue",
    2: "wed",
    3: "thu",
    4: "fri",
    5: "sat",
    6: "sun"
}
# Get the date the list is being prepared for
day = int(input("Preparing for day  : "))
month = int(input("Preparing for month: "))
year = int(input("Preparing for year : "))
date = datetime.date(year, month, day)
today_str = "{:%Y-%m-%d}".format(date)
# Read daily tasks
with open(daily_file, "r") as text_file:
    daily_tasks = text_file.readlines()
# Add - ST:
for t in daily_tasks:
    if "- ST:" in t:
        new_tasks.append(t[:len(t)-1])
# Add - GU:
for t in daily_tasks:
    if "- GU:" in t:
        new_tasks.append(t[:len(t)-1])
# Add coming events
get_coming_events(year, month, day)
with open(coming_events_file, "r") as text_file:
    coming_events = text_file.readlines()
for e in coming_events:
    new_tasks.append("- due:" + e[:len(e)-1])
# Add booked tasks
with open(booked_file, "r") as text_file:
    booked_tasks = text_file.readlines()
for t in booked_tasks:
    if t[6:6+10] <= today_str:
        new_tasks.append(t[:len(t)-1])
# Add - MW:
for t in daily_tasks:
    if "- MW:" in t:
        new_tasks.append(t[:len(t)-1])
# Add - SH:
for t in daily_tasks:
    if "- SH:" in t:
        new_tasks.append(t[:len(t)-1])
# Add shopping list items from shlist
with open(shlist_file, "r") as text_file:
    shlist_tasks = text_file.readlines()
for t in shlist_tasks:
    if "- SH:" in t:
        new_tasks.append(t[:len(t)-1])
# Add - LU:
for t in daily_tasks:
    if "- LU:" in t:
        new_tasks.append(t[:len(t)-1])
# Add - DR:
for t in daily_tasks:
    if "- DR:" in t:
        new_tasks.append(t[:len(t)-1])
# Add existing (late) tasks
with open(today_file, "r") as text_file:
    late_tasks = text_file.readlines()
for i in late_tasks:
    if "+stays" in i:
        i = i[2:len(i)-1]
        #print('\n', i)
        #yn = input("Do you want to keep this task as late? (y/n): ")
        #if yn == 'y':
        # task_string = "- " + today_str + " " + i
        task_string = "- " + i
        if "+late" not in task_string:
            task_string = " +late" + task_string
        new_tasks.append(task_string)
# Add - AW:
for t in daily_tasks:
    if "- AW:" in t:
        new_tasks.append(t[:len(t)-1])
# Add weekly tasks
with open(weekly_file, "r") as text_file:
    weekly_tasks = text_file.readlines()
for t in weekly_tasks:
    dow = t[t.find("dow:")+4:t.find("dow:")+4+3]
    if weekdays[date.weekday()] == dow:
        new_tasks.append(t[:len(t)-1])
# Add periodic tasks
with open(periodic_file, "r") as text_file:
    periodic_tasks = text_file.readlines()
for t in periodic_tasks:
    if t[0] != 'x' and t[6:6+10] <= today_str:
        new_tasks.append(t[:len(t)-1])
# counter_limit = int(input("How many TTL tasks to add: "))
counter_limit = 5
# Add Laguna tasks
with open(laguna_file, "r") as text_file:
    laguna_tasks = text_file.readlines()
counter = 0
in_ttl = False
for t in laguna_tasks:
    if t[:5] == "# TTL":
        in_ttl = True
    elif in_ttl and len(t) > 1 and t[:5] != "# TTL":
        if t[0] == '#':
            in_ttl = False
        elif counter < counter_limit:
            if len(laguna_tasks) >= counter_limit:
                new_tasks.append(t[:len(t)-1])
                counter += 1
# Add Fusion tasks
with open(fusion_file, "r") as text_file:
    fusion_tasks = text_file.readlines()
counter = 0
in_ttl = False
for t in fusion_tasks:
    if t[:5] == "# TTL":
        in_ttl = True
    elif in_ttl and len(t) > 1 and t[:5] != "# TTL":
        if t[0] == '#':
            in_ttl = False
        elif counter < counter_limit:
            if len(fusion_tasks) >= counter_limit:
                new_tasks.append(t[:len(t)-1])
                counter += 1
# Add Noras tasks
with open(noras_file, "r") as text_file:
    noras_tasks = text_file.readlines()
counter = 0
in_ttl = False
for t in noras_tasks:
    if t[:5] == "# TTL":
        in_ttl = True
    elif in_ttl and len(t) > 1 and t[:5] != "# TTL":
        if t[0] == '#':
            in_ttl = False
        elif counter < counter_limit:
            if len(fusion_tasks) >= counter_limit:
                new_tasks.append(t[:len(t)-1])
                counter += 1
# Add Skola tasks
with open(skola_file, "r") as text_file:
    skola_tasks = text_file.readlines()
counter = 0
in_ttl = False
for t in skola_tasks:
    if t[:5] == "# TTL":
        in_ttl = True
    elif in_ttl and len(t) > 1 and t[:5] != "# TTL":
        if t[0] == '#':
            in_ttl = False
        elif counter < counter_limit:
            if len(fusion_tasks) >= counter_limit:
                new_tasks.append(t[:len(t)-1])
                counter += 1
# Add - DN:
for t in daily_tasks:
    if "- DN:" in t:
        new_tasks.append(t[:len(t)-1])
# Add - ER:
for t in daily_tasks:
    if "- ER:" in t:
        new_tasks.append(t[:len(t)-1])
# Write new tasks
for t in new_tasks:
    with open(today_file, "w") as text_file:
        for t in new_tasks:
            print(t, file=text_file)
