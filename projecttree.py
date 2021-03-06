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
#regexes
datepattern = re.compile(r"t:(\d{4})-(\d{2})-(\d{2})")
projectpattern = re.compile(r'\+[\S]+')

now = datetime.datetime.now()

def getfolderlist():
    PROJECTLISTPATH = os.getenv("TODOTXT_PROJECTTREE_FOLDER")

    if PROJECTLISTPATH is None:
        PROJECTLISTPATH = pathlib.Path.home()

    p = pathlib.Path(PROJECTLISTPATH)
    folderlist = {"No Project": []}
    for i in p.glob('*/'):
        folderlist[i.name.lower()] = []
    return folderlist

print(getfolderlist())
def printTodo(tododict):
    tododictSize = tododict.__len__()
    i = 0

    print("Todos: ")
    for project in tododict:
        i = i + 1

        #all todo's have a project.
        if set(tododict[project]) == set() or set(tododict[project]) == {''} :
            print(t, project)
            print(l, s,"Make Next Todo For This Project")
            continue
        elif i == tododictSize:
            print(s, project.capitalize())
            firstblock = e
        else:
            print(t, project.capitalize())
            firstblock = l
            
        if tododict[project] == []:
            print(l, s, " Make next todo for this project", sep='')
        else:
            for task in tododict[project]:
                if task == "": # then it was removed by the filter.
                    continue
                printstring = re.sub(fr'\+{project}', "", task, flags=re.IGNORECASE)
                printstring = datepattern.sub(' ', printstring)
                printstring = " ".join(printstring.split())  # removes duplicate whitespaces *and* \n.
                if task == tododict[project][-1]:
                    print(firstblock, s, " ", printstring.capitalize(), sep='')
                else:
                    print(firstblock, t, " ", printstring.capitalize(), sep='')


def main(todo_file, projectfolderlist):

    with open(todo_file, 'r') as f:
        content = f.readlines()
        projects = projectfolderlist
        for i, task in enumerate(content):
            taskstring = str(i+1) +" "+ task
            projectregex = projectpattern.search(task)
            match = datepattern.search(task)


            if match is not None: # Future filter stuff
                tdate = match.group()[2:]
                tdate = datetime.datetime.strptime(tdate, "%Y-%m-%d")
                if tdate > now:
                    continue
                    #taskstring = ""

            if projectregex is not None:
                projectregexstr = projectregex.group()[1:].lower()  # remove the +
                if projectregexstr in projects:
                    projects[projectregexstr].append(taskstring)
                else:
                    projects[projectregexstr] = [taskstring]
            else:
                projects["No Project"].append(taskstring)
    print(projects)
    printTodo(projects)


# stuff to start the thing. -
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: projecttree.py [TODO_FILE] [DONE_FILE] <projectfolder>")
        sys.exit(1)
    ff = getfolderlist()
    main(sys.argv[1], ff)
