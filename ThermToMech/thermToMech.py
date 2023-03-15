from abaqus import *
from abaqusConstants import *
import os

def transform(tName,mName,freq,eloutput):
    thispath,thermalfile = os.path.split(tName)
    thermal_job_name = os.path.splitext(thermalfile)[0]
    output_freq = freq
    element_output=eloutput
    sname = tName
    tname = thispath + '/'+mName+'.inp'

    with open(sname,"r") as f:
        lines=f.readlines()

    r=[i.upper() for i in lines]
    if os.path.exists(tname):
        reply=getWarningReply('The mechanical job file exists!\nOverwrite?', (YES, NO))
        if reply==YES:
            pass
        elif reply==NO:
            return
    with open(tname,"w") as f_w:
        step_num=0
        for line in r:
            line=line.replace(', ', ',').replace(' ,',',')
            if line.startswith('*ELEMENT'):
                line=line.replace("DC3D8","C3D8R")
                line=line.replace("DC3D20","C3D20R")
                line=line.replace("DC3D4","C3D4")
                line=line.replace("DC3D10","C3D10")
            elif line.startswith('*STEP'):
                step_num=step_num+1
                line=line.replace("NLGEOM=NO","NLGEOM")
            elif line.startswith('*HEAT TRANSFER'):
                line="*STATIC, STABILIZE\n"
            elif line.startswith('*DFLUX'):
                line="**"
            elif line.startswith("** OUTPUT REQUESTS"):
                line="*TEMPERATURE, file=%s, bstep=%d\n" \
                    %(thermal_job_name,step_num)
            elif line.startswith('*SFILM'):
                line="**"
            elif line.startswith('*SRADIATE'):
                line="**"
            elif line.startswith('*OUTPUT,FIELD'):
                line="*OUTPUT, FIELD, FREQUENCY="+output_freq+"\n"
            elif line.startswith('NT'):
                line="NT,U\n*ELEMENT OUTPUT\n"+element_output+"\n"

            f_w.write(line)

    print tname+' has been created successfully.'
    return
