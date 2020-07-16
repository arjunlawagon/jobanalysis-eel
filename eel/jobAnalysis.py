import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import *
import ftplib
import eel


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


def findprog(x, l):
    pos = re.search("PROGRAM - ", l)
    if pos:
        x.addprog(l[21:30])
        x.addcpu(float(l[73:78].strip()))


def printComparisonPlot(prjversion, bauversion):
    fig, axs = plt.subplots(2, 1)
    fig.suptitle("JOB RESOURCE ANALYSIS", fontsize=16)

    i = 0
    while i <= 1:
        if i == 0:
            axs[i].set_title('CPU Usage Comparison')
            axs[i].set_ylabel('CPU')
            axs[i].plot(bauversion.steps, bauversion.cpu, '--', label="BAU")
            axs[i].plot(prjversion.steps, prjversion.cpu, '--', label="PRJ")
        else:
            axs[i].set_title('EXCP Comparison')
            axs[i].set_ylabel('EXCP')
            axs[i].plot(bauversion.steps, bauversion.excp, '--', label="BAU")
            axs[i].plot(prjversion.steps, prjversion.excp, '--', label="PRJ")

        axs[i].set_xlabel('STEP ' + str(bau.steps[0]) + "to " + str(bau.steps[-1]))
        axs[i].legend()
        axs[i].autoscale(enable=True)
        axs[i].set_xticks([])
        i += 1


def addTableSummary(jobversion):
    """ADD 1 ROW AT END OF STEPS FOR SUMMARY"""
    jobversion.steps.append("SUMMARY")
    jobversion.prog.append("")
    jobversion.cpu.append(max(jobversion.cpu))
    jobversion.excp.append(max(jobversion.excp))


def calculateElapseTime(jobversion):
    time_arr = [None] * len(jobversion.steps)
    time_arr[0] = jobversion.start.replace(".", ":").strip()
    time_arr[-2] = jobversion.end.replace(".", ":").strip()

    FMT = '%H:%M:%S'
    time_arr[-1] = datetime.strptime(time_arr[-2], FMT) - datetime.strptime(time_arr[0], FMT)
    return time_arr


def genTableData(jobversion):
    return list(map(list, zip(jobversion.steps, jobversion.prog, jobversion.cpu,
                              jobversion.excp, jobversion.execTime)))


def genTablePlot(dataclust, axname, version):
    colors = ["#56b5fd", "#56b5fd", "#56b5fd", "#56b5fd", "#56b5fd", "#56b5fd"]
    fig, axname = plt.subplots()
    fig.suptitle("JOB STEP ANALYSIS " + version + " VERSION")
    collabel = ("STEPS", "PROGRAM", "CPU", "EXCP", "TIME")
    axname.axis('tight')
    axname.axis('off')
    axname.autoscale(enable=True)
    tablename = axname.table(cellText=dataclust, colLabels=collabel, loc='center', cellLoc="center",
                             colColours=colors)


def showPlots():
    plt.show()



def main_proc(baujob, prjjob):
    bau.initialize()
    prj.initialize()
    status_text1.set("")
    status_text2.set("")
    if baujob == "":
        status_text1.set("Please provide input")
        return
    else:
        status_text1.set("")
    if prjjob == "":
        status_text2.set("Please provide input")
        return
    else:
        status_text2.set("")

    baujobtxt = baujob + ".txt"
    prjjobtxt = prjjob + ".txt"

    try:
        with open(baujobtxt, "r") as inputtxt:
            for line in inputtxt:
                findstarttime(bau, line)
                findendtime(bau, line)
                findstep(bau, line)
                findprog(bau, line)
    except OSError as e:
        status_text1.set(str(e)[10:35])
        return
    try:
        with open(prjjobtxt, "r") as inputtxt2:
            for line in inputtxt2:
                findstarttime(prj, line)
                findendtime(prj, line)
                findstep(prj, line)
                findprog(prj, line)
    except OSError as e:
        status_text2.set(str(e)[10:35])
        return

    status_text1.set("Processing")
    status_text2.set("Processing")
    # CREATE COMPARISON PLOT
    printComparisonPlot(prjversion=prj, bauversion=bau)

    # CREATE TABLE PLOT FOR BAU
    addTableSummary(bau)
    bau.setExecTime(calculateElapseTime(bau))
    genTablePlot(genTableData(bau), "bau_ax", "BAU")

    # CREATE TABLE PLOT FOR PRJ
    addTableSummary(prj)
    prj.setExecTime(calculateElapseTime(prj))
    genTablePlot(genTableData(prj), "prj_ax", "PRJ")

    # DISPLAY ALL PLOTS
    showPlots()
    status_text1.set("DONE")
    status_text2.set("DONE")


# this is a function to get the user input from the text input box
def getracfValue():
    userInput = inputRacf.get()
    return userInput


# this is a function to get the user input from the text input box
def getpasswordValue():
    userInput = inputPass.get()
    return userInput


# this is the function called when the button is clicked
def btnLoginClick():
    print('login click')
    user = getracfValue()
    password = getpasswordValue()
    print(user)
    print(password)
    ftpConnect(user, password)


def ftpConnect(user, password):
    #    ftp = ftplib.FTP("10.20.208.29",user,password)
    ftp = ftplib.FTP("test.rebex.net", user, password)
    try:
        filelist = ftp.nlst()
    except ftplib.error_perm as x:
        if x.args[0][:3] != '550':
            raise
    else:
        status_text1.set("connected")


# this is a function to get the user input from the text input box
def getbauValue():
    userInput = inputBAU.get()
    return userInput


# this is a function to get the user input from the text input box
def getprjValue():
    userInput = inputPRJ.get()
    return userInput


# this is the function called when the button is clicked
def btnAnalyseClick():
    main_proc(getbauValue(), getprjValue())


root = Tk()

# This is the section of code which creates the main window
root.geometry('600x150')
root.configure(background='#F0F8FF')
root.title('Joblog Analysis Tool')

# This is the section of code which creates the a label
status_text1 = StringVar()
status_text1.set("")
status_text2 = StringVar()
status_text2.set("")
baustatus = Label(root, text="disconnected", textvariable=status_text1,
                  bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=320, y=27)

prjstatus = Label(root, text="disconnected", textvariable=status_text2,
                  bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=320, y=57)

# This is the section of code which creates the a label
Label(root, text='Enter BAU joblog:', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=15, y=27)

# This is the section of code which creates a text input box
inputBAU = Entry(root)
inputBAU.place(x=120, y=20)

# This is the section of code which creates the a label
Label(root, text='Enter PRJ joblog:', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=15, y=57)

# This is the section of code which creates a text input box
inputPRJ = Entry(root)
inputPRJ.place(x=120, y=50)

# This is the section of code which creates a button
Button(root, text='ANALYSE', bg='#F0F8FF', font=('arial', 12, 'normal'), command=btnAnalyseClick).place(x=15, y=90)

if __name__ == "__main__":
    root.mainloop()
