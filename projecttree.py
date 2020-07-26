#!/usr/bin/env python
import os
import pathlib
import sys
import re
import datetime

# prefixes:
l   = " ├──"
ll  = " │    ├──"
ls  = " |    └──"
s   = " └── "



PROJECTLISTPATH = os.getenv("TODOTXT_PROJECTTREE_FOLDER")

if PROJECTLISTPATH is None:
    PROJECTLISTPATH = pathlib.Path.home()


p = pathlib.Path(PROJECTLISTPATH)
folderlist = {"No Project" : [] }
for i in p.glob('*/'):
    folderlist[i.name.lower()] = []

def printTodo(tododict):
    now = datetime.datetime.now()
    datepattern = re.compile(r"t:(\d{4})-(\d{2})-(\d{2})")
    print("Todos: ")
    for project in tododict:
        print(l, project)
        if tododict[project] == [] :
            print(ls, "Make next todo for this project")
        else:
            for task in tododict[project]:
                printstring = re.sub(fr'\+{project}', "", task)
                match = datepattern.search(task)
                if not match == None:
                    tdate = match.group()[2:]
                    tdate = datetime.datetime.strptime(tdate, "%Y-%m-%d")
                    if tdate <= now:
                        printstring = datepattern.sub(' ', task)
                        printstring = " ".join(printstring.split()) # removes duplicate whitespaces *and* \n.
                        if task == tododict[project][-1]:
                            print(ls, printstring)
                        else:
                            print(ll, printstring)

                else:
                    if task == tododict[project][-1]:
                        print(ls, printstring, end='')
                    else:
                        print(ll, printstring, end='')


def main(todo_file, done_file, projectfilelist):


    with open(todo_file, 'r') as f:
        content = f.readlines()
        projects = folderlist
        for i, task in enumerate(content):
            reg = r'\+[\S]+'
            projectregex = re.search(reg, task)
            if not projectregex == None :
                projectregexstr = projectregex.group()[1:] # remove the +
                if projectregexstr in projects :
                    projects[projectregexstr].append(task)
                else:
                    projects[projectregexstr] = [task]
            else :
                projects["No Project"].append(task)
    printTodo(projects)



# stuff to start the thing. -
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: projecttree.py [TODO_FILE] [DONE_FILE] <projectfolder>")
        sys.exit(1)

    if os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]):
        if len(sys.argv) == 4:
            main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
        else:
            main(sys.argv[1], sys.argv[2], p)
    else:
        print("Error: %s or %s doesn't exist" % (sys.argv[1], sys.argv[2]))
        sys.exit(1)
    # print(os.getenv("TODOTXT_FINAL_FILTER"))
