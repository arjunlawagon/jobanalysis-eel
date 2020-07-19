import re
from datetime import datetime
import eel
import time

eel.init('web')


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

error = ""

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
    pos =  re.search("-P...     S...", l)
    pos2 = re.search("-P....... S...", l)
    pos3 = re.search("-P...     S.......", l)
    if pos or pos2 or pos3:
        print(l)
        x.addstep(l[30:38].strip())
        x.addexcp(int(l[49:51].strip()))


def findprog(x, l):
    pos = re.search("PROGRAM - ", l)
    if pos:
        x.addprog(l[21:30])
        x.addcpu(float(l[73:78].strip()))


def calculateElapseTime(jobversion):
    time_arr = [''] * (len(jobversion.steps) + 1)
    time_arr[0] = jobversion.start.replace(".", ":").strip()
    time_arr[-2] = jobversion.end.replace(".", ":").strip()

    FMT = '%H:%M:%S'
    elapse = abs(datetime.strptime(time_arr[-2], FMT) - datetime.strptime(time_arr[0], FMT)).seconds
    print(elapse)
    if elapse == 0:
        time_arr[-1] = "< 1sec"
    else:
        time_arr[-1] = str(convert(elapse))

    return time_arr


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    timestr = ""
    if hour > 0:
        timestr = timestr + str(hour) + "hr "
    if minutes > 0:
        timestr = timestr + str(minutes) + "min "
    if seconds > 0:
        timestr = timestr + str(seconds) + "sec"

    return timestr


def addTableSummary(jobversion):
    """ADD 1 ROW AT END OF STEPS FOR SUMMARY"""
    jobversion.steps.append("SUMMARY")
    jobversion.prog.append("")
    jobversion.cpu.append(max(jobversion.cpu))
    jobversion.excp.append(max(jobversion.excp))


@eel.expose
def mainprocess(baujob, prjjob):
    bau.initialize()
    prj.initialize()
    print("Analysing string tokens...")
    if baujob == "":
        print("bau iput is empty")
        return '-1'

    if prjjob == "":
        print("prj input is empty")
        return '-1'

    print("bau")
    for line in baujob:
        findstarttime(bau, line)
        findendtime(bau, line)
        findstep(bau, line)
        findprog(bau, line)

    print("prj")
    for line in prjjob:
        findstarttime(prj, line)
        findendtime(prj, line)
        findstep(prj, line)
        findprog(prj, line)

    if len(bau.getStep()) == 0:
        return "-2"

    if len(prj.getStep()) == 0:
        return "-3"

    bau.setExecTime(calculateElapseTime(bau))
    prj.setExecTime(calculateElapseTime(prj))
    addTableSummary(bau)
    addTableSummary(prj)
    time.sleep(2)
    print("Analysis completed.")
    return '00'


@eel.expose
def getSteps(job):
    if job == "bau":
        return bau.getStep()
    else:
        return prj.getStep()


@eel.expose
def getExcps(job):
    if job == "bau":
        return bau.getExcp()
    else:
        return prj.getExcp()


@eel.expose
def getProgs(job):
    if job == "bau":
        return bau.getProg()
    else:
        return prj.getProg()


@eel.expose
def getCpus(job):
    if job == "bau":
        return bau.getCpu()
    else:
        return prj.getCpu()


@eel.expose
def getExecTimes(job):
    if job == "bau":
        return bau.getExecTime()
    else:
        return prj.getExecTime()


@eel.expose
def getStart(job):
    if job == "bau":
        return bau.getStart()
    else:
        prj.getStart()


@eel.expose
def getEnd(job):
    if job == "bau":
        return bau.getEnd()
    else:
        return prj.getEnd()


eel.start('index.html', size=(780, 680))
