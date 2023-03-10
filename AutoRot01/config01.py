import os
from abaqus import *

absPath = os.path.abspath(__file__)
absDir  = os.path.dirname(absPath)
configfile = os.path.join(absDir, 'rot.config')
def config(axis,speed):
    f=open(configfile, 'w')
    f.writelines(axis+'\n')
    f.writelines(str(1-speed))
    f.close()
