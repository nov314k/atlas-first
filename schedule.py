#!/mingw64/bin/python3

import datetime

default_durations = 4
with open("E:/dev/0/Dropbox/Dropbox/today.pmd.txt", "r") as tasks_file:
    tasks = tasks_file.readlines()
new_tasks = []
if "- ST: " in tasks[0]:
    beg = datetime.datetime(2000, 1, 1, 0, 0)
else:
    beg = datetime.datetime.now()
for t in tasks:
    tokens = t.split()
    duration = default_durations
    for tok in tokens:
        if tok[0:4] == "dur:":
            duration = int(tok[4:len(tok)])
    end = beg + datetime.timedelta(minutes=duration)
    new_tasks.append("- " + "{:%H:%M}".format(beg) + "-{:%H:%M} ".format(end) + t[2:len(t)-1])
    beg = end
with open("E:/dev/0/Dropbox/Dropbox/schedule.pmd.txt", "w") as text_file:
    for t in new_tasks:
        text_file.write(t + '\n')



