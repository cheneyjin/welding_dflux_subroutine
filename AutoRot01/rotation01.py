import time
from abaqus import *
from abaqusConstants import *

absPath = os.path.abspath(__file__)
absDir  = os.path.dirname(absPath)
configfile = os.path.join(absDir, 'rot.config')

def rotation():
    with open(configfile) as f:
        axis = f.readline()
        t = f.readline()
        period = float(t)
    vps = session.viewports[session.currentViewportName]
    v = vps.view
    n = 100
    k = 100
    ang = 360.0/n
    if axis == 'Z-axis\n':
        for i in range(k):
            v.rotate(zAngle=ang,drawImmediately=True)
            time.sleep(period)
            milestone('Total','cycles',i,k)
    elif axis == 'Y-axis\n':
        for i in range(k):
            v.rotate(yAngle=ang,drawImmediately=True)
            time.sleep(period)
            milestone('Total','cycles',i,k)
    elif axis == 'X-axis\n':
        for i in range(k):
            v.rotate(xAngle=ang,drawImmediately=True)
            time.sleep(period)
            milestone('Total','cycles',i,k)
