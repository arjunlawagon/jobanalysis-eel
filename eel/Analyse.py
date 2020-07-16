import re
from datetime import datetime
import eel

eel.init('mountain')


class job:
    def __init__(self):
        self.steps = []
        self.excp = []
        self.prog = []
        self.cpu = []
        self.start = ''
        self.end = ''
        self.execTime = []

    def initialize(self):
        self.steps = []
        self.excp = []
        self.prog = []
        self.cpu = []
        self.start = ''
        self.end = ''
        self.execTime = []

    def getStep(self):
        return self.steps

    def getExcp(self):
        return self.excp

    def getProg(self):
        return self.prog

    def getCpu(self):
        return self.cpu

    def getExecTime(self):
        return self.execTime

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def setstart(self, start):
        self.start = start

    def setend(self, end):
        self.end = end

    def addstep(self, step):
        self.steps.append(step)

    def addexcp(self, excp):
        self.excp.append(excp)

    def addcpu(self, cpu):
        self.cpu.append(cpu)

    def addprog(self, prg):
        self.prog.append(prg)

    def setExecTime(self, timearr):
        self.execTime = timearr


bau = job()
prj = job()


def findstarttime(x, l):
    pos = l.find("STARTED")
    if pos == 39:
        timestart = l[54:62]
        x.setstart(timestart)


def findendtime(x, l):
    pos = l.find("ENDED - TIME")
    if pos == 39:
        x.setend(l[52:62])


def findstep(x, l):
    pos = re.search("-P...     S...", l)
    if pos:
        x.addstep(l[30:36])
        x.addexcp(int(l[49:51].strip()))
        print(l)


def findprog(x, l):
    pos = re.search("PROGRAM - ", l)
    if pos:
        x.addprog(l[21:30])
        x.addcpu(float(l[73:78].strip()))
        print(l)


@eel.expose
def mainprocess(baujob, prjjob):
    bau.initialize()
    prj.initialize()
    print("running python from eel")
    if baujob == "":
        return "-1"

    if prjjob == "":
        return "-1"

    for line in baujob:
        findstarttime(bau, line)
        findendtime(bau, line)
        findstep(bau, line)
        findprog(bau, line)

    for line in prjjob:
        findstarttime(prj, line)
        findendtime(prj, line)
        findstep(prj, line)
        findprog(prj, line)

    return "00"

@eel.expose
def dummy(dummy_param):
    print("I got a parameter: ", dummy_param)
    return "string_value", 1, 1.2, True, [1, 2, 3, 4], {"name": "eel"}


@eel.expose
def getStep(job):
    print("getStep input: " + str(job))
    if job == "bau":
        print(bau.getStep())
        return bau.getStep()
    else:
        return prj.getStep()

@eel.expose
def getExcp(job):
    return job.getExcp()

@eel.expose
def getProg(job):
    return job.getProg()

@eel.expose
def getCpu(job):
    return job.getCpu()

@eel.expose
def getExecTime(job):
    return job.getExecTime()

@eel.expose
def getStart(job):
    return job.getStart()

@eel.expose
def getEnd(job):
    return job.getEnd()

eel.start('index.html', size=(900, 700))
