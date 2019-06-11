#!/mingw64/bin/python3

import datetime

def schedule():
    default_duration = 4
    with open("E:/dev/0/Dropbox/Dropbox/today.pmd.txt", "r") as tasks_file:
        tasks = tasks_file.readlines()
    new_tasks = []
    if "- ST: " in tasks[0]:
        beg = datetime.datetime(2000, 1, 1, 0, 0)
    else:
        beg = datetime.datetime.now()
    for t in tasks:
        if t[4] == ":" and t[10] == ":":
            t = "- " + t[14:]
        tokens = t.split()
        duration = default_duration
        for tok in tokens:
            if tok[0:4] == "dur:":
                duration = int(tok[4:])
        end = beg + datetime.timedelta(minutes=duration)
        new_tasks.append("- "
                         + "{:%H:%M}".format(beg)
                         + "-{:%H:%M} ".format(end)
                         + t[2:len(t)-1])
        beg = end
    with open("E:/dev/0/Dropbox/Dropbox/today.pmd.txt", "w") as tasks_file:
        for t in new_tasks:
            tasks_file.write(t + '\n')

if __name__ == "__main__":
    schedule()
