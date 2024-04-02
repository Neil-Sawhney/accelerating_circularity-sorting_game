import datetime

startTime = 0
def setStartTime():
    global startTime
    startTime = datetime.datetime.now()
    return startTime

def getTime():
    return (datetime.datetime.now() - startTime).total_seconds()
