#!/usr/bin/env python
import os
import pathlib
import sys
import re
import datetime

# prefixes:
t = " ├──"
l = " │  "
s = " └──"
e = "    "


def getfolderlist():
    PROJECTLISTPATH = os.getenv("TODOTXT_PROJECTTREE_FOLDER")

    if PROJECTLISTPATH is None:
        PROJECTLISTPATH = pathlib.Path.home()

    p = pathlib.Path(PROJECTLISTPATH)
    folderlist = {"No Project": []}
    for i in p.glob('*/'):
        folderlist[i.name.lower()] = []
    return folderlist


def printTodo(tododict):
    now = datetime.datetime.now()
    datepattern = re.compile(r"t:(\d{4})-(\d{2})-(\d{2})")
    tododictSize = tododict.__len__()
    i = 0

    print("Todos: ")
    for project in tododict:
        i = i + 1
        if i == tododictSize:
            print(s, project)
            firstblock = e
        else:
            print(t, project)
            firstblock = l
        if tododict[project] == []:
            print(l, s, "Make next todo for this project")
        else:
            for task in tododict[project]:
                printstring = re.sub(fr'\+{project}', "", task)
                match = datepattern.search(task)
                if match is not None:
                    tdate = match.group()[2:]
                    tdate = datetime.datetime.strptime(tdate, "%Y-%m-%d")
                    if tdate <= now:
                        printstring = datepattern.sub(' ', task)
                        printstring = " ".join(printstring.split())  # removes duplicate whitespaces *and* \n.
                        if task == tododict[project][-1]:
                            print(firstblock, s, printstring, sep='')
                        else:
                            print(firstblock, t, printstring, sep='')

                else:
                    if task == tododict[project][-1]:
                        print(firstblock, s, printstring, sep='', end='')
                    else:
                        print(firstblock, t, printstring, sep='', end='')


def main(todo_file, projectfolderlist):
    with open(todo_file, 'r') as f:
        content = f.readlines()
        projects = projectfolderlist
        for i, task in enumerate(content):
            reg = r'\+[\S]+'
            projectregex = re.search(reg, task)
            if projectregex is not None:
                projectregexstr = projectregex.group()[1:]  # remove the +
                if projectregexstr in projects:
                    projects[projectregexstr].append(task)
                else:
                    projects[projectregexstr] = [task]
            else:
                projects["No Project"].append(task)
    printTodo(projects)


# stuff to start the thing. -
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: projecttree.py [TODO_FILE] [DONE_FILE] <projectfolder>")
        sys.exit(1)
    ff = getfolderlist()
    main(sys.argv[1], ff)
