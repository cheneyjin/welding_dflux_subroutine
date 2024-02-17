# This code is used to transfer a heat analysis job to 
# mechanical one in sequential thermal-mechanical analysis
# User inputs start here:
#########################################
thermal_job_name='modelT'
mech_job_name='modelS'
output_freq='20'
element_output='LE,S'
#########################################
sname='./'+thermal_job_name+'.inp'
tname='./'+mech_job_name+'.inp'

with open(sname,"r") as f:
    lines=f.readlines()

r=[i.upper() for i in lines]
with open(tname,"w") as f_w:
    step_num=0
    for line in r:
        line=line.replace(', ', ',').replace(' ,',',')
        if line.startswith('*ELEMENT'):
            line=line.replace("DC3D8","C3D8R")
            line=line.replace("DC3D20","C3D20R")
            line=line.replace("DC3D4","C3D4")
            line=line.replace("DC3D6","C3D6")
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
            line=line.replace("FIELD", "FIELD,FREQUENCY="+output_freq)
        elif line.startswith('NT'):
            line="NT,U\n*ELEMENT OUTPUT\n"+element_output+"\n"

        f_w.write(line)
